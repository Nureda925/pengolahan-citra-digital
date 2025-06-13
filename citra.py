import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class AplikasiPengolahanCitra:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengolahan Citra - One Piece Pastel Theme")
        self.root.state('zoomed') 
        self.root.configure(bg="#FFF7D6") 

        # Header
        self.header_label = Label(self.root, text=" 🌞🚢 Aplikasi Pengolahan Citra Digital 🌞🚢 ",
        font=("OnePiece", 20, "bold"), fg="#000000", bg="#AEDFF7", pady=20) 
        self.header_label.pack(fill='x')

        # Frame Menu di kiri
        self.menu_frame = Label(self.root, bg="#FAD4C0", width=10, height=15)  
        self.menu_frame.place(x=20, y=100)

        menu_title = Label(self.menu_frame, text="⚓ Menu ⚓", font=("OnePiece", 14, "bold"),
        bg="#FAD4C0", fg="#47312A")  
        menu_title.pack(pady=10)

        # Tombol-tombol menu
        self.create_button("📂 Input Gambar", self.load_image)
        self.create_button("♥ Grayscale", self.to_grayscale)
        self.create_button("⚪ Biner", self.to_binary)
        self.create_button("☀️ Brightness (+)", self.arithmetic_op)
        self.create_button("✖ Logika (AND)", self.logic_op)
        self.create_button("🌫️ Blur", self.blur_image)
        self.create_button("📊 Histogram", self.show_histogram)
        self.create_button("🔍 Edge Detection", self.sharpen_filter)
        self.create_button("🔧 Morfologi", self.morphology_ops)
        self.create_button("💾 Save Image", self.save_image)

        # Frame untuk menampilkan gambar di tengah
        self.image_frame = Label(self.root, bg="#FFFFFF", relief="ridge", width=800, height=500)  
        self.image_frame.place(x=300, y=120)

        image_title = Label(self.root, text=" ~ Gambar ~ ", font=("OnePiece", 15),
        bg="#AEDFF7", fg="black")  
        image_title.place(x=750, y=100)

        self.original = None
        self.binary = None

    def create_button(self, text, command):
        button = Button(self.menu_frame, text=text, command=command, font=("Poppins", 11, "bold"),
        bg="#F89090", fg="white", activebackground="#F89090", relief='flat',
        width=25, height=1, cursor="hand2")  
        button.pack(pady=4)

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.original = cv2.imread(path)
            self.display_image(self.original)

    def display_image(self, img):
        if len(img.shape) == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img_rgb)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            self.image_frame.configure(image=img_tk)
            self.image_frame.image = img_tk

    def to_grayscale(self):
        if self.original is not None:
            gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
            self.display_image(gray)

    def to_binary(self):
        if self.original is not None:
            gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
            _, self.binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            self.display_image(self.binary)

    def arithmetic_op(self):
        if self.original is not None:
            added = cv2.add(self.original, np.ones_like(self.original, dtype=np.uint8) * 50)
            self.display_image(added)

    def logic_op(self):
        if self.binary is not None:
            result = cv2.bitwise_and(self.binary, self.binary)
            self.display_image(result)

    def blur_image(self):
        if self.original is not None:
            blur = cv2.GaussianBlur(self.original, (5, 5), 0)
            self.display_image(blur)

    def show_histogram(self):
        if self.original is not None:
            color = ('b', 'g', 'r')
            for i, col in enumerate(color):
                hist = cv2.calcHist([self.original], [i], None, [256], [0, 256])
                plt.plot(hist, color=col)
                plt.xlim([0, 256])
            plt.title("Histogram")
            plt.show()

    def sharpen_filter(self):
        if self.original is not None:
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            sharpened = cv2.filter2D(self.original, -1, kernel)
            self.display_image(sharpened)

    def morphology_ops(self):
        if self.original is not None:
            gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

            dilated = cv2.dilate(binary, kernel1, iterations=1)
            eroded = cv2.erode(dilated, kernel2, iterations=1)

            self.display_image(eroded)

    def save_image(self):
        if self.processed is not None:
            path = filedialog.asksaveasfilename(defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if path:
                img_to_save = self.processed
                if len(img_to_save.shape) == 3 and img_to_save.shape[2] == 3:
                    img_to_save = cv2.cvtColor(img_to_save, cv2.COLOR_RGB2BGR)
                cv2.imwrite(path, img_to_save)

if __name__ == '__main__':
    root = Tk()
    app = AplikasiPengolahanCitra(root)
    root.mainloop()
