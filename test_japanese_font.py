import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 利用可能なフォントをリストアップ
print("利用可能なフォント:")
fonts = [f.name for f in fm.fontManager.ttflist]
japanese_fonts = [f for f in fonts if any(keyword in f.lower() for keyword in ['jp', 'japan', 'noto', 'meiryo', 'yu gothic', 'ms gothic', 'ms pgothic', 'hiragino'])]
print("日本語関連フォント:")
for font in japanese_fonts[:10]:  # 最初の10個を表示
    print(f"  - {font}")

# japanize-matplotlibのテスト
try:
    import japanize_matplotlib
    japanize_matplotlib.japanize()
    print("\n✅ japanize-matplotlib が正常にロードされました")
except ImportError:
    print("\n❌ japanize-matplotlib がインストールされていません")

# 簡単なプロットテスト
plt.figure(figsize=(8, 6))
plt.bar(['Aコンテナ', 'Bコンテナ'], [3, 5])
plt.title('水差しパズル - 容器の容量')
plt.ylabel('容量 (L)')
plt.savefig('test_japanese.png', dpi=100, bbox_inches='tight')
print("\nテスト画像 'test_japanese.png' を保存しました")
