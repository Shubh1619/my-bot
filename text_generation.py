import google.generativeai as genai
import tkinter as tk
from tkinter import Toplevel, Text, Button
import pyperclip
import keyboard
import threading
import time
import tkinter.font as tkfont

# Configure Gemini API key
genai.configure(api_key="API KEY")

# Generate content using Gemini
def generate_content(prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text

# Show a popup with loading first, then update with Gemini result
def show_loading_and_generate(prompt):
    root = tk.Tk()
    root.withdraw()

    dialog = Toplevel(root)
    dialog.title("Generated Content")
    dialog.geometry("600x400")
    dialog.attributes("-topmost", True)

    # Set custom bold font
    bold_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

    # Text widget with "Loading..." message
    text_widget = Text(dialog, wrap="word", width=70, height=20, font=bold_font)
    text_widget.insert("1.0", "⏳ Generating content, please wait...")
    text_widget.config(state="normal")
    text_widget.pack(padx=10, pady=10)

    # Close button
    close_button = Button(dialog, text="Close", command=dialog.destroy, font=bold_font)
    close_button.pack(pady=10)

    # Background thread to fetch content
    def generate_and_update():
        try:
            result = generate_content(prompt)
        except Exception as e:
            result = f"❌ Error generating content: {str(e)}"

        text_widget.config(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", result)

    threading.Thread(target=generate_and_update).start()
    root.mainloop()

# Hotkey handler
def handle_hotkey():
    time.sleep(0)  # Give clipboard time to update
    prompt = pyperclip.paste().strip()
    if prompt:
        print(f"📋 Prompt copied: {prompt}")
        threading.Thread(target=show_loading_and_generate, args=(prompt,)).start()

# Main function
def main():
    print("🕵️ Gemini Clipboard Bot is running. Press Ctrl+Q to trigger.")
    keyboard.add_hotkey("ctrl+q", handle_hotkey)
    keyboard.wait()  # Keep script running

if __name__ == "__main__":
    main()


