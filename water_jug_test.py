#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
水差しパズル機能テスト（日本語フォント対応確認）
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use('Agg')  # GUI不要のバックエンド

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import japanize_matplotlib
from math import gcd
from collections import deque

def test_water_jug_functions():
    """水差しパズルの基本機能テスト"""
    print("=== 水差しパズル機能テスト ===")
    
    # フォント設定
    try:
        japanize_matplotlib.japanize()
        print("OK: japanize-matplotlib設定完了")
    except Exception as e:
        print(f"Warning: japanize-matplotlib error: {e}")
    
    # 基本テストケース
    test_cases = [
        (3, 5, 4, True),   # 解あり
        (2, 6, 4, True),   # 解あり
        (2, 4, 3, False),  # 解なし
        (7, 11, 6, True),  # 解あり
    ]
    
    print("\n1. 数学的解存在判定テスト:")
    print("-" * 40)
    
    for a, b, goal, expected in test_cases:
        result = is_solvable(a, b, goal)
        status = "OK" if result == expected else "NG"
        print(f"{status}: A={a}L, B={b}L, 目標={goal}L → {result}")
    
    # 解法テスト
    print("\n2. 解法アルゴリズムテスト:")
    print("-" * 40)
    
    a, b, goal = 3, 5, 4
    if is_solvable(a, b, goal):
        steps = solve_water_jug_problem(a, b, goal)
        print(f"問題: {a}Lと{b}Lの容器で{goal}Lを測定")
        print(f"手順数: {len(steps)}ステップ")
        for i, step in enumerate(steps[:5], 1):  # 最初の5ステップのみ表示
            print(f"  {i}. {step}")
        if len(steps) > 5:
            print(f"  ... (他{len(steps)-5}ステップ)")
    
    # グラフ作成テスト
    print("\n3. 日本語グラフ作成テスト:")
    print("-" * 40)
    
    try:
        create_test_graph()
        print("OK: 日本語グラフ作成成功")
        print("ファイル: test_water_jug_graph.png を生成")
    except Exception as e:
        print(f"NG: グラフ作成エラー: {e}")
    
    print("\n=== テスト完了 ===")

def is_solvable(a, b, goal):
    """数学的に解が存在するかチェック"""
    if goal > max(a, b):
        return False
    return goal % gcd(a, b) == 0

def solve_water_jug_problem(a, b, goal):
    """BFSによる最短解を求める"""
    if not is_solvable(a, b, goal):
        return []
    
    queue = deque([(0, 0, [])])
    visited = set()
    
    while queue:
        state_a, state_b, path = queue.popleft()
        
        if state_a == goal or state_b == goal:
            return path
        
        if (state_a, state_b) in visited:
            continue
        visited.add((state_a, state_b))
        
        # 可能な操作
        operations = [
            (a, state_b, "A容器を満たす"),
            (state_a, b, "B容器を満たす"),
            (0, state_b, "A容器を空にする"),
            (state_a, 0, "B容器を空にする"),
        ]
        
        # AからBに移す
        transfer = min(state_a, b - state_b)
        operations.append((state_a - transfer, state_b + transfer, f"AからBに{transfer}L移す"))
        
        # BからAに移す
        transfer = min(state_b, a - state_a)
        operations.append((state_a + transfer, state_b - transfer, f"BからAに{transfer}L移す"))
        
        for new_a, new_b, operation in operations:
            queue.append((new_a, new_b, path + [operation]))
    
    return []

def create_test_graph():
    """テスト用の日本語グラフを作成"""
    # テストデータ
    states = [(0, 0), (3, 0), (0, 3), (3, 3), (1, 3)]
    steps = ["初期状態", "A容器を満たす", "AからBに移す", "B容器を満たす", "目標達成"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 各ステップのバー
    for i, (a_val, b_val) in enumerate(states):
        y_pos = len(states) - i - 1
        
        # A容器（青）- 左側
        if a_val > 0:
            ax.barh(y_pos, -a_val, height=0.6, color='#3498db', alpha=0.8)
            ax.text(-a_val/2, y_pos, f"{a_val}L", ha='center', va='center', 
                   color='white', fontweight='bold')
        
        # B容器（緑）- 右側  
        if b_val > 0:
            ax.barh(y_pos, b_val, height=0.6, color='#2ecc71', alpha=0.8)
            ax.text(b_val/2, y_pos, f"{b_val}L", ha='center', va='center', 
                   color='white', fontweight='bold')
        
        # ステップ説明
        ax.text(-4.5, y_pos, steps[i], ha='right', va='center', fontsize=10)
    
    # グラフ設定
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax.axvline(x=-3, color='blue', linestyle='--', alpha=0.7)
    ax.axvline(x=5, color='green', linestyle='--', alpha=0.7)
    
    ax.set_xlim(-5, 6)
    ax.set_ylim(-0.5, len(states) - 0.5)
    ax.set_title("水差しパズル: 4Lを測定する手順", fontsize=14, fontweight='bold')
    ax.set_xlabel("水量 (リットル)", fontsize=12)
    
    # 凡例
    a_patch = mpatches.Patch(color='#3498db', label='A容器 (3L)')
    b_patch = mpatches.Patch(color='#2ecc71', label='B容器 (5L)')
    ax.legend(handles=[a_patch, b_patch], loc='lower right')
    
    ax.set_yticks([])
    ax.grid(axis='x', alpha=0.3)
    
    # ファイル保存
    plt.tight_layout()
    plt.savefig('test_water_jug_graph.png', dpi=150, bbox_inches='tight', 
               facecolor='white', edgecolor='none')
    plt.close()

if __name__ == "__main__":
    test_water_jug_functions()
