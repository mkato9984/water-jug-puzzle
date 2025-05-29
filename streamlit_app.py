# 水差しパズル - 測定可能チェッカー (Cloudエラー対応緊急修正版)
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import networkx as nx
from collections import deque
from math import gcd
import os
import sys
import io

# ====== 基本アルゴリズム関数 ======

def is_solvable(a, b, goal):
    """数学的に解が存在するかチェック"""
    if goal > max(a, b):
        return False
    return goal % gcd(a, b) == 0

def solve_water_jug_problem(a, b, goal):
    """BFSで水差しパズルを解く"""
    if not is_solvable(a, b, goal):
        return None
    
    # BFSの初期設定
    queue = deque([(0, 0, [])])
    visited = set([(0, 0)])
    
    while queue:
        state_a, state_b, path = queue.popleft()
        
        # ゴール状態のチェック
        if state_a == goal or state_b == goal:
            return path
        
        # 可能な操作の生成
        operations = []
        
        # 操作1: Aを満たす
        if state_a < a:
            if (a, state_b) not in visited:
                operations.append((a, state_b, f"A容器を満たす → ({a}L, {state_b}L)"))
                visited.add((a, state_b))
        
        # 操作2: Bを満たす
        if state_b < b:
            if (state_a, b) not in visited:
                operations.append((state_a, b, f"B容器を満たす → ({state_a}L, {b}L)"))
                visited.add((state_a, b))
        
        # 操作3: Aを空にする
        if state_a > 0:
            if (0, state_b) not in visited:
                operations.append((0, state_b, f"A容器を空にする → (0L, {state_b}L)"))
                visited.add((0, state_b))
        
        # 操作4: Bを空にする
        if state_b > 0:
            if (state_a, 0) not in visited:
                operations.append((state_a, 0, f"B容器を空にする → ({state_a}L, 0L)"))
                visited.add((state_a, 0))
        
        # 操作5: AからBに移す
        if state_a > 0 and state_b < b:
            pour = min(state_a, b - state_b)
            new_a, new_b = state_a - pour, state_b + pour
            if (new_a, new_b) not in visited:
                operations.append((new_a, new_b, f"AからBに{pour}L移す → ({new_a}L, {new_b}L)"))
                visited.add((new_a, new_b))
        
        # 操作6: BからAに移す
        if state_b > 0 and state_a < a:
            pour = min(state_b, a - state_a)
            new_a, new_b = state_a + pour, state_b - pour
            if (new_a, new_b) not in visited:
                operations.append((new_a, new_b, f"BからAに{pour}L移す → ({new_a}L, {new_b}L)"))
                visited.add((new_a, new_b))
        
        # 次のステップをキューに追加
        for next_a, next_b, operation in operations:
            queue.append((next_a, next_b, path + [operation]))
    
    return None

def extract_path_states(steps, a_cap, b_cap):
    """ステップのリストから各状態を抽出"""
    states = [(0, 0)]  # 初期状態
    
    for step in steps:
        desc_parts = step.split("→")
        if len(desc_parts) == 2:
            state_str = desc_parts[1].strip()
            if state_str.startswith("(") and state_str.endswith(")"):
                # 括弧内の状態を抽出 (XL, YL)
                state_str = state_str[1:-1].replace("L", "").strip()
                a_val, b_val = map(int, state_str.split(","))
                states.append((a_val, b_val))
    
    return states

# ====== グラフ作成関数（英語ベース、エラー回避モード） ======

