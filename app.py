import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# .env 読み込み（ローカル用）
load_dotenv()

st.set_page_config(page_title="Streamlit × LangChain LLMアプリ", page_icon="🤖")

st.title("🤖 Streamlit × LangChain LLMアプリ")
st.write(
    "このアプリは、入力したテキストをLangChain経由でLLMに渡して回答します。\n"
    "1) 下のラジオで専門家の役割を選ぶ\n"
    "2) 質問を入力して送信\n"
    "※ OpenAIのAPIキーは `.env` の `OPENAI_API_KEY` に設定してください。"
)

# 専門家選択（A/Bは必須＋おまけ1種）
role = st.radio(
    "専門家の種類を選択：",
    ("ビジネスコンサルタント(A)", "英語コーチ(B)", "データアナリスト(C)"),
    horizontal=True
)

# 入力フォーム
user_text = st.text_input("質問（プロンプト）を入力：", placeholder="例）新規事業の戦略を考えて")

def ask_llm(user_input: str, expert_type: str) -> str:
    if expert_type == "ビジネスコンサルタント(A)":
        system_msg = (
            "あなたは優秀なビジネスコンサルタントです。"
            "実行手順・数値例・想定リスクと対策も併記して、実務で使える提案をしてください。"
        )
    elif expert_type == "英語コーチ(B)":
        system_msg = (
            "あなたは丁寧な英語学習コーチです。"
            "学習者のレベルを仮定し、例文・和訳・練習問題・学習計画も提示してください。"
        )
    else:  # データアナリスト(C)
        system_msg = (
            "あなたは有能なデータアナリストです。"
            "前提・仮説・KPI・分析手順・可視化案・次アクションを簡潔に提案してください。"
        )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    messages = [SystemMessage(content=system_msg), HumanMessage(content=user_input)]
    resp = llm.invoke(messages)
    return resp.content

if st.button("送信", type="primary"):
    if not user_text.strip():
        st.warning("質問を入力してください。")
    else:
        with st.spinner("考え中..."):
            try:
                answer = ask_llm(user_text, role)
                st.markdown("### 🧠 回答")
                st.write(answer)
            except Exception as e:
                st.error(
                    f"エラー: {e}\n\n"
                    "・OPENAI_API_KEY が設定されているか\n"
                    "・ネットワーク状況\n"
                    "・モデル名の綴り などをご確認ください。"
                )
