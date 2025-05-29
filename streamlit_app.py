# 水差しパズル - 測定可能チェッカー
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import networkx as nx
from collections import deque
from math import gcd

# 日本語フォントの設定（Streamlit Community Cloud対応）
try:
    import japanize_matplotlib
    japanize_matplotlib.japanize()
    font_available = True
except ImportError:
    plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    font_available = False

def is_solvable(a, b, goal):
    """数学的に解が存在するかチェック"""
    return goal <= max(a, b) and goal % gcd(a, b) == 0

def simulate_pour_path(path, a_cap, b_cap):
    """パスから操作ログを生成"""
    log = []
    for i in range(1, len(path)):
        a1, b1 = path[i - 1]
        a2, b2 = path[i]
        if a2 == a_cap and a1 != a_cap:
            log.append(f"Fill A completely  ({a2}L, {b2}L)")
        elif b2 == b_cap and b1 != b_cap:
            log.append(f"Fill B completely  ({a2}L, {b2}L)")
        elif a2 == 0 and a1 != 0:
            log.append(f"Empty A  ({a2}L, {b2}L)")
        elif b2 == 0 and b1 != 0:
            log.append(f"Empty B  ({a2}L, {b2}L)")
        elif a2 < a1 and b2 > b1:
            t = b2 - b1
            log.append(f"Pour A to B ({t}L)  ({a2}L, {b2}L)")
        elif b2 < b1 and a2 > a1:
            t = a2 - a1
            log.append(f"Pour B to A ({t}L)  ({a2}L, {b2}L)")
        else:
            log.append(f"Unknown operation  ({a2}L, {b2}L)")
    return log

def solve_water_jug_problem(a_cap, b_cap, goal):
    """水差しパズルを解く"""
    G = nx.DiGraph()
    visited = set()
    queue = deque()
    initial = (0, 0)
    queue.append(initial)
    visited.add(initial)

    def next_states(a, b):
        """現在の状態から遷移可能な次の状態を生成"""
        res = []
        res.append((a_cap, b))  # Aを満タンにする
        res.append((a, b_cap))  # Bを満タンにする
        res.append((0, b))      # Aを空にする
        res.append((a, 0))      # Bを空にする
        res.append((a - min(a, b_cap - b), b + min(a, b_cap - b)))  # AからBに注ぐ
        res.append((a + min(b, a_cap - a), b - min(b, a_cap - a)))  # BからAに注ぐ
        return res

    # BFSで状態空間を探索
    while queue:
        current = queue.popleft()
        for next_state in next_states(*current):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
            G.add_edge(current, next_state)
    
    # 目標量を含む状態を探す
    goal_states = [s for s in visited if goal in s]
    for g in goal_states:
        try:
            path = nx.shortest_path(G, source=initial, target=g)
            log = simulate_pour_path(path, a_cap, b_cap)
            return log
        except nx.NetworkXNoPath:
            continue
    return []

def extract_path_states(steps, a_cap, b_cap):
    """ステップから各状態を抽出"""
    states = [(0, 0)]  # 初期状態
    for step in steps:
        try:
            state_str = step.split("(")[1].split(")")[0]
            parts = state_str.split(",")
            a_val = int(parts[0].strip().replace("L", ""))
            b_val = int(parts[1].strip().replace("L", ""))
            states.append((a_val, b_val))
        except (IndexError, ValueError):
            states.append(states[-1])
    return states

