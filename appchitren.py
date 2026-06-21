import streamlit as st
from pathlib import Path
import base64

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="CHI TRÊN",
    page_icon="😡",
    layout="wide"
)

st.title("😡 CHI TRÊN")
st.caption("Nhập đáp án theo từng số. Sau khi nhấn Enter, đáp án đúng sẽ hiện ngay bên dưới và tự động nhảy sang câu tiếp theo.")

# Khởi tạo trạng thái lưu vị trí ô cần nhảy tiếp theo
if "next_focus_idx" not in st.session_state:
    st.session_state.next_focus_idx = None

def giaiphau_next_focus(current_idx):
    st.session_state.next_focus_idx = current_idx + 1

# =========================
# DỮ LIỆU TRẠM
# =========================
STATIONS = [
    {
"name": "Trạm 1",
"image": "1.png",
"answers": {
"1": "xg đòn",
"2": "xg vai",
"3": "xg trụ",
"4": "xg cổ tay",
"5": "xg bàn tay",
"6": "xg đốt ngón tay",
"7": "xg quay",
"8": "xg cánh tay"
        }
    },
    {
       "name": "Trạm 2",
"image": "2.png",
"answers": {
"1": "đầu ức",
"2": "củ nón",
"3": "rãnh dưới đg thang",
"4": "đầu cùng vai"
        }    
    },
    {
        "name": "Trạm 3",
"image": "3.png",
"answers": {
"1": "khuyết trên vai",
"2": "mỏm quạ",
"3": "diện khớp đòn",
"4": "mỏm cùng vai",
"6": "hố dưới gai",
"7": "gai vai",
"8": "hố trên gai",
"9": "ổ chảo"
        }
    },
    {
"name": "Trạm 4",
"image": "4.png",
"answers": {
"1": "chỗ bám cơ trên gai",
"2": "chỏm xg cánh tay",
"3": "cổ giải phẫu",
"4": "cổ phẫu thuật",
"6": "lồi củ delta",
"7": "củ lớn",
"13": "rãnh gian củ",
"14": "củ bé"
        }
    },
    {
"name": "Trạm 8",
"image": "8.png",
"answers": {
"1": "đầu gần xg cánh tay",
"2": "ròng rọc",
"3": "rãnh cho tk quay"
        }
    },
    {
"name": "Trạm 9",
"image": "9.png",
"answers": {
"1": "hố vẹt",
"2": "mỏm trên lồi cầu trong",
"3": "ròng rọc",
"4": "chỏm con",
"5": "mỏm trên lồi cầu ngoài",
"6": "hố quay",
"7": "hố khuỷu",
"8": "rãnh tk trụ"
        }
    },
    {
        "name": "Trạm 10",
"image": "10.png",
"answers": {
"1": "lồi củ xg quay",
"2": "đg xiên",
"3": "cổ xg quay",
"4": "chỏm xg quay",
"5": "lồi củ xg trụ",
"7": "mỏm khuỷu",
"8": "khuyết ròng rọc",
"9": "mỏm vẹt",
"10": "khuyết quay xg trụ"
        }
    },
    {
       "name": "Trạm 11",
"image": "11.png",
"answers": {
"1": "chỏm xg quay",
"2": "cổ xg quay",
"3": "lồi củ xg quay",
"4": "đường xiên",
"5": "khuyết trụ xg quay",
"6": "củ sau",
"7": "vùng khớp xg nguyệt",
"8": "vùng khớp xg thuyền",
"9": "mỏm trâm quay"
        }
    },
    {
"name": "Trạm 12",
"image": "12.png",
"answers": {
"1": "mỏm khuỷu",
"2": "lồi củ xg trụ",
"3": "mỏm trâm trụ",
"5": "mỏm vẹt",
"6": "khuyết ròng rọc"
        }
    },
    {
"name": "Trạm 14",
"image": "14.png",
"answers": {
"1": "phần đòn cơ ngực lớn",
"2": "phần ức cơ ngực lớn",
"3": "cơ ngực lớn",
"4": "cơ delta",
"5": "tm đầu",
"6": "rãnh delta ngực"
        }
    },
    {
"name": "Trạm 15",
"image": "15.png",
"answers": {
"1": "cơ dưới đòn",
"2": "cơ ngực lớn",
"3": "chỗ bám của cân vào sàn nách",
"4": "tk ngực trong",
"5": "cơ ngực lớn (cắt)",
"6": "cân xương đòn ngực",
"7": "cơ ngực bé",
"8": "tk ngực ngoài",
"9": "nhánh ngực của đm ngực-mỏm cùng vai",
"10": "tm đầu"
        }
    },
    {
 "name": "Trạm 16",
"image": "16.png",
"answers": {
"1": "nguyên ủy cơ delta",
"2": "cơ tròn bé",
"3": "cổ phẫu thuật xg cánh tay",
"4": "mép trong rãnh gian củ",
"5": "lỗ tứ giác",
"6": "tam giác cánh tay tam đầu",
"7": "đầu ngoài cơ tam đầu cánh tay",
"8": "mỏm khuỷu",
"9": "đầu dài cơ tam đầu cánh tay",
"10": "cơ tròn lớn",
"11": "tam giác bả vai tam đầu",
"12": "cơ dưới gai",
"13": "cắt mép cơ thang",
"14": "cơ trên gai",
"15": "rãnh trên xg vai (lỗ)"
        }
    },
    {
"name": "Trạm 17",
"image": "17.png",
"answers": {
"1": "cơ trên gai",
"2": "cơ dưới gai",
"3": "cơ tròn bé",
"4": "cơ tròn lớn"
        }
    },
    {
"name": "Trạm 18",
"image": "18.png",
"answers": {
"1": "nhánh tk cơ delta",
"2": "nhánh bì cánh tay trên ngoài",
"3": "tk nách",
"4": "đm mũ cánh tay sau",
"5": "đm cánh tay sâu",
"6": "tk quay",
"7": "đầu ngoài cơ tam đầu cánh tay",
"8": "đm mũ vai",
"9": "đm trên vai",
"10": "tk trên vai",
"11": "dây chằng trên xg vai"
        }
    },
    {
 "name": "Trạm 19",
"image": "19.png",
"answers": {
"1": "tm dưới đòn",
"2": "tm nách",
"3": "tm đầu",
"4": "đôi tm cánh tay"
        }
    },
    {
"name": "Trạm 20",
"image": "20.png",
"answers": {
"1": "đm dưới đòn",
"2": "đm ngực trên",
"3": "đm ngực ngoài",
"4": "đm cánh tay",
"5": "đm mũ vai",
"6": "đm mũ cánh tay sau",
"7": "đm mũ cánh tay trước",
"8": "đm ngực cùng vai",
"9": "đm nách"
        }
    },
    {
"name": "Trạm 21",
"image": "21.png",
"answers": {
"1": "bó trong",
"2": "bó ngoài",
"3": "tk ngực ngoài",
"4": "đm nách",
"5": "tk cơ bì",
"6": "tk ngực trong",
"7": "tk bì cánh tay trong",
"8": "tk giữa",
"9": "cơ ngực bé",
"10": "tk bì cẳng tay trong",
"11": "tk trụ",
"12": "tk bì cẳng tay ngoài"
        }
    },
    {
"name": "Trạm 22",
"image": "22.png",
"answers": {
"1": "tk cơ bì",
"2": "tk ngực ngoài",
"3": "tk trên vai",
"4": "tk lưng vai",
"5": "tk giữa",
"6": "bó ngoài",
"7": "phần trước của thân trên",
"8": "thân trên",
"9": "nhánh nối vào tk hoành",
"10": "tk nách",
"11": "tk cơ dưới đòn",
"12": "tk quay",
"13": "tk dưới vai trên",
"14": "tk ngực lưng",
"15": "tk dưới vai dưới",
"16": "tk trụ",
"17": "tk giữa",
"18": "phần trước của thân dưới",
"19": "thân dưới",
"20": "tk ngực trong",
"21": "tk bì cánh tay trong",
"22": "tk bì cẳng tay trong",
"23": "tk ngực dài"
        }
    },



]

