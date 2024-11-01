import streamlit as st
import pandas as pd
import statsmodels.api as sm
import requests

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

data_nextage = {
    '価格': [200, 150, 300, 250, 100],
    '広告費': [50, 40, 60, 70, 30],
    '在庫数': [100, 120, 80, 90, 110],
    '車両品質': [4.5, 4.0, 4.8, 4.6, 4.2],
    '店舗立地': [3, 5, 4, 2, 4],
    '成約率': [0.5, 0.6, 0.55, 0.65, 0.6],
    '売上': [300, 250, 350, 330, 210]
}

# Streamlitアプリの設定
st.title('セールス分析')
st.write('セールスデータの回帰分析（因果探索）')

# データセットの選択
dataset = st.selectbox('データセット', ('Mercedes', 'BMW', 'NEXSTAGE'))

# データフレームの選択
if dataset in ['Mercedes', 'BMW']:
    dataframe = st.selectbox('データフレーム', ('ブランド', 'サービス'))
else:
    dataframe = st.selectbox('データフレーム', ('車両', '価格'))

# 選択されたデータセットに基づいてデータフレームを作成
if dataset == 'Mercedes':
    df = pd.DataFrame(data_mercedes)
elif dataset == 'BMW':
    df = pd.DataFrame(data_bmw)
else:
    df = pd.DataFrame(data_nextage)

# 説明変数と目的変数に分ける
if dataframe == 'サービス':
    X = df[['ローン・リースプラン', '保証サービス', '広告費']]
    y = df['売上']
elif dataframe == 'ブランド':
    X = df[['ブランドイメージ', '顧客体験', 'リレーションシップ営業']]
    y = df['売上']
elif dataframe == '車両':
    X = df[['車両品質', '店舗立地', '成約率']]
    y = df['売上']
else:
    X = df[['価格', '広告費', '在庫数']]
    y = df['売上']

# 定数項を追加
X = sm.add_constant(X)

# 重回帰分析モデルの作成とフィッティング
model = sm.OLS(y, X).fit()

# 結果の出力
results_summary = model.summary()

# Groq APIをコールして分析
API_URL = 'https://api.groq.com/openai/v1/'
MODEL = 'Llama-3.1-70b-Versatile'
API_KEY = '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'
maxTokens = 4096

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

data = {
    'model': MODEL,
    'max_tokens': maxTokens,
    'messages': [
        {
            'role': 'system',
            'content': '貴方は専門家です。できるだけわかりやすく答えてください。必ず、日本語で答えてください。'
        },
        {
            'role': 'user',
            'content': '以下の文章を分析してください。'+str(results_summary)
        }
    ]
}

response = requests.post(f'{API_URL}chat/completions', headers=headers, json=data)
#groqResp = response.json()['choices'][0]['message']['content']

# Streamlitで結果を表示
st.subheader('Regression Results')
st.text(results_summary)

st.subheader('Groq API Analysis Results')
st.text(groqResp)
#st.text(response.json()['choices'][0]['message']['content'])
