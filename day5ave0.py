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
st.markdown('###### 詳細は')
link = '[イチゲブログ](https://kikuichige.com/17379/)'
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
#******これやると日付が文字列なのでdateの処理が面倒くさいのでやめた
        # #今日の日付を文字列で取得
        # nowadays = datetime.now()
        # yesterday = nowadays - timedelta(1)
        # yesterday=yesterday.strftime('%Y-%m-%d')
        # st.text('昨日は'+yesterday)
        # #csvの1番最後の日付の文字列取得
        # s=df1.index[-1]
        # target = ' '
        # idx = s.find(target)
        # r = s[:idx]
        # st.text('csvに保存されている前日は'+r)
        # if yesterday == r:
        #     data=df1
        # else:
        #     yf.pdr_override() #追加
        #     today = date.today()
        #     ago = today - relativedelta(months=1)
        #     data = pdr.get_data_yahoo('^N225',  ago, today) #修正
        #     data.to_csv("nikkei.csv")
        #     yf.pdr_override() #追加
#*******end
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
            text='<span style="color:red">表示更新を押してください！</span>'
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
# #ichige_sconsole.csvをデータフレームで開く
# df = pd.read_csv('ichige_sconsole.csv')
# #st.text_inputの第一引数-ラベル、第二引数-初期値
# query_name=st.text_input('検索したいワード（例python　空欄のままで下のセレクトボックスから選んでもOKです')
# #st.form内のデータはsubmit_btnが押されると更新される。keyは、このフォームの名前で何でもいい。
# with st.form(key='profile_form'):
# #セレクトボックス今回はマルチセレクトにした。
# #上位クエリと掲載順位だけのデータフレームを作り掲載順位の最小値を抽出
#     df_value_min = df[['上位のクエリ','掲載順位']].groupby('上位のクエリ').min()
#     #掲載順位昇順で並べ替え
#     f_s = df_value_min.sort_values('掲載順位')
#     #index（上位のクエリ）の一覧作成。indexがarray型なのでtolistでlist化
#     query_list=f_s.index.values.tolist()
#     #検索したいワードに値がある場合は、その値が含まれるクエリのみにする。
#     l_in = [s for s in query_list if query_name in s]
#     #セレクトボックス初期値空欄に設定
#     l_in.insert(0, '-')
#     # selected_query=st.selectbox('クエリ候補(検索したいワードに入力してEnterすると候補が選択できます。▽をクリック！）',l_in[:100])
#  #マルチセレクト
#     mul_sel=st.multiselect(
#             '▼をクリック！全区間で平均検索順位の高い順に２００個表示されます。:red[2つ選んで表示を押してください。](検索したいワードに入力してEnterすると候補を絞れます。）',
#             l_in[:200]
#         )
  
#     submit_btn=st.form_submit_button('表示')
#     cancel_btn=st.form_submit_button('消す')
#     if submit_btn:
#         if mul_sel:
#             selected_query=mul_sel[0]
#     #1個しか選択していないときmul_sel[1]を参照するとout of indexのエラーになるので対策
#             try:
#                 selected_query1=mul_sel[1]
#             except:
#                 selected_query1='windows アプリ 自動操作 python'
#                 #Htmlのspanタグが使える
#                 text='<span style="color:red">Warning！</span><span style="color:black">1個しか選ばれていないので２個目は適当に表示してます。</span>'
#                 st.write(text, unsafe_allow_html=True)
 
#     #何も選択しないで表示を押したときの対策。適当なワードで表示する。
#         else:
#             selected_query='pandas 表計算'
#             selected_query1='windows アプリ 自動操作 python'
#             #Htmlのspanタグが使える
#             text='<span style="color:red">Warning！</span><span style="color:black">何も選ばれていないので適当に表示してます。</span>'
#             st.write(text, unsafe_allow_html=True)

#         #グループ化により選ばれたクエリのみでデータフレーム作成
#         df_a1 = df.groupby("上位のクエリ").get_group(selected_query)
#         df_b1 = df.groupby("上位のクエリ").get_group(selected_query1)

