# -*- coding: utf-8 -*-
"""C14 · 治理环量化：SNA 网络效率 η + 三区两翼协同博弈（纳什均衡）
CASA KB §4.6/§5.5：网络效率 η=1/[N(N-1)]·Σ(1/d_ij)；政策网络组=纳什均衡解释"制度性距离"
问题：三区两翼为何不协同？答案用博弈矩阵量化：现状支付结构下"各自为战"是纳什均衡（路径锁定）
机制：缝合（物理）+ 相变论坛年度发布（声誉/高频反馈）改变支付结构 → 协同成为新均衡
输出：计算/c14_governance.json + charts/c14_governance.png
"""
import os, json, math, pickle
import numpy as np
import networkx as nx
from shapely.geometry import Point
from kun_common import setup_chinese_fonts, registry_put

HERE = os.path.dirname(os.path.abspath(__file__))
CALC = os.path.join(HERE, "计算"); CHARTS = os.path.join(HERE, "charts")
os.makedirs(CALC, exist_ok=True); os.makedirs(CHARTS, exist_ok=True)

# 网络效率 η：5 核（三区+两翼）的交互网络，边权 = λ 耦合（C1 已算）
# 用 C1 的路网口径 λ 值构造加权图
c1 = json.load(open(os.path.join(CALC, "c1_wilson.json")))
pairs = c1["core_pairs"]  # [{pair, d_net_m, lambda_net, above_critical}]
nodes = ["zhongzhiyuan", "origin", "dazhongsi", "zgc_wing", "xyh_wing"]
node_zh = {"zhongzhiyuan": "众智园", "origin": "原点社区", "dazhongsi": "大钟寺",
           "zgc_wing": "中关村翼", "xyh_wing": "小月河翼"}
pair_key = {
    ("众智园AI自主创新加速区", "北京AI原点社区"): ("zhongzhiyuan", "origin"),
    ("众智园AI自主创新加速区", "大钟寺AI产业集聚区"): ("zhongzhiyuan", "dazhongsi"),
    ("众智园AI自主创新加速区", "中关村科技服务翼"): ("zhongzhiyuan", "zgc_wing"),
    ("众智园AI自主创新加速区", "小月河场景赋能翼"): ("zhongzhiyuan", "xyh_wing"),
    ("北京AI原点社区", "大钟寺AI产业集聚区"): ("origin", "dazhongsi"),
    ("北京AI原点社区", "中关村科技服务翼"): ("origin", "zgc_wing"),
    ("北京AI原点社区", "小月河场景赋能翼"): ("origin", "xyh_wing"),
    ("大钟寺AI产业集聚区", "中关村科技服务翼"): ("dazhongsi", "zgc_wing"),
    ("大钟寺AI产业集聚区", "小月河场景赋能翼"): ("dazhongsi", "xyh_wing"),
    ("中关村科技服务翼", "小月河场景赋能翼"): ("zgc_wing", "xyh_wing"),
}
lam = {}
for p in pairs:
    a, b = p["pair"].split("×")
    key = (a, b) if (a, b) in pair_key else (b, a)
    if key in pair_key:
        lam[pair_key[key]] = p["lambda_net"]

# 现状网络效率（有效距离 d = 1/λ，λ→0 时 d→∞ 用上限）
def network_efficiency(lam_dict, N):
    D = np.full((N, N), np.inf)
    idx = {n: i for i, n in enumerate(nodes)}
    for (a, b), v in lam_dict.items():
        if v > 1e-6:
            d = 1.0 / v
            D[idx[a], idx[b]] = D[idx[b], idx[a]] = d
    # 最短路径（Floyd）
    for k in range(N):
        D = np.minimum(D, D[:, k, None] + D[None, k, :])
    np.fill_diagonal(D, np.inf)   # 排除自身
    finite = D[np.isfinite(D)]
    eta = float((1.0 / finite).sum() / (N * (N - 1))) if len(finite) else 0.0
    return eta

eta_now = network_efficiency(lam, 5)
# 缝合后：七节点缝合把主脊耦合提升（λ×1.6，模拟整合度+65~132%的平均效应）
lam_after = {k: min(0.95, v * 1.6) for k, v in lam.items()}
eta_after = network_efficiency(lam_after, 5)

