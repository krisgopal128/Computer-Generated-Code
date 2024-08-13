# User Guide for OCR PDF to Audio Conversion Tool

## Requirements:

- Python 3.x
- Tkinter
- PyPDF2
- pytesseract
- PIL (Pillow)
- pdf2image
- pyttsx3
- easyocr

## How to Use:

1. **Launch the Application**: Run the Python script (`ocr_pdf_to_audio.py`).

2. **Select PDF File**: 
   - Click the "Select PDF File" button.
   - Choose the PDF file you want to process.

3. **Enable OCR (Optional)**: 
   - Check the "Enable OCR" checkbox if you want to extract text from images within the PDF.
   - Select the OCR tool you want to use (PyTesseract or EasyOCR).

4. **Select Language**:
   - Choose the language for OCR from the dropdown.

5. **Select Voice Gender**:
   - Choose the desired voice gender (male or female) for audio conversion.

6. **Specify Page Range (Optional)**:
   - Enter the page range you want to process (e.g., `1-3` or `2,4,6`). If left empty, the entire document will be processed.

7. **Process PDF**: 
   - Click the "Process PDF" button to extract text from the selected PDF.
   - The extracted text will be displayed in the text area.

8. **Convert to Audio**: 
   - After processing the PDF, click the "Convert to Audio" button to save the extracted text as an audio file (`output.mp3`).

9. **Play Audio**: 
   - Click the "Play" button to listen to the generated audio.

10. **Clear Text**: 
    - Click the "Clear" button to reset the application and start over.

## Features:

- **File Selection**: Allows you to select a PDF file for processing.
- **OCR Tool Selection**: Choose between PyTesseract and EasyOCR for OCR processing.
- **Language Selection**: Supports multiple languages for OCR.
- **Voice Gender**: Choose between male and female voices for audio conversion.
- **Page Range**: Process specific pages or the entire document.
- **Text Area**: Displays the extracted text for review.
- **Progress Bar**: Indicates the progress of PDF processing.
- **Audio Conversion**: Converts extracted text to an audio file.
- **Play Audio**: Listen to the generated audio within the application.
- **Clear Button**: Resets the application to its initial state.

## Notes:

- Ensure all dependencies are installed before running the application.
- PyTesseract and EasyOCR require additional setup. Refer to their respective documentation for installation instructions.
- The application saves the audio file as `output.mp3` in the working directory.


Code generated on GPT‑4o & gemma-1.5-pro-exp-0801 dated 13-Aug-2024

