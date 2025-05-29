# 日本語フォントテスト用
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st

def test_japanese_fonts():
    """利用可能な日本語フォントをテストして最適なものを選択"""
    
    # 利用可能なフォントを検索
    all_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 日本語フォント候補（優先順位順）
    japanese_font_candidates = [
        'Noto Sans JP',
        'BIZ UDGothic', 
        'Yu Gothic',
        'Meiryo',
        'MS Gothic',
        'Hiragino Sans',
        'IPAGothic',
        'Noto Sans CJK JP'
    ]
    
    print("=== フォントテスト結果 ===")
    
    # 各フォントをテスト
    for font in japanese_font_candidates:
        if font in all_fonts:
            try:
                # テスト描画
                plt.figure(figsize=(8, 2))
                plt.rcParams['font.family'] = [font]
                plt.text(0.5, 0.5, f'日本語テスト: {font}', 
                        fontsize=14, ha='center', va='center')
                plt.title(f'Font Test: {font}')
                plt.axis('off')
                
                # Streamlitで表示
                st.write(f"✅ {font} - 正常動作")
                st.pyplot(plt.gcf())
                plt.close()
                
                return font  # 最初に成功したフォントを返す
                
            except Exception as e:
                print(f"❌ {font} - エラー: {e}")
                plt.close()
        else:
            print(f"⚠️ {font} - インストールされていません")
    
    return None

# Streamlitアプリ
st.title("日本語フォントテスト")
best_font = test_japanese_fonts()

if best_font:
    st.success(f"最適なフォント: {best_font}")
else:
    st.error("日本語フォントが見つかりませんでした")
