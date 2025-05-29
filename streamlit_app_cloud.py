# 水差しパズル - 測定可能チェッカー（Streamlit Cloud対応版）
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import networkx as nx
import matplotlib.font_manager as fm
from collections import deque
from math import gcd
import os
import platform

# Streamlit Cloud環境用の日本語フォント設定
def setup_matplotlib_japanese_cloud():
    """Streamlit Cloud環境での確実な日本語フォント設定"""
    japanese_support = False
    
    # 環境検出
    is_cloud = (
        os.environ.get('STREAMLIT_SERVER_PORT') or 
        'streamlit' in platform.platform().lower() or
        os.environ.get('DYNO')  # Heroku
    )
    
    # Matplotlibバックエンドを明示的に設定
    import matplotlib
    matplotlib.use('Agg')
    
    try:
        # ステップ1: japanize-matplotlibを試行
        import japanize_matplotlib
        japanize_matplotlib.japanize()
        
        if is_cloud:
            # Streamlit Cloud環境用フォント設定
            font_candidates = [
                'Noto Sans CJK JP',    # Linux環境での日本語フォント
                'DejaVu Sans',         # フォールバック
                'sans-serif'
            ]
            plt.rcParams['font.family'] = font_candidates
            st.info("🌐 Streamlit Cloud環境で japanize-matplotlib を使用中")
        else:
            # ローカル環境用フォント設定
            font_candidates = [
                'Noto Sans JP',
                'BIZ UDGothic', 
                'Yu Gothic',
                'sans-serif'
            ]
            plt.rcParams['font.family'] = font_candidates
            st.info("💻 ローカル環境で japanize-matplotlib を使用中")
        
        # 基本設定
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 10
        
        # フォントキャッシュ更新
        try:
            fm.fontManager.__init__()
        except:
            pass
        
        # 日本語テスト
        try:
            fig, ax = plt.subplots(figsize=(2, 1))
            ax.text(0.5, 0.5, '日本語テスト', ha='center', va='center', fontsize=10)
            plt.close(fig)
            japanese_support = True
            st.success("✅ 日本語フォント設定完了")
        except Exception as e:
            st.warning(f"⚠️ 日本語テストエラー: {e}")
            
    except ImportError:
        # japanize-matplotlibがない場合の手動設定
        st.warning("⚠️ japanize-matplotlib 未インストール - 手動設定を試行中")
        
        if is_cloud:
            # Cloud環境: 最小限の英語フォント
            plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
            st.info("🌐 Cloud環境: 英語フォントを使用")
        else:
            # ローカル環境: 利用可能なフォントを検索
            available_fonts = [f.name for f in fm.fontManager.ttflist]
            
            japanese_fonts = [
                'Noto Sans JP', 'BIZ UDGothic', 'Yu Gothic', 
                'Meiryo', 'MS Gothic', 'Hiragino Sans'
            ]
            
            found_font = None
            for font in japanese_fonts:
                if font in available_fonts:
                    found_font = font
                    break
            
            if found_font:
                plt.rcParams['font.family'] = [found_font, 'sans-serif']
                japanese_support = True
                st.success(f"✅ 日本語フォント見つかりました: {found_font}")
            else:
                plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
                st.info("💻 ローカル環境: 英語フォントを使用")
        
        plt.rcParams['axes.unicode_minus'] = False
    
    except Exception as e:
        # エラー時の安全なフォールバック
        plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
        plt.rcParams['axes.unicode_minus'] = False
        st.error(f"❌ フォント設定エラー: {e}")
    
    return japanese_support

# フォント設定を実行
japanese_support = setup_matplotlib_japanese_cloud()

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
            transfer = b2 - b1
            if japanese_support:
                log.append(f"A→Bに{transfer}L注ぐ → ({a2}L, {b2}L)")
            else:
                log.append(f"Pour {transfer}L from A→B → ({a2}L, {b2}L)")
        elif b2 < b1 and a2 > a1:
            transfer = a2 - a1
            if japanese_support:
                log.append(f"B→Aに{transfer}L注ぐ → ({a2}L, {b2}L)")
            else:
                log.append(f"Pour {transfer}L from B→A → ({a2}L, {b2}L)")
        else:
            if japanese_support:
                log.append(f"状態変化 → ({a2}L, {b2}L)")
            else:
                log.append(f"State change → ({a2}L, {b2}L)")
    
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
        states = []
        states.append((a_cap, b))  # Aを満タンにする
        states.append((a, b_cap))  # Bを満タンにする
        states.append((0, b))      # Aを空にする
        states.append((a, 0))      # Bを空にする
        
        # AからBに注ぐ
        pour_a_to_b = min(a, b_cap - b)
        states.append((a - pour_a_to_b, b + pour_a_to_b))
        
        # BからAに注ぐ
        pour_b_to_a = min(b, a_cap - a)
        states.append((a + pour_b_to_a, b - pour_b_to_a))
        
        return states

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
    
    for goal_state in goal_states:
        try:
            path = nx.shortest_path(G, source=initial, target=goal_state)
            return simulate_pour_path(path, a_cap, b_cap)
        except nx.NetworkXNoPath:
            continue
    
    return []

