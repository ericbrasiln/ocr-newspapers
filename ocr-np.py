import pytesseract
from pdf2image import convert_from_path
import os
import sys
import re

def ocr_pdf(pdf_path):
    ''' Function to perform OCR on a Portuguese PDF
    Args:
    pdf_path (str): The path to the PDF

    Returns:
    str: The extracted text from the PDF
    '''
    # Converting the PDF into images with reduced resolution to save memory
    images = convert_from_path(pdf_path, dpi=150)
    # Initializing the variable that will store the extracted text
    text = ''
    # Iterating over the images
    for i, image in enumerate(images):
        # Performing OCR
        text += pytesseract.image_to_string(image, lang='por')
        # Include string with page number between pages
        text += f'\nPage {i+1}/{len(images)}\n\n'
        # Include extraction progress
        print(f'Extracting text from page {i+1}/{len(images)}')
        # Deleting the image from memory after processing to save RAM
        del image
    # Returning the extracted text
    return text

def save_text(text, txt_path):
    ''' Function to save the extracted text into a txt file
    Args:
    text (str): The extracted text
    txt_path (str): The path to the file
    '''
    # Opening the txt file
    with open(txt_path, 'w') as file:
        # Writing the extracted text
        file.write(text)

def clean_filename(filename):
    ''' Function to sanitize the file name by removing special characters
    Args:
    filename (str): The file name

    Returns:
    str: The sanitized file name
    '''
    # Removing special characters
    filename = re.sub(r'[^A-Za-z0-9_\-]', '_', filename)
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Remove dots before the extension and replace with underscore
    filename = re.sub(r'\.(?=[^.]*$)', '_', filename)
    return filename

def process_pdfs_in_directory(input_dir, output_dir):
    ''' Function to process all PDFs in an input directory and save the txt files in an output directory
    Args:
    input_dir (str): The path to the input directory containing the PDFs
    output_dir (str): The path to the output directory where the txt files will be saved
    '''
    # Check if the output directory exists, otherwise create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            cleaned_filename = clean_filename(os.path.splitext(filename)[0]) + ".txt"
            txt_path = os.path.join(output_dir, cleaned_filename)

            # Check if the text file already exists
            if os.path.exists(txt_path):
                print(f'Checking if {cleaned_filename} already exists...')
                print(f'{cleaned_filename} already exists. Skipping to the next file.')
                continue

            print(f'Processing {filename}...')
            text = ocr_pdf(pdf_path)
            save_text(text, txt_path)
            print(f'{filename} processed and saved as {txt_path}')

if __name__ == '__main__':
    # Checking if the number of arguments is valid
    if len(sys.argv) != 3:
        print('Usage: python ocr_tess.py <input_dir> <output_dir>')
        sys.exit(1)
    # Getting the input and output directory paths
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    # Processing the PDFs in the input directory
    process_pdfs_in_directory(input_dir, output_dir)
