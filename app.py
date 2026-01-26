import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('人口推移')

df = pd.read_csv('c01.csv')

st.title('アプリの概要')
st.write('本アプリは国勢調査の人口データを用いて、都道府県別の人口推移を可視化するWebアプリです。')

with st.sidebar:
    st.header('設定')

    # 都道府県を選択（複数可）
    selected_pre = st.multiselect('都道府県を選択してください（複数選択可）',
                            df['都道府県名'].unique(),
                            default=['北海道'])
    
    # 分類を選択
    population_type = st.selectbox('分類を選択してください',
        ['人口（総数）', '人口（男）', '人口（女）']
    )

    # 表示形式を選択
    option = st.radio('表示形式を選択してください',
                      ['表', 'グラフ'])
    
# 年順に並べ替える
df = df[df['都道府県名'].isin(selected_pre).sort_values('西暦（年）')]

if option == '表':
    st.subheader('データ一覧')
    st.dataframe(df[['都道府県名', '西暦（年）', population_type]])

elif option == 'グラフ':
    y_min = df[population_type].min()
    y_max = df[population_type].max()

    fig = px.line(
        df,
        x='西暦（年）',
        y=population_type,
        color='都道府県名',
        range_x=[1910, df['西暦（年）'].max()],
        range_y=[y_min, y_max]
    )
    st.plotly_chart(fig)