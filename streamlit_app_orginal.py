import streamlit as st
import fitz 
from PIL import Image
import os
import tempfile

st.title("🎈 ระบบวิเคราะห์เอกสารสำหรับการรับงานพิมพ์")



def analyze_image_type(image):
    """Analyzes an image and determines its type (grayscale, black & white, blank, or color)."""
    img = image.convert("RGB")
    pixels = img.getdata()

    is_blank = all(pixel == (255, 255, 255) for pixel in pixels)
    if is_blank:
        return "Blank"

    for r, g, b in pixels:
        if not (abs(r - g) < 5 and abs(g - b) < 5 and abs(b - r) < 5):
            return "Color"

    is_bw = all(pixel == (0, 0, 0) or pixel == (255, 255, 255) for pixel in pixels)
    return "Black & White" if is_bw else "Grayscale"

def count_page_types(pdf_path):
    """Counts the number of color, grayscale, and blank pages in a PDF."""
    color_count, grayscale_count, blank_count = 0, 0, 0
    doc = fitz.open(pdf_path)
    results = []
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_type = analyze_image_type(img)
        results.append((page_num + 1, image_type))
        
        if image_type == "Color":
            color_count += 1
        elif image_type == "Grayscale" or image_type == "Black & White":
            grayscale_count += 1
        elif image_type == "Blank":
            blank_count += 1
    
    return results, color_count, grayscale_count, blank_count

# Streamlit UI
st.title("PDF Page Color Analyzer")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.getvalue())
        pdf_path = temp_pdf.name
    
    results, color_count, grayscale_count, blank_count = count_page_types(pdf_path)
    
    st.subheader("Analysis Results")
    st.write(f"Total Pages: {len(results)}")
    st.write(f"Color Pages: {color_count}")
    st.write(f"Grayscale/Black & White Pages: {grayscale_count}")
    st.write(f"Blank Pages: {blank_count}")
    
    st.subheader("Page-wise Analysis")
    for page_num, image_type in results:
        st.write(f"Page {page_num}: {image_type}")
