import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import os
import tempfile

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

with st.sidebar:
    st.header("Pricing Configuration")
    color_price = st.number_input("Price per color page", min_value=0.0, value=5.0)
    bw_price = st.number_input("Price per grayscale/black & white page", min_value=0.0, value=2.0)
    
    cover_option = st.checkbox("Include Cover?")
    if cover_option:
        cover_paper_type = st.selectbox("Cover Paper Type", ["Glossy", "Matte", "Cardstock"])
        cover_paper_price = st.number_input("Cover Paper Price", min_value=0.0, value=10.0)
        cover_print_price = st.number_input("Cover Print Price", min_value=0.0, value=15.0)
    
    content_paper_type = st.selectbox("Content Paper Type", ["Standard", "Premium", "Recycled"])
    content_paper_price = st.number_input("Content Paper Price", min_value=0.0, value=1.0)

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
    
    # Price Calculation
    total_price = (color_count * color_price) + (grayscale_count * bw_price) + (len(results) * content_paper_price)
    if cover_option:
        total_price += cover_paper_price + cover_print_price
    
    st.subheader("Total Estimated Price")
    st.write(f"Total Printing Cost: {total_price:.2f}")
