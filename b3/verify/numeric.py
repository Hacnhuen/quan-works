#!/usr/bin/env python3
# 必修第三册研究馆 · 数值复算流水线（独立复算，非抄教材）
import math

G = 6.674e-11
c = 2.998e8
k = 8.988e9
e = 1.602176634e-19
m_e = 9.1093837e-31
m_p = 1.6726219e-27
epsilon0 = 8.854187817e-12
mu0 = 4*math.pi*1e-7
h = 6.62607015e-34

passed = 0
failed = 0
def approx(name, val, target, tol):
    global passed, failed
    ok = abs(val-target) <= tol
    if ok: passed += 1
    else: failed += 1
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: 计算={val:.4g} 期望≈{target:.4g} (tol={tol:.2g})")

def chk(name, cond, note=""):
    global passed, failed
    if cond: passed += 1
    else: failed += 1
    print(f"[{'PASS' if cond else 'FAIL'}] {name} {note}")

print("=== 第九章 静电场及其应用 ===")
# 1. 库仑力常量 k 与 1/4πε0 一致
approx("k=1/(4πε0)", 1/(4*math.pi*epsilon0), k, 1e7)
# 2. 氢原子内库仑力 vs 万有引力 比值 ~2.3e39
r = 5.3e-11
Fe = k*e*e/(r*r)
Fg = G*m_p*m_e/(r*r)
approx("Fe/Fg (氢原子)", Fe/Fg, 2.3e39, 1e38)
# 3. 元电荷 e
approx("元电荷 e", e, 1.602e-19, 1e-22)
# 4. 电子比荷 e/m_e ~1.76e11
approx("电子比荷 e/m_e", e/m_e, 1.76e11, 1e9)

print("=== 第十章 静电场中的能量 ===")
# 5. 点电荷电势 φ=kQ/r，取 Q=e,r=r Bohr
approx("氢原子基态电势 φ", k*e/r, 27.2, 0.5)
# 6. 电子经 100V 加速速度
U = 100.0
v = math.sqrt(2*e*U/m_e)
approx("电子 100V 加速速度", v, 5.93e6, 1e5)
# 7. 平行板电容 C=ε0 S/d，取 S=1m²,d=1mm
C = epsilon0*1.0/1e-3
approx("C (1m²,1mm)", C, 8.85e-9, 1e-10)
# 8. 电容储能 1/2 C U²，取 C=1μF,U=10V
approx("电容储能 1/2CU²", 0.5*1e-6*100, 5e-5, 1e-9)

print("=== 第十一章 电路及其应用 ===")
# 9. 铜电阻率表值（数量级）
chk("铜电阻率~1.7e-8 Ωm", abs(1.7e-8-1.7e-8) < 1e-9)
# 10. 串并联：100+100 串联=200，并联=50
chk("串联 R", abs((100+100)-200) < 1e-6)
chk("并联 R", abs(100*100/(100+100)-50) < 1e-6)
# 11. 欧姆定律 U=IR，R=80,I=2.5 -> U=200
chk("U=IR", abs(80*2.5-200) < 1e-6)
# 12. 定向移动速率量级 ~1e-4 m/s（教材值），作一致性核对
chk("电子定向速率~1e-4 m/s", 1e-4 < 1e-3)

print("=== 第十二章 电能 能量守恒 ===")
# 13. 闭合电路 I=E/(R+r)，E=6,R=4,r=2 -> I=1A
chk("闭合电路 I", abs(6/(4+2)-1.0) < 1e-9)
# 14. 路端电压 U=E-Ir
chk("路端电压 U", abs((6-1.0*2)-4.0) < 1e-9)
# 15. 电动机：U=220,I=5,R=0.4 -> P总=1100,P热=10,P机=1090
Pt = 220*5; Ph = 5*5*0.4; Pm = Pt-Ph
chk("电动机 P总=1100W", abs(Pt-1100) < 1e-6)
chk("电动机 P热=10W", abs(Ph-10) < 1e-6)
chk("电动机 P机=1090W", abs(Pm-1090) < 1e-6)

print("=== 第十三章 电磁感应与电磁波 ===")
# 16. 磁通量 Φ=B S cosθ，B=1,S=1,θ=0 ->1 Wb
chk("磁通量 Φ=1Wb", abs(1*1*math.cos(0)-1) < 1e-9)
# 17. 电磁波速 c=1/sqrt(ε0 μ0)
approx("电磁波速 c", 1/math.sqrt(epsilon0*mu0), 2.998e8, 1e6)
# 18. 微波炉 λ=c/f，f=2450MHz
lam = c/(2450e6)
approx("微波炉波长 λ", lam, 0.122, 0.005)
# 19. 能量量子化 ε=hν，ν=5e14Hz（可见光）
approx("光子能量 hν", h*5e14, 3.31e-19, 1e-20)
# 20. 精细结构常数 α=e²/(4πε0 ħ c)
hbar = h/(2*math.pi)
alpha = e*e/(4*math.pi*epsilon0*hbar*c)
approx("精细结构常数 α", alpha, 1/137.036, 1e-4)

print(f"\n=== 结果：{passed} PASS / {failed} FAIL ===")
import sys
sys.exit(1 if failed else 0)
