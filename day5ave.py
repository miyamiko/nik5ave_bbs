import streamlit as st
import pandas as pd
from pandas_datareader import data  as pdr #修正
# import datetime
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import yfinance as yf #追加
yf.pdr_override() #追加

st.title('日経平均今日の5日線　-　イチゲブログ')
st.caption('日経平均の今日5日線上にくる株価がいくらになるか計算します')
st.markdown('###### Streamelitやこのサイトの関連情報は')
link = '[イチゲブログ](https://kikuichige.com/17180/)'
st.markdown(link, unsafe_allow_html=True)
# link = '[Yahoo!ファイナンス 日経平均株価](https://finance.yahoo.co.jp/quote/998407.O/history)'
# st.markdown(link, unsafe_allow_html=True)
text='<span style="color:red"><a href="https://finance.yahoo.co.jp/quote/998407.O/history">Yahoo!ファイナンス 日経平均株価時系列</a>でデータを確認してください！</span>'
st.write(text, unsafe_allow_html=True)
st.text('5日平均計算式\nx=x1+x2+x3+x4+x　（x:今日の終値=5日平均線　x1～x4：1～4日前の終値）より\nx=(x1+x2+x3+x4)/4になる。つまり4日平均に今日の終値がなれば、その値が今日の終値＝5日線になる。')
with st.form(key='profile_form'):

    submit_btn=st.form_submit_button('5日線表示')
    cancel_btn=st.form_submit_button('消す')
    if submit_btn:
        df1=pd.read_csv("nikkei.csv",index_col=0)

        today = date.today()
        ago = today - relativedelta(months=1)
        data = pdr.get_data_yahoo('^N225',  ago, today) #修正
        data.to_csv("nikkei.csv")
        close6=data[['Close']]
        close61=close6.iloc[::-1]
        close62=close61[0:5]
        close62.reset_index(inplace=True)
        closer=close62['Close'].round(2)
        dayd=close62['Date'].dt.date
        closer=closer.rename("終値")
        dayd=dayd.rename("日付")
        close_5days=pd.concat([dayd,closer],axis=1)
        close_5days
        tstr = today.strftime('%Y/%m/%d')
        old5days=closer.values.tolist()
        old5daysave=round(sum(old5days)/len(old5days),2)
        st.text(tstr+'の5日平均線は'+str(old5daysave))
        old4days=old5days[:4]
        old4daysave=round(sum(old4days)/len(old4days),2)
        st.text(tstr+'の4日平均線は'+str(old4daysave))
        st.text('投資をおこなう際には、当ホームページに掲載されている情報に全面的に依拠し、\n投資判断する事はお控えいただき、必ずご自身の判断でなされるようお願いいたします。')
st.title('簡易掲示板イチゲブログ')
st.caption('csvファイルを使って掲示板作ってみました。')
with st.form(key='keijiban_form'):
    name=st.text_input('名前')
    message=st.text_input('メッセージ')
    st.text('投稿を押したあと表示更新を押してください。')
    toukou_btn=st.form_submit_button('投稿')
    hyouji_btn=st.form_submit_button('表示更新')
    st.markdown('###### 簡易掲示板')
    # del_no=st.text_input('削除する番号を選んでください')
    #セレクトボックス
    df=pd.read_csv("toukou.csv",index_col=0)
    st.dataframe(df)
    del_list=df.index.values
    del_no=st.selectbox(
            '削除する番号を選んでください',
            (del_list))
    # hyouji_btn=st.form_submit_button('削除直後や、セレクトボックスの値がおかしいときは、このボタンを押してください。セレクトボックスの番号がリフレッシュされます。')
    del_btn=st.form_submit_button('削除')
    if toukou_btn or hyouji_btn:
        # df=pd.read_csv("toukou.csv",index_col=0)
        if toukou_btn: 
            dt_now = datetime.now()
            toukoubi=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
            columns = [ '投稿日','名前','内容']
            list = [[toukoubi,name,message
            ]]
            df_append = pd.DataFrame(data=list, columns=columns)
            df1 = pd.concat([df, df_append], ignore_index=True, axis=0)
            df=df1
            df.to_csv("toukou.csv")
            text='<span style="color:blue">表示更新を押してください！</span>'
            st.write(text, unsafe_allow_html=True)
        else:
            df1=df
        # df1
        del_list=df.index.values
        # del_no=st.selectbox(
        #         '削除する番号を選んでください',
        #         (del_list))
    if del_btn:
        # st.text('del_no'+del_no)
        # df=pd.read_csv("toukou.csv",index_col=0)
        df1=df.drop(del_no, axis=0)
        # df1
        df=df1
        del_list=df.index.values
        df.to_csv("toukou.csv")
        text='<span style="color:red">表示更新を押してください！</span>'
        st.write(text, unsafe_allow_html=True)
