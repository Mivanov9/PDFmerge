import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import PyPDF2


class Application(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.file_list = []
        self.btn_frame = tk.Frame(self)
        # Buttons
        self.input_button = tk.Button(self.btn_frame)
        self.output_button = tk.Button(self.btn_frame)
        self.delete_button = tk.Button(self.btn_frame)
        self.move_up_button = tk.Button(self.btn_frame)
        self.move_down_button = tk.Button(self.btn_frame)
        # Tree view
        self.pdf_list = ttk.Treeview(self, columns=1, selectmode="browse", show=["headings"])
        self.pdf_list_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.pdf_list.yview)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.root.title("PDF Merger")
        self.root.resizable(False, False)
        # Button frame
        self.btn_frame.grid(row=0, column=0)
        # input button
        self.input_button["text"] = "Add PDF"
        self.input_button["command"] = self.input_pdf
        self.input_button.grid(row=0, column=0)
        # delete button
        self.delete_button["text"] = "Remove PDF"
        self.delete_button["command"] = self.delete_pdf
        self.delete_button.grid(row=1, column=0)
        # Save As button
        self.output_button["text"] = "Save As"
        self.output_button["command"] = self.output_pdf
        self.output_button.grid(row=2, column=0)
        # Move up button
        self.move_up_button["text"] = "Move up"
        self.move_up_button["command"] = self.move_up_pdf
        self.move_up_button.grid(row=3, column=0)
        # Move down button
        self.move_down_button["text"] = "Move down"
        self.move_down_button["command"] = self.move_down_pdf
        self.move_down_button.grid(row=4, column=0)
        # Tree view
        self.pdf_list.grid(row=0, column=1)
        self.pdf_list.heading('#1', text='File Name')
        self.pdf_list.column('#1', width=200)
        # Tree Scrollbar
        self.pdf_list_scrollbar.grid(row=0, column=1, sticky="nse")
        self.pdf_list.configure(yscrollcommand=self.pdf_list_scrollbar.set)

    def input_pdf(self):
        file_names = filedialog.askopenfilenames(filetypes=[("PDF", ".pdf")])
        if not file_names:
            return
        for file_name in file_names:
            self.file_list.append(file_name)
            file_name_formatted = file_name.split("/")
            self.pdf_list.insert(parent="", index="end", iid=None, values=file_name_formatted[-1])
        return

    def output_pdf(self):
        # if no files added
        if not self.file_list:
            return
        result = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", ".pdf")])
        # if save file prompt canceled
        if not result:
            return
        merger = PyPDF2.PdfFileMerger()
        for file in self.file_list:
            merger.append(file)
        merger.write(result)
        merger.close()

    def delete_pdf(self):
        selection = self.pdf_list.focus()
        if not selection:
            return
        del self.file_list[self.pdf_list.index(selection)]
        self.pdf_list.delete(selection)
        return

    def move_up_pdf(self):
        selection = self.pdf_list.focus()
        if not selection:
            return
        i = self.pdf_list.index(selection)
        if i == 0:
            return
        j = i - 1
        self.pdf_list.move(selection, self.pdf_list.parent(selection), index=j)
        self.file_list[j], self.file_list[i] = self.file_list[i], self.file_list[j]
        return

    def move_down_pdf(self):
        selection = self.pdf_list.focus()
        if not selection:
            return
        i = self.pdf_list.index(selection)
        if i == len(self.file_list) - 1:
            return
        j = i + 1
        self.pdf_list.move(selection, self.pdf_list.parent(selection), index=j)
        self.file_list[j], self.file_list[i] = self.file_list[i], self.file_list[j]
        return
