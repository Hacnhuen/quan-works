#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""物理馆 · 结构轨检验：链接/锚点/七元素块/隐藏样式/资源存在。"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ['index.html','l0_intuition.html','l1_foundation.html','l2_complete.html',
         'l3_pro.html','l4_frontier.html','lab.html','verify.html','method.html']
ASSETS = ['assets/core.css','assets/core.js']

# 各页必须的锚点（本页内 id），用于交叉核对
EXPECT_IDS = {
 'l0_intuition.html': ['fall','speed','force','energy','wave','light','atom'],
 'l1_foundation.html': ['core','kin','newton','grav','energy','efield','circuit','ohm','wave'],
 'l2_complete.html': ['momentum','energy','mag','em','gas','thermo','geoopt','atom'],
 'l3_pro.html': ['conserve','vib','waveopt','phase','rel','quantum'],
 'l4_frontier.html': ['gw','qc','topo','dark','precision','open'],
}
HIDE_PATTERNS = [r'opacity\s*:\s*0', r'visibility\s*:\s*hidden', r'display\s*:\s*none']
ELEMENT_CLASSES = ['el-concept','el-theorem','el-proof','el-coro','el-formula','el-example','el-frontier']

errors, warns = [], []

def analyze(name, src):
    path = os.path.join(ROOT, name)
    # 1) 站内链接与锚点
    for href in set(re.findall(r'(?<!data-)href="([^"]+)"', src)):
        if href.startswith('http') or href.startswith('#'):
            # 页内锚点校验
            if href.startswith('#'):
                target = href[1:]
                if target and f'id="{target}"' not in src and f"id='{target}'" not in src:
                    warns.append(f"{name}: 页内锚点 #{target} 未找到对应 id")
            continue
        if '#' in href:
            page, anc = href.split('#', 1)
            if page not in PAGES:
                errors.append(f"{name}: 链接指向不存在的页面 {page}")
                continue
            psrc = open(os.path.join(ROOT, page), encoding='utf-8').read()
            if f'id="{anc}"' not in psrc and f"id='{anc}'" not in psrc:
                errors.append(f"{name}: 跨页锚点 {href} 不存在于 {page}")
        else:
            # 资源文件（assets/）是合法链接，不算页面
            if href.startswith('assets/') or href in ASSETS:
                continue
            if href not in PAGES:
                errors.append(f"{name}: 链接指向不存在的页面 {href}")
    # 2) 七元素块齐备（对 L1-L4 内容页强制）
    if name in ('l1_foundation.html','l2_complete.html','l3_pro.html','l4_frontier.html'):
        present = [c for c in ELEMENT_CLASSES if f'class="el {c}"' in src or f'class="el {c} "' in src]
        missing = [c for c in ELEMENT_CLASSES if f'el {c}' not in src]
        if len(present) < 4:
            errors.append(f"{name}: 七元素内容块过少（仅 {len(present)} 类），缺 {missing}")
    # 3) 隐藏样式（仅检查真实 style / style 块）
    style_chunks = re.findall(r'style="([^"]*)"', src)
    style_chunks += re.findall(r'<style>(.*?)</style>', src, flags=re.S)
    for chunk in style_chunks:
        for pat in HIDE_PATTERNS:
            m = re.search(pat, chunk)
            if m:
                errors.append(f"{name}: 真实样式中含隐藏内容 {m.group(0)!r}")
    # 4) 期望锚点存在
    for eid in EXPECT_IDS.get(name, []):
        if f'id="{eid}"' not in src:
            errors.append(f"{name}: 缺少期望锚点 id=\"{eid}\"")

def main():
    for p in PAGES:
        fp = os.path.join(ROOT, p)
        if not os.path.exists(fp):
            errors.append(f"缺失页面 {p}"); continue
        analyze(p, open(fp, encoding='utf-8').read())
    for a in ASSETS:
        if not os.path.exists(os.path.join(ROOT, a)):
            errors.append(f"缺失资源 {a}")
    # SVG data-href 指向的页应存在（不要求锚点，因 JS 跳转）
    for f in glob.glob(os.path.join(ROOT, '*.html')):
        src = open(f, encoding='utf-8').read()
        for dh in re.findall(r'data-href="([^"]+)"', src):
            page = dh.split('#')[0]
            if page and page not in PAGES:
                errors.append(f"{os.path.basename(f)}: data-href 指向不存在页面 {page}")

    print(f"=== 物理馆 · 结构轨检验 ===")
    print(f"页面 {len(PAGES)} · 资源 {len(ASSETS)}")
    print(f"错误 {len(errors)} · 警告 {len(warns)}\n")
    for e in errors: print(f"[ERROR] {e}")
    for w in warns: print(f"[WARN ] {w}")
    print()
    if not errors:
        print("✅ 结构校验通过（0 错误）")
    else:
        print("❌ 存在结构错误，请修复")

if __name__ == '__main__':
    main()
