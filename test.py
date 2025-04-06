import google.generativeai as genai
import tkinter as tk
from tkinter import Toplevel, Text, Button
import pyperclip
import keyboard
import threading
import time
import tkinter.font as tkfont 


# Configure your Gemini API key
genai.configure(api_key="AIzaSyCQ2aKUxOM3SnXsGZTY0VQ4uhqWZtAf0vQ")

# Generate content from Gemini
def generate_content(prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text

# Show content in a popup

def show_copyable_message(content):
    root = tk.Tk()
    root.withdraw()

    dialog = Toplevel(root)
    dialog.title("Generated Content")
    dialog.geometry("600x400")
    dialog.attributes("-topmost", True)

    # Set custom bold font
    bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

    text_widget = Text(dialog, wrap="word", width=70, height=20, font=bold_font)
    text_widget.insert("1.0", content)
    text_widget.config(state="normal")
    text_widget.pack(padx=10, pady=10)

    close_button = Button(dialog, text="Close", command=dialog.destroy, font=bold_font)
    close_button.pack(pady=10)

    root.mainloop()


# Handler for hotkey (Ctrl+Shift+C)
def handle_hotkey():
    time.sleep(0)  # Ensure clipboard is updated
    prompt = pyperclip.paste().strip()
    if prompt:
        print(f"📋 Prompt copied: {prompt}")
        generated_content = generate_content(prompt)
        threading.Thread(target=show_copyable_message, args=(generated_content,)).start()

# Main function
def main():
    print("🕵️ Gemini Clipboard Bot is running. Press Ctrl+c+q to trigger.")
    keyboard.add_hotkey("ctrl+q", handle_hotkey)
    keyboard.wait()  # Keep the script running

if __name__ == "__main__":
    main()

