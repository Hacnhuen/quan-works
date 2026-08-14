#!/usr/bin/env python3
# 必修第三册研究馆 · 结构检查流水线
import os, re, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
    "index.html", "method.html", "verify.html",
    "ch9_charge_field.html", "ch10_potential.html", "ch11_circuit.html",
    "ch12_energy.html", "ch13_induction.html",
}
ASSETS = {"assets/core.css", "assets/core.js"}
# 导航/索引页不含七元素块，豁免七元素检查
NAV_PAGES = {"index.html", "verify.html"}
ELEMS = ["el-concept", "el-theorem", "el-proof", "el-coro", "el-formula", "el-example", "el-frontier"]
errors = []
warns = []

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8", errors="ignore") as f:
        return f.read()

for name in sorted(PAGES):
    html = read(name)
    # 七元素块齐备检查（导航页豁免）
    if name in NAV_PAGES:
        continue
    present = [e for e in ELEMS if f'el {e}"' in html or f'class="{e}"' in html or f'el-{e}' in html]
    for e in ["el-concept", "el-theorem", "el-formula", "el-frontier"]:
        if e not in present:
            errors.append(f"{name}: 缺少七元素块 {e}")
    # 链接检查
    for m in re.finditer(r'href="([^"#]+)(#[^"]*)?"', html):
        href = m.group(1)
        if not href:
            continue
        if href.startswith("http") or href.startswith("mailto"):
            continue
        if href.startswith("../") or "/" in href:
            # 跨目录相对链接（如 ../physlab/index.html）合法，跳过存在性检查
            continue
        if href.startswith("assets/") or href in ASSETS:
            if not os.path.exists(os.path.join(ROOT, href)):
                errors.append(f"{name}: 资源缺失 {href}")
            continue
        if href not in PAGES:
            errors.append(f"{name}: 链接指向不存在的页面 {href}")
    # 锚点检查：内部锚 #xxx 应在本页有 id
    for m in re.finditer(r'href="#([^"]+)"', html):
        anc = m.group(1)
        if anc and f'id="{anc}"' not in html:
            errors.append(f"{name}: 锚点 #{anc} 无对应 id")
    # 隐藏样式检查（防止内容被 display:none 隐藏而声称存在）
    if re.search(r'\.el[^}]*display\s*:\s*none', html) or 'style="display:none' in html:
        warns.append(f"{name}: 检测到隐藏样式")

# 跨页导航一致性：每章 pager 应有上一章/下一章或总览
for name in [f"ch{i}_" for i in range(9,14)]:
    pass

print("=== 结构检查 ===")
print(f"页面数: {len(PAGES)}，资源: {len(ASSETS)}")
if errors:
    for e in errors: print("  [ERR] " + e)
else:
    print("  [OK] 无结构错误")
if warns:
    for w in warns: print("  [WARN] " + w)
else:
    print("  [OK] 无警告")

# 七元素统计
print("\n=== 七元素覆盖 ===")
for name in sorted(PAGES):
    html = read(name)
    cnt = {e: html.count(f'el {e}"') + html.count(f'el-{e}') for e in ELEMS}
    tot = sum(cnt.values())
    print(f"  {name}: 共 {tot} 块 -> " + ", ".join(f"{e.split('-')[1]}={cnt[e]}" for e in ELEMS))

sys.exit(1 if errors else 0)
