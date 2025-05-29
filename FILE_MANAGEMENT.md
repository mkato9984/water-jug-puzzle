# Water Jug Puzzle - ファイル管理記録

## ファイル構成と用途

### 🎯 現在使用中（本番）
- `streamlit_app.py` - **メインファイル** (本番環境・Streamlit Cloud対応)
- `requirements.txt` - Python依存関係定義
- `README.md` - プロジェクト説明・使用方法
- `.streamlit/config.toml` - Streamlit設定（テーマ・サーバー設定）

### 📚 バックアップ・参考ファイル
- `streamlit_app_backup.py` - 初期バックアップ（シンプル版）
- `streamlit_app_fixed.py` - 改良版（日本語フォント強化・参考用）

### 📋 ドキュメント
- `WORK_LOG_WATER_JUG_PUZZLE.md` - 全体作業ログ
- `WORK_LOG_2025-05-29_RECOVERY.md` - 復旧作業ログ
- `FILE_MANAGEMENT.md` - このファイル

### 🔧 設定ファイル
- `.gitignore` - Git無視ファイル設定
- `.git/` - Gitリポジトリデータ

## 📁 推奨管理方法

### 保持すべきファイル（必須）
1. `streamlit_app.py` - 現在の本番ファイル
2. `requirements.txt` - 依存関係
3. `README.md` - プロジェクト説明
4. `.streamlit/config.toml` - 設定

### 保持すべきファイル（バックアップ）
1. `streamlit_app_backup.py` - 動作確認済みクリーンバージョン
2. `streamlit_app_fixed.py` - 日本語フォント改良版（参考用）

### 削除済みファイル（2025-05-29）
- `streamlit_app_working_2025-05-29.py` - 作業用一時ファイル
- `check_fonts.py` - フォントチェック用テストファイル
- `test_app.py` - 動作テスト用ファイル
- `test_japanese_font.py` - 日本語フォントテスト用ファイル

## 🎯 アプリケーション概要

### 機能
- **水差しパズル解法**: 数学的解存在判定（GCD算法）
- **最短経路探索**: BFSアルゴリズム実装
- **視覚化**: Matplotlib横棒グラフによるステップ表示
- **日本語対応**: ローカル・クラウド環境対応

### デプロイ状況
- **ローカル**: http://localhost:9000 - 正常動作
- **Streamlit Cloud**: https://water-jug-puzzle.streamlit.app/ - 動作中
- **GitHub**: mkato9984/water-jug-puzzle - 同期済み

## 🔄 今後の開発方針

### ファイル変更時のルール
1. **メインファイル変更前**: `streamlit_app_backup.py`から新しいバックアップ作成
2. **大きな変更時**: 日付入りバックアップファイル作成
3. **テスト完了後**: 不要な一時ファイルは削除

### バージョン管理
- **Git**: 主要変更のコミット・プッシュ
- **バックアップ**: 動作確認済みファイルの保持
- **ドキュメント**: 作業ログの継続更新

## 📊 ファイルサイズ・更新情報
- `streamlit_app.py`: 最新版（シンタックスエラー修正済み）
- `streamlit_app_backup.py`: 初期安定版
- `streamlit_app_fixed.py`: 改良版（日本語フォント強化）

## 🏁 現在の状態
**最終更新**: 2025年5月29日  
**状態**: ✅ 正常動作・バックアップ完了  
**次ステップ**: GitHubコミット推奨