IMAGE_DIR = Path(".")

if "station_index" not in st.session_state:
    st.session_state.station_index = 0

# =========================
# THANH SIDEBAR (ĐÃ THÊM CHỌN TRẠM NHANH)
# =========================
st.sidebar.header("⚙️ Cài đặt")

# Tạo danh sách tên các trạm để sinh viên bấm chọn nhanh
station_names = [s["name"] for s in STATIONS]

# Đồng bộ Selectbox với session_state hiện tại của trạm
selected_station_name = st.sidebar.selectbox(
    "Chọn trạm làm bài nhanh:",
    options=station_names,
    index=st.session_state.station_index
)

# Cập nhật lại chỉ số trạm dựa trên lựa chọn từ Selectbox của sinh viên
station_index = station_names.index(selected_station_name)
if station_index != st.session_state.station_index:
    st.session_state.station_index = station_index
    st.rerun()

station = STATIONS[station_index]

show_all_answers = st.sidebar.checkbox("Hiện toàn bộ đáp án cho giảng viên", value=False)

if st.sidebar.button("🔄 Làm lại trạm này"):
    for key in list(st.session_state.keys()):
        if key.startswith(f"answer_{station_index}_"):
            del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("⬅️ Quay lại trạm trước") and station_index > 0:
    st.session_state.station_index -= 1
    st.rerun()

