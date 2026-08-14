#!/usr/bin/env python3
"""InfoLab 检验流水线 · 阶段 1：独立重算全站关键数值。

不依赖任何模型，纯计算。每次修改内容后都应该跑一遍。
用法：cd infolab && python3 verify/numeric.py
退出码 0 = 全部通过，1 = 有数值不符。
"""
from math import log2, log, exp

CHECKS = []


def h2(p: float) -> float:
    """二元熵，单位 bit。"""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)


def check(name: str, got: float, want: float, tol: float = 5e-4) -> None:
    ok = abs(got - want) <= tol * max(1.0, abs(want))
    CHECKS.append((name, got, want, ok))


# ---------------- L1 基础 ----------------
check("H2(0.5) = 1",                 h2(0.5),            1.0)
check("H2(0.1)",                     h2(0.1),            0.4690, 2e-3)
check("H2(0.11)",                    h2(0.11),           0.4999, 2e-3)
check("H2 symmetry H2(.3)=H2(.7)",   h2(0.3) - h2(0.7),  0.0)
check("BSC(0.1) capacity",           1 - h2(0.1),        0.5310, 2e-3)
check("BSC(0.11) capacity",          1 - h2(0.11),       0.5000, 2e-3)
check("BSC(1.0) capacity = 1",       1 - h2(1.0),        1.0)
check("BSC(0.5) capacity = 0",       1 - h2(0.5),        0.0)
check("BEC(0.5) capacity = 0.5",     1 - 0.5,            0.5)
check("log2(3)",                     log2(3),            1.5850, 1e-3)

# 三元最大熵上界
check("max H of 3 symbols",          -3 * (1/3) * log2(1/3), 1.5850, 1e-3)

# ---------------- L1 Shannon-Hartley ----------------
snr = 10 ** (20 / 10)
check("SH C(20dB, 20MHz) Mbps",      20 * log2(1 + snr), 133.15, 1e-2)
check("spectral eff @20dB",          log2(1 + snr),      6.6582, 1e-3)
check("Shannon limit Eb/N0 (dB)",    10 * log(log(2)) / log(10), -1.5917, 1e-3)

# ---------------- L2 ----------------
# 典型集：p=0.25, n=200
p, n = 0.25, 200
check("H2(0.25)",                    h2(p),              0.8113, 1e-3)
check("typical set exponent nH",     n * h2(p),          162.26, 1e-3)
check("typical fraction 2^{n(H-1)}", n * (h2(p) - 1),    -37.74, 1e-3)

# ---------------- L3 率失真 ----------------
check("R(D) bern p=.5 D=.1",         h2(0.5) - h2(0.1),  0.5310, 2e-3)
check("R(D) bern D>=min(p,1-p) -> 0", max(0.0, h2(0.3) - h2(0.3)), 0.0)
check("gaussian: 1 bit = 6.02 dB",   10 * log(4) / log(10), 6.0206, 1e-3)
check("gaussian R(sigma=1,D=0.25)",  0.5 * log2(1 / 0.25), 1.0)

# ---------------- L4 量子 ----------------
# 去极化信道 d=2, p=0.2 -> 输出谱 {0.9, 0.1}
check("depolarizing chi* (d=2,p=.2)", 1 - h2(0.1),       0.5310, 2e-3)
check("  matches BSC(0.1) capacity",  (1 - h2(0.1)) - (1 - h2(0.1)), 0.0)
# Bell 态条件熵
check("Bell state S(A|B) = -1",      0.0 - 1.0,          -1.0)

# ---------------- L4 Landauer ----------------
kB = 1.380649e-23
eV = 1.602176634e-19
check("kB*T*ln2 @300K (J)",          kB * 300 * log(2),  2.8703e-21, 1e-3)
check("  in eV",                     kB * 300 * log(2) / eV, 0.017916, 1e-3)
check("  in units of kB*T",          log(2),             0.6931, 1e-3)
check("CMOS gap (1e-17 J / bound)",  1e-17 / (kB * 300 * log(2)), 3484.0, 5e-2)

# ---------------- L4 缩放律 ----------------
E, A, alpha, B, beta = 1.69, 406.4, 0.3392, 410.7, 0.2849


def chinchilla(N: float, D: float) -> float:
    return E + A / N ** alpha + B / D ** beta


