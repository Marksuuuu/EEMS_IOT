import tkinter as tk
import signal
import sys

def on_closing():
    # This function is called when the user tries to close the window
    print("Window closed or close button clicked")
    root.destroy()

def check_window_response():
    # This function checks if the window is still responsive
    if root.winfo_exists():  # Check if the window still exists
        print("Window is responsive")
    else:
        print("Window is closed or not responding")
        root.quit()  # Exit the mainloop if the window is closed

def shutdown_handler(signum, frame):
    print("Shutdown detected")
    root.quit()

root = tk.Tk()
root.title("Window Monitoring")

# Bind the window closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Check window responsiveness every 1 second (you can adjust the interval as needed)
root.after(1000, check_window_response)

# Register a signal handler to catch shutdown events
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# Start the tkinter mainloop
try:
    root.mainloop()
except KeyboardInterrupt:
    print("KeyboardInterrupt: Exiting...")
    sys.exit(1)