if st.sidebar.button("➡️ Chuyển sang trạm tiếp theo") and station_index < len(STATIONS) - 1:
    st.session_state.station_index += 1
    st.rerun()

st.markdown("---")
st.subheader(station["name"])

# =========================
# CHIA CỘT CHÍNH (Cột 1: Ảnh cố định, Cột 2: Ô nhập)
# =========================
st.markdown("""
<style>
[data-testid="stColumn"]:nth-of-type(1) {
    position: -webkit-sticky;
    position: sticky;
    top: 50px;
    align-self: start;
    max-height: 85vh;
    overflow: hidden;
}
.sticky-img {
    width: 100%;
    max-height: 80vh;
    object-fit: contain;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.answer-divider {
    margin-top: 15px;
    margin-bottom: 15px;
    border-bottom: 1px solid #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([5, 5], gap="large")

with col1:
    image_path = IMAGE_DIR / station["image"]
    if image_path.exists():
        with open(image_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        ext = image_path.suffix.replace(".", "")
        st.markdown(f'<img class="sticky-img" src="data:image/{ext};base64,{img_data}">', unsafe_allow_html=True)
    else:
        st.error(f"Không tìm thấy ảnh: {image_path}")

with col2:
    st.markdown("### ✍️ Nhập đáp án")
    
    if show_all_answers:
        with st.expander("👁️ Xem nhanh toàn bộ đáp án"):
            for num, ans in station["answers"].items():
                st.write(f"**Số {num}:** {ans}")

    # Lấy danh sách các số câu hỏi của trạm hiện tại
    numbers = list(station["answers"].keys())

    # Vòng lặp sinh các ô điền câu hỏi gốc của Streamlit
    for i, number in enumerate(numbers):
        correct_answer = station["answers"][number]

        st.markdown(f"**Số {number}:**")

        user_answer = st.text_input(
            "",
            key=f"answer_{station_index}_{number}",
            placeholder="Nhập đáp án rồi nhấn Enter...",
            label_visibility="collapsed",
            on_change=giaiphau_next_focus,
            args=(i,)
        )

        if user_answer.strip():
            if user_answer.strip().lower() == correct_answer.strip().lower():
                st.success("✅ Đúng chính xác!")
            else:
                st.error(f"❌ Đáp án đúng: **{correct_answer}**")

        st.markdown('<div class="answer-divider"></div>', unsafe_allow_html=True)

    # ĐOẠN ĐIỀU KHIỂN NHẢY CON TRỎ
    if st.session_state.next_focus_idx is not None:
        st.components.v1.html(f"""
            <script>
            setTimeout(function() {{
                const inputs = window.parent.document.querySelectorAll('input[type="text"]');
                const nextInput = inputs[{st.session_state.next_focus_idx}];
                if (nextInput) {{
                    nextInput.focus();
                    nextInput.scrollIntoView({{behavior: "smooth", block: "center"}});
                }}
            }}, 300);
            </script>
        """, height=0, width=0)
        st.session_state.next_focus_idx = None

    # Nút chuyển tiếp nhanh ở cuối phần điền đáp án
    st.markdown (".")
    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        if st.button("⬅️ Trạm trước", key="btn_prev", use_container_width=True) and station_index > 0:
            st.session_state.station_index -= 1
            st.rerun()

    with nav_col2:
        if st.button("Trạm tiếp theo ➡️", key="btn_next", use_container_width=True) and station_index < len(STATIONS) - 1:
            st.session_state.station_index += 1
            st.rerun()
