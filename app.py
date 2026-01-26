import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('人口推移')

df = pd.read_csv('c01.csv')

with st.sidebar:
    selected_pre = st.multiselect('都道府県を選択してください（複数選択可）',
                            df['都道府県名'].unique())
    year = st.selectbox('西暦を選択してください',
                         df['西暦（年）'].unique())
    color = st.selectbox('分類を選択してください',
        ['人口（総数）', '人口（男）', '人口（女）']
    )

    option = st.radio('表示形式を選択してください',
                      ['表', 'グラフ'])
    
df = df[df['都道府県名'].isin(selected_pre)]
df = df[df['西暦（年）']== year]

if option == '表':
    st.dataframe(df, width=800, height=220)

elif option == 'グラフ':
    fig = px.scatter(
        df,
        x='都道府県名',
        y='西暦（年）',
        color=color,
        trendline='ols',
        range_x=[0, df['都道府県名'].max()],
        range_y=[0, df['西暦（年）'].max()]
    )
    st.plotly_chart(fig)