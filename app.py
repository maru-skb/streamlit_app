import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('人口推移')

df = pd.read_csv('c01.csv')

with st.sidebar:
    selected_cats = st.multiselect('都道府県を選択してください（複数選択可）',
                            df['都道府県名'])
    media = st.selectbox('広告媒体を選択してください',
                         df['media'].unique())
    color = st.selectbox('分類を選択してください',
        ['性別', '年齢層', '季節']
    )
    if color == '性別':
        color = 'sex'
    elif color == '年齢層':
        color = 'age'
    elif color == '季節':
        color = 'season'
    option = st.radio('表示形式を選択してください',
                      ['表', 'グラフ'])