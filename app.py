import streamlit as st
import pandas as pd
st.image("logo.jpg")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }

    .title {
        text-align: center;
        color: #8B0000;
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
    }

    .result-title {
        font-size: 15px;
        color: #666;
    }

    .result-value {
        font-size: 25px;
        font-weight: bold;
        color: #8B0000;
    }

    div.stButton > button {
        width: 100%;
        background-color: #8B0000;
        color: white;
        font-size: 17px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px;
    }

    div.stButton > button:hover {
        background-color: #a52a2a;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ"


# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<div class="title">💰 APP TÍNH LÃI GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Tính toán tiền lãi theo lãi đơn hoặc lãi kép</div>',
    unsafe_allow_html=True
)


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=10_000_000.0,
        step=500_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=120,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

with col2:
    hinh_thuc_nhan_lai = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

    loai_lai = st.radio(
        "📊 Phương pháp tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ],
        horizontal=True
    )

    st.info(
        "💡 Lãi suất được hiểu là lãi suất theo năm."
    )


# =========================
# NÚT TÍNH TOÁN
# =========================
st.markdown("---")

if st.button("🧮 TÍNH TIỀN LÃI"):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r_nam = lai_suat / 100

    # Số tháng
    so_thang = int(ky_han)

    # =========================
    # XÁC ĐỊNH SỐ KỲ NHẬN LÃI
    # =========================
    if hinh_thuc_nhan_lai == "Hàng tháng":
        so_ky = so_thang
        thang_moi_ky = 1

    elif hinh_thuc_nhan_lai == "Hàng quý":
        so_ky = so_thang // 3

        # Nếu kỳ hạn không chia hết cho 3
        if so_thang % 3 != 0:
            so_ky += 1

        thang_moi_ky = 3

    else:
        # Cuối kỳ chỉ có 1 lần nhận lãi
        so_ky = 1
        thang_moi_ky = so_thang

    # =========================
    # TÍNH LÃI
    # =========================
    bang_du_lieu = []

    tong_lai = 0
    gia_tri_hien_tai = tien_gui

    # -------------------------
    # LÃI ĐƠN
    # -------------------------
    if loai_lai == "Lãi đơn":

        lai_moi_thang = tien_gui * r_nam / 12

        for ky in range(1, so_ky + 1):

            if hinh_thuc_nhan_lai == "Cuối kỳ":
                so_thang_ky = so_thang
            else:
                so_thang_ky = min(
                    thang_moi_ky,
                    so_thang - (ky - 1) * thang_moi_ky
                )

            tien_lai_ky = tien_gui * r_nam * so_thang_ky / 12

            tong_lai += tien_lai_ky

            if hinh_thuc_nhan_lai == "Cuối kỳ":
                thoi_diem = f"Tháng {so_thang}"
            else:
                thoi_diem = f"Kỳ {ky}"

            bang_du_lieu.append({
                "Kỳ": thoi_diem,
                "Tiền gốc": format_money(tien_gui),
                "Tiền lãi kỳ này": format_money(tien_lai_ky),
                "Tổng lãi tích lũy": format_money(tong_lai),
                "Tổng tiền": format_money(tien_gui + tong_lai)
            })

    # -------------------------
    # LÃI KÉP
    # -------------------------
    else:

        # Lãi kép được tính theo số lần nhập lãi
        if hinh_thuc_nhan_lai == "Hàng tháng":
            lai_suat_ky = r_nam / 12

        elif hinh_thuc_nhan_lai == "Hàng quý":
            lai_suat_ky = r_nam / 4

        else:
            # Cuối kỳ
            lai_suat_ky = r_nam

        for ky in range(1, so_ky + 1):

            tien_truoc_ky = gia_tri_hien_tai

            # Với cuối kỳ, chỉ tính một lần
            gia_tri_hien_tai = gia_tri_hien_tai * (
                1 + lai_suat_ky
            )

            tien_lai_ky = gia_tri_hien_tai - tien_truoc_ky

            tong_lai += tien_lai_ky

            if hinh_thuc_nhan_lai == "Cuối kỳ":
                thoi_diem = f"Tháng {so_thang}"
            else:
                thoi_diem = f"Kỳ {ky}"

            bang_du_lieu.append({
                "Kỳ": thoi_diem,
                "Tiền gốc": format_money(tien_truoc_ky),
                "Tiền lãi kỳ này": format_money(tien_lai_ky),
                "Tổng lãi tích lũy": format_money(tong_lai),
                "Tổng tiền": format_money(gia_tri_hien_tai)
            })

    # =========================
    # KẾT QUẢ
    # =========================
    tong_tien = tien_gui + tong_lai

    st.markdown("---")
    st.subheader("📊 Kết quả tính toán")

    col1, col2, col3 = st.columns(3)

    # Tiền lãi định kỳ
    if len(bang_du_lieu) > 0:
        lai_dinh_ky = (
            bang_du_lieu[0]["Tiền lãi kỳ này"]
        )
    else:
        lai_dinh_ky = "0 VNĐ"

    with col1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💵 Tiền lãi định kỳ</div>
                <div class="result-value">{lai_dinh_ky}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">📈 Tổng tiền lãi</div>
                <div class="result-value">{format_money(tong_lai)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">💰 Tổng tiền nhận được</div>
                <div class="result-value">{format_money(tong_tien)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # THÔNG TIN TÓM TẮT
    # =========================
    st.markdown("---")

    st.subheader("📝 Tóm tắt khoản tiền gửi")

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    with summary_col1:
        st.metric(
            "Số tiền gửi",
            format_money(tien_gui)
        )

    with summary_col2:
        st.metric(
            "Kỳ hạn",
            f"{so_thang} tháng"
        )

    with summary_col3:
        st.metric(
            "Lãi suất",
            f"{lai_suat:.2f}%/năm"
        )

    with summary_col4:
        st.metric(
            "Loại lãi",
            loai_lai
        )

    # =========================
    # BẢNG CHI TIẾT
    # =========================
    st.markdown("---")
    st.subheader("📋 Chi tiết tiền lãi")

    df = pd.DataFrame(bang_du_lieu)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # CÔNG THỨC
    # =========================
    with st.expander("📚 Xem công thức tính"):

        if loai_lai == "Lãi đơn":
            st.markdown("""
            **Công thức lãi đơn:**

            **Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12**

            **Tổng tiền = Tiền gốc + Tiền lãi**

            Với lãi đơn, tiền lãi được tính dựa trên **số tiền gốc ban đầu**.
            """)

        else:
            st.markdown("""
            **Công thức lãi kép:**

            **Tổng tiền = Tiền gốc × (1 + lãi suất kỳ)ⁿ**

            **Tiền lãi = Tổng tiền − Tiền gốc**

            Với lãi kép, tiền lãi của mỗi kỳ được **nhập vào vốn** để tiếp tục
            sinh lãi ở các kỳ sau.
            """)

    st.success(
        f"✅ Hoàn tất! Sau {so_thang} tháng, "
        f"bạn nhận được khoảng **{format_money(tong_tien)}**."
    )
