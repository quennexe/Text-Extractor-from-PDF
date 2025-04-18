import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pdf_utils import load_language, extract_text, save_text_to_file

class PDFTextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.lang_code = "tr"
        self.theme = "light"
        self.lang_data = load_language(self.lang_code)
        self.pdf_path = None

        self.root.geometry("700x600")
        self.build_interface()
        self.apply_theme()

    def build_interface(self):
        
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(pady=5)

        lang_label = tk.Label(lang_frame, text=self.lang_data["language"])
        lang_label.pack(side=tk.LEFT)

        self.lang_var = tk.StringVar(value=self.lang_code)
        lang_menu = tk.OptionMenu(lang_frame, self.lang_var, "tr", "en", self.change_language)
        lang_menu.pack(side=tk.LEFT)

        # Tema seçimi
        theme_frame = tk.Frame(self.root)
        theme_frame.pack()

        theme_label = tk.Label(theme_frame, text=self.lang_data["theme"])
        theme_label.pack(side=tk.LEFT)

        self.theme_var = tk.StringVar(value=self.theme)
        theme_menu = tk.OptionMenu(theme_frame, self.theme_var, "light", "dark", self.change_theme)
        theme_menu.pack(side=tk.LEFT)

        # OCR checkbox
        self.use_ocr_var = tk.BooleanVar()
        self.ocr_check = tk.Checkbutton(self.root, text=self.lang_data["use_ocr"], variable=self.use_ocr_var)
        self.ocr_check.pack(pady=5)

        # PDF seçme
        self.select_btn = tk.Button(self.root, text=self.lang_data["select_pdf"], command=self.select_pdf)
        self.select_btn.pack(pady=5)

        # Sayfa aralığı
        page_frame = tk.Frame(self.root)
        page_frame.pack()

        page_label = tk.Label(page_frame, text=self.lang_data["enter_pages"])
        page_label.pack(side=tk.LEFT)

        self.page_entry = tk.Entry(page_frame)
        self.page_entry.pack(side=tk.LEFT, padx=5)

        # Metni çıkar
        self.extract_btn = tk.Button(self.root, text=self.lang_data["extract_text"], command=self.extract_pdf_text)
        self.extract_btn.pack(pady=5)

        # Metin kutusu
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)

        # Kaydet
        self.save_btn = tk.Button(self.root, text=self.lang_data["save_text"], command=self.save_text)
        self.save_btn.pack(pady=5)

    def change_language(self, selected_lang):
        self.lang_code = selected_lang
        self.lang_data = load_language(self.lang_code)
        self.update_labels()

    def update_labels(self):
        self.root.title(self.lang_data["title"])
        self.select_btn.config(text=self.lang_data["select_pdf"])
        self.extract_btn.config(text=self.lang_data["extract_text"])
        self.save_btn.config(text=self.lang_data["save_text"])
        self.ocr_check.config(text=self.lang_data["use_ocr"])

    def change_theme(self, selected_theme):
        self.theme = selected_theme
        self.apply_theme()

    def apply_theme(self):
        bg = "#ffffff" if self.theme == "light" else "#2e2e2e"
        fg = "#000000" if self.theme == "light" else "#ffffff"

        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg)
            except:
                pass
        self.text_area.configure(bg="#f0f0f0" if self.theme == "light" else "#1e1e1e", fg=fg)

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_path = file_path

    def extract_pdf_text(self):
        if not self.pdf_path:
            messagebox.showerror("Hata", "Lütfen önce bir PDF seçin.")
            return

        page_range = self.page_entry.get()
        use_ocr = self.use_ocr_var.get()
        text = extract_text(self.pdf_path, page_range, use_ocr)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, text)

    def save_text(self):
        text = self.text_area.get(1.0, tk.END).strip()
        if text:
            save_text_to_file(text)
        else:
            messagebox.showinfo("Bilgi", "Kaydedilecek metin yok.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFTextExtractorApp(root)
    root.title("PDF Text Extractor")
    root.mainloop()
