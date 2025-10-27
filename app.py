import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# --- DỮ LIỆU CÁC KHỐI LỚP (ĐÃ NHẬP TỪ YÊU CẦU CỦA BẠN) ---

DATA_NGU_VAN = {
    "Lớp 6": {
        "Chủ đề 1: Tôi và các bạn": [
            "Bức tranh của em gái tôi – Tạ Duy Anh: Câu chuyện cảm động về tình anh em, sự hối hận và trưởng thành.",
            "Cuộc chia tay của những con búp bê – Khánh Hoài: Phản ánh nỗi đau trẻ em khi cha mẹ ly hôn."
        ],
        "Chủ đề 2: Yêu thương và chia sẻ": [
            "Gió lạnh đầu mùa – Thạch Lam: Tình người, lòng nhân ái trong cuộc sống.",
            "Mẹ tôi – Ét-môn-đô đơ A-mi-xi: Tình mẫu tử thiêng liêng.",
            "Nói và nghe: Kể về người thân mà em yêu quý."
        ],
        "Chủ đề 3: Quê hương, đất nước": [
            "Cô Tô – Nguyễn Tuân: Vẻ đẹp thiên nhiên và con người."
        ]
    },
    "Lớp 7": {
        "Chủ đề 1: Con người Việt Nam": [
            "Cuộc chia tay của những con búp bê – Khánh Hoài: Tình cảm anh em trong hoàn cảnh éo le.",
            "Mẹ tôi – Ét-môn-đô đơ A-mi-xi: Tình mẫu tử sâu sắc.",
            "Nói và nghe: Kể chuyện về lòng nhân hậu."
        ],
        "Chủ đề 2: Quê hương, đất nước": [
            "Sài Gòn tôi yêu – Minh Hương: Niềm tự hào và tình yêu với thành phố.",
            "Tĩnh dạ tứ – Lý Bạch: Nỗi nhớ quê hương da diết.",
            "Qua Đèo Ngang – Bà Huyện Thanh Quan: Nỗi niềm cô đơn và nhớ nước thương nhà.",
            "Viết bài nghị luận về tình yêu quê hương."
        ],
        "Chủ đề 3: Ước mơ và khát vọng": [
            "Những cánh buồm – Hoàng Trung Thông: Ước mơ của người cha gửi gắm cho con.",
            "Ca Huế trên sông Hương – Hà Ánh Minh: Nét đẹp văn hóa dân tộc.",
            "Thực hành nói: Trình bày cảm nghĩ về một nét đẹp văn hóa Việt Nam."
        ]
    },
    "Lớp 8": {
        "Chủ đề 1: Tình cảm gia đình": [
            "Trong lòng mẹ – Nguyên Hồng: Nỗi tủi hờn và tình mẫu tử sâu nặng.",
            "Chiếc lá cuối cùng – O. Henry: Bài học về hi sinh và lòng nhân ái.",
            "Nói và nghe: Kể lại một kỉ niệm xúc động về tình cảm gia đình."
        ],
        "Chủ đề 2: Quê hương, đất nước": [
            "Lặng lẽ Sa Pa – Nguyễn Thành Long: Vẻ đẹp của người lao động thầm lặng.",
            "Tức nước vỡ bờ – Ngô Tất Tố: Sức phản kháng mạnh mẽ của người nông dân.",
            "Viết bài nghị luận về nhân vật văn học."
        ],
        "Chủ đề 3: Thiên nhiên và con người": [
            "Ôn dịch, thuốc lá – Nguyễn Khắc Viện: Lời cảnh báo về tác hại của thuốc lá.",
            "Bàn về đọc sách – Chu Quang Tiềm: Ý nghĩa của việc đọc."
        ]
    },
    "Lớp 9": {
        "Chủ đề 1: Tổ quốc và con người Việt Nam": [
            "Mùa xuân nho nhỏ – Thanh Hải: Khát vọng sống cống hiến, hòa nhập với đất nước, quê hương.",
            "Viếng lăng Bác – Viễn Phương: Tình cảm sâu nặng, kính yêu Bác Hồ.",
            "Bếp lửa – Bằng Việt: Tình bà cháu, ngọn lửa của tình thương và nghị lực sống.",
            "Đoàn thuyền đánh cá – Huy Cận: Vẻ đẹp lao động và thiên nhiên, niềm tự hào dân tộc."
        ],
        "Chủ đề 2: Cuộc sống và con người": [
            "Lặng lẽ Sa Pa – Nguyễn Thành Long: Vẻ đẹp thầm lặng của người lao động.",
            "Chiếc lược ngà – Nguyễn Quang Sáng: Tình cha con cảm động trong chiến tranh.",
            "Nói và nghe: Kể về một tấm gương sống đẹp."
        ],
        "Chủ đề 3: Suy nghĩ về cuộc sống": [
            "Nghị luận xã hội: Tình yêu thương, sự sẻ chia, tinh thần trách nhiệm.",
            "Nghị luận văn học: Cảm nhận về một bài thơ, đoạn thơ, nhân vật văn học."
        ]
    }
}


