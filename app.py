
# app.py
# Streamlit LLMアプリのエントリーポイント
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import os

st.title("専門家LLMチャットアプリ")
st.write("""
このアプリは、選択した専門家の視点でLLM（大規模言語モデル）があなたの質問に回答します。

【使い方】
1. 専門家の種類をラジオボタンで選択してください。
2. 質問や相談内容を入力フォームに記入し、「送信」ボタンを押してください。
3. 選択した専門家になりきったLLMの回答が表示されます。
""")

# 専門家の種類とシステムメッセージ
experts = {
	"医師": "あなたは優秀な医師です。医学的な知識と患者への思いやりを持って回答してください。",
	"弁護士": "あなたは経験豊富な弁護士です。法律の専門知識をもとに、分かりやすく丁寧に回答してください。",
	"ITエンジニア": "あなたは最新技術に精通したITエンジニアです。技術的な観点から分かりやすく回答してください。"
}

# ラジオボタンで専門家選択
selected_expert = st.radio("専門家を選択してください", list(experts.keys()))

# 入力フォーム
user_input = st.text_area("質問や相談内容を入力してください", height=100)

def get_llm_response(user_text, expert_type):
	"""
	入力テキストと専門家タイプを受け取り、LLMからの回答を返す
	"""
	system_message = SystemMessage(content=experts[expert_type])
	human_message = HumanMessage(content=user_text)
	openai_api_key = os.getenv("OPENAI_API_KEY")
	llm = ChatOpenAI(
		openai_api_key=openai_api_key,
		model="gpt-3.5-turbo",
		temperature=0.7
	)
	response = llm([system_message, human_message])
	return response.content

if st.button("送信"):
	if not user_input.strip():
		st.warning("質問内容を入力してください。")
	else:
		with st.spinner("LLMが回答中..."):
			answer = get_llm_response(user_input, selected_expert)
		st.success("【%s】としての回答:" % selected_expert)
		st.write(answer)
