
import tkinter as tk
from tkinter import filedialog
from PIL import Image

def convert_to_dds(image_path, output_path):
    image = Image.open(image_path)
    image.save(output_path, format='DDS')

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        output_path = filedialog.asksaveasfilename(defaultextension=".dds", filetypes=[("DDS files", "*.dds")])
        if output_path:
            convert_to_dds(file_path, output_path)
            tk.messagebox.showinfo("Success", "Image converted to DDS format successfully!")

root = tk.Tk()
root.title("Image to DDS Converter")

select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=20)

root.mainloop()