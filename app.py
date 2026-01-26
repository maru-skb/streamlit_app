import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title('人口推移')

df = pd.read_csv('c01.csv')

with st.sidebar:
    st.header('メニュー')

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
                      ['アプリの概要', '表', 'グラフ'])
    
# 年順に並べ替える
df = df[df['都道府県名'].isin(selected_pre)]
df = df.sort_values('西暦（年）')

if option == 'アプリの概要':
    st.title('アプリの概要')
    st.write('本アプリは、e-statの「国勢調査」のデータを使用して、都道府県別の人口推移を可視化します。')
    st.write('サイドバーから都道府県や人口分類を選択して、グラフや表を確認してください。')

    with st.expander('データの出典と注意点'):
        st.write('・出典：政府統計の総合窓口(e-stat)「国勢調査」')
        st.write('・大正から平成までの人口推移を確認できます')
        st.write('・単位：人')                

elif option == 'グラフ':
    st.title(f'{population_type}の推移と比較')

    # 折れ線グラフを表示
    fig1 = px.line(
        df,
        x='西暦（年）',
        y=population_type,
        color='都道府県名',
    )
    st.plotly_chart(fig1)

    # 最新年の合計を表示
    latest_year = df['西暦（年）'].max()
    total_value = df[df['西暦（年）'] == latest_year][population_type].sum()
    st.metric(
        label=f'{latest_year}年の選択合計',
        value=f'{int(total_value):,}人'
        )

    # 棒グラフを表示
    st.write(f'{latest_year}年の比較')
    # 最新年だけのデータをグラフにする
    df_latest = df[df['西暦（年）'] == latest_year]
    fig2 = px.bar(
        df_latest,
        x = '都道府県名',
        y = population_type,
        color = '都道府県名'
    )
    st.plotly_chart(fig2)

elif option == '表':
    st.title('データ一覧')
    st.write(f'{selected_pre}のデータです')
    st.dataframe(df[['都道府県名', '西暦（年）', population_type]])