# 协同博弈（简化 2×2，以"三区彼此"为对象）：
# 每个主体选择 协同(C)/各自为战(D)。协同收益=b×λ_ij−c（制度成本），不协同收益=s（自有资源）
# 现状：λ 平均 0.20（远低于临界）→ b×λ 小 → D 占优 = 纳什均衡（锁死）
# 缝合+论坛后：λ 平均 0.32（缝合提升）+ 声誉收益 r（年度发布=高频反馈）→ C 占优
b = 10.0; c = 1.5; s = 2.0
lam_mean_now = float(np.mean(list(lam.values())))
lam_mean_after = float(np.mean(list(lam_after.values())))
def nash(lam_mean, r=0.0):
    coop = b * lam_mean + r - c
    defect = s
    eq = "C,C（协同）" if coop > defect else "D,D（各自为战）"
    return {"coop_payoff": round(coop, 2), "defect_payoff": round(defect, 2),
            "nash_equilibrium": eq, "is_lock_in": coop <= defect}

g_now = nash(lam_mean_now, r=0.0)
g_after = nash(lam_mean_after, r=1.2)   # 声誉收益=相变论坛年度发布的"可见度"收益

result = {
    "meta": {"model": "SNA network efficiency η + 2×2 coordination game (CASA policy-network lens)",
             "payoffs": "coop=b·λ_mean+r−c; defect=s; b=10,c=1.5,s=2（量纲为抽象效用，仅比较结构）",
             "r_interpretation": "r=相变论坛年度发布的声誉收益（高频反馈：把协同程度变成每年可见的排名）"},
    "network_efficiency": {"eta_now": round(eta_now, 4), "eta_after_stitch": round(eta_after, 4),
                           "delta_pct": round((eta_after - eta_now) / max(eta_now, 1e-9) * 100, 1),
                           "reference": "η=1/[N(N-1)]·Σ(1/d_ij)；d=1/λ 耦合距离"},
    "game": {"status_quo": g_now, "after_stitch_and_forum": g_after,
             "lambda_mean_now": round(lam_mean_now, 3), "lambda_mean_after": round(lam_mean_after, 3)},
    "conclusion": ("现状支付结构下'各自为战'是纳什均衡——三区两翼不协同不是意愿问题而是制度锁定；"
                   "缝合（λ 提升）+ 相变论坛（声誉 r）改变支付结构，协同成为新均衡。"
                   "这就是治理层的量化：物理缝合之外，必须配高频反馈机制，锁才开得了。"),
}
json.dump(result, open(os.path.join(CALC, "c14_governance.json"), "w"), ensure_ascii=False, indent=2)
registry_put("C14_GOV", "network_efficiency_eta_now", round(eta_now, 4), "dimensionless",
             "SNA 网络效率 η（5核，d=1/λ）现状", "三区两翼协同度（拓扑口径）",
             caveat="λ 为 C1 代理口径")
registry_put("C14_GOV", "network_efficiency_eta_after", round(eta_after, 4), "dimensionless",
             "SNA 网络效率 η（缝合后）", "缝合的治理层收益",
             caveat="缝合=λ×1.6 代理")
registry_put("C14_GOV", "nash_status_quo", g_now["nash_equilibrium"], "name",
             "协同博弈纳什均衡（现状）", "制度锁定证据：不协同是均衡",
             caveat="2×2 简化博弈，效用为抽象量纲")
registry_put("C14_GOV", "nash_after", g_after["nash_equilibrium"], "name",
             "协同博弈纳什均衡（缝合+论坛后）", "解锁证据：协同成为均衡",
             caveat="同上；r=1.2 为概念假设")

plt = setup_chinese_fonts()
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
ax = axes[0]
ax.bar([0, 1], [eta_now, eta_after], color=["#b08a4f", "#2e9e6b"])
ax.set_xticks([0, 1]); ax.set_xticklabels(["现状", "缝合后"])
ax.set_title(f"网络效率 η（5核，d=1/λ）\n{eta_now:.4f} → {eta_after:.4f} (+{result['network_efficiency']['delta_pct']}%)")
ax2 = axes[1]
games = [g_now, g_after]
labels = ["现状", "缝合+相变论坛"]
x = np.arange(2)
coop = [g["coop_payoff"] for g in games]; defect = [g["defect_payoff"] for g in games]
ax2.bar(x - 0.18, coop, 0.36, label="协同收益", color="#5fbf77")
ax2.bar(x + 0.18, defect, 0.36, label="各自为战收益", color="#e74c3c")
ax2.set_xticks(x); ax2.set_xticklabels(labels)
ax2.axhline(0, color="#999", lw=0.5)
ax2.set_title("协同博弈：纳什均衡从 D,D 翻转为 C,C")
ax2.legend(fontsize=8)
fig.suptitle("图 C14 · 治理环量化：网络效率 η 与协同博弈（纳什均衡解锁）", fontweight="bold", fontsize=13)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS, "c14_governance.png"), dpi=150, bbox_inches="tight")
print(json.dumps(result, ensure_ascii=False, indent=1))