check("Chinchilla L(70e9, 1.4e12)",  chinchilla(70e9, 1.4e12), 1.9174, 1e-3)
check("Chinchilla E in bit/token",   E / log(2),         2.4383, 1e-3)
check("  E as BPC (4 chars/token)",  E / log(2) / 4,     0.6096, 1e-3)
# 单调性：N 与 D 增大 loss 必须下降，且永远 > E
check("  L decreasing in N",
      float(chinchilla(1e10, 1e12) > chinchilla(1e11, 1e12)), 1.0)
check("  L decreasing in D",
      float(chinchilla(1e10, 1e11) > chinchilla(1e10, 1e12)), 1.0)
check("  L never below E",
      float(chinchilla(1e15, 1e15) > E),                  1.0)

# ---------------- L4 最大熵骰子 ----------------
def dice_mean(lam: float) -> float:
    z = sum(exp(lam * k) for k in range(1, 7))
    return sum(k * exp(lam * k) for k in range(1, 7)) / z


lo, hi = -5.0, 5.0
for _ in range(200):
    mid = (lo + hi) / 2
    if dice_mean(mid) < 4.5:
        lo = mid
    else:
        hi = mid
lam = (lo + hi) / 2
z = sum(exp(lam * k) for k in range(1, 7))
ps = [exp(lam * k) / z for k in range(1, 7)]
Hdice = -sum(q * log2(q) for q in ps)

check("maxent dice lambda (mu=4.5)", lam,                0.3710, 5e-3)
check("maxent dice H",               Hdice,              2.3279, 5e-3)
check("maxent dice p(6)",            ps[5],              0.3475, 5e-3)
check("maxent dice p(1)",            ps[0],              0.0544, 5e-3)
check("  info gained vs uniform",    log2(6) - Hdice,    0.2571, 5e-3)
check("  dice constraint satisfied", sum((k + 1) * ps[k] for k in range(6)), 4.5, 1e-6)
# 健全性：mu=3.5 必须退回均匀分布
lo2, hi2 = -5.0, 5.0
for _ in range(200):
    mid = (lo2 + hi2) / 2
    if dice_mean(mid) < 3.5:
        lo2 = mid
    else:
        hi2 = mid
check("maxent dice lambda (mu=3.5)=0", (lo2 + hi2) / 2,  0.0, 1e-3)

# ---------------- L1 Huffman 界 ----------------
def huffman_avg_len(probs):
    """返回 Huffman 平均码长。"""
    import heapq
    if len(probs) == 1:
        return 1.0
    heap = [(pr, i, None, None) for i, pr in enumerate(probs)]
    heapq.heapify(heap)
    counter = len(probs)
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, (a[0] + b[0], counter, a, b))
        counter += 1
    lengths = {}

    def walk(node, depth):
        if node[2] is None:
            lengths[node[1]] = max(depth, 1)
            return
        walk(node[2], depth + 1)
        walk(node[3], depth + 1)

    walk(heap[0], 0)
    return sum(probs[i] * lengths[i] for i in range(len(probs)))


for dist in ([0.5, 0.25, 0.125, 0.125],
             [0.4, 0.2, 0.2, 0.1, 0.1],
             [0.3, 0.3, 0.2, 0.1, 0.1],
             [1 / 6] * 6):
    Hd = -sum(q * log2(q) for q in dist if q > 0)
    Ld = huffman_avg_len(dist)
    ok_lo = Ld >= Hd - 1e-9
    ok_hi = Ld < Hd + 1
    CHECKS.append((f"Huffman H<=L<H+1 for {dist}", Ld, Hd, ok_lo and ok_hi))

# 二的负幂分布应当零冗余
check("Huffman zero redundancy (dyadic)",
      huffman_avg_len([0.5, 0.25, 0.125, 0.125]), 1.75, 1e-9)


# ---------------- 输出 ----------------
def main() -> int:
    bad = [c for c in CHECKS if not c[3]]
    for name, got, want, ok in CHECKS:
        tag = "PASS" if ok else "FAIL"
        print(f"{tag}  {name:38s} got={got:<14.6g} want={want:.6g}")
    print()
    print(f"{len(CHECKS) - len(bad)}/{len(CHECKS)} numeric checks passed")
    if bad:
        print("\n以下数值与页面标称不符，请先修正内容：")
        for name, got, want, _ in bad:
            print(f"  - {name}: got {got:.6g}, expected {want:.6g}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
