import tkinter as tk
from tkinter import Label
import time
import threading
from datetime import datetime
import pyautogui

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

        # Mouse position display
        self.mouse_label = Label(self.root, text="Mouse Position: (0, 0)", font=("Helvetica", 14))
        self.mouse_label.pack(pady=10)

        # Initialize variables
        self.start_time = None
        self.running = False
        self.elapsed_time = 0
        self.last_two_mouse_positions = []

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
        self.last_two_mouse_positions.clear()
        self.mouse_label.config(text="Mouse Position: (0, 0)")

    def update_mouse_position(self, timestamp, x, y):
        self.last_two_mouse_positions.append((timestamp, x, y))
        if len(self.last_two_mouse_positions) > 2:
            self.last_two_mouse_positions.pop(0)
        self.update_mouse_label()

    def update_mouse_label(self):
        if len(self.last_two_mouse_positions) > 0:
            last_positions = "\n".join([f"Time: {pos[0]}, Position: ({pos[1]}, {pos[2]})" for pos in self.last_two_mouse_positions])
            self.mouse_label.config(text=f"Last Two Mouse Positions:\n{last_positions}")

app_instance = None

def set_app_instance(instance):
    global app_instance
    app_instance = instance

def main():
    root = tk.Tk()
    app = FocusTrackerGUI(root)
    set_app_instance(app)
    root.mainloop()

if __name__ == "__main__":
    main()
