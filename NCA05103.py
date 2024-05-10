import streamlit as st
import pandas as pd
import base64

# データフレームを初期化する関数
def init_df():
    data = {'食品名': [], 'エネルギー': [], 'たんぱく質': [], '脂質': [], '炭水化物': [], '食塩': [], '単価': []}
    return pd.DataFrame(data)

# Streamlitアプリを設定
st.title('食品データベース')


# サイドバーに配置する要素（Aページの場合）
st.sidebar.subheader('食品成分の登録')
food_name = st.sidebar.text_input('食品名を入力してください')
energy = st.sidebar.slider('エネルギー', min_value=0.0, max_value=1000.0, step=0.1, format="%.1f")  # 小数点第1位まで表示
protein = st.sidebar.slider('たんぱく質', min_value=0.0, max_value=100.0, step=0.1, format="%.1f")  # 小数点第1位まで表示
fat = st.sidebar.slider('脂質', min_value=0.0, max_value=100.0, step=0.1, format="%.1f")  # 小数点第1位まで表示
carbs = st.sidebar.slider('炭水化物', min_value=0.0, max_value=100.0, step=0.1, format="%.1f")  # 小数点第1位まで表示
salt = st.sidebar.slider('食塩', min_value=0.0, max_value=10.0, step=0.1, format="%.1f")  # 小数点第1位まで表示
price = st.sidebar.slider('単価', min_value=0.0, max_value=1000.0, step=0.1)  # 単価は整数表示
register_button = st.sidebar.button('食品成分を登録')
reset_button = st.sidebar.button('リセット')


# データフレームを取得
df = st.session_state.get('food_df', None)

# データフレームがない場合は初期化
if df is None:
    df = init_df()
    st.session_state['food_df'] = df

# 食品成分を登録する関数
def register_food(food_name, energy, protein, fat, carbs, salt, price):
    new_row = {'食品名': food_name, 'エネルギー': energy, 'たんぱく質': protein, '脂質': fat, '炭水化物': carbs, '食塩': salt, '単価': price}
    df.loc[len(df)] = new_row
    st.session_state['food_df'] = df

# 登録ボタンがクリックされたら食品成分を登録
if register_button:
    if food_name != '':
        register_food(food_name, energy, protein, fat, carbs, salt, price)

# リセットボタンがクリックされたらデータフレームをリセット
if reset_button:
    df = init_df()
    st.session_state['food_df'] = df

# 登録された食品成分を表示する
st.subheader('新しく登録された食品:')
st.write(df)

# CSVファイルをストリーミングしてダウンロード
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="food_data.csv">食品データをダウンロード</a>'
st.markdown(href, unsafe_allow_html=True)

# 保存した食品データをアップロード
uploaded_file = st.sidebar.file_uploader('保存した食品データをアップロード', type=['csv'])
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    combined_df = pd.concat([df, uploaded_df], ignore_index=True)
    st.subheader('保存した食品データと新しい食品データ:')
    st.write(combined_df)
    
else:
    st.subheader('保存した食品データと新しい食品データ:')
    st.write(df)
    
# 初期表示時に結合した食品データをダウンロードできるリンクを表示
combined_filename = 'combined_food_list.csv'
b64_combined = base64.b64encode(df.to_csv(index=False).encode()).decode()
href_combined = f'<a href="data:file/csv;base64,{b64_combined}" download="{combined_filename}">結合した食品データをダウンロード</a>'
st.markdown(href_combined, unsafe_allow_html=True)