def create_simple_visualization(states, steps, a, b, goal):
    """英語ベースの簡易グラフを作成（フォント問題回避）"""
    # 最低限の設定でフォント問題を回避
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 10,
        'figure.autolayout': True
    })
    
    fig, ax = plt.subplots(figsize=(12, max(8, len(states) * 0.8)))
    
    # 各ステップのバー描画
    for i, (a_val, b_val) in enumerate(states):
        y_pos = len(states) - i - 1
        
        # A容器（青色）
        if a_val > 0:
            ax.barh(y_pos, -a_val, height=0.6, color='#3498db', alpha=0.8)
            ax.text(-a_val/2, y_pos, f"{a_val}L", 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        
        # B容器（緑色）
        if b_val > 0:
            ax.barh(y_pos, b_val, height=0.6, color='#2ecc71', alpha=0.8)
            ax.text(b_val/2, y_pos, f"{b_val}L", 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        
        # ステップ説明（英語ベース）
        step_description = ""
        if i == 0:
            step_description = "Initial state (0L, 0L)"
        elif i <= len(steps):
            action = steps[i-1].split("→")[0].strip()
            step_description = f"Step {i}: {action}"
                
        ax.text(-a-0.5, y_pos, step_description, 
                ha='right', va='center', fontsize=9)
    
    # グラフの設定
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=-a, color='blue', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=b, color='green', linestyle='--', linewidth=1, alpha=0.7)
    
    ax.set_xlim(-a-2, b+2)
    ax.set_ylim(-0.5, len(states) - 0.5)
    
    # X軸のラベル
    x_ticks = list(range(-a, 0)) + list(range(0, b+1))
    x_tick_labels = [f"{abs(x)}L" for x in x_ticks]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels)
    
    # Y軸を非表示
    ax.set_yticks([])
    ax.grid(axis='x', linestyle='-', alpha=0.3)
    
    # タイトル英語表記
    ax.set_title(f"Water Jug Puzzle: Measuring {goal}L", fontsize=14, fontweight='bold')
    ax.set_xlabel("Water Volume (Liters)", fontsize=12)
    
    # 凡例
    a_patch = mpatches.Patch(color='#3498db', label=f"Container A ({a}L)")
    b_patch = mpatches.Patch(color='#2ecc71', label=f"Container B ({b}L)")
    a_line = plt.Line2D([0], [0], color='blue', linestyle='--', label="Container A Max")
    b_line = plt.Line2D([0], [0], color='green', linestyle='--', label="Container B Max")
    ax.legend(handles=[a_patch, b_patch, a_line, b_line], loc='lower right')
    
    return fig

# ====== メイン関数 ======

