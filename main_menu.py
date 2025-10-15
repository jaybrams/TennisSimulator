import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# --- Configuration ---
INITIAL_WIDTH = 1280
INITIAL_HEIGHT = 720
IMAGE_PATH = os.path.join("assets", "background.jpg")  # Make sure this is your correct image name


# --- Functions ---
def show_we_did_it_message():
    messagebox.showinfo("Success!", "We Did It!")


def close_application():
    root.destroy()


def resize_background(event):
    """Resizes the background image whenever the window size changes."""
    new_width = event.width
    new_height = event.height

    resized_image = original_image.resize((new_width, new_height))

    # Store the bg image reference on the ROOT window ---
    root.new_background_image = ImageTk.PhotoImage(resized_image)

    # Update the background label to use this new, safe reference
    background_label.config(image=root.new_background_image)


# --- Main Application Setup ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tennis Simulator - Main Menu")
    root.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")
    root.resizable(True, True)

    try:
        original_image = Image.open(IMAGE_PATH)

        # --- Store the bg image reference on the ROOT window ---
        root.background_image = ImageTk.PhotoImage(original_image.resize((INITIAL_WIDTH, INITIAL_HEIGHT)))

        # Configure the label to use this safe reference
        background_label = tk.Label(root, image=root.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Force the window to draw the image immediately on startup
        root.update_idletasks()

        root.bind("<Configure>", resize_background)

    except FileNotFoundError:
        print(f"Error: Could not find background image at '{IMAGE_PATH}'.")
        root.config(bg="black")

    # --- (Button creation and placement is unchanged) ---
    button_frame = tk.Frame(root, bg="#212121")

    did_it_button = tk.Button(
        button_frame, text="New Game", font=("Arial", 14), command=show_we_did_it_message
    )
    exit_button = tk.Button(
        button_frame, text="Exit Game", font=("Arial", 14), command=close_application
    )

    did_it_button.pack(pady=10, padx=20, fill='x')
    exit_button.pack(pady=10, padx=20, fill='x')
    button_frame.place(relx=0.5, rely=0.5, anchor='center')

    root.mainloop()