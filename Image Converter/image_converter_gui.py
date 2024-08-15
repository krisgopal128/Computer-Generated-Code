import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pickle
from PIL import Image, ImageTk
import os

class ImageConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # File selection dialog
        self.file_label = tk.Label(root, text="Select input file:")
        self.file_label.pack()
        self.file_entry = tk.Entry(root, width=40)
        self.file_entry.pack()
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        # Preview area
        self.preview_area = tk.Label(root, text="Preview:")
        self.preview_area.pack()
        self.preview_image = tk.Label(root, text="")
        self.preview_image.pack()

        # Output format selection
        self.format_label = tk.Label(root, text="Output format:")
        self.format_label.pack()
        self.format_var = tk.StringVar()
        self.format_var.set("jpg")
        self.format_menu = ttk.OptionMenu(root, self.format_var, "jpg", "png", "gif", "bmp", "tiff", "webp", "jpeg", "ico", "psd")
        self.format_menu.pack()

        # Output file name entry
        self.output_label = tk.Label(root, text="Output file name:")
        self.output_label.pack()
        self.output_entry = tk.Entry(root, width=40)
        self.output_entry.pack()

        # Quality adjustment
        self.quality_label = tk.Label(root, text="Quality (1-100):")
        self.quality_label.pack()
        self.quality_var = tk.IntVar()
        self.quality_var.set(100)
        self.quality_scale = tk.Scale(root, from_=1, to=100, variable=self.quality_var, orient=tk.HORIZONTAL)
        self.quality_scale.pack()

        # Gray scale option
        self.gray_scale_var = tk.BooleanVar()
        self.gray_scale_var.set(False)
        self.gray_scale_checkbox = tk.Checkbutton(root, text="Gray scale", variable=self.gray_scale_var)
        self.gray_scale_checkbox.pack()

        # Progress bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        # Conversion button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_image)
        self.convert_button.pack()

        # Error message label
        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.pack()

        # Load last used settings
        try:
            with open("settings.pkl", "rb") as f:
                settings = pickle.load(f)
                self.format_var.set(settings["format"])
                self.output_entry.insert(0, settings["output_file"])
                self.quality_var.set(settings["quality"])
                if "gray_scale" in settings:
                    self.gray_scale_var.set(settings["gray_scale"])
        except FileNotFoundError:
            pass

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .gif .bmp .tiff .webp .ico .psd")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)
        self.preview_image.config(text="Preview:")
        self.preview_image.config(image="")
        img = Image.open(file_path)
        img.thumbnail((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        self.preview_image.config(image=img_tk)
        self.preview_image.image = img_tk

    def convert_image(self):
        input_file = self.file_entry.get()
        output_format = self.format_var.get()
        output_file = self.output_entry.get() + "." + output_format
        quality = self.quality_var.get()
        gray_scale = self.gray_scale_var.get()

        try:
            img = Image.open(input_file)
            if gray_scale:
                img = img.convert("L")
            img.save(output_file, output_format, quality=quality)
            self.progress_bar["value"] = 100
            self.progress_bar.update()
            messagebox.showinfo("Conversion complete", f"Image converted to {output_format} format.")
        except Exception as e:
            self.error_label.config(text=str(e))
            self.progress_bar["value"] = 0
            self.progress_bar.update()

        # Save last used settings
        with open("settings.pkl", "wb") as f:
            pickle.dump({"format": self.format_var.get(), "output_file": self.output_entry.get(), "quality": self.quality_var.get(), "gray_scale": self.gray_scale_var.get()}, f)

    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageConverterGUI(root)
    gui.mainloop()