#         #日付のリスト化
#         date_list = df['日付'].to_list()

#         #重複削除-set()を使って重複削除すると、できたものがセット{}になって昔使えたlist()でリストにならないので、この方法はNG
#         # date_list_set=set(date_list)

#         #重複削除-これだとリストにできる
#         date_list_set = []

#         for i in date_list:
#             if i not in date_list_set:
#                 date_list_set.append(i)
#         #日付以外、空データのデータフレーム作成
#         columns = ['上位のクエリ', '掲載順位','日付']
#         df_x = pd.DataFrame(index=[], columns=columns)

#         for i in date_list_set:
#             list = [[None,None,i]]
#             df_append = pd.DataFrame(data=list, columns=columns)
#             df_x1 = pd.concat([df_x, df_append], ignore_index=True, axis=0)
#             df_x=df_x1

#         #データフレームと空のデータフレームを結合
#         df_contact_a1=pd.concat([df_a1,df_x])
#         df_contact_b1=pd.concat([df_b1,df_x])
#         #日付が同じ行は削除、必ず空の行を後ろに結合する。前に入れると空の行がのこってしまう。
#         df_a2=df_contact_a1.drop_duplicates(subset='日付')
#         df_b2=df_contact_b1.drop_duplicates(subset='日付')
#         #列名'掲載順位'を各選ばれたクエリに変更
#         df_a2=df_a2.rename(columns={'掲載順位': selected_query})
#         df_b2=df_b2.rename(columns={'掲載順位': selected_query1})
#         #日付とクエリのデータフレーム作成
#         df_a3=df_a2[['日付',selected_query]]
#         df_b3=df_b2[['日付',selected_query1]]
#         #日付の年市も2桁と月だけ切り出す
#         df_a3['日付']=df_a3['日付'].str[2:7]
#         df_b3['日付']=df_b3['日付'].str[2:7]
#         #日付をキーにマージ
#         df_contact=pd.merge(df_a3, df_b3, on='日付')
#         #ソート
#         df_a4 = df_a3.sort_values('日付')
#         df_b4 = df_b3.sort_values('日付')
#         #結果表の処理、グラフはa4、b4使う。欠損しているものを0または100にするとグラフがみにくくなるため。
#         #欠損を0で埋める。Nanだと.round().astype(int)ができない。
#         df_a5=df_a4.fillna(0)
#         #検索順を四捨五入して少数から整数へ
#         df_a5[selected_query]=df_a5[selected_query].round().astype(int)
#         df_b5=df_b4.fillna(0)
#         df_b5[selected_query1]=df_b5[selected_query1].round().astype(int)
#         #結果を日付をキーにして結合
#         result_df=pd.merge(df_a5,df_b5,on='日付')
#         st.text('イチゲブログ検索ワード別検索順位　（0は検索順位圏外または、その月に検索されていない）')
#         result_df
#         #text内の改行は\n
#         st.text('検索ワード”'+selected_query+'”または”'+selected_query1+'”を\nGoogleで検索してイチゲブログhttps://kikuichige.comが出るか確認してみてください。')
#         #matplotlib
#         fig,ax=plt.subplots()
#         ax.invert_yaxis()
#         #場複数系列の場合２つに分けか１つに２つ書く、この場合x軸同じでもx,y書く。この場合ラベルが使えない
#         ax.plot(df_a4['日付'],df_a4[selected_query],label=selected_query,marker='o')
#         ax.plot(df_b4['日付'],df_b4[selected_query1],label=selected_query1,marker='o')
#         ax.set_title('イチゲブログ検索ワード別検索順位')
#         ax.set_xlabel('日付')
#         #y軸ラベル横書き
#         ax.set_ylabel('検索順位',rotation='horizontal')
#         ax.grid()
#         #label表示に必要
#         ax.legend()
#         st.pyplot(fig)
        
        