import qrcode
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def generate_qr():
    global qr_img
    data = entry.get()
    if not data.strip():
        messagebox.showwarning("Input Required", "Please enter text or URL.")
        return

    # Generate base QR code
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)  # High error correction
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Load and paste logo
    try:
        logo = Image.open("logo.png")
        basewidth = 60
        wpercent = basewidth / float(logo.size[0])
        hsize = int(float(logo.size[1]) * float(wpercent))
        logo = logo.resize((basewidth, hsize), Image.LANCZOS)

        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    except FileNotFoundError:
        messagebox.showwarning("Logo Missing", "Logo file 'logo.png' not found. QR will be generated without logo.")

    # Display
    img_resized = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img_resized)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk
    qr_img = img
    save_btn.config(state=NORMAL)

def save_qr():
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if file_path:
        qr_img.save(file_path)
        messagebox.showinfo("Saved", f"QR Code saved to:\n{file_path}")

# GUI
app = Tk()
app.title("QR Code Generator with Logo")
app.geometry("400x400")
app.config(bg="#f9f9f9")

Label(app, text="Enter text or URL:", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)

entry = Entry(app, width=40, font=("Arial", 12))
entry.pack(pady=5)

Button(app, text="Generate QR Code", command=generate_qr, font=("Arial", 12), bg="#0078D7", fg="white").pack(pady=10)

qr_label = Label(app, bg="#f9f9f9")
qr_label.pack(pady=10)

save_btn = Button(app, text="Save QR Code", command=save_qr, state=DISABLED, font=("Arial", 12), bg="green", fg="white")
save_btn.pack(pady=5)

app.mainloop()
