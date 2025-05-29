# 水差しパズル - 測定可能チェッカー
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import networkx as nx
import matplotlib.font_manager as fm
from collections import deque
from math import gcd

# 日本語フォント設定の強化（Streamlit Cloud対応）
def setup_matplotlib_japanese():
    """Streamlit Cloud環境での日本語フォント設定の強化版"""
    japanese_support = False
    
    # 方法1: japanize-matplotlibを使用（最優先）
    try:
        import japanize_matplotlib
        japanize_matplotlib.japanize()
        
        # 日本語フォント設定の強制適用
        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        
        # テスト描画で日本語対応を確認
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.text(0.5, 0.5, 'テスト', fontsize=12)
        plt.close(fig)
        
        japanese_support = True
        print("✅ japanize-matplotlib が正常に設定されました")
        
    except ImportError:
        print("⚠️ japanize-matplotlib がインストールされていません")
    except Exception as e:
        print(f"⚠️ japanize-matplotlib の設定に失敗: {e}")
    
    # 方法2: 手動でのフォント設定（フォールバック）
    if not japanese_support:
        try:
            # Streamlit Cloud で利用可能なフォントを優先順位で試行
            font_candidates = [
                'DejaVu Sans',  # Streamlit Cloudで確実に利用可能
                'Liberation Sans',
                'Noto Sans',
                'Arial',
                'sans-serif'
            ]
            
            for font in font_candidates:
                try:
                    plt.rcParams['font.family'] = [font]
                    break
                except:
                    continue
            
            # 日本語文字が表示できない場合の設定
            plt.rcParams['axes.unicode_minus'] = False
            plt.rcParams['font.size'] = 10
            
            print(f"🔧 フォールバックフォント '{font}' を使用します")
            
        except Exception as e:
            print(f"❌ フォント設定に失敗: {e}")
            plt.rcParams['font.family'] = ['DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
    
    return japanese_support

# フォント設定を実行
japanese_support = setup_matplotlib_japanese()

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
            if japanese_support:
                log.append(f"Aを満タンにする → ({a2}L, {b2}L)")
            else:
                log.append(f"Fill A completely → ({a2}L, {b2}L)")
        elif b2 == b_cap and b1 != b_cap:
            if japanese_support:
                log.append(f"Bを満タンにする → ({a2}L, {b2}L)")
            else:
                log.append(f"Fill B completely → ({a2}L, {b2}L)")
        elif a2 == 0 and a1 != 0:
            if japanese_support:
                log.append(f"Aを空にする → ({a2}L, {b2}L)")
            else:
                log.append(f"Empty A → ({a2}L, {b2}L)")
        elif b2 == 0 and b1 != 0:
            if japanese_support:
                log.append(f"Bを空にする → ({a2}L, {b2}L)")
            else:
                log.append(f"Empty B → ({a2}L, {b2}L)")
        elif a2 < a1 and b2 > b1:
            t = b2 - b1
            if japanese_support:
                log.append(f"A→Bに{t}L注ぐ → ({a2}L, {b2}L)")
            else:
                log.append(f"Pour {t}L from A→B → ({a2}L, {b2}L)")
        elif b2 < b1 and a2 > a1:
            t = a2 - a1
            if japanese_support:
                log.append(f"B→Aに{t}L注ぐ → ({a2}L, {b2}L)")
            else:
                log.append(f"Pour {t}L from B→A → ({a2}L, {b2}L)")
        else:
            if japanese_support:
                log.append(f"不明な操作 → ({a2}L, {b2}L)")
            else:
                log.append(f"Unknown operation → ({a2}L, {b2}L)")
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
    """グラフ可視化を作成（日本語フォント対応強化版）"""
    
    # japanize-matplotlibの再設定を確実に行う
    try:
        import japanize_matplotlib
        japanize_matplotlib.japanize()
        
        # matplotlibのRCパラメータを強制的に日本語対応にする
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10
        
        # 日本語フォントが利用可能な場合の設定
        if japanese_support:
            plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
        
    except ImportError:
        # japanize-matplotlibが利用できない場合のフォールバック
        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
    
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
            if japanese_support:
                step_text = f"初期状態 (0L, 0L)"
            else:
                step_text = f"Initial State (0L, 0L)"
            ax.text(-a-0.5, y_pos, step_text, 
                    ha='right', va='center', fontsize=9)
        elif i <= len(steps):
            step_description = steps[i-1].split("→")[0].strip()
            step_text = f"Step{i}: {step_description}"
            ax.text(-a-0.5, y_pos, step_text, 
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
    if japanese_support:
        title = f"水差しパズル: {goal}Lを測定"
        xlabel = "水量 (リットル)"
    else:
        title = f"Water Jug Puzzle: Measuring {goal}L"
        xlabel = "Water Volume (Liters)"
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    
    # 凡例
    if japanese_support:
        a_label = f"A容器 ({a}L)"
        b_label = f"B容器 ({b}L)"
        a_max_label = "A容器最大値"
        b_max_label = "B容器最大値"
    else:
        a_label = f"Container A ({a}L)"
        b_label = f"Container B ({b}L)"
        a_max_label = "Container A Max"
        b_max_label = "Container B Max"
    
    a_patch = mpatches.Patch(color='#3498db', label=a_label)
    b_patch = mpatches.Patch(color='#2ecc71', label=b_label)
    a_line = plt.Line2D([0], [0], color='blue', linestyle='--', label=a_max_label)
    b_line = plt.Line2D([0], [0], color='green', linestyle='--', label=b_max_label)
    ax.legend(handles=[a_patch, b_patch, a_line, b_line], loc='lower right')
    
    return fig

# Streamlitアプリのメイン部分
def main():
    # タイトル
    if japanese_support:
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

    # フォント状況の表示
    if japanese_support:
        st.info("ℹ️ 日本語フォントが利用可能です。")
    else:
        st.warning("⚠️ 日本語フォントが利用できません。グラフは英語で表示されます。 / Japanese fonts are not available. Graphs will be displayed in English.")

    # サイドバーでの入力
    if japanese_support:
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
    if japanese_support:
        st.subheader(f"📊 結果 / Result: {goal}Lを測定する")
    else:
        st.subheader(f"📊 Result: Measuring {goal}L")

    # 数学的チェック
    if is_solvable(a, b, goal):
        if japanese_support:
            st.success("✅ 測定可能です！ / Measurable!")
            spinner_text = "最短手順を計算中..."
        else:
            st.success("✅ Measurable!")
            spinner_text = "Calculating shortest path..."
        
        # 解を求める
        with st.spinner(spinner_text):
            steps = solve_water_jug_problem(a, b, goal)
        
        if steps:
            if japanese_support:
                st.write(f"最短手順 / Shortest path: {len(steps)}ステップ")
            else:
                st.write(f"Shortest path: {len(steps)} steps")
            
            # ステップ表示
            if show_steps:
                if japanese_support:
                    st.write("📝 詳細な手順 / Detailed Steps")
                else:
                    st.write("📝 Detailed Steps")
                
                for i, step in enumerate(steps, 1):
                    st.write(f"Step {i}: {step}")
            
            # グラフ可視化
            if show_graph:
                if japanese_support:
                    st.write("📈 視覚的な手順 / Visual Steps")
                else:
                    st.write("📈 Visual Steps")
                
                states = extract_path_states(steps, a, b)
                fig = create_visualization(states, steps, a, b, goal)
                st.pyplot(fig)
        else:
            if japanese_support:
                st.error("❌ エラー: パスが見つかりませんでした。")
            else:
                st.error("❌ Error: No path found.")
    else:
        if japanese_support:
            st.error("❌ 測定できません。この組み合わせでは目標量を作ることはできません。")
        else:
            st.error("❌ Measurement not possible. The target volume cannot be achieved with this combination.")

    # 説明セクション
    with st.expander("🤔 水差しパズルとは？ / What is Water Jug Puzzle?"):
        if japanese_support:
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
    if japanese_support:
        st.markdown("💡 **開発者向け**: このアプリはNetworkXとBFSアルゴリズムを使用して最短解を求めています。")
    else:
        st.markdown("💡 **For Developers**: This app uses NetworkX and BFS algorithm to find the shortest solution.")

if __name__ == "__main__":
    main()