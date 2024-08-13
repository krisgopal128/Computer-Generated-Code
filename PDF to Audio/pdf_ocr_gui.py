import tkinter as tk
from tkinter import filedialog, Text, ttk, messagebox
import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import io  # Importing io module
from tkinter import scrolledtext
import pyttsx3
import os
import easyocr  # Importing easyocr

class PDFOCRGUI:
    def __init__(self, master):
        self.master = master
        master.title("OCR PDF to Audio")

        self.pdf_file_path = None
        self.extracted_text = ""
        self.ocr_enabled = tk.BooleanVar(value=False)
        self.selected_language = tk.StringVar(value="eng")  # Default language
        self.voice_gender = tk.StringVar(value="female")  # Default voice gender
        self.selected_ocr_tool = tk.StringVar(value="pytesseract")  # Default OCR tool

        self.create_widgets()

    def create_widgets(self):
        # PDF File Name Display
        self.file_label = tk.Label(self.master, text="No file selected")
        self.file_label.pack(pady=5)

        # File Selection
        self.select_button = tk.Button(self.master, text="Select PDF File", command=self.select_pdf_file)
        self.select_button.pack(pady=10)

        # OCR Checkbox
        self.ocr_checkbox = tk.Checkbutton(self.master, text="Enable OCR", variable=self.ocr_enabled, command=self.toggle_ocr_options)
        self.ocr_checkbox.pack()

        # OCR Tool Selection (Hidden until OCR is enabled)
        self.ocr_tool_label = tk.Label(self.master, text="Select OCR Tool:")
        self.ocr_tool_radio_pytesseract = tk.Radiobutton(self.master, text="PyTesseract", variable=self.selected_ocr_tool, value="pytesseract")
        self.ocr_tool_radio_easyocr = tk.Radiobutton(self.master, text="EasyOCR", variable=self.selected_ocr_tool, value="easyocr")

        # Language Selection
        self.language_label = tk.Label(self.master, text="Select Language:")
        self.language_label.pack()

        self.language_options = ["eng", "fra", "deu", "spa", "ita", "jpn", "chi_sim", "chi_tra", "rus"]  # Adjusted for PyTesseract
        self.language_dropdown = ttk.Combobox(self.master, textvariable=self.selected_language, values=self.language_options)
        self.language_dropdown.pack()

        # Voice Gender Selection
        self.voice_label = tk.Label(self.master, text="Select Voice Gender:")
        self.voice_label.pack()

        self.voice_options = ["male", "female"]
        self.voice_dropdown = ttk.Combobox(self.master, textvariable=self.voice_gender, values=self.voice_options)
        self.voice_dropdown.pack()

        # Page Range Selection
        self.page_range_label = tk.Label(self.master, text="Page Range (e.g., 1-5 or 3,6,9):")
        self.page_range_label.pack()
        self.page_range_entry = tk.Entry(self.master)
        self.page_range_entry.pack()

        # Button Frame for horizontal layout
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(pady=10)

        # Process Button
        self.process_button = tk.Button(self.button_frame, text="Process PDF", command=self.process_pdf, state="disabled")
        self.process_button.grid(row=0, column=0, padx=5)

        # Convert to Audio Button
        self.convert_audio_button = tk.Button(self.button_frame, text="Convert to Audio", command=self.convert_to_audio, state="disabled")
        self.convert_audio_button.grid(row=0, column=1, padx=5)

        # Play Audio Button
        self.play_audio_button = tk.Button(self.button_frame, text="Play", command=self.play_audio, state="disabled")
        self.play_audio_button.grid(row=0, column=2, padx=5)

        # Text Display with Scrollbar
        self.text_area = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.text_area.pack(pady=10, fill="both", expand=True)

        # Progress Bar
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=5)

        # Clear Button
        self.clear_button = tk.Button(self.master, text="Clear", command=self.clear_text)
        self.clear_button.pack()

    def toggle_ocr_options(self):
        if self.ocr_enabled.get():
            self.ocr_tool_label.pack()
            self.ocr_tool_radio_pytesseract.pack()
            self.ocr_tool_radio_easyocr.pack()
        else:
            self.ocr_tool_label.pack_forget()
            self.ocr_tool_radio_pytesseract.pack_forget()
            self.ocr_tool_radio_easyocr.pack_forget()

    def select_pdf_file(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_file_path:
            self.file_label.config(text=os.path.basename(self.pdf_file_path))
            self.process_button.config(state="normal")

    def process_pdf(self):
        if not self.pdf_file_path:
            return

        self.process_button.config(state="disabled")
        self.convert_audio_button.config(state="disabled")
        self.play_audio_button.config(state="disabled")
        self.progress["value"] = 0
        self.extracted_text = ""
        self.text_area.delete("1.0", tk.END)

        self.process_pdf_thread()

    def process_pdf_thread(self):
        try:
            pdf_reader = PyPDF2.PdfReader(open(self.pdf_file_path, 'rb'))
            num_pages = len(pdf_reader.pages)

            page_range = self.page_range_entry.get()
            if page_range:
                pages_to_process = self.parse_page_range(page_range, num_pages)
            else:
                pages_to_process = range(num_pages)

            total_pages = len(pages_to_process)

            for i, page_num in enumerate(pages_to_process):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                if self.ocr_enabled.get():
                    try:
                        images = convert_from_path(self.pdf_file_path, first_page=page_num + 1, last_page=page_num + 1)
                        for img in images:
                            if self.selected_ocr_tool.get() == "pytesseract":
                                ocr_text = pytesseract.image_to_string(img, lang=self.selected_language.get())
                            else:  # easyocr selected
                                reader = easyocr.Reader([self.selected_language.get()])
                                ocr_text = reader.readtext(img, detail=0)
                                ocr_text = " ".join(ocr_text)
                            text = ocr_text
                    except Exception as e:
                        print(f"Error during OCR: {e}")
                        messagebox.showerror("Error", f"Error processing PDF with OCR: {e}")

                self.extracted_text += text
                self.progress["value"] = (i + 1) / total_pages * 100
                self.master.update_idletasks()

            self.text_area.insert(tk.END, self.extracted_text)
            self.process_button.config(state="normal")
            self.convert_audio_button.config(state="normal")
            self.play_audio_button.config(state="normal")

        except Exception as e:
            messagebox.showerror("Error", f"Error processing PDF: {e}")
            self.process_button.config(state="normal")

    def parse_page_range(self, page_range, num_pages):
        pages = set()
        for part in page_range.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.update(range(start - 1, end))
            else:
                pages.add(int(part) - 1)
        return sorted(pages)

    def convert_to_audio(self):
        if self.extracted_text:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            selected_voice = voices[0].id if self.voice_gender.get() == "male" else voices[1].id
            engine.setProperty('voice', selected_voice)
            engine.save_to_file(self.extracted_text, 'output.mp3')
            engine.runAndWait()
            messagebox.showinfo("Success", "Text has been converted to audio and saved as 'output.mp3'.")

    def play_audio(self):
        if os.path.exists("output.mp3"):
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            selected_voice = voices[0].id if self.voice_gender.get() == "male" else voices[1].id
            engine.setProperty('voice', selected_voice)
            engine.say(self.extracted_text)
            engine.runAndWait()

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.convert_audio_button.config(state="disabled")
        self.play_audio_button.config(state="disabled")
        self.progress["value"] = 0
        self.file_label.config(text="No file selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFOCRGUI(root)
    root.mainloop()
