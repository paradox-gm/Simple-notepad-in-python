import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

class IDE:
    def __init__(self, master):
        self.master = master
        master.title("IDEal")

        self.create_menu()
        self.create_text_widget()

    def create_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_ide)

        self.help_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

    def create_text_widget(self):
        self.text_widget = scrolledtext.ScrolledText(self.master, width=100, height=30)
        self.text_widget.pack()
        x_scrollbar = tk.Scrollbar(self.master, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_widget.configure(xscrollcommand=x_scrollbar.set)

        # create vertical scrollbar
        y_scrollbar = tk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.text_widget.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.configure(yscrollcommand=y_scrollbar.set)
        self.text_widget.bind("<KeyRelease>", self.highlight_syntax)  # bind syntax highlighting to text widget

    def new_file(self):
        self.text_widget.delete("1.0", "end")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", file_content)

    def save_file(self):
        if self.file_path:
            file_content = self.text_widget.get("1.0", "end")
            with open(self.file_path, "w") as file:
                file.write(file_content)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            file_content = self.text_widget.get("1.0", "end")
            with open(file_path, "w") as file:
                file.write(file_content)
            self.file_path = file_path

    def exit_ide(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.master.destroy()

    def show_about(self):
        messagebox.showinfo("About", "IDEal version 1.0")

    def highlight_syntax(self, event=None):
        """Highlight syntax in the text widget"""
        start = "1.0"
        end = "end"
        self.text_widget.tag_remove("keyword", start, end)  # remove previous tag
        keyword = "print"
        pos = start
        while True:
            pos = self.text_widget.search(keyword, pos, stopindex=end)
            if not pos:
                break
            # apply tag to keyword
            self.text_widget.tag_add("keyword", pos, f"{pos}+{len(keyword)}c")
            pos = f"{pos}+{len(keyword)}c"

        # configure tag for keyword
        self.text_widget.tag_config("keyword", foreground="blue")


root = tk.Tk()
ide = IDE(root)
root.mainloop()
