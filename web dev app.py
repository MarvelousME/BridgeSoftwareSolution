import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import webbrowser
from tkinterdnd2 import TkinterDnD, DND_FILES
from pygments import lex
from pygments.lexers import HtmlLexer, CssLexer, JavascriptLexer, PythonLexer
from pygments.styles import get_style_by_name
from PIL import Image, ImageTk
import subprocess
from datetime import datetime

class WebsiteBuilder(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Website Builder")
        self.geometry("1000x700")
        self.configure(bg="#2e2e2e")

        self.base_path = None
        self.copied_item = None
        self.log = []

        # Create UI elements
        self.create_widgets()
        self.apply_dark_mode()

    def create_widgets(self):
        # Menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New File", command=self.create_new_file)
        file_menu.add_command(label="New Folder", command=self.create_new_folder)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="View Logs", command=self.view_logs)
        view_menu.add_command(label="Switch Theme", command=self.switch_theme)
        menu_bar.add_cascade(label="View", menu=view_menu)

        terminal_menu = tk.Menu(menu_bar, tearoff=0)
        terminal_menu.add_command(label="Run Server", command=self.run_server)
        terminal_menu.add_command(label="Git Commit", command=self.git_commit)
        terminal_menu.add_command(label="Run Python", command=self.run_python_script)
        menu_bar.add_cascade(label="Terminal", menu=terminal_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # Path selection
        self.path_label = tk.Label(self, text="No directory selected", bg="#2e2e2e", fg="#00ff00")
        self.path_label.pack(pady=10)

        self.select_path_button = tk.Button(self, text="Select Path", command=self.select_path, bg="#4b4b4b", fg="#00ff00")
        self.select_path_button.pack(pady=5)

        # File tree
        self.file_tree = ttk.Treeview(self)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        self.file_tree.bind("<<TreeviewSelect>>", self.on_file_select)
        self.file_tree.drop_target_register(DND_FILES)
        self.file_tree.dnd_bind('<<Drop>>', self.on_drop)

        # Scrollbars for file tree
        tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.file_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)

        # Content editor
        self.file_content = tk.Text(self, height=15, bg="#1e1e1e", fg="#00ff00", insertbackground="#00ff00", undo=True)
        self.file_content.pack(fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(self, bg="#2e2e2e")
        button_frame.pack(pady=5)

        self.save_button = tk.Button(button_frame, text="Save", command=self.save_file, bg="#4b4b4b", fg="#00ff00")
        self.save_button.grid(row=0, column=0, padx=5)

        self.new_file_button = tk.Button(button_frame, text="New File", command=self.create_new_file, bg="#4b4b4b", fg="#00ff00")
        self.new_file_button.grid(row=0, column=1, padx=5)

        self.new_folder_button = tk.Button(button_frame, text="New Folder", command=self.create_new_folder, bg="#4b4b4b", fg="#00ff00")
        self.new_folder_button.grid(row=0, column=2, padx=5)

        self.copy_button = tk.Button(button_frame, text="Copy", command=self.copy_item, bg="#4b4b4b", fg="#00ff00")
        self.copy_button.grid(row=0, column=3, padx=5)

        self.move_button = tk.Button(button_frame, text="Move", command=self.move_item, bg="#4b4b4b", fg="#00ff00")
        self.move_button.grid(row=0, column=4, padx=5)

        self.duplicate_button = tk.Button(button_frame, text="Duplicate", command=self.duplicate_item, bg="#4b4b4b", fg="#00ff00")
        self.duplicate_button.grid(row=0, column=5, padx=5)

        self.rename_button = tk.Button(button_frame, text="Rename", command=self.rename_item, bg="#4b4b4b", fg="#00ff00")
        self.rename_button.grid(row=0, column=6, padx=5)

        self.preview_button = tk.Button(button_frame, text="Preview Website", command=self.preview_website, bg="#4b4b4b", fg="#00ff00")
        self.preview_button.grid(row=0, column=7, padx=5)

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_file, bg="#4b4b4b", fg="#00ff00")
        self.delete_button.grid(row=0, column=8, padx=5)

        self.theme_button = tk.Button(button_frame, text="Switch Theme", command=self.switch_theme, bg="#4b4b4b", fg="#00ff00")
        self.theme_button.grid(row=0, column=9, padx=5)

        self.find_button = tk.Button(button_frame, text="Find", command=self.find_text, bg="#4b4b4b", fg="#00ff00")
        self.find_button.grid(row=0, column=10, padx=5)

        self.replace_button = tk.Button(button_frame, text="Replace", command=self.replace_text, bg="#4b4b4b", fg="#00ff00")
        self.replace_button.grid(row=0, column=11, padx=5)

        self.run_server_button = tk.Button(button_frame, text="Run Server", command=self.run_server, bg="#4b4b4b", fg="#00ff00")
        self.run_server_button.grid(row=0, column=12, padx=5)

        self.git_button = tk.Button(button_frame, text="Git Commit", command=self.git_commit, bg="#4b4b4b", fg="#00ff00")
        self.git_button.grid(row=0, column=13, padx=5)

        self.open_python_button = tk.Button(button_frame, text="Run Python", command=self.run_python_script, bg="#4b4b4b", fg="#00ff00")
        self.open_python_button.grid(row=0, column=14, padx=5)

        self.log_button = tk.Button(button_frame, text="View Logs", command=self.view_logs, bg="#4b4b4b", fg="#00ff00")
        self.log_button.grid(row=0, column=15, padx=5)

        self.file_content.bind("<KeyRelease>", self.syntax_highlight)

        # Preview Page button at the bottom right
        self.preview_page_button = tk.Button(self, text="Preview Page", command=self.preview_current_page, bg="#4b4b4b", fg="#00ff00")
        self.preview_page_button.pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=10)

    def apply_dark_mode(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="#1e1e1e", fieldbackground="#1e1e1e", foreground="#00ff00")
        style.configure("Treeview.Heading", background="#2e2e2e", foreground="#00ff00")
        style.map("Treeview", background=[('selected', '#4b4b4b')], foreground=[('selected', '#00ff00')])
        self.file_tree.tag_configure('html', foreground='#ff0000')
        self.file_tree.tag_configure('css', foreground='#00ff00')
        self.file_tree.tag_configure('js', foreground='#0000ff')
        self.file_tree.tag_configure('python', foreground='#ffcc00')
        self.file_tree.tag_configure('image', foreground='#ff00ff')
        self.file_tree.tag_configure('other', foreground='#00ffff')

    def select_path(self):
        self.base_path = filedialog.askdirectory()
        if self.base_path:
            self.path_label.config(text=self.base_path)
            self.update_file_tree()
            self.log_action(f"Selected directory: {self.base_path}")

    def update_file_tree(self):
        self.file_tree.delete(*self.file_tree.get_children())
        self.add_tree_nodes('', self.base_path)

    def add_tree_nodes(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            ext = os.path.splitext(p)[1].lower()
            tag = 'other'
            if ext == '.html':
                tag = 'html'
            elif ext == '.css':
                tag = 'css'
            elif ext == '.js':
                tag = 'js'
            elif ext == '.py':
                tag = 'python'
            elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                tag = 'image'
            oid = self.file_tree.insert(parent, 'end', text=p, open=False, tags=(tag, 'folder' if os.path.isdir(abspath) else 'file',))
            if os.path.isdir(abspath):
                self.add_tree_nodes(oid, abspath)

    def on_file_select(self, event):
        selected_item = self.file_tree.selection()[0]
        file_path = self.get_full_path(selected_item)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                self.view_image(file_path)
            else:
                self.load_file_content(file_path)
            self.log_action(f"Selected file: {file_path}")
        else:
            self.file_content.delete(1.0, tk.END)

    def get_full_path(self, item):
        path_parts = []
        while item:
            path_parts.append(self.file_tree.item(item, 'text'))
            item = self.file_tree.parent(item)
        path_parts.reverse()
        return os.path.join(self.base_path, *path_parts)

    def load_file_content(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                content = file.read()
        self.file_content.delete(1.0, tk.END)
        self.file_content.insert(tk.END, content)
        self.syntax_highlight(None)

    def save_file(self):
        selected_item = self.file_tree.selection()[0]
        file_path = self.get_full_path(selected_item)
        if os.path.isfile(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                content = self.file_content.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("Save", "File saved successfully")
            self.log_action(f"Saved file: {file_path}")
        else:
            messagebox.showwarning("Save", "Please select a file to save")

    def create_new_file(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            folder_path = self.get_full_path(selected_item)
        else:
            folder_path = self.base_path

        file_name = simpledialog.askstring("New File", "Enter file name:")
        if file_name:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("")
            self.update_file_tree()
            self.file_tree.selection_set(self.file_tree.get_children()[-1])
            self.on_file_select(None)
            self.log_action(f"Created new file: {file_path}")

    def create_new_folder(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            folder_path = self.get_full_path(selected_item)
        else:
            folder_path = self.base_path

        folder_name = simpledialog.askstring("New Folder", "Enter folder name:")
        if folder_name:
            new_folder_path = os.path.join(folder_path, folder_name)
            os.makedirs(new_folder_path, exist_ok=True)
            self.update_file_tree()
            self.log_action(f"Created new folder: {new_folder_path}")

    def copy_item(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            self.copied_item = self.get_full_path(selected_item[0])
            messagebox.showinfo("Copy", "Item copied successfully")
            self.log_action(f"Copied item: {self.copied_item}")

    def move_item(self):
        selected_item = self.file_tree.selection()
        if selected_item and self.copied_item:
            dest_folder = self.get_full_path(selected_item[0])
            dest_path = os.path.join(dest_folder, os.path.basename(self.copied_item))
            shutil.move(self.copied_item, dest_path)
            self.copied_item = None
            self.update_file_tree()
            messagebox.showinfo("Move", "Item moved successfully")
            self.log_action(f"Moved item to: {dest_path}")

    def duplicate_item(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            src_path = self.get_full_path(selected_item[0])
            dest_path = src_path + "_copy"
            if os.path.isfile(src_path):
                shutil.copy(src_path, dest_path)
            else:
                shutil.copytree(src_path, dest_path)
            self.update_file_tree()
            messagebox.showinfo("Duplicate", "Item duplicated successfully")
            self.log_action(f"Duplicated item: {src_path} to {dest_path}")

    def rename_item(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            old_path = self.get_full_path(selected_item[0])
            new_name = simpledialog.askstring("Rename", "Enter new name:")
            if new_name:
                new_path = os.path.join(os.path.dirname(old_path), new_name)
                os.rename(old_path, new_path)
                self.update_file_tree()
                messagebox.showinfo("Rename", "Item renamed successfully")
                self.log_action(f"Renamed item: {old_path} to {new_path}")

    def delete_file(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            file_path = self.get_full_path(selected_item[0])
            if os.path.isfile(file_path):
                os.remove(file_path)
                self.update_file_tree()
                messagebox.showinfo("Delete", "File deleted successfully")
                self.log_action(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                self.update_file_tree()
                messagebox.showinfo("Delete", "Folder deleted successfully")
                self.log_action(f"Deleted folder: {file_path}")
            else:
                messagebox.showwarning("Delete", "Please select a file or folder to delete")
        else:
            messagebox.showwarning("Delete", "Please select a file or folder to delete")

    def preview_website(self):
        if self.base_path:
            index_file = os.path.join(self.base_path, 'index.html')
            if os.path.exists(index_file):
                webbrowser.open('file://' + os.path.realpath(index_file))
                self.log_action(f"Previewed website: {index_file}")
            else:
                messagebox.showwarning("Preview", "No index.html file found to preview")
        else:
            messagebox.showwarning("Preview", "Please select a directory first")

    def switch_theme(self):
        current_theme = self.cget('bg')
        if current_theme == "#2e2e2e":
            self.configure(bg="#ffffff")
            self.path_label.configure(bg="#ffffff", fg="#000000")
            self.file_content.configure(bg="#ffffff", fg="#000000", insertbackground="#000000")
            for widget in self.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg="#f0f0f0", fg="#000000")
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg="#ffffff")
        else:
            self.configure(bg="#2e2e2e")
            self.path_label.configure(bg="#2e2e2e", fg="#00ff00")
            self.file_content.configure(bg="#1e1e1e", fg="#00ff00", insertbackground="#00ff00")
            for widget in self.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.configure(bg="#4b4b4b", fg="#00ff00")
                elif isinstance(widget, tk.Frame):
                    widget.configure(bg="#2e2e2e")

    def syntax_highlight(self, event):
        content = self.file_content.get("1.0", tk.END)
        self.file_content.mark_set("range_start", "1.0")
        data = self.file_content.get("1.0", tk.END)
        
        for tag in self.file_content.tag_names():
            self.file_content.tag_delete(tag)
        
        lexer = HtmlLexer()
        file_path = self.get_full_path(self.file_tree.selection()[0])
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.css':
            lexer = CssLexer()
        elif ext == '.js':
            lexer = JavascriptLexer()
        elif ext == '.py':
            lexer = PythonLexer()

        tokens = lex(content, lexer)
        for token in tokens:
            token_type = str(token[0]).split('.')[-1]
            token_text = token[1]
            start_index = self.file_content.index("range_start + %dc" % content.find(token_text))
            end_index = self.file_content.index("range_start + %dc" % (content.find(token_text) + len(token_text)))
            self.file_content.tag_add(token_type, start_index, end_index)
            self.file_content.tag_config(token_type, foreground=get_style_by_name('monokai').styles[token[0]])

    def find_text(self):
        find_string = simpledialog.askstring("Find Text", "Enter text to find:")
        if find_string:
            idx = '1.0'
            while True:
                idx = self.file_content.search(find_string, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                lastidx = '%s+%dc' % (idx, len(find_string))
                self.file_content.tag_add('found', idx, lastidx)
                idx = lastidx
            self.file_content.tag_config('found', foreground='red', background='yellow')

    def replace_text(self):
        find_string = simpledialog.askstring("Find Text", "Enter text to find:")
        replace_string = simpledialog.askstring("Replace Text", "Enter replacement text:")
        if find_string and replace_string:
            content = self.file_content.get(1.0, tk.END)
            new_content = content.replace(find_string, replace_string)
            self.file_content.delete(1.0, tk.END)
            self.file_content.insert(1.0, new_content)
            messagebox.showinfo("Replace", f"Replaced '{find_string}' with '{replace_string}'")
            self.log_action(f"Replaced text: '{find_string}' with '{replace_string}'")

    def run_server(self):
        if self.base_path:
            subprocess.Popen(['python', '-m', 'http.server'], cwd=self.base_path)
            messagebox.showinfo("Server", "Server started at http://localhost:8000")
            webbrowser.open('http://localhost:8000')
            self.log_action("Started local server at http://localhost:8000")
        else:
            messagebox.showwarning("Server", "Please select a directory first")

    def git_commit(self):
        commit_message = simpledialog.askstring("Git Commit", "Enter commit message:")
        if commit_message and self.base_path:
            subprocess.Popen(['git', 'add', '.'], cwd=self.base_path)
            subprocess.Popen(['git', 'commit', '-m', commit_message], cwd=self.base_path)
            messagebox.showinfo("Git Commit", "Changes committed successfully")
            self.log_action(f"Committed changes to git with message: {commit_message}")
        else:
            messagebox.showwarning("Git Commit", "Please select a directory and enter a commit message")

    def run_python_script(self):
        selected_item = self.file_tree.selection()[0]
        file_path = self.get_full_path(selected_item)
        if file_path.endswith('.py'):
            result = subprocess.run(['python', file_path], capture_output=True, text=True)
            output = result.stdout + result.stderr
            output_window = tk.Toplevel(self)
            output_window.title("Python Script Output")
            output_text = tk.Text(output_window, wrap=tk.WORD, bg="#1e1e1e", fg="#00ff00", insertbackground="#00ff00")
            output_text.pack(fill=tk.BOTH, expand=True)
            output_text.insert(tk.END, output)
            self.log_action(f"Ran Python script: {file_path}")
        else:
            messagebox.showwarning("Run Python", "Please select a Python (.py) file")

    def view_image(self, file_path):
        image = Image.open(file_path)
        image_window = tk.Toplevel(self)
        image_window.title("Image Viewer")
        img = ImageTk.PhotoImage(image)
        img_label = tk.Label(image_window, image=img)
        img_label.image = img
        img_label.pack()

    def view_logs(self):
        log_window = tk.Toplevel(self)
        log_window.title("Change Logs")
        log_text = tk.Text(log_window, wrap=tk.WORD, bg="#1e1e1e", fg="#00ff00", insertbackground="#00ff00")
        log_text.pack(fill=tk.BOTH, expand=True)
        for log_entry in self.log:
            log_text.insert(tk.END, log_entry + "\n")

    def log_action(self, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {action}"
        self.log.append(log_entry)

    def show_help(self):
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_text = tk.Text(help_window, wrap=tk.WORD, bg="#1e1e1e", fg="#00ff00", insertbackground="#00ff00")
        help_text.pack(fill=tk.BOTH, expand=True)
        help_content = """
        Website Builder Help:

        File Menu:
        - New File: Create a new file in the selected directory.
        - New Folder: Create a new folder in the selected directory.
        - Save: Save the current file.
        - Exit: Exit the application.

        Edit Menu:
        - Find: Find text in the current file.
        - Replace: Replace text in the current file.

        View Menu:
        - View Logs: View the log of actions.
        - Switch Theme: Toggle between light and dark themes.

        Terminal Menu:
        - Run Server: Start a local HTTP server in the selected directory.
        - Git Commit: Commit changes to the Git repository.
        - Run Python: Run the selected Python script.

        Help Menu:
        - Help: Show this help message.

        Additional Features:
        - Drag and drop files into the selected directory.
        - Syntax highlighting for HTML, CSS, JavaScript, and Python files.
        - Image viewer for viewing images in a popup window.
        - Logs for tracking actions.
        """
        help_text.insert(tk.END, help_content)

    def preview_current_page(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            file_path = self.get_full_path(selected_item[0])
            if file_path.endswith('.html'):
                webbrowser.open('file://' + os.path.realpath(file_path))
                self.log_action(f"Previewed page: {file_path}")
            else:
                messagebox.showwarning("Preview Page", "Please select an HTML file to preview")
        else:
            messagebox.showwarning("Preview Page", "Please select a file to preview")

    def on_drop(self, event):
        files = self.tk.splitlist(event.data)
        for file in files:
            shutil.copy(file, self.base_path)
        self.update_file_tree()
        messagebox.showinfo("File Drop", "Files dropped successfully")
        self.log_action(f"Dropped files: {', '.join(files)}")

if __name__ == "__main__":
    app = WebsiteBuilder()
    app.mainloop()
