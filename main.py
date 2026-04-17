import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

st.title("🎨 QR Code Generator with Logo")

# Input for URL/Text
url_data = st.text_input("ระบุ URL หรือข้อความ:")
logo_file = st.file_uploader("อัปโหลดโลโก้ (PNG/JPG):", type=['jpg', 'jpeg', 'png'])

if st.button("สร้าง QR Code") and url_data:
    # สร้าง QR Code โดยใช้ ERROR_CORRECT_H เพื่อให้สามารถใส่รูปทับได้
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(url_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # ใส่โลโก้ตรงกลาง
    if logo_file:
        logo = Image.open(logo_file)
        # ปรับขนาดโลโก้ (ประมาณ 25% ของพื้นที่)
        base_width = qr_img.size[0] // 5
        h_size = int(logo.size[1] * (base_width / float(logo.size[0])))
        logo = logo.resize((base_width, h_size), Image.Resampling.LANCZOS)
        
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)
        qr_img.paste(logo, pos)

    # แสดงผลและปุ่มดาวน์โหลด
    st.image(qr_img, use_container_width=True)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.download_button("ดาวน์โหลด", buf.getvalue(), "qrcode.png", "image/png")
