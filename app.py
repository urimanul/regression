import streamlit as st
import pandas as pd
import statsmodels.api as sm
import requests
from io import BytesIO
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import tempfile
import textwrap

# サンプルデータの作成
data_mercedes = {
    'ブランドイメージ': [4.5, 4.6, 4.7, 4.8, 4.9] * 20,
    '顧客体験': [5, 4, 5, 4.5, 5] * 20,
    'リレーションシップ営業': [4.2, 4.0, 4.8, 4.5, 4.6] * 20,
    'ローン・リースプラン': [3.5, 4.0, 3.8, 3.7, 4.1] * 20,
    '保証サービス': [4.5, 4.6, 4.4, 4.3, 4.7] * 20,
    '広告費': [60, 70, 50, 40, 80] * 20,
    '売上': [500, 480, 510, 495, 530] * 20
}

# フォントをWebからダウンロードして登録
font_url = 'https://www.ryhintl.com/font-nasu/Nasu-Regular.ttf'  # 使用したいフォントファイルのURL
font_name = 'MS-Gothic'
response = requests.get(font_url)
with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tf:
    tf.write(response.content)
    pdfmetrics.registerFont(TTFont(font_name, tf.name))

# PDF生成関数
def generate_pdf(content):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    
    # 日本語フォント設定
    p.setFont(font_name, 10)
    p.drawString(10, 550, "Regression Result Analysis")
    text = p.beginText(10, 530)
    text.setFont(font_name, 10)
    text.setLeading(12)
    
    # テキストをページ幅に合わせて折り返し
    max_width = 800  # ページ横幅に収まるように調整
    for line in content.split("\n"):
        wrapped_lines = textwrap.wrap(line, width=90)  # 90文字ごとに改行
        for wrapped_line in wrapped_lines:
            text.textLine(wrapped_line)
        text.textLine("")  # 行間を開ける
    
    p.drawText(text)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

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
else:
    df = pd.DataFrame(data_mercedes)

# 説明変数と目的変数に分ける
if dataframe == 'サービス':
    X = df[['ローン・リースプラン', '保証サービス', '広告費']]
    y = df['売上']
elif dataframe == 'ブランド':
    X = df[['ブランドイメージ', '顧客体験', 'リレーションシップ営業']]
    y = df['売上']
else:
    X = df[['ブランドイメージ', '顧客体験', 'リレーションシップ営業']]
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
groqResp = response.json()['choices'][0]['message']['content']

# Streamlitで結果を表示
st.subheader('Regression 結果')
st.text(results_summary)
st.subheader('結果分析')
st.text_area('Result Analysis', groqResp, height=300)

# PDFボタンの作成
if st.button("結果を印刷"):
    pdf_buffer = generate_pdf(str(results_summary) + "\n\n" + groqResp)
    st.download_button("Download PDF", pdf_buffer, "分析結果.pdf", "application/pdf")