# --- CẤU HÌNH API KEY VÀ CÁC HÀM XỬ LÝ CHAT ---

OPTIONS_LOP = ["Tất cả khối lớp", "Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9"]


def initialize_gemini_api():
    """Lấy API Key từ Streamlit Secrets hoặc Biến môi trường."""
    try:
        # Ưu tiên lấy Key từ secrets.toml (cho Streamlit Cloud)
        if "general" in st.secrets and "GOOGLE_API_KEY" in st.secrets["general"]:
            api_key_value = st.secrets["general"]["GOOGLE_API_KEY"]
        elif "GOOGLE_API_KEY" in st.secrets:
            api_key_value = st.secrets["GOOGLE_API_KEY"]
        else:
            # Lấy từ Biến môi trường hệ thống/Terminal
            api_key_value = os.environ.get("GOOGLE_API_KEY") 
            if not api_key_value:
                return None
        
        os.environ["GOOGLE_API_KEY"] = api_key_value
        return api_key_value
        
    except Exception:
        return None

def get_system_message(lop_selected):
    """Tạo System Prompt dựa trên lớp học được chọn."""
    if lop_selected == "Tất cả khối lớp":
        lop_context = "Ngữ Văn THCS (Lớp 6 đến Lớp 9)."
    else:
        lop_context = f"Ngữ Văn THCS, đặc biệt chú trọng kiến thức cho {lop_selected}."
        
    return SystemMessage(
        content=(
            f"Bạn là một Trợ lý Ngữ Văn THCS thân thiện, thông minh, chuyên về {lop_context}. "
            "Hãy trả lời các câu hỏi về văn học, ngữ pháp, và kiến thức xã hội với giọng điệu phù hợp học sinh."
        )
    )

def get_chat_response(api_key, conversation_history, user_input, lop_selected):
    """Gửi lịch sử chat và câu hỏi mới đến mô hình Gemini."""
    
    # Khởi tạo mô hình Gemini-2.5-flash
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=api_key,
    )
    
    # Thêm câu hỏi hiện tại vào lịch sử
    conversation_history.append(HumanMessage(content=user_input))
    
    # Gửi lịch sử và nhận phản hồi
    response = llm.invoke(conversation_history)
    
    # Cập nhật lịch sử với phản hồi của AI
    conversation_history.append(response)
    
    return response.content, conversation_history

# --- CÁC MODE CHỨC NĂNG ---

