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

    with st.expander('データの詳細と注意点'):
        st.write('・データ元：e-stat 男女別人口-全国, 都道府県（大正9年～平成27年）「国勢調査」')
        st.write('・期間：大正9年から平成27年までの人口推移を確認できます')
        st.write('・単位：人')
        st.write('・注意点：本来データにあった、全国および人口集中地区・人口集中地区以外、というデータは除外している')                

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

    with st.expander('グラフについて'):
        st.write('このグラフは選択した都道府県の人口の変化を折れ線グラフで表わしている。')
        st.write('都道府県を複数選択することで、各都道府県の人口を比較することができる。')
        st.write('折れ線グラフが右肩上がりなら増加、右肩下がりなら減少していることが分かる。')
        st.write('各都道府県を比較することで、地域ごとの増減の違いが分かる。')

    # 最新年の合計を表示
    latest_year = df['西暦（年）'].max()
    # 最新年から選んだ都道府県の人口合計を計算する
    total_value = df[df['西暦（年）'] == latest_year][population_type].sum()
    st.metric(
        label=f'選択した都道府県（{latest_year}）年の合計人口',
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

    with st.expander('グラフについて'):
        st.write('このグラフは選択した都道府県の最新（2015年）の人口を棒グラフで表わしている。')
        st.write('都道府県を複数選択することで、各都道府県の人口を比較することができる。')
        st.write('棒グラフが高いほど、その地域の人口が多いことが分かる。')

    # 選択したデータ一覧を表示
elif option == '表':
    st.title('データ一覧')
    st.write(f'{selected_pre}のデータです')
    st.dataframe(df[['都道府県名', '西暦（年）', population_type]])
