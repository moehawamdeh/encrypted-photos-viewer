#!/usr/bin/env python3

import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from io import BytesIO
from Crypto.Cipher import AES

    
import re

def extract_number(filename):
    """Extracts the number inside parentheses in the filename."""
    match = re.search(r'\((\d+)\)', filename)  # Find number inside ()
    return int(match.group(1)) if match else float('inf')  # Default to a high number if no match

def decrypt_file(key, in_filename):
    """
    Decrypts a file encrypted with AES (EAX mode).
    Assumes file format: [nonce(16 bytes) + tag(16 bytes) + ciphertext(...)]. 
    Returns the decrypted bytes.
    """
    with open(in_filename, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

class ImageViewer:
    def __init__(self, master, images_data, file_names):
        self.master = master
        self.images_data = images_data
        self.file_names = file_names
        self.index = 0
        self.rotation_angle = 0  # Track rotation angle
        
        if self.file_names:
            self.master.title(self.file_names[0])
        else:
            self.master.title("Encrypted Image Viewer")
        
        self.label = tk.Label(master)
        self.label.pack(fill=tk.BOTH, expand=True)
        
        self.master.bind("<Left>", self.show_prev)
        self.master.bind("<Right>", self.show_next)
        self.master.bind("<space>", self.rotate_image)  # Bind spacebar to rotation
        
        self.master.bind("<Configure>", self.on_resize)
        
        if self.images_data:
            self.show_image(0)
        else:
            messagebox.showinfo("Info", "No images found!")

    def show_image(self, idx):
        self.index = idx
        img_stream = BytesIO(self.images_data[idx])
        self.pil_img = Image.open(img_stream)

        # Apply the stored rotation angle
        if self.rotation_angle:
            self.pil_img = self.pil_img.rotate(self.rotation_angle, expand=True)

        self.master.title(self.file_names[idx])  # Update window title with file name
        self.resize_image()

    def rotate_image(self, event):
        if hasattr(self, 'pil_img'):
            self.rotation_angle = (self.rotation_angle + 90) % 360
            self.pil_img = self.pil_img.rotate(90, expand=True)
            self.resize_image()

    def resize_image(self):
        if hasattr(self, 'pil_img'):
            window_width = max(1, self.master.winfo_width())
            window_height = max(1, self.master.winfo_height())

            img_width, img_height = self.pil_img.size
            if img_width <= 0 or img_height <= 0:
                return

            aspect_ratio = img_width / img_height

            if window_width / aspect_ratio <= window_height:
                new_width = max(1, window_width)
                new_height = max(1, int(window_width / aspect_ratio))
            else:
                new_height = max(1, window_height)
                new_width = max(1, int(window_height * aspect_ratio))

            resized_img = self.pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.tk_img = ImageTk.PhotoImage(resized_img)

            self.label.config(image=self.tk_img)

    def on_resize(self, event):
        self.resize_image()

    def show_prev(self, event):
        self.index = (self.index - 1) % len(self.images_data)
        self.show_image(self.index)
        
    def show_next(self, event):
        self.index = (self.index + 1) % len(self.images_data)
        self.show_image(self.index)

def main():
    root_for_key = tk.Tk()
    root_for_key.withdraw()

    key_str = simpledialog.askstring("Enter Key", "Please enter the 16-byte AES key:")

    if not key_str:
        messagebox.showwarning("Warning", "No key provided. Exiting...")
        return

    key = key_str.encode('utf-8')

    if len(key) != 16:
        messagebox.showwarning("Warning", "Key must be exactly 16 bytes for AES-128. Exiting...")
        return

    root_for_key.destroy()

    enc_dir = 'encrypted_images'
    
    enc_files = sorted(
        [os.path.join(enc_dir, f) for f in os.listdir(enc_dir) if f.lower().endswith('.enc')],
        key=lambda x: extract_number(os.path.basename(x))  # Sort using extracted number
    )

    
    images_data = []
    file_names = []
    
    for ef in enc_files:
        try:
            decrypted_data = decrypt_file(key, ef)
            images_data.append(decrypted_data)
            file_names.append(os.path.basename(ef))
        except Exception as e:
            print(f"Failed to decrypt {ef}: {e}")
    
    root = tk.Tk()
    root.geometry("800x600")
    viewer = ImageViewer(root, images_data, file_names)
    root.mainloop()

if __name__ == '__main__':
    main()
