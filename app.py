import streamlit as st
import pandas as pd
import statsmodels.api as sm

# サンプルデータの作成
data_mercedes = {
    'ブランドイメージ': [4.8, 4.7, 4.9, 4.6, 5.0],
    '顧客体験': [5, 4, 5, 4.5, 5],
    'リレーションシップ営業': [4.2, 4.0, 4.8, 4.5, 4.6],
    'ローン・リースプラン': [3.5, 4.0, 3.8, 3.7, 4.1],
    '保証サービス': [4.5, 4.6, 4.4, 4.3, 4.7],
    '広告費': [60, 70, 50, 40, 80],
    '価格設定': [800, 850, 820, 830, 810],
    '売上': [500, 480, 510, 495, 530]
}

data_bmw = {
    'ブランドイメージ': [4.5, 4.6, 4.7, 4.8, 4.9],
    '顧客体験': [4.8, 4.7, 4.9, 4.6, 5.0],
    'リレーションシップ営業': [4.1, 4.3, 4.2, 4.4, 4.5],
    'ローン・リースプラン': [3.8, 3.9, 4.0, 4.1, 4.2],
    '保証サービス': [4.3, 4.4, 4.5, 4.6, 4.7],
    '広告費': [55, 65, 75, 85, 95],
    '価格設定': [780, 790, 800, 810, 820],
    '売上': [490, 500, 510, 520, 530]
}

# Streamlitアプリの設定
st.title('Sales Analysis')
st.write('This app performs a regression analysis on sales data.')

# データセットの選択
dataset = st.selectbox('Select Dataset', ('Mercedes', 'BMW'))

# 選択されたデータセットに基づいてデータフレームを作成
if dataset == 'Mercedes':
    df = pd.DataFrame(data_mercedes)
else:
    df = pd.DataFrame(data_bmw)

# 説明変数と目的変数に分ける
X = df[['ローン・リースプラン', '保証サービス', '広告費']]
y = df['売上']

# 定数項を追加
X = sm.add_constant(X)

# 重回帰分析モデルの作成とフィッティング
model = sm.OLS(y, X).fit()

# 結果の出力
results_summary = model.summary()

# Streamlitで結果を表示
st.subheader('Regression Results')
st.text(results_summary)