def mode_rag_qa(api_key, lop_selected):
    """Tính năng Hỏi đáp (Chatbot cơ bản)."""
    st.header("💬 Trợ Lý Ngữ Văn THCS (Gemini Chatbot)")
    st.caption(f"Đang trả lời với trọng tâm kiến thức: **{lop_selected}** (Sử dụng kiến thức chung của AI).")
    
    # Khởi tạo Lịch sử Chat (Nếu chưa tồn tại hoặc lớp thay đổi)
    if "conversation_history" not in st.session_state or st.session_state.get('last_lop') != lop_selected:
        st.session_state.conversation_history = [get_system_message(lop_selected)]
        st.session_state.last_lop = lop_selected
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": f"Chào em! Hiện tại AI đã được đặt trọng tâm vào **{lop_selected}**. Em có câu hỏi gì về Ngữ Văn không?"})
        
    # Hiển thị lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Xử lý input của người dùng
    if prompt := st.chat_input("Em có câu hỏi gì về Ngữ Văn hoặc kiến thức khác không?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Hiển thị tin nhắn người dùng
        with st.chat_message("user"):
            st.markdown(prompt)

        # Lấy và hiển thị phản hồi của AI
        with st.chat_message("ai"):
            with st.spinner("Gemini đang suy nghĩ..."):
                
                response_content, st.session_state.conversation_history = get_chat_response(
                    api_key, 
                    st.session_state.conversation_history, 
                    prompt, 
                    lop_selected
                )
                st.markdown(response_content)
                st.session_state.messages.append({"role": "assistant", "content": response_content})

def mode_reading(lop_selected):
    """Tính năng Đọc hiểu, hiển thị dữ liệu các khối lớp."""
    st.header("📖 Đọc hiểu - Chương trình Ngữ Văn THCS")
    st.markdown("Dưới đây là danh sách các tác phẩm và chủ đề chính theo Khối lớp.")
    
    current_lop = lop_selected
    
    # Xử lý khi chọn 'Tất cả khối lớp'
    if current_lop == "Tất cả khối lớp":
        st.info("Hiển thị tóm tắt Chủ đề và Tác phẩm của tất cả các khối lớp.")
        
        for lop, data in DATA_NGU_VAN.items():
            with st.expander(f"**📚 {lop}**", expanded=False):
                for chu_de, tac_pham_list in data.items():
                    st.subheader(f"➡️ {chu_de}")
                    for tac_pham in tac_pham_list:
                        st.markdown(f"- {tac_pham}")
    
    # Xử lý khi chọn lớp cụ thể
    elif current_lop in DATA_NGU_VAN:
        st.success(f"Chi tiết Chủ đề và Tác phẩm cho **{current_lop}**:")
        
        data = DATA_NGU_VAN[current_lop]
        for chu_de, tac_pham_list in data.items():
            st.markdown(f"### 🎯 {chu_de}")
            for tac_pham in tac_pham_list:
                st.markdown(f"- {tac_pham}")
    
    st.markdown("---")
    st.info("Trong tương lai, tính năng này sẽ cho phép bạn tải lên văn bản để AI tóm tắt hoặc phân tích.")


def mode_writing():
    """Tính năng Viết."""
    st.header("✍️ Viết (Viết văn/Sáng tạo nội dung)")
    st.warning("Tính năng đang được phát triển. AI sẽ giúp bạn kiểm tra ngữ pháp, gợi ý từ ngữ, hoặc phát triển ý tưởng cho bài viết văn.")
    user_text = st.text_area("Nhập đoạn văn bản của bạn ở đây:", height=300)
    if st.button("Kiểm tra và Gợi ý"):
        st.info(f"Đã nhận văn bản {len(user_text)} ký tự. (Chờ AI phân tích...)")

def mode_speaking_listening():
    """Tính năng Nói & Nghe."""
    st.header("🗣️ Nói & Nghe")
    st.warning("Tính năng đang được phát triển. Sẽ cho phép tương tác bằng giọng nói hoặc phân tích ngữ điệu.")
    st.write("Sử dụng micro để thực hành phát âm hoặc luyện thuyết trình theo chủ đề Ngữ Văn.")
    st.button("Bắt đầu Ghi âm/Luyện nói")
    
# --- STREAMLIT APP CỐT LÕI ---

st.set_page_config(page_title="Trợ Lý Ngữ Văn THCS", layout="wide")

api_key = initialize_gemini_api()

if not api_key:
    st.warning("Vui lòng đặt Key Gemini API của bạn vào file `.streamlit/secrets.toml` dưới tên **`GOOGLE_API_KEY`** để sử dụng ứng dụng.")
    st.stop()


# 1. Cài đặt Thanh Sidebar (Navigation)
with st.sidebar:
    st.title("📚 Trợ Lý Ngữ Văn THCS")
    st.subheader("Chọn Chế độ")
    
    mode = st.radio(
        "Các Chức năng Chính:",
        ("💬 Chatbot Ngữ Văn", "📖 Đọc hiểu", "✍️ Viết", "🗣️ Nói & Nghe"),
        index=0 
    )
    
    st.markdown("---")
    
    # --- BỘ LỌC KHỐI LỚP ---
    st.subheader("Phạm vi Kiến thức")
    lop_selected = st.selectbox(
        "Chọn Khối lớp:",
        OPTIONS_LOP,
        index=0 
    )
    st.session_state.lop_selected = lop_selected
    
    st.markdown("---")
    st.caption("Sử dụng Gemini API (Google).")
    st.caption(f"Trạng thái: ✅ Đã tải API Key.")


# 2. Hiển thị nội dung dựa trên chế độ đã chọn
with st.container():
    # Luôn khởi tạo lại lịch sử chat khi chuyển mode để tránh lỗi
    if st.session_state.get('current_mode') != mode:
         st.session_state.pop("conversation_history", None) 
         st.session_state.pop("messages", None) 
         st.session_state.current_mode = mode

    if mode == "💬 Chatbot Ngữ Văn":
        mode_rag_qa(api_key, lop_selected)
    elif mode == "📖 Đọc hiểu":
        mode_reading(lop_selected)
    elif mode == "✍️ Viết":
        mode_writing()
    elif mode == "🗣️ Nói & Nghe":
        mode_speaking_listening()