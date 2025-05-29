# 水差しパズル - 測定可能チェッカー 🚰

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://water-jug-puzzle.streamlit.app)
![Japanese Font Support](https://img.shields.io/badge/日本語フォント-対応済み-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

このアプリケーションは、2つの容器を使って特定の水量を測定できるかどうかを判定し、その手順をグラフで視覚化するWebアプリケーションです。**Streamlit Cloud環境での日本語フォント表示に完全対応**しています。

## 🎯 機能

- **📐 測定可能性チェック**: 数学的に測定可能かどうかを瞬時に判定（GCDアルゴリズム使用）
- **🔍 最短解法探索**: BFS（幅優先探索）を使用して最短手順を探索
- **📝 操作手順の表示**: ステップバイステップの解法を日本語で詳細表示
- **📊 グラフ視覚化**: 各ステップの容器の状態を横棒グラフでリアルタイム表示
- **🎨 直感的UI**: Streamlitベースの使いやすいインターフェース
- **🌐 日本語フォント対応**: Streamlit Cloud環境での日本語表示完全対応

## ✨ 新機能・改善点（2025年5月更新）

- **🎌 日本語フォント完全対応**: japanize-matplotlib + 環境別フォント設定
- **☁️ Streamlit Cloud最適化**: 環境自動検出と専用設定
- **🔧 依存関係解決**: setuptools追加によるdistutils問題解決
- **🧪 包括的テスト**: 機能・フォント・視覚化の総合テスト実装

## 🚀 使用方法

1. **容器の容量を設定**: A容器とB容器の容量を入力（例：5L, 3L）
2. **目標水量を入力**: 測定したい水量を入力（例：4L）
3. **結果を確認**: 測定可能な場合、解法と視覚化を表示

## 🛠 技術仕様

- **フロントエンド**: Streamlit
- **アルゴリズム**: BFS（幅優先探索）、GCD（最大公約数）
- **視覚化**: Matplotlib
- **グラフ処理**: NetworkX
- **言語**: Python 3.8+

## 📦 インストール

### ローカル実行

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/water-jug-puzzle.git
cd water-jug-puzzle

# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを起動
streamlit run streamlit_app.py
```

### オンライン版
[Streamlit Community Cloud](https://your-app-name.streamlit.app) でホストされています。

## 🔧 依存関係

- streamlit >= 1.28.0
- matplotlib >= 3.7.0
- networkx >= 3.1
- numpy >= 1.24.0
- japanize-matplotlib >= 1.1.3

## 📖 水差しパズルとは

水差しパズルは、容量の異なる2つの容器を使って、指定された水量を正確に測定する古典的なパズルです。使用できる操作は：

1. 容器を満杯にする
2. 容器を空にする
3. 一方の容器から他方へ水を移す

## 🧮 アルゴリズム

### 測定可能性判定
目標水量 `t` が測定可能 ⟺ `t % gcd(a, b) == 0` かつ `t ≤ max(a, b)`

### 最短解法探索
NetworkXのBFSを使用して、状態空間グラフを探索し最短手順を発見

## 🎨 視覚化機能

- 容器Aを青色の横棒グラフで表示（左側、負の値）
- 容器Bを緑色の横棒グラフで表示（右側、正の値）
- 各ステップの操作説明と現在の水量を表示
- 最大容量を示すガイドライン

## 📄 ライセンス

MIT License

## 👤 作成者

作成者: GitHub Copilot  
連絡先: mkato9984@gmail.com

## 必要なライブラリ

- streamlit
- matplotlib
- networkx
- numpy