def extract_path_states(steps, a_cap, b_cap):
    """ステップから各状態を抽出"""
    states = [(0, 0)]  # 初期状態
    
    for step in steps:
        try:
            # "→ (xL, yL)" の形式から数値を抽出
            if "→" in step and "(" in step and ")" in step:
                state_part = step.split("→")[1].strip()
                state_str = state_part.split("(")[1].split(")")[0]
                parts = state_str.split(",")
                
                a_val = int(parts[0].strip().replace("L", ""))
                b_val = int(parts[1].strip().replace("L", ""))
                states.append((a_val, b_val))
            else:
                # パースエラーの場合は前の状態を維持
                states.append(states[-1])
                
        except (IndexError, ValueError, AttributeError):
            # エラー時は前の状態を維持
            states.append(states[-1])
    
    return states

def create_visualization(states, steps, a, b, goal):
    """グラフ可視化を作成（Cloud対応版）"""
    
    # 図のサイズ調整
    fig_height = max(6, len(states) * 0.6)
    fig, ax = plt.subplots(figsize=(12, fig_height))
    
    # 各ステップのグラフ描画
    for i, (a_val, b_val) in enumerate(states):
        y_pos = len(states) - i - 1
        
        # A容器（青）- 左側に負の値で表示
        if a_val > 0:
            ax.barh(y_pos, -a_val, height=0.6, color='#3498db', alpha=0.8, label='A' if i == 0 else "")
            ax.text(-a_val/2, y_pos, f"{a_val}L", 
                   ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        
        # B容器（緑）- 右側に正の値で表示
        if b_val > 0:
            ax.barh(y_pos, b_val, height=0.6, color='#2ecc71', alpha=0.8, label='B' if i == 0 else "")
            ax.text(b_val/2, y_pos, f"{b_val}L", 
                   ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        
        # ステップ説明テキスト
        if i == 0:
            if japanese_support:
                step_text = "初期状態"
            else:
                step_text = "Initial"
        elif i <= len(steps):
            # ステップの説明を短縮
            step_desc = steps[i-1].split("→")[0].strip()
            if len(step_desc) > 15:
                step_desc = step_desc[:12] + "..."
            step_text = f"Step{i}: {step_desc}"
        else:
            step_text = f"Step{i}"
        
        ax.text(-a-1, y_pos, step_text, ha='right', va='center', fontsize=8)
    
    # 容器の最大値線
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=-a, color='blue', linestyle='--', linewidth=1, alpha=0.6)
    ax.axvline(x=b, color='green', linestyle='--', linewidth=1, alpha=0.6)
    
    # 軸設定
    ax.set_xlim(-a-2, b+2)
    ax.set_ylim(-0.5, len(states) - 0.5)
    
    # X軸ラベル
    x_ticks = list(range(-a, 0)) + list(range(0, b+1))
    x_labels = [f"{abs(x)}L" for x in x_ticks]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels)
    ax.set_yticks([])
    
    # グリッド
    ax.grid(axis='x', alpha=0.3)
    
    # タイトルとラベル（フォント対応）
    try:
        if japanese_support:
            title = f"水差しパズル: {goal}Lを測定"
            xlabel = "水量 (リットル)"
        else:
            title = f"Water Jug Puzzle: Measuring {goal}L"
            xlabel = "Water Volume (Liters)"
            
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=12)
        
    except Exception:
        # フォント問題時の英語フォールバック
        title = f"Water Jug Puzzle: Measuring {goal}L"
        xlabel = "Water Volume (Liters)"
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel(xlabel, fontsize=12)
    
    # 凡例
    try:
        if japanese_support:
            handles = [
                mpatches.Patch(color='#3498db', label=f'A容器 ({a}L)'),
                mpatches.Patch(color='#2ecc71', label=f'B容器 ({b}L)')
            ]
        else:
            handles = [
                mpatches.Patch(color='#3498db', label=f'Container A ({a}L)'),
                mpatches.Patch(color='#2ecc71', label=f'Container B ({b}L)')
            ]
        ax.legend(handles=handles, loc='lower right')
        
    except Exception:
        # 凡例エラー時の英語フォールバック
        handles = [
            mpatches.Patch(color='#3498db', label=f'Container A ({a}L)'),
            mpatches.Patch(color='#2ecc71', label=f'Container B ({b}L)')
        ]
        ax.legend(handles=handles, loc='lower right')
    
    plt.tight_layout()
    return fig

