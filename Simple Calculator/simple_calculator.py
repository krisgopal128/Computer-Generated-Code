import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("300x400")
        self.expression = ""

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 15), background='#008080', foreground='#FFFFFF', borderwidth=1)
        self.style.map('TButton', background=[('active', '#006666')])
        
        # Entry widget
        self.display = ttk.Entry(root, font=('Arial', 18), justify='right', foreground='#008080', background='#FFFFFF')
        self.display.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

        # Button layout
        button_texts = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        for i, text in enumerate(button_texts):
            button = ttk.Button(root, text=text, command=lambda t=text: self.on_button_click(t))
            button.grid(row=(i // 4) + 1, column=i % 4, sticky='nsew', padx=5, pady=5)

        # Configure grid weights
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
            root.grid_columnconfigure(i % 4, weight=1)

        # Bind keys
        root.bind('<Key>', self.on_key_press)
        
    def on_button_click(self, char):
        if char == 'C':
            self.clear()
        elif char == '=':
            self.calculate()
        else:
            self.update_expression(char)

    def on_key_press(self, event):
        char = event.char
        if char in '0123456789+-*/':
            self.update_expression(char)
        elif char in '\r=':
            self.calculate()
        elif char in '\b\x7f\x1b':
            self.clear()
    
    def update_expression(self, char):
        if len(self.expression) < 18:
            self.expression += char
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
    
    def clear(self):
        self.expression = ""
        self.display.delete(0, tk.END)
    
    def calculate(self):
        try:
            result = eval(self.expression)
            self.expression = str(result)
        except Exception as e:
            self.expression = "Error"
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()