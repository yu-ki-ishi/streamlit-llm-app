import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 

st.set_page_config(
    page_title="専門家チャット",
    page_icon="💬", 
    layout="centered"
)

st.title("専門家チャット Webアプリ")
st.write("""
このアプリでは、入力フォームにテキストを入力し、ラジオボタンで専門家を選ぶことで、
OpenAI API がその専門家として回答します。  
- 専門家を選択してください  
- 質問を入力してください  
- 「送信」ボタンで回答が表示されます
""")

user_input = st.text_area("質問を入力してください:")
expert_choice = st.radio(
    "専門家を選択してください:",
    ("プログラミングの専門家", "マーケティングの専門家")
)

def get_llm_response(user_text: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類に応じてOpenAI APIからの回答を返す
    """

    if expert_type == "プログラミングの専門家":
        system_message = "あなたはプログラミングに詳しい専門家です。わかりやすく丁寧に回答してください。"
    elif expert_type == "マーケティングの専門家":
        system_message = "あなたはマーケティング戦略や市場分析に詳しい専門家です。具体例を交えて回答してください。"
    else:
        system_message = "あなたは有識者として丁寧に回答してください。"

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_text}
        ],
        temperature=0
    )

    answer = completion.choices[0].message.content
    return answer

if st.button("送信"):
    if not user_input.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            answer = get_llm_response(user_input, expert_choice)
        st.success("回答:")
        st.write(answer)