def main():
    st.set_page_config(
        page_title="Water Jug Puzzle",
        page_icon="🚰",
        layout="wide"
    )
    
    # エラー回避のため言語設定を判断
    language_setting = st.sidebar.selectbox(
        "Language / 言語", 
        ["English", "日本語 (UI Only)"], 
        index=0
    )
    
    use_japanese_ui = language_setting == "日本語 (UI Only)"
    
    # タイトル
    if use_japanese_ui:
        st.title("🥤 水差しパズル - Water Jug Puzzle")
        st.markdown("""
        このアプリは、2つの水差しを使って目標の水量を測定できるかどうかを判定し、
        可能な場合は最短手順を表示します。
        """)
    else:
        st.title("🥤 Water Jug Puzzle")
        st.markdown("""
        This app determines whether a target water volume can be measured using two jugs,
        and displays the shortest procedure if possible.
        """)
    
    # グラフの日本語フォント問題の説明
    st.warning("""
    **Note:** Due to Streamlit Cloud font limitations, the graph will be displayed in English. / 
    **注意:** Streamlit Cloud環境のフォント制限により、グラフの表示は英語になります。
    """)

    # サイドバーでの入力
    if use_japanese_ui:
        st.sidebar.header("パラメータ設定 / Parameters")
        a = st.sidebar.number_input("A容器の容量 (L)", min_value=1, max_value=20, value=3)
        b = st.sidebar.number_input("B容器の容量 (L)", min_value=1, max_value=20, value=5)
        goal = st.sidebar.number_input("目標の水量 (L)", min_value=1, max_value=max(a, b), value=4)
        
        st.sidebar.header("表示オプション / Display Options")
        show_steps = st.sidebar.checkbox("ステップを表示 / Show Steps", value=True)
        show_graph = st.sidebar.checkbox("グラフで可視化 / Show Graph", value=True)
    else:
        st.sidebar.header("Parameters")
        a = st.sidebar.number_input("Container A Capacity (L)", min_value=1, max_value=20, value=3)
        b = st.sidebar.number_input("Container B Capacity (L)", min_value=1, max_value=20, value=5)
        goal = st.sidebar.number_input("Target Volume (L)", min_value=1, max_value=max(a, b), value=4)
        
        st.sidebar.header("Display Options")
        show_steps = st.sidebar.checkbox("Show Steps", value=True)
        show_graph = st.sidebar.checkbox("Show Graph", value=True)

    # メイン処理
    if use_japanese_ui:
        st.subheader(f"📊 結果 / Result: {goal}Lを測定する")
    else:
        st.subheader(f"📊 Result: Measuring {goal}L")

    # 数学的チェック
    if is_solvable(a, b, goal):
        if use_japanese_ui:
            st.success("✅ 測定可能です！ / Measurable!")
            spinner_text = "最短手順を計算中..."
        else:
            st.success("✅ Measurable!")
            spinner_text = "Calculating shortest path..."
        
        # 解を求める
        with st.spinner(spinner_text):
            steps = solve_water_jug_problem(a, b, goal)
        
        if steps:
            if use_japanese_ui:
                st.write(f"最短手順 / Shortest path: {len(steps)}ステップ")
            else:
                st.write(f"Shortest path: {len(steps)} steps")
            
            # ステップ表示
            if show_steps:
                if use_japanese_ui:
                    st.write("📝 詳細な手順 / Detailed Steps")
                else:
                    st.write("📝 Detailed Steps")
                
                for i, step in enumerate(steps, 1):
                    st.write(f"Step {i}: {step}")
            
            # グラフ可視化
            if show_graph:
                if use_japanese_ui:
                    st.write("📈 視覚的な手順 / Visual Steps")
                else:
                    st.write("📈 Visual Steps")
                
                states = extract_path_states(steps, a, b)
                try:
                    # 安全なエラー回避版グラフ生成
                    fig = create_simple_visualization(states, steps, a, b, goal)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error generating visualization: {e}")
                    st.info("Try refreshing the page or using smaller container sizes.")
        else:
            if use_japanese_ui:
                st.error("❌ エラー: パスが見つかりませんでした。")
            else:
                st.error("❌ Error: No path found.")
    else:
        if use_japanese_ui:
            st.error("❌ 測定できません。この組み合わせでは目標量を作ることはできません。")
        else:
            st.error("❌ Measurement not possible. The target volume cannot be achieved with this combination.")

    # 説明セクション
    with st.expander("🤔 What is Water Jug Puzzle? / 水差しパズルとは？"):
        if use_japanese_ui:
            st.write("""
            **水差しパズル**は、容量の異なる2つの容器を使って、目標となる量の水を正確に測るパズルです。
            
            **ルール:**
            1. 容器を完全に満たす
            2. 容器を完全に空にする
            3. 一方の容器から他方に水を移す（あふれる場合は満タンまで）
            
            **数学的に解が存在する条件:**
            - 目標量が両方の容器の最大公約数 (GCD) の倍数であること
            - 目標量が大きい方の容器の容量以下であること
            """)
        else:
            st.write("""
            **Water Jug Puzzle** is a problem where you need to measure a target amount of water using two containers of different capacities.
            
            **Rules:**
            1. Fill a container completely
            2. Empty a container completely
            3. Pour water from one container to another (until the target container is full)
            
            **Mathematical condition for solvability:**
            - The target volume must be a multiple of the greatest common divisor (GCD) of the two container capacities
            - The target volume must be less than or equal to the capacity of the larger container
            """)

    # フッター
    st.markdown("---")
    st.markdown("💡 **Technical Note:** This app uses BFS (Breadth-First Search) algorithm to find the shortest solution path.")
    st.markdown("📌 **Font Notice:** Due to font limitations in Streamlit Cloud, visualization is shown in English.")

if __name__ == "__main__":
    main()
