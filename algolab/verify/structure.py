#!/usr/bin/env python3
"""AlgoLab 检验流水线 · 阶段 1b：结构、链接与"内容是否真的可见"检查。

历史事故（信息论馆）：曾因 reveal 动画 opacity:0 导致整页内容对读者不可见。
本脚本把该类问题列为硬性失败项。

用法：cd algolab && python3 verify/structure.py
"""
import re
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = sorted(ROOT.glob("*.html"))

# 各层级必须具备的内容块。
# L0 是启蒙层，刻意不使用形式化的定理/公式块，只要求有交互实验与自检。
REQUIRED_BLOCKS = {
    "l0": (),
    "l1": ("el-concept", "el-theorem", "el-formula", "el-example"),
    "l2": ("el-concept", "el-theorem", "el-proof", "el-coro"),
    "l3": ("el-concept", "el-theorem", "el-formula", "el-example"),
    "l4": ("el-concept", "el-theorem", "el-formula", "el-example"),
}

# 可能导致内容被隐藏的样式（details/summary 折叠除外，见白名单）
HIDE_PATTERNS = (
    r"opacity\s*:\s*0(?![.\d])",
    r"visibility\s*:\s*hidden",
    r"display\s*:\s*none",
)


def main() -> int:
    if not PAGES:
        print("FAIL 未找到任何 html 页面")
        return 1

    ids = {}
    for p in PAGES:
        src = p.read_text(encoding="utf-8")
        ids[p.name] = set(re.findall(r'id="([^"]+)"', src))

    errs = []
    warns = []

    for p in PAGES:
        raw = p.read_text(encoding="utf-8")
        name = p.name
        # 代码示例块（<pre><code>…</code></pre>）里的内容是展示用源码，不应参与检查
        src = re.sub(r"<pre><code>.*?</code></pre>", "", raw, flags=re.S)

        # --- 1) 站内链接与锚点有效性 ---
        # 排除 data-href（SVG 知识图谱节点用，非真实 <a> 链接，由 JS 跳转）
        for href in set(re.findall(r'(?<!data-)href="([^"]+)"', src)):
            if href.startswith(("http://", "https://", "mailto:", "#!")):
                continue
            file_part, _, anchor = href.partition("#")
            target = file_part or name
            if target.endswith(".css") or target.endswith(".js"):
                if not (ROOT / target).exists():
                    errs.append(f"{name}: 资源文件不存在 {target}")
                continue
            if target not in ids:
                errs.append(f"{name}: 链接指向不存在的页面 {target}")
            elif anchor and anchor not in ids[target]:
                errs.append(f"{name}: 锚点不存在 {target}#{anchor}")

        # --- 2) 内容页按层级检查内容块齐备 ---
        m_lvl = re.fullmatch(r"(l[0-4])_.*", p.stem)
        if m_lvl:
            for need in REQUIRED_BLOCKS[m_lvl.group(1)]:
                if need not in src:
                    errs.append(f"{name}: 缺少必需内容块 .{need}")
            if 'class="lab"' not in src:
                warns.append(f"{name}: 没有交互实验块 .lab")
            if 'class="quiz"' not in src and "<details>" not in src:
                warns.append(f"{name}: 没有自检 / 答案块")

        # --- 3) 内容是否被样式隐藏（reveal-up 事故防护）---
        # 只检查"真实样式"：style="..." 属性与 <style> 块；不误伤叙述文本里的字面。
        style_chunks = re.findall(r'style="([^"]*)"', src)
        style_chunks += re.findall(r"<style>(.*?)</style>", src, flags=re.S)
        for chunk in style_chunks:
            for pat in HIDE_PATTERNS:
                m = re.search(pat, chunk)
                if m:
                    errs.append(f"{name}: 真实样式中含隐藏内容 {m.group(0)!r}")

    # 汇总
    print(f"\n{len(PAGES)} 个页面已检查　·　{len(errs)} 个错误　·　{len(warns)} 个警告")
    for w in warns:
        print("  WARN", w)
    for e in errs:
        print("  ERR ", e)
    if errs:
        print("结构检查未通过。")
        return 1
    print("结构检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
