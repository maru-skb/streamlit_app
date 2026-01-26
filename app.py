import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('人口推移')

df = pd.read_csv('c01.csv')

st.title('アプリの概要')

with st.sidebar:
    selected_pre = st.multiselect('都道府県を選択してください（複数選択可）',
                            df['都道府県名'].unique())
    population_type = st.selectbox('分類を選択してください',
        ['人口（総数）', '人口（男）', '人口（女）']
    )

    option = st.radio('表示形式を選択してください',
                      ['表', 'グラフ'])
    
df = df[df['都道府県名'].isin(selected_pre)]

if option == '表':
    st.dataframe(df)

elif option == 'グラフ':
    fig = px.scatter(
        df,
        x='西暦（年）',
        y=population_type,
        color='都道府県名',
        trendline='ols',
        range_x=[1910, df['西暦（年）'].max()],
        range_y=[0, df[population_type].max()]
    )
    st.plotly_chart(fig)