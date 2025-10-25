import streamlit as st

st.set_page_config(page_title="Văn AI Demo", page_icon="🔥")

st.title("🪄 Trợ lý ảo Văn AI - Bếp lửa")
st.write("Chào bạn! Tôi là trợ lý ảo giúp bạn tìm hiểu về bài thơ **'Bếp lửa' của Bằng Việt**.")

question = st.text_input("Bạn muốn hỏi điều gì về bài thơ 'Bếp lửa'?")

if question:
    st.write("🤖 Trợ lý trả lời:")
    st.write(f"Bạn vừa hỏi: '{question}' — tôi sẽ giúp bạn tìm hiểu nội dung, ý nghĩa hoặc nghệ thuật của bài thơ!")