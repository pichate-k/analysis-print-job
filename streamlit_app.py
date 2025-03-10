import streamlit as st
import fitz 
import PyMuPDF
from PIL import Image
import os

st.title("🎈 ระบบวิเคราะห์เอกสารสำหรับการรับงานพิมพ์")

def analyze_image_type(image_path):
    """Analyzes an image and determines its type (grayscale, black & white, blank, or color)."""
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size
        pixels = img.getdata()

        # Check for blank image
        is_blank = all(pixel == (255, 255, 255) for pixel in pixels)
        if is_blank:
            return "blank"

        # Check for color by examining RGB differences per pixel
        for r, g, b in pixels:
            if not (abs(r - g) < 5 and abs(g - b) < 5 and abs(b - r) < 5):
                return "color"  # Found a pixel that's not grayscale

        # If no color pixel is found, check for black & white
        is_bw = all(pixel == (0,0,0) or pixel == (255,255,255) for pixel in pixels)

        if is_bw:
          return "black & white"
        else:
          return "grayscale"


    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error: {e}"

def count_page_types(pdf_path, output_folder="images"):
    """Counts the number of color, grayscale, and blank pages in a PDF."""
    color_count = 0
    grayscale_count = 0
    blank_count = 0
    try:
        os.makedirs(output_folder, exist_ok=True)
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc[page_num]
            pix = page.get_pixmap()
            image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img.save(image_path)

            image_type = analyze_image_type(image_path)
            print(f"Page {page_num+1}: {image_type}")

            if image_type == "color":
                color_count += 1
            elif image_type == "grayscale" or image_type == "black & white":
                grayscale_count += 1
            elif image_type == "blank":
                blank_count += 1

        print(f"Successfully converted {doc.page_count} pages to images in '{output_folder}'")
        print(f"Color pages: {color_count}")
        print(f"Grayscale/Black & White pages: {grayscale_count}")
        print(f"Blank pages: {blank_count}")

    except FileNotFoundError:
        print(f"Error: PDF file not found at '{pdf_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

# File uploader
uploaded_file = st.file_uploader("Upload your work as pdf")
pdf_file_path = "/content/Lean Canvas.pdf"  # Replace with the actual path to your PDF file
count_page_types(pdf_file_path)

