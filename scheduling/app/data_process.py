import os

import cv2
import pandas as pd
import pytesseract
from dotenv import load_dotenv
from pdf2image import convert_from_path
from tqdm import tqdm

# Load Tesseract path from environment
load_dotenv()  # <-- loads the .env file
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")

# Paths
pdf_path = "data/2025_february/HosInfo/Funktionsoversigt.pdf"
save_dir = "data/results/2025_february/"
output_dir = os.path.join(save_dir, "pdf_images")
os.makedirs(output_dir, exist_ok=True)

# Convert PDF to images
pages = convert_from_path(pdf_path, dpi=600)


def preprocess_image(image):
    """
    Apply preprocessing to enhance OCR accuracy.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return binary


def extract_table(image):
    """
    Detect table structure and extract cell content with OCR.
    """
    # Detect table grid
    edges = cv2.Canny(image, 50, 150)  # Edge detection
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter and sort contours by position
    cells = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 15 and h > 15:  # Filter small boxes
            cells.append((x, y, w, h))
    cells = sorted(cells, key=lambda b: (b[1], b[0]))  # Sort by row (y) and then column (x)

    # Extract text from each cell
    rows = []
    current_row_y = None
    row = []
    for x, y, w, h in cells:
        if current_row_y is None or abs(y - current_row_y) > 10:
            if row:
                rows.append(row)
            row = []
            current_row_y = y
        cell = image[y : y + h, x : x + w]
        text = pytesseract.image_to_string(cell, config="--psm 7", lang="dan").strip()
        row.append(text)
    if row:
        rows.append(row)

    return rows


# Perform OCR on each page
all_data = []
for indx, page in tqdm(enumerate(pages), desc="Processing PDF pages", total=len(pages)):
    # Save each page as an image
    image_path = os.path.join(output_dir, f"page_{indx + 1}.png")
    page.save(image_path, "PNG")

    # Load the image for OpenCV preprocessing
    image = cv2.imread(image_path)
    preprocessed_image = preprocess_image(image)

    # Extract table content
    table = extract_table(preprocessed_image)
    all_data.extend(table)

# Convert structured data to a DataFrame
df = pd.DataFrame(all_data)

# Save the extracted data to files
df.to_excel(os.path.join(save_dir, "output_data.xlsx"), index=False)
df.to_csv(os.path.join(save_dir, "output_data.csv"), index=False)

print(f"Data saved to {save_dir} as both CSV and Excel.")
