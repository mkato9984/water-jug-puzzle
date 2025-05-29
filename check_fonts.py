import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# システムにインストールされているフォントを確認
print("=== システムフォント一覧 ===")
fonts = fm.fontManager.ttflist
japanese_fonts = []

for font in fonts:
    font_name = font.name.lower()
    if any(keyword in font_name for keyword in ['jp', 'japan', 'noto', 'meiryo', 'yu gothic', 'ms gothic', 'ms mincho', 'hiragino']):
        japanese_fonts.append(font.name)
        print(f"日本語フォント候補: {font.name}")

print(f"\n見つかった日本語フォント数: {len(japanese_fonts)}")

if japanese_fonts:
    print(f"最初の日本語フォント: {japanese_fonts[0]}")
    # 最初のフォントでテスト
    plt.rcParams['font.family'] = japanese_fonts[0]
    plt.rcParams['axes.unicode_minus'] = False
    
    # 簡単なテスト
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, "日本語テスト", ha='center', va='center', fontsize=20)
    ax.set_title("フォントテスト")
    plt.savefig("font_test.png", dpi=100, bbox_inches='tight')
    print("font_test.png を保存しました")
else:
    print("日本語フォントが見つかりませんでした")
    
# japanize-matplotlibの確認
try:
    import japanize_matplotlib
    print("\njapanize-matplotlib が利用可能です")
    japanize_matplotlib.japanize()
    
    # テスト
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, "japanize-matplotlib テスト", ha='center', va='center', fontsize=20)
    ax.set_title("japanize-matplotlib フォントテスト")
    plt.savefig("japanize_test.png", dpi=100, bbox_inches='tight')
    print("japanize_test.png を保存しました")
except ImportError:
    print("japanize-matplotlib がインストールされていません")
