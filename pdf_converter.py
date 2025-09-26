import fitz  # PyMuPDF
import os

def pdf_to_pngs(pdf_path, output_dir, zoom=2):
    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))

        out_path = os.path.join(output_dir, f"page_{page_num+1}.png")
        pix.save(out_path)
        print(f"Saved {out_path}")

    doc.close()


# change these paths for your project
pdf_path = "data/the_last_dinosaur.pdf"
output_dir = "data/book"
pdf_to_pngs(pdf_path, output_dir, zoom=2)