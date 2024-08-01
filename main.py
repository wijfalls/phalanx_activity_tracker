import cv2
import pyautogui
import time
import os
from threading import Thread
from datetime import datetime

import gui


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def adjust_camera_settings(cap):
    # Adjust camera settings (values may need to be tuned for your specific camera)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.6)  # Brightness range is usually from 0 to 1
    cap.set(cv2.CAP_PROP_CONTRAST, 0.5)    # Contrast range is usually from 0 to 1
    cap.set(cv2.CAP_PROP_EXPOSURE, -4)     # Exposure values vary; -4 is usually brighter


def capture_picture(folder):
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Adjust camera settings
    adjust_camera_settings(cap)

    # Allow camera to warm up
    warm_up_time = 2  # seconds
    print(f"Camera warming up for {warm_up_time} seconds...")
    for i in range(warm_up_time):
        time.sleep(1)
        print(f"{warm_up_time - i} seconds remaining")

    # Read a frame from the webcam
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
    else:
        # Save the captured frame to disk with a timestamp
        timestamp = get_timestamp()
        filename = os.path.join(folder, f"picture_{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Captured {filename}")
    
    # Release the webcam
    cap.release()


def capture_screenshot(folder, app):
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    
    # Save the screenshot to disk with a timestamp
    timestamp = get_timestamp()
    filename = os.path.join(folder, f"screenshot_{timestamp}.png")
    screenshot.save(filename)
    print(f"Captured {filename}")
    
    # Get mouse position
    mouse_x, mouse_y = pyautogui.position()
    app.update_mouse_position(timestamp, mouse_x, mouse_y)


def start_capturing(app):
    picture_folder = "pictures"
    screenshot_folder = "screenshots"
    interval = 3
    count = 10
    
    # Create folders if they do not exist
    os.makedirs(picture_folder, exist_ok=True)
    os.makedirs(screenshot_folder, exist_ok=True)

    for i in range(1, count + 1):
        picture_thread = Thread(target=lambda: capture_picture(picture_folder))
        screenshot_thread = Thread(target=lambda: capture_screenshot(screenshot_folder, app))
        
        picture_thread.start()
        screenshot_thread.start()
        
        picture_thread.join()
        screenshot_thread.join()
        
        time.sleep(interval)
    
    print("Finished capturing pictures and screenshots.")


def main():
    # Start the GUI in the main thread
    gui_thread = Thread(target=gui.main)
    gui_thread.start()

    # Wait for the GUI to initialize and get the app instance
    time.sleep(2)
    app = gui.app_instance

    # Start capturing in a separate thread
    capture_thread = Thread(target=start_capturing, args=(app,))
    capture_thread.start()


if __name__ == "__main__":
    main()
