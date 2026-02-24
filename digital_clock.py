import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Main window
root = tk.Tk()
root.title("Modern Digital Clock")
root.geometry("500x300")
root.resizable(False, False)

# Theme variables
dark_mode = True

# Function to update time
def update_time():
    now = datetime.now()
    
    if time_format.get() == "24":
        current_time = now.strftime("%H:%M:%S")
    else:
        current_time = now.strftime("%I:%M:%S %p")
    
    current_date = now.strftime("%A, %d %B %Y")
    
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    
    root.after(1000, update_time)

# Toggle theme
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    
    if dark_mode:
        root.config(bg="#1e1e1e")
        time_label.config(bg="#1e1e1e", fg="#00ffcc")
        date_label.config(bg="#1e1e1e", fg="white")
    else:
        root.config(bg="white")
        time_label.config(bg="white", fg="black")
        date_label.config(bg="white", fg="gray")

# Background setup
root.config(bg="#1e1e1e")

# Time format selection
time_format = tk.StringVar(value="24")

format_frame = tk.Frame(root, bg="#1e1e1e")
format_frame.pack(pady=10)

tk.Radiobutton(format_frame, text="24 Hour", variable=time_format,
               value="24", bg="#1e1e1e", fg="white",
               selectcolor="#333").pack(side="left", padx=10)

tk.Radiobutton(format_frame, text="12 Hour", variable=time_format,
               value="12", bg="#1e1e1e", fg="white",
               selectcolor="#333").pack(side="left", padx=10)

# Time Label
time_label = tk.Label(root, font=("Helvetica", 48, "bold"),
                      bg="#1e1e1e", fg="#00ffcc")
time_label.pack(pady=10)

# Date Label
date_label = tk.Label(root, font=("Helvetica", 16),
                      bg="#1e1e1e", fg="white")
date_label.pack(pady=5)

# Theme Button
theme_button = tk.Button(root, text="Toggle Theme",
                         command=toggle_theme,
                         font=("Helvetica", 12),
                         bg="#444", fg="white")
theme_button.pack(pady=20)

# Start clock
update_time()

root.mainloop()