#!/usr/bin/env python3
"""InfoLab 检验流水线 · 阶段 1b：结构、链接与"内容是否真的可见"检查。

历史事故：曾因 reveal 动画的 opacity:0 导致整页内容对读者不可见。
本脚本把该类问题列为硬性失败项。

用法：cd infolab && python3 verify/structure.py
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
        # 代码示例块（<pre><code>…</code></pre>）里的内容是展示用的源码，
        # 不应参与链接 / 隐藏样式检查，否则会产生大量假阳性。
        src = re.sub(r"<pre><code>.*?</code></pre>", "", raw, flags=re.S)

        # --- 1) 站内链接与锚点有效性 ---
        for href in set(re.findall(r'href="([^"]+)"', src)):
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
            # 每个内容页都必须有交互实验与自检
            if "class=\"lab\"" not in src:
                warns.append(f"{name}: 没有交互实验块 .lab")
            if "class=\"quiz\"" not in src and "<details>" not in src:
                warns.append(f"{name}: 没有自检 / 答案块")

        # --- 3) 隐藏内容检测 ---
        for pat in HIDE_PATTERNS:
            for m in re.finditer(pat, src):
                line = src[: m.start()].count("\n") + 1
                errs.append(
                    f"{name}:{line}: 检测到可能隐藏内容的样式 `{m.group(0)}`"
                )

        # --- 4) 每页必须引用共享样式与脚本 ---
        if 'href="assets/core.css"' not in src:
            errs.append(f"{name}: 未引用 assets/core.css")
        if p.stem != "index" and 'src="assets/core.js"' not in src:
            warns.append(f"{name}: 未引用 assets/core.js")

        # --- 5) 定理编号唯一性与出处年份 ---
        thms = re.findall(r"定理\s*T(\d+)", src)
        if thms and not re.search(r"(19|20)\d{2}", src):
            errs.append(f"{name}: 出现定理编号但全页无任何年份，疑似缺出处")

        # --- 6) canvas 必须有配套的 data-h ---
        for m in re.finditer(r"<canvas([^>]*)>", src):
            attrs = m.group(1)
            if "data-h" not in attrs:
                line = src[: m.start()].count("\n") + 1
                warns.append(f"{name}:{line}: canvas 缺少 data-h，高度可能为默认值")

        # --- 7) 侧栏锚点必须在正文存在 ---
        side = re.search(r'<aside class="side">(.*?)</aside>', src, re.S)
        if side:
            for a in re.findall(r'href="#([^"]+)"', side.group(1)):
                if a not in ids[name]:
                    errs.append(f"{name}: 侧栏锚点 #{a} 在正文中不存在")

    # --- 8) 全站定理编号不应重复定义在不同页 ---
    thm_pages = {}
    for p in PAGES:
        src = p.read_text(encoding="utf-8")
        for t in set(re.findall(r"定理\s*T(\d+)\s*·", src)):
            thm_pages.setdefault(t, []).append(p.name)
    for t, pages in sorted(thm_pages.items(), key=lambda kv: int(kv[0])):
        if len(pages) > 1:
            warns.append(f"定理 T{t} 在多页被定义：{', '.join(pages)}")

    for e in errs:
        print("FAIL " + e)
    for w in warns:
        print("WARN " + w)

    print()
    print(f"{len(PAGES)} 个页面已检查　·　{len(errs)} 个错误　·　{len(warns)} 个警告")
    if not errs:
        print("结构检查通过。")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
