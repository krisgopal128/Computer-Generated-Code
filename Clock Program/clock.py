import time
import tkinter as tk
import math

class Clock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Digital & Analogue Clock")
        self.mode = 1  # 1: Both, 2: Analog, 3: Digital

        self.clock_label = tk.Label(self.root, font=('Helvetica', 48), bg='black', fg='green')
        self.clock_label.pack(fill='both', expand=1)

        self.analog_clock = tk.Canvas(self.root, width=400, height=400, bg='black')
        self.analog_clock.pack(fill='both', expand=1)
        self.analog_clock.create_oval(50, 50, 350, 350, width=5, outline='green')

        self.toggle_button = tk.Button(self.root, text="Toggle Clock", command=self.toggle_clock)
        self.toggle_button.pack(fill='x')

        self.update_time()
        self.update_analog_time()

    def update_time(self):
        if self.mode == 1 or self.mode == 3:
            current_time = time.strftime("%H:%M:%S")
            self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def update_analog_time(self):
        if self.mode == 1 or self.mode == 2:
            self.analog_clock.delete('all')
            self.analog_clock.create_oval(50, 50, 350, 350, width=5, outline='green')
            current_time = time.localtime()
            hours = current_time.tm_hour % 12
            minutes = current_time.tm_min
            seconds = current_time.tm_sec
            hour_angle = math.pi / 6 * hours + math.pi / 360 * minutes
            minute_angle = math.pi / 30 * minutes + math.pi / 1800 * seconds
            second_angle = math.pi / 30 * seconds
            self.analog_clock.create_line(200, 200, 200 + 80 * math.sin(hour_angle), 200 - 80 * math.cos(hour_angle), width=5, fill='green')
            self.analog_clock.create_line(200, 200, 200 + 120 * math.sin(minute_angle), 200 - 120 * math.cos(minute_angle), width=3, fill='green')
            self.analog_clock.create_line(200, 200, 200 + 150 * math.sin(second_angle), 200 - 150 * math.cos(second_angle), width=1, fill='red')
        self.root.after(1000, self.update_analog_time)

    def toggle_clock(self):
        self.mode = (self.mode % 3) + 1
        if self.mode == 1:  # Both
            self.clock_label.pack(fill='both', expand=1)
            self.analog_clock.pack(fill='both', expand=1)
            self.root.title("Digital & Analogue Clock")
        elif self.mode == 2:  # Analog
            self.clock_label.pack_forget()
            self.analog_clock.pack(fill='both', expand=1)
            self.root.title("Analog Clock")
        elif self.mode == 3:  # Digital
            self.clock_label.pack(fill='both', expand=1)
            self.analog_clock.pack_forget()
            self.root.title("Digital Clock")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    clock = Clock()
    clock.run()
