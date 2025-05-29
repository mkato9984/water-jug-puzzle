import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from math import gcd

def is_solvable(a, b, goal):
    return goal <= max(a, b) and goal % gcd(a, b) == 0

st.title("水差しパズル - 測定可能チェッカー")

a = st.number_input("A容器の容量 (L)", min_value=1, value=3)
b = st.number_input("B容器の容量 (L)", min_value=1, value=5)
goal = st.number_input("目標の水量 (L)", min_value=1, value=4)

if is_solvable(a, b, goal):
    st.success(f"{goal}L は測定可能です ✅")
    if st.button("操作手順を表示"):
        from collections import deque
        import networkx as nx

        def simulate_pour_path(path, a_cap, b_cap):
            log = []
            for i in range(1, len(path)):
                a1, b1 = path[i - 1]
                a2, b2 = path[i]
                if a2 == a_cap and a1 != a_cap:
                    log.append(f"Aを満タンにする → ({a2}L, {b2}L)")
                elif b2 == b_cap and b1 != b_cap:
                    log.append(f"Bを満タンにする → ({a2}L, {b2}L)")
                elif a2 == 0 and a1 != 0:
                    log.append(f"Aを空にする → ({a2}L, {b2}L)")
                elif b2 == 0 and b1 != 0:
                    log.append(f"Bを空にする → ({a2}L, {b2}L)")
                elif a2 < a1 and b2 > b1:
                    t = b2 - b1
                    log.append(f"A→Bに{t}L注ぐ → ({a2}L, {b2}L)")
                elif b2 < b1 and a2 > a1:
                    t = a2 - a1
                    log.append(f"B→Aに{t}L注ぐ → ({a2}L, {b2}L)")
                else:
                    log.append(f"不明な操作 → ({a2}L, {b2}L)")
            return log

        def solve_water_jug_problem(a_cap, b_cap, goal):
            G = nx.DiGraph()
            visited = set()
            queue = deque()
            initial = (0, 0)
            queue.append(initial)
            visited.add(initial)

            def next_states(a, b):
                res = []
                res.append((a_cap, b))
                res.append((a, b_cap))
                res.append((0, b))
                res.append((a, 0))
                res.append((a - min(a, b_cap - b), b + min(a, b_cap - b)))
                res.append((a + min(b, a_cap - a), b - min(b, a_cap - a)))
                return res

            while queue:
                current = queue.popleft()
                for next_state in next_states(*current):
                    if next_state not in visited:
                        visited.add(next_state)
                        queue.append(next_state)                    G.add_edge(current, next_state)
                    
            goal_states = [s for s in visited if goal in s]
            for g in goal_states:
                try:
                    path = nx.shortest_path(G, source=initial, target=g)
                    log = simulate_pour_path(path, a_cap, b_cap)
                    return log
                except nx.NetworkXNoPath:
                    continue
            return []

        steps = solve_water_jug_problem(a, b, goal)
        for i, step in enumerate(steps, 1):
            st.write(f"Step {i}: {step}")
            
        # グラフで視覚化する
        if st.button("グラフで表示"):
            # パスから各ステップの状態を抽出
            def extract_path_states(steps, a_cap, b_cap):
                states = [(0, 0)]  # 初期状態
                for step in steps:
                    # ステップの説明から状態を抽出 (例: "Aを満タンにする → (3L, 0L)")
                    state_str = step.split("→")[1].strip()
                    # 文字列 "(3L, 0L)" から数値を抽出
                    a_val = int(state_str.split(",")[0].strip("( L)"))
                    b_val = int(state_str.split(",")[1].strip(" L)"))
                    states.append((a_val, b_val))
                return states
            
            states = extract_path_states(steps, a, b)
            
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # 各ステップに対してグラフを作成
            for i, (a_val, b_val) in enumerate(states):
                # 上下に配置するためのy位置
                y_pos = len(states) - i - 1
                
                # A容器（青色）- 負の値で左側に表示
                if a_val > 0:
                    ax.barh(y_pos, -a_val, height=0.6, color='#3498db', alpha=0.8)
                    ax.text(-a_val/2, y_pos, f"{a_val}L", 
                            ha='center', va='center', color='white', fontweight='bold')
                
                # B容器（緑色）- 正の値で右側に表示
                if b_val > 0:
                    ax.barh(y_pos, b_val, height=0.6, color='#2ecc71', alpha=0.8)
                    ax.text(b_val/2, y_pos, f"{b_val}L", 
                            ha='center', va='center', color='white', fontweight='bold')
                
                # ステップ番号と説明
                if i == 0:
                    ax.text(-a-0.5, y_pos, f"初期状態 (0L, 0L)", 
                            ha='right', va='center')
                elif i < len(steps) + 1:
                    step_description = steps[i-1].split("→")[0].strip()
                    ax.text(-a-0.5, y_pos, f"❶ {step_description}", 
                            ha='right', va='center')
            
            # 最大容量を示す点線
            ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
            ax.axvline(x=-a, color='blue', linestyle='--', linewidth=1)
            ax.axvline(x=b, color='green', linestyle='--', linewidth=1)
            
            # グラフの装飾
            ax.set_xlim(-a-1, b+1)
            ax.set_ylim(-0.5, len(states) - 0.5)
            
            # X軸のラベルを調整
            x_ticks = list(range(-a, 0)) + list(range(0, b+1))
            x_tick_labels = [f"{abs(x)}L" for x in x_ticks]
            ax.set_xticks(x_ticks)
            ax.set_xticklabels(x_tick_labels)
            
            # Y軸のラベルを削除
            ax.set_yticks([])
            
            # グリッド線
            ax.grid(axis='x', linestyle='-', alpha=0.3)
            
            # タイトル
            ax.set_title(f"B容器を基準に{goal}Lを測る手順 （ステップ別一覧・左右分離）")
            ax.set_xlabel("水の量 (リットル)")
            
            # 凡例
            import matplotlib.patches as mpatches
            a_patch = mpatches.Patch(color='#3498db', label=f'A容器 ({a}L)')
            b_patch = mpatches.Patch(color='#2ecc71', label=f'B容器 ({b}L)')
            a_line = plt.Line2D([0], [0], color='blue', linestyle='--', label=f'A容器の最大 ({a}L)')
            b_line = plt.Line2D([0], [0], color='green', linestyle='--', label=f'B容器の最大 ({b}L)')
            ax.legend(handles=[a_patch, b_patch, a_line, b_line], loc='lower right')
            
            st.pyplot(fig)
else:
    st.error("❌ 測定できません。この組み合わせでは目標量を作ることはできません。")