def main():
    """メインアプリケーション"""
    
    # タイトル
    if japanese_support:
        st.title("🥤 水差しパズル - Water Jug Puzzle")
        st.markdown("2つの水差しを使って目標の水量を測定できるかを判定し、最短手順を表示します。")
    else:
        st.title("🥤 Water Jug Puzzle")
        st.markdown("Determine if a target water volume can be measured using two jugs and show the shortest procedure.")

    # 環境情報表示
    col1, col2 = st.columns(2)
    with col1:
        if japanese_support:
            st.info("✅ 日本語フォント利用可能")
        else:
            st.warning("⚠️ 英語フォントを使用中")
    
    with col2:
        is_cloud = os.environ.get('STREAMLIT_SERVER_PORT') is not None
        if is_cloud:
            st.info("🌐 Streamlit Cloud環境")
        else:
            st.info("💻 ローカル環境")

    # サイドバー入力
    st.sidebar.header("Parameters / パラメータ")
    a = st.sidebar.number_input("Container A / A容器 (L)", min_value=1, max_value=20, value=3)
    b = st.sidebar.number_input("Container B / B容器 (L)", min_value=1, max_value=20, value=5)
    goal = st.sidebar.number_input("Target / 目標 (L)", min_value=1, max_value=max(a, b), value=4)
    
    st.sidebar.header("Options / オプション")
    show_steps = st.sidebar.checkbox("Show Steps / 手順表示", value=True)
    show_graph = st.sidebar.checkbox("Show Graph / グラフ表示", value=True)

    # メイン処理
    if japanese_support:
        st.subheader(f"📊 結果: {goal}Lを測定")
    else:
        st.subheader(f"📊 Result: Measuring {goal}L")

    # 解存在チェック
    if is_solvable(a, b, goal):
        if japanese_support:
            st.success("✅ 測定可能です！")
            spinner_text = "最短手順を計算中..."
        else:
            st.success("✅ Measurable!")
            spinner_text = "Calculating shortest path..."
        
        # 解を求める
        with st.spinner(spinner_text):
            steps = solve_water_jug_problem(a, b, goal)
        
        if steps:
            if japanese_support:
                st.write(f"**最短手順: {len(steps)}ステップ**")
            else:
                st.write(f"**Shortest path: {len(steps)} steps**")
            
            # 手順表示
            if show_steps:
                if japanese_support:
                    st.write("### 📝 詳細手順")
                else:
                    st.write("### 📝 Detailed Steps")
                
                for i, step in enumerate(steps, 1):
                    st.write(f"**Step {i}:** {step}")
            
            # グラフ表示
            if show_graph:
                if japanese_support:
                    st.write("### 📈 視覚的手順")
                else:
                    st.write("### 📈 Visual Steps")
                
                try:
                    states = extract_path_states(steps, a, b)
                    fig = create_visualization(states, steps, a, b, goal)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"グラフ描画エラー / Graph error: {e}")
        else:
            if japanese_support:
                st.error("❌ 解が見つかりませんでした")
            else:
                st.error("❌ No solution found")
    else:
        if japanese_support:
            st.error("❌ 測定不可能です")
            st.write("この組み合わせでは目標量を測定することはできません。")
        else:
            st.error("❌ Measurement impossible")
            st.write("The target volume cannot be achieved with this combination.")

    # 説明
    with st.expander("ℹ️ About Water Jug Puzzle / 水差しパズルについて"):
        if japanese_support:
            st.write("""
            **水差しパズル**は2つの異なる容量の容器を使って目標の水量を正確に測るパズルです。
            
            **可能な操作:**
            - 容器を完全に満たす
            - 容器を完全に空にする  
            - 一方から他方に水を移す
            
            **解が存在する条件:**
            - 目標量 ≤ max(容器A, 容器B)
            - 目標量が両容器のGCDの倍数
            """)
        else:
            st.write("""
            **Water Jug Puzzle** is about measuring a target amount using two containers of different capacities.
            
            **Allowed operations:**
            - Fill a container completely
            - Empty a container completely
            - Pour from one container to another
            
            **Solution exists when:**
            - Target ≤ max(Container A, Container B)
            - Target is a multiple of GCD of both capacities
            """)

if __name__ == "__main__":
    main()
