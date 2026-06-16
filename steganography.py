import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image
import random
import pyperclip


def encode_message_in_image(image_path, message, output_image_path, key):
    img = Image.open(image_path)
    img = img.convert("RGB")

    message += "####"
    binary_message = ''.join([format(ord(char), '08b') for char in message])

    pixels = list(img.getdata())

    random.seed(key)   # ✅ string key works

    pixel_indices = list(range(len(pixels)))
    random.shuffle(pixel_indices)

    for i in range(len(binary_message)):
        pixel_index = pixel_indices[i]
        r, g, b = pixels[pixel_index]

        r = (r & ~1) | int(binary_message[i])

        pixels[pixel_index] = (r, g, b)

    img.putdata(pixels)
    img.save(output_image_path, 'PNG')

    messagebox.showinfo("Success", f"Message encoded and saved in {output_image_path}")
    show_main_menu()


def decode_message_from_image(image_path, key):
    img = Image.open(image_path)
    img = img.convert("RGB")

    pixels = list(img.getdata())

    random.seed(key)   # ✅ same string key used

    pixel_indices = list(range(len(pixels)))
    random.shuffle(pixel_indices)

    binary_message = ''

    for pixel_index in pixel_indices:
        r, g, b = pixels[pixel_index]
        binary_message += str(r & 1)

    message = ''.join([
        chr(int(binary_message[i:i+8], 2))
        for i in range(0, len(binary_message), 8)
    ])

    message = message.split("####")[0]

    display_decoded_message(message)


def display_decoded_message(message):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Decoded Message:", font=label_font,
             bg=bg_color, fg=fg_color).pack(pady=10)

    text_area = ScrolledText(root, height=4, width=50,
                             font=label_font, bg=input_bg,
                             fg=input_fg, bd=0, relief=tk.FLAT)

    text_area.pack(pady=10)
    text_area.insert(tk.END, message)
    text_area.config(state=tk.DISABLED)

    def copy_to_clipboard():
        pyperclip.copy(message)
        messagebox.showinfo("Copied", "Message copied to clipboard!")

    CurvedButton(root, text="Copy to Clipboard",
                 font=button_font,
                 command=copy_to_clipboard).pack(pady=10)

    CurvedButton(root, text="Back",
                 font=button_font,
                 command=show_main_menu).pack(pady=10)


def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Image Steganography Project",
             font=title_font, bg=bg_color, fg=fg_color).pack(pady=20)

    CurvedButton(root, text="Encode Message",
                 font=button_font,
                 command=encode_menu).pack(pady=10)

    CurvedButton(root, text="Decode Message",
                 font=button_font,
                 command=decode_menu).pack(pady=10)

    CurvedButton(root, text="About App",
                 font=button_font,
                 command=about_app).pack(pady=10)


def encode_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Encode Message",
             font=title_font, bg=bg_color,
             fg=fg_color).pack(pady=10)

    global image_path
    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if not image_path:
        show_main_menu()
        return

    tk.Label(root, text="Enter Secret Message:",
             font=label_font, bg=bg_color,
             fg=fg_color).pack(pady=10)

    global message_entry
    message_entry = tk.Text(root, height=4, width=50,
                            font=label_font, bg=input_bg,
                            fg=input_fg, bd=0,
                            relief=tk.FLAT)
    message_entry.pack(pady=10)

    tk.Label(root, text="Enter Key (default: 13579):",
             font=label_font, bg=bg_color,
             fg=fg_color).pack(pady=10)

    global key_entry
    key_entry = tk.Entry(root, font=label_font,
                         bg=input_bg, fg=input_fg,
                         bd=0, relief=tk.FLAT)
    key_entry.insert(0, "13579")
    key_entry.pack(pady=10)

    CurvedButton(root, text="Encode",
                 font=button_font,
                 command=encode_action).pack(pady=10)

    CurvedButton(root, text="Back",
                 font=button_font,
                 command=show_main_menu).pack(pady=10)


def encode_action():
    message = message_entry.get("1.0", tk.END).strip()

    output_image_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )

    key = key_entry.get() if key_entry.get() else "13579"   # ✅ FIXED

    if message and output_image_path:
        encode_message_in_image(image_path, message,
                                output_image_path, key)


def decode_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Decode Message",
             font=title_font, bg=bg_color,
             fg=fg_color).pack(pady=10)

    global image_path
    image_path = filedialog.askopenfilename(
        title="Select Encoded Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )

    if not image_path:
        show_main_menu()
        return

    tk.Label(root, text="Enter Key (default: 13579):",
             font=label_font, bg=bg_color,
             fg=fg_color).pack(pady=10)

    global key_entry
    key_entry = tk.Entry(root, font=label_font,
                         bg=input_bg, fg=input_fg,
                         bd=0, relief=tk.FLAT)
    key_entry.insert(0, "13579")
    key_entry.pack(pady=10)

    CurvedButton(root, text="Decode",
                 font=button_font,
                 command=decode_action).pack(pady=10)

    CurvedButton(root, text="Back",
                 font=button_font,
                 command=show_main_menu).pack(pady=10)


def decode_action():
    key = key_entry.get() if key_entry.get() else "13579"   # ✅ FIXED
    decode_message_from_image(image_path, key)


def about_app():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="About App",
             font=title_font, bg=bg_color,
             fg=fg_color).pack(pady=20)

    about_text = (
        "This program hides secret messages in images.\n"
        "Only users with the correct key can decode it."
    )

    tk.Label(root, text=about_text,
             font=label_font, bg=bg_color,
             fg=fg_color, wraplength=500,
             justify="left").pack(pady=20)

    CurvedButton(root, text="Back",
                 font=button_font,
                 command=show_main_menu).pack(pady=10)


class CurvedButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg=button_bg, fg=button_fg,
                       relief=tk.FLAT, bd=0,
                       padx=20, pady=10)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = hover_bg

    def on_leave(self, e):
        self['bg'] = button_bg


# UI Settings
bg_color = "#191919"
fg_color = "#FFFFFF"
button_bg = "#FF7F50"
button_fg = "#FFFFFF"
hover_bg = "#FF4500"
input_bg = "#87CEFA"
input_fg = "#000000"

title_font = ("Helvetica", 18, "bold")
label_font = ("Helvetica", 14)
button_font = ("Helvetica", 16, "bold")
small_font = ("Helvetica", 10)


# Main Window
root = tk.Tk()
root.title("Image Steganography")
root.geometry("700x700")
root.configure(bg=bg_color)

show_main_menu()

root.mainloop()