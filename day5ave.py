import streamlit as st
import pandas as pd
import yfinance as yf
import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# --- 初期設定: 必要なCSVファイルがない場合に作成する ---
def initialize_csv(filename, columns):
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename)

initialize_csv("nikkei.csv", ["Date", "Close"])
initialize_csv("toukou.csv", ["投稿日", "名前", "内容"])

# --- メイン処理 ---
st.title('日経平均今日の5日線 - イチゲブログ')
st.caption('日経平均の今日5日線上にくる株価がいくらになるか計算します')

st.markdown('###### Streamlitやこのサイトの関連情報は')
st.markdown('[イチゲブログ](https://kikuichige.com/17180/)', unsafe_allow_html=True)

text='<span style="color:red"><a href="https://finance.yahoo.co.jp/quote/998407.O/history">Yahoo!ファイナンス 日経平均株価時系列</a>でデータを確認してください！</span>'
st.write(text, unsafe_allow_html=True)

st.text('5日平均計算式:\nx = (x1+x2+x3+x4+x_today)/5')

with st.form(key='profile_form'):
    submit_btn = st.form_submit_button('5日線表示')
    if submit_btn:
        today = date.today()
        ago = today - relativedelta(months=1)
        
        # yfinanceでデータ取得 (auto_adjust=Trueで列名をシンプルにする)
        data = yf.download('^N225', start=ago, end=today, auto_adjust=True)
        
        if not data.empty:
            data.to_csv("nikkei.csv")
            
            # 直近5日分を取得
            close6 = data[['Close']].iloc[::-1].head(5)
            close6.reset_index(inplace=True)
            
            # 表示用に整形
            closer = close6['Close'].round(2)
            dayd = close6['Date'].dt.date
            
            # 名前の変更（エラー回避のためname属性を直接変更）
            closer.name = "終値"
            dayd.name = "日付"
            
            close_5days = pd.concat([dayd, closer], axis=1)
            st.table(close_5days) # dataframeよりtableの方が見やすい場合があります
            
            # 計算処理
            tstr = dayd.iloc[0].strftime('%Y年%m月%d日')
            old5days = closer.values.tolist()
            old5daysave = round(sum(old5days)/len(old5days), 2)
            
            st.success(f'{tstr}時点の5日移動平均値: {old5daysave}')
            
            old4days = old5days[:4]
            old4daysave = round(sum(old4days)/len(old4days), 2)
            st.info(f'直近4日間の平均値: {old4daysave}')
        else:
            st.error("データの取得に失敗しました。時間をおいて試してください。")

# --- 掲示板セクション ---
st.divider()
st.title('簡易掲示板')

# 最新の投稿を読み込み
df_board = pd.read_csv("toukou.csv", index_col=0)

with st.form(key='keijiban_form'):
    name = st.text_input('名前')
    message = st.text_area('メッセージ') # 長文入力に対応
    toukou_btn = st.form_submit_button('投稿')
    
    if toukou_btn and name and message:
        dt_now = datetime.now()
        toukoubi = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
        new_data = pd.DataFrame([[toukoubi, name, message]], columns=['投稿日', '名前', '内容'])
        df_board = pd.concat([df_board, new_data], ignore_index=True)
        df_board.to_csv("toukou.csv")
        st.success("投稿しました！")
        st.rerun() # 画面を更新して最新の状態を表示

st.dataframe(df_board, use_container_width=True)

# 削除機能
if not df_board.empty:
    del_no = st.selectbox('削除する番号を選んでください', df_board.index)
    if st.button('選択した投稿を削除'):
        df_board = df_board.drop(del_no, axis=0)
        df_board.to_csv("toukou.csv")
        st.warning(f"番号 {del_no} を削除しました。")
        st.rerun()