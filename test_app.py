import streamlit as st
import sys
import os

# Pythonバージョンと環境の情報を表示
st.write(f"Python version: {sys.version}")
st.write(f"Platform: {sys.platform}")

# 現在のディレクトリとファイル一覧
st.write(f"Current directory: {os.getcwd()}")
st.write("Files in directory:")
for file in os.listdir("."):
    st.write(f"- {file}")

# インポートテスト
try:
    import japanize_matplotlib
    st.success("✅ japanize_matplotlib imported successfully")
except ImportError as e:
    st.error(f"❌ japanize_matplotlib import failed: {e}")

try:
    import matplotlib.pyplot as plt
    st.success("✅ matplotlib imported successfully")
except ImportError as e:
    st.error(f"❌ matplotlib import failed: {e}")

try:
    import networkx as nx
    st.success("✅ networkx imported successfully")
except ImportError as e:
    st.error(f"❌ networkx import failed: {e}")
