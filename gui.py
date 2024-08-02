import tkinter as tk
from tkinter import Label
import time
import threading
from datetime import datetime

class FocusTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Tracker")
        self.root.geometry("400x300")

        # Timer display
        self.timer_label = Label(self.root, text="Timer: 00:00", font=("Helvetica", 24))
        self.timer_label.pack(pady=20)

        # Suggestions display
        self.suggestions_label = Label(self.root, text="Suggestions:", font=("Helvetica", 18))
        self.suggestions_label.pack(pady=20)

        self.suggestions_text = Label(self.root, text="Placeholder for suggestions based on focus and activity", font=("Helvetica", 14))
        self.suggestions_text.pack(pady=10)

        # Initialize variables
        self.start_time = None
        self.running = False
        self.elapsed_time = 0

        # Start/Stop button
        self.start_stop_button = tk.Button(self.root, text="Start", font=("Helvetica", 14), command=self.start_stop)
        self.start_stop_button.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset", font=("Helvetica", 14), command=self.reset)
        self.reset_button.pack(pady=10)

    def update_timer(self):
        while self.running:
            self.elapsed_time = int(time.time() - self.start_time)
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"Timer: {minutes:02d}:{seconds:02d}")
            time.sleep(1)

    def start_stop(self):
        if self.running:
            # Stop the timer
            self.running = False
            self.start_stop_button.config(text="Start")
        else:
            # Start the timer
            if self.elapsed_time == 0:
                self.start_time = time.time()
            else:
                self.start_time = time.time() - self.elapsed_time
            self.running = True
            self.start_stop_button.config(text="Stop")
            threading.Thread(target=self.update_timer).start()

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.timer_label.config(text="Timer: 00:00")
        self.start_stop_button.config(text="Start")

def main():
    root = tk.Tk()
    app = FocusTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
