import os
import sys
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess

# ==== Ventana base ====
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Atenea Convert DDS ↔ PNG")
app.configure(fg_color="black")

# Escala dinámica
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
vmin = min(screen_width, screen_height) / 1080
app.geometry(f"{int(700*vmin)}x{int(580*vmin)}")


# ==== Rutas de iconos para versión EXE ====
base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
ico_path = os.path.join(base_path, "logo.ico")
png_path = os.path.join(base_path, "logo.png")

# Icono
if os.path.exists(png_path):
    try:
        icon_image = ImageTk.PhotoImage(Image.open(png_path))
        app.iconphoto(True, icon_image)
    except:
        pass

if os.path.exists(ico_path):
    try:
        app.iconbitmap(ico_path)
    except:
        pass


# ==== Widgets principales ====
title = ctk.CTkLabel(app, text="Atenea Convert DDS ↔ PNG",
                     font=("Segoe UI", int(26*vmin), "bold"),
                     text_color="#007BFF")
title.pack(pady=int(20*vmin))

frame = ctk.CTkFrame(app, fg_color="black")
frame.pack(expand=True)


# Carpetas
input_folder = ctk.StringVar()
output_folder = ctk.StringVar()

ctk.CTkLabel(frame, text="📂 Input Folder:", text_color="white",
             font=("Segoe UI", int(14*vmin))).pack()

ctk.CTkEntry(frame, textvariable=input_folder, width=int(450*vmin),
             font=("Segoe UI", int(13*vmin))).pack(pady=5)

ctk.CTkButton(frame, text="Select Folder", fg_color="#007BFF",
              command=lambda: input_folder.set(filedialog.askdirectory())).pack(pady=10)


ctk.CTkLabel(frame, text="📂 Output Folder:", text_color="white",
             font=("Segoe UI", int(14*vmin))).pack()

ctk.CTkEntry(frame, textvariable=output_folder, width=int(450*vmin),
             font=("Segoe UI", int(13*vmin))).pack(pady=5)

ctk.CTkButton(frame, text="Select Folder", fg_color="#007BFF",
              command=lambda: output_folder.set(filedialog.askdirectory())).pack(pady=20)


# ==== Selector de formato (igual que PNG ↔ WEBP) ====
export_format = ctk.StringVar(value="PNG")

ctk.CTkLabel(frame, text="🎨 Output Format:", text_color="white",
             font=("Segoe UI", int(14*vmin))).pack(pady=5)

def set_fmt(value):
    export_format.set(value)

format_switch = ctk.CTkSegmentedButton(frame, values=["PNG", "DDS"],
                                       variable=export_format,
                                       command=set_fmt,
                                       font=("Segoe UI", int(12*vmin)))
format_switch.pack(pady=int(10*vmin))


# ==== Convertir ====
def convert_images():
    in_folder = input_folder.get()
    out_folder = output_folder.get()
    fmt = export_format.get()

    if not in_folder or not out_folder:
        messagebox.showwarning("Error", "Please select both folders before converting.")
        return

    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    input_ext = ".dds" if fmt == "PNG" else ".png"
    files = [os.path.join(r,f) for r,_,fs in os.walk(in_folder) for f in fs if f.lower().endswith(input_ext)]

    if not files:
        messagebox.showinfo("No files", f"No {input_ext.upper()} files were found in the selected folder.")
        return

    texconv = os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(sys.executable)), "texconv.exe")

    for path in files:
        try:
            base = os.path.splitext(os.path.basename(path))[0]
            subfolder = os.path.relpath(os.path.dirname(path), in_folder)
            save_path = os.path.join(out_folder, subfolder)
            os.makedirs(save_path, exist_ok=True)

            if fmt == "PNG":
                Image.open(path).save(os.path.join(save_path, base+".png"), "PNG")

            elif fmt == "DDS":
                if not os.path.exists(texconv):
                    messagebox.showerror("Error", "texconv.exe not found! Make sure it's included next to the exe.")
                    return
                subprocess.run([texconv, "-f", "R8G8B8A8_UNORM", "-srgb", "-y", "-o", save_path, path],
                               creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass

    messagebox.showinfo("✅ Done", f"Images successfully converted to {fmt}!")


ctk.CTkButton(frame, text="Convert", fg_color="#007BFF",
              font=("Segoe UI", int(18*vmin), "bold"),
              width=int(200*vmin), height=int(45*vmin),
              command=convert_images).pack(pady=int(25*vmin))


footer = ctk.CTkLabel(app, text="© 2025 Atenea Store Tools",
                      text_color="#007BFF",
                      font=("Segoe UI", int(12*vmin)))
footer.pack(pady=int(10*vmin))


app.mainloop()
