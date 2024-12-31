import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from controllers.doc_parser import DocParser
from controllers.translate_api_controller import TranslateAPIController

class MainView(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.file_path = tk.StringVar()
        self.pack()
        self.translate_controller = TranslateAPIController()
        self.languages = self.translate_controller.getSupportedLanguages()
        self.identified_language_label = None
        self._build_ui()

    def _build_ui(self):
        # Input Language Dropdown
        ttk.Label(self, text="Traducere din limba:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_language = tk.StringVar(value="Identifica limba")
        self.input_language_dropdown = ttk.Combobox(self, textvariable=self.input_language, state="readonly")
        self.input_language_dropdown['values'] = ["Identifica limba"] + [lang['name'] for lang in self.languages]
        self.input_language_dropdown.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.input_language_dropdown.bind("<<ComboboxSelected>>", self._clear_identified_language)

        # Output Language Dropdown
        ttk.Label(self, text="Traducere in limba:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.output_language = tk.StringVar(value="Alege limba")
        self.output_language_dropdown = ttk.Combobox(self, textvariable=self.output_language, state="readonly")
        self.output_language_dropdown['values'] = [lang['name'] for lang in self.languages]
        self.output_language_dropdown.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Select File Button
        ttk.Label(self, text="Alege fisierul").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.file_path_entry = ttk.Entry(self, width=15, textvariable=self.file_path)
        self.file_path_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.select_file_button = ttk.Button(self, text="Cauta...", command=self._select_file)
        self.select_file_button.grid(row=2, column=2, pady=5)

        # Placeholder for Identified Language Label
        self.identified_language_label = ttk.Label(self, text="", anchor="center")
        self.identified_language_label.grid(row=3, column=0, columnspan=3, pady=5)

        # Output Textbox with Scrollbar
        self.output_text = tk.Text(self, wrap="word", height=20, width=60)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=self.scrollbar.set)
        self.output_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.scrollbar.grid(row=4, column=3, sticky="ns")

        self.text_menu = tk.Menu(self, tearoff=0)
        self.text_menu.add_command(label="Select All", command=lambda: self.output_text.tag_add("sel", "1.0", "end"))
        self.text_menu.add_command(label="Copy", command=self._copy_selected)
        self.output_text.bind("<Button-3>", self._show_context_menu)
        self.output_text.bind("<Control-a>", self._select_all)

        # Translate Button
        self.translate_button = ttk.Button(self, text="Tradu", command=self._translate)
        self.translate_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Configure row/column weights for resizing
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def _clear_identified_language(self, event=None):
        self.identified_language_label.config(text="")

    def _show_context_menu(self, event):
        try:
            self.text_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.text_menu.grab_release()

    def _select_all(self, event=None):
        self.output_text.tag_add("sel", "1.0", "end")
        self.output_text.mark_set(tk.INSERT, "1.0")
        self.output_text.see(tk.INSERT)
        return "break"

    def _copy_selected(self):
        try:
            self.clipboard_clear()
            selected_text = self.output_text.get("sel.first", "sel.last")
            self.clipboard_append(selected_text)
            self.update()
        except tk.TclError:
            messagebox.showerror("Error", "No text selected to copy.")


    def _select_file(self):
        self.file_path_entry.delete(0, "end")
        self.file_path = filedialog.askopenfilename(
            title="Alege fisierul",
            filetypes=[
                ("Supported Files", "*.pdf *.txt *.docx"),
                ("PDF Files", "*.pdf"),
                ("Text Files", "*.txt"),
                ("Word Documents", "*.docx")
                ]
            )
        if self.file_path:
            self.file_path_entry.delete(0, "end")
            self.file_path_entry.insert(0, os.path.basename(self.file_path))
            messagebox.showinfo("File Selected", f"Selected file: {os.path.basename(self.file_path)}")

    def _translate(self):
        print(self.file_path)
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file to translate.")
            return
        
        if self.output_language.get() == "Alege limba":
            messagebox.showerror("Error", "Please select an output language.")
            return
        
        try:
            doc_parser = DocParser(self.file_path)
            source_text = doc_parser.extracted_text
            if self.input_language.get() == "Identifica limba":
                source_lang = self.translate_controller.detectLanguage(source_text)
                language_name = [lang["name"] for lang in self.languages if lang["language"] == source_lang][0]
                self.identified_language_label.config(text=f"Limba identificată este: {language_name}")
            else:
                source_lang = [lang["language"] for lang in self.languages if lang["name"] == self.input_language.get()][0]
                self.identified_language_label.config(text="")
            target_lang = [lang["language"] for lang in self.languages if lang["name"] == self.output_language.get()][0]
            self.output_text.delete(1.0, "end")

            translation = self.translate_controller.translate(source_text, source_lang, target_lang)
            self.output_text.insert(1.0, translation)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

