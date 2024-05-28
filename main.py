import streamlit as st
from langchain.memory import ConversationBufferMemory
from utils import get_chat_response

st.title("mini ChatGPT")

with st.sidebar:
    openai_api_key = st.text_input("请输入您的OpenAI API密钥：", type="password")
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True) # return_messages=True表示展示聊天记录
    # 先给回话状态添加一个初始化消息，用于展示ai的欢迎语
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮助您的？"}]

for message in st.session_state["messages"]:
    # 刚开始只有一个欢迎语，只创建一个欢迎语的聊天组件
    # st.chat_message用于创建一个聊天界面的组件，role表示消息的发送方，content表示消息的内容
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("请输入您的问题：")
new_chat = st.button("新的聊天")

if prompt:
    if not openai_api_key:
        st.info("请输入你的OpenAI API密钥")
        st.stop()
    # messages是一个列表，可以将输入的聊天添加到列表中
    st.session_state["messages"].append({"role": "human", "content": prompt})
    # 创建一个人类的聊天组件，并将输入的内容写入
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"], openai_api_key)
    msg = {"role": "ai", "content": response}
    # 把回复添加到列表中
    st.session_state["messages"].append(msg)
    # 创建一个ai聊天组件，并将回复的内容写入
    st.chat_message("ai").write(response)

if new_chat:
    st.session_state.clear()
    # 重新初始化memory和添加初始的欢迎消息
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai", "content": "你好，我是你的AI助手，有什么可以帮助您的？"}]

    # streamlit不支持直接刷新页面，需要使用experimental_rerun()
    st.experimental_rerun()