def create_visualization(states, steps, a, b, goal):
    """グラフ可視化を作成"""
    fig, ax = plt.subplots(figsize=(12, max(8, len(states) * 0.8)))
    
    # 各ステップに対してグラフを作成
    for i, (a_val, b_val) in enumerate(states):
        y_pos = len(states) - i - 1
        
        # A容器（青色）- 負の値で左側に表示
        if a_val > 0:
            ax.barh(y_pos, -a_val, height=0.6, color='#3498db', alpha=0.8)
            ax.text(-a_val/2, y_pos, f"{a_val}L", 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        
        # B容器（緑色）- 正の値で右側に表示
        if b_val > 0:
            ax.barh(y_pos, b_val, height=0.6, color='#2ecc71', alpha=0.8)
            ax.text(b_val/2, y_pos, f"{b_val}L", 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        
        # ステップ説明
        if i == 0:
            ax.text(-a-0.5, y_pos, "Initial state", 
                    ha='right', va='center', fontsize=9)
        elif i <= len(steps):
            step_description = steps[i-1].split("(")[0].strip()
            ax.text(-a-0.5, y_pos, f"Step{i}: {step_description}", 
                    ha='right', va='center', fontsize=9)
    
    # 最大容量を示す点線
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=-a, color='blue', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=b, color='green', linestyle='--', linewidth=1, alpha=0.7)
    
    # グラフの装飾
    ax.set_xlim(-a-2, b+2)
    ax.set_ylim(-0.5, len(states) - 0.5)
    
    # X軸のラベル
    x_ticks = list(range(-a, 0)) + list(range(0, b+1))
    x_tick_labels = [f"{abs(x)}L" for x in x_ticks]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    
    # Y軸を非表示
    ax.set_yticks([])
    
    # グリッド
    ax.grid(axis='x', linestyle='-', alpha=0.3)
    
    # タイトルとラベル
    ax.set_title(f"Water Jug Puzzle: Measuring {goal}L", fontsize=14, fontweight='bold')
    ax.set_xlabel("Water Volume (Liters)", fontsize=12)
    
    # 凡例
    a_patch = mpatches.Patch(color='#3498db', label=f"Container A ({a}L)")
    b_patch = mpatches.Patch(color='#2ecc71', label=f"Container B ({b}L)")
    a_line = plt.Line2D([0], [0], color='blue', linestyle='--', label=f"Container A Max")
    b_line = plt.Line2D([0], [0], color='green', linestyle='--', label=f"Container B Max")
    ax.legend(handles=[a_patch, b_patch, a_line, b_line], loc='lower right')
    
    return fig

# Streamlitアプリ
st.title("🥤 水差しパズル - Water Jug Puzzle")
st.markdown("""
このアプリは、2つの水差しを使って目標の水量を測定できるかどうかを判定し、
可能な場合は最短手順を表示します。

This app determines whether a target water volume can be measured using two jugs,
and displays the shortest procedure if possible.
""")

# フォント状況の表示
if not font_available:
    st.info("ℹ️ 日本語フォントが利用できません。グラフは英語で表示されます。 / Japanese fonts are not available. Graphs will be displayed in English.")

# サイドバーでの入力
st.sidebar.header("パラメータ設定 / Parameters")
a = st.sidebar.number_input("A容器の容量 / Container A (L)", min_value=1, max_value=20, value=3)
b = st.sidebar.number_input("B容器の容量 / Container B (L)", min_value=1, max_value=20, value=5)
goal = st.sidebar.number_input("目標の水量 / Target (L)", min_value=1, max_value=max(a, b), value=4)

# 表示オプション
st.sidebar.header("表示オプション / Display Options")
show_steps = st.sidebar.checkbox("ステップを表示 / Show Steps", value=True)
show_graph = st.sidebar.checkbox("グラフで可視化 / Show Graph", value=True)

# メイン処理
st.subheader(f"📊 結果 / Result: {goal}Lを測定する")

# 数学的チェック
if is_solvable(a, b, goal):
    st.success("✅ 測定可能です！ / Measurable!")
    
    # 解を求める
    with st.spinner("最短手順を計算中... / Calculating shortest path..."):
        steps = solve_water_jug_problem(a, b, goal)
    
    if steps:
        st.write(f"**最短手順 / Shortest path: {len(steps)}ステップ**")
        
        # ステップ表示
        if show_steps:
            st.subheader("📝 詳細な手順 / Detailed Steps")
            for i, step in enumerate(steps, 1):
                st.write(f"**Step {i}**: {step}")
        
        # グラフ可視化
        if show_graph:
            st.subheader("📈 視覚的な手順 / Visual Steps")
            states = extract_path_states(steps, a, b)
            fig = create_visualization(states, steps, a, b, goal)
            st.pyplot(fig)
    else:
        st.error("❌ 解が見つかりませんでした（プログラムエラー）/ Solution not found (program error)")
else:
    st.error("❌ 測定できません。この組み合わせでは目標量を作ることはできません。")
    st.error("❌ Cannot measure. This combination cannot produce the target amount.")
    st.info(f"💡 ヒント / Hint: 目標量は{gcd(a, b)}の倍数である必要があります。/ Target must be a multiple of {gcd(a, b)}.")

# 説明セクション
with st.expander("🤔 水差しパズルとは？ / What is Water Jug Puzzle?"):
    st.markdown("""
    **水差しパズル / Water Jug Puzzle**は、異なる容量の2つの容器を使って、
    正確な量の水を測定する古典的なパズルです。

    **基本ルール / Basic Rules:**
    - 容器を満タンにする / Fill a container completely
    - 容器を空にする / Empty a container completely  
    - 一方の容器からもう一方に水を移す / Pour from one container to another

    **数学的条件 / Mathematical Condition:**
    目標量が測定可能な条件は、目標量が2つの容器の容量の最大公約数で割り切れることです。
    
    The target amount is measurable if it is divisible by the GCD of the two container capacities.
    """)

# フッター
st.markdown("---")
st.markdown("💡 **開発者向け / For Developers**: このアプリはNetworkXとBFSアルゴリズムを使用して最短解を求めています。/ This app uses NetworkX and BFS algorithm to find the shortest solution.")
