import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess

app = tk.Tk()
app.title("Atenea Convert DDS ↔ PNG")
app.configure(bg="black")

# --- Initial scale ---
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
vmin = min(screen_width, screen_height) / 1080
app.geometry(f"{int(700*vmin)}x{int(480*vmin)}")

# --- Base path for exe packaging ---
base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
ico_path = os.path.join(base_path, "logo.ico")
png_path = os.path.join(base_path, "logo.png")
texconv_path = os.path.join(base_path, "texconv.exe")

# --- Window icon ---
if os.path.exists(png_path):
    try:
        logo_img = ImageTk.PhotoImage(Image.open(png_path))
        app.iconphoto(True, logo_img)
    except Exception as e:
        print("Could not load PNG as icon:", e)

if os.path.exists(ico_path):
    try:
        app.iconbitmap(ico_path)
    except Exception as e:
        print("Could not load ICO as icon:", e)

# --- Fonts ---
def scaled_font(size, style="normal", weight="normal"):
    return ("Segoe UI", int(size*vmin), style, weight)

title_font = scaled_font(18, "bold")
normal_font = scaled_font(11)
main_color = "#007BFF"

# --- Center frame ---
frame = tk.Frame(app, bg="black")
frame.pack(expand=True)

# --- Widgets ---
title_label = tk.Label(frame, text="Atenea Convert DDS ↔ PNG", fg=main_color, bg="black", font=title_font)
title_label.pack(pady=(int(30*vmin), int(25*vmin)))

input_folder = tk.StringVar()
output_folder = tk.StringVar()

lbl_input = tk.Label(frame, text="📂 Input folder:", bg="black", fg="white", font=normal_font)
lbl_input.pack()
entry_input = tk.Entry(frame, textvariable=input_folder, width=55, font=normal_font)
entry_input.pack(pady=(0, int(5*vmin)))
btn_input = tk.Button(frame, text="Select folder", bg=main_color, fg="white",
                      font=scaled_font(9), padx=int(5*vmin), pady=int(3*vmin), cursor="hand2")
btn_input.pack(pady=(0,int(15*vmin)))

lbl_output = tk.Label(frame, text="📂 Output folder:", bg="black", fg="white", font=normal_font)
lbl_output.pack()
entry_output = tk.Entry(frame, textvariable=output_folder, width=55, font=normal_font)
entry_output.pack(pady=(0, int(5*vmin)))
btn_output = tk.Button(frame, text="Select folder", bg=main_color, fg="white",
                       font=scaled_font(9), padx=int(5*vmin), pady=int(3*vmin), cursor="hand2")
btn_output.pack(pady=(0,int(25*vmin)))

# --- Export format option ---
export_format = tk.StringVar(value="PNG")
lbl_format = tk.Label(frame, text="🎨 Output format:", bg="black", fg="white", font=normal_font)
lbl_format.pack()
format_menu = tk.OptionMenu(frame, export_format, "PNG", "DDS")
format_menu.config(bg=main_color, fg="white", font=scaled_font(9), cursor="hand2")
format_menu["menu"].config(bg="black", fg="white", font=scaled_font(9))
format_menu.pack(pady=(0, int(20*vmin)))

btn_convert = tk.Button(frame, text="Convert", bg=main_color, fg="white",
                        font=scaled_font(12, "bold"), padx=int(20*vmin), pady=int(10*vmin), cursor="hand2")
btn_convert.pack(pady=(int(10*vmin), int(10*vmin)))

footer = tk.Label(app, text="© 2025 Atenea Store Tools", bg="black", fg=main_color, font=scaled_font(9, "italic"))
footer.pack(side="bottom", pady=int(10*vmin))

# --- Functions ---
def select_folder(var):
    path = filedialog.askdirectory()
    if path: var.set(path)

btn_input.config(command=lambda: select_folder(input_folder))
btn_output.config(command=lambda: select_folder(output_folder))

# --- Conversion function ---
def convert_images():
    in_folder = input_folder.get()
    out_folder = output_folder.get()
    fmt = export_format.get()

    if not in_folder or not out_folder:
        messagebox.showwarning("Error", "Please select both folders before converting.")
        return

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    # Determine input extension based on target format
    input_ext = ".dds" if fmt == "PNG" else ".png"
    files_to_convert = [os.path.join(r,f) for r,d,files in os.walk(in_folder) for f in files if f.lower().endswith(input_ext)]

    if not files_to_convert:
        messagebox.showinfo("No files", f"No {input_ext.upper()} files were found in the selected folder.")
        return

    for file_path in files_to_convert:
        try:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            subfolder = os.path.relpath(os.path.dirname(file_path), in_folder)
            out_path = os.path.join(out_folder, subfolder)
            os.makedirs(out_path, exist_ok=True)

            if fmt == "PNG":
                Image.open(file_path).save(os.path.join(out_path, base_name+".png"), "PNG")
            elif fmt == "DDS":
                if not os.path.exists(texconv_path):
                    messagebox.showerror("Error", "texconv.exe not found! Make sure it's in the same folder as this script or exe.")
                    return
                subprocess.run(
                    [texconv_path, "-f", "DXT5", "-o", out_path, file_path],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
        except Exception as e:
            print(f"Error with {file_path}: {e}")

    messagebox.showinfo("✅ Conversion complete", f"All images were successfully converted to {fmt}!")

btn_convert.config(command=convert_images)

app.mainloop()
