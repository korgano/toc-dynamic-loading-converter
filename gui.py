# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import main


class TOCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown TOC Generator")
        self.root.geometry("900x600")

        self.file_path = None
        self.headers = []
        self.entries = []

        self.setup_ui()

    # ----------------------------
    # UI Setup
    # ----------------------------

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        self.file_label = tk.Label(top_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT)

        tk.Button(
            top_frame,
            text="Select Markdown File",
            command=self.load_file
        ).pack(side=tk.RIGHT)

        # Table Frame
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Preview Frame
        preview_frame = tk.Frame(self.root)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(preview_frame, text="TOC Preview").pack(anchor="w")

        self.preview_text = tk.Text(preview_frame, height=10)
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Action Buttons
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            action_frame,
            text="Generate Preview",
            command=self.generate_preview
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="Export File",
            command=self.export_file
        ).pack(side=tk.RIGHT, padx=5)

    # ----------------------------
    # File Handling
    # ----------------------------

    def load_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")]
        )

        if not path:
            return

        self.file_path = path
        self.file_label.config(text=path)

        main.setup_logger(path)

        content = main.load_markdown(path)
        self.headers = main.extract_headers(content)

        self.render_table()

    # ----------------------------
    # Table Rendering
    # ----------------------------

    def render_table(self):
        # Clear previous UI
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.entries = []

        # Header row
        header = tk.Frame(self.table_frame)
        header.pack(fill=tk.X)

        tk.Label(header, text="Header", width=30, anchor="w").pack(side=tk.LEFT)
        tk.Label(header, text="Description", width=30, anchor="w").pack(side=tk.LEFT)
        tk.Label(header, text="Keywords", width=30, anchor="w").pack(side=tk.LEFT)

        # Data rows
        for h in self.headers:
            row = tk.Frame(self.table_frame)
            row.pack(fill=tk.X, pady=2)

            tk.Label(row, text=h["text"], width=30, anchor="w").pack(side=tk.LEFT)

            desc_entry = tk.Entry(row, width=30)
            desc_entry.pack(side=tk.LEFT, padx=2)

            keyword_entry = tk.Entry(row, width=30)
            keyword_entry.pack(side=tk.LEFT, padx=2)

            self.entries.append({
                "header": h["text"],
                "level": h["level"],
                "description_entry": desc_entry,
                "keywords_entry": keyword_entry
            })

    # ----------------------------
    # Data Collection
    # ----------------------------

    def collect_data(self):
        enriched = []

        for e in self.entries:
            enriched.append({
                "header": e["header"],
                "level": e["level"],
                "description": e["description_entry"].get(),
                "keywords": e["keywords_entry"].get()
            })

        return enriched

    # ----------------------------
    # Actions
    # ----------------------------

    def generate_preview(self):
        if not self.headers:
            messagebox.showerror("Error", "No file loaded")
            return

        data = self.collect_data()
        toc = main.generate_toc(data)

        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, toc)

    def export_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file loaded")
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md")]
        )

        if not output_path:
            return

        try:
            data = self.collect_data()
            main.process_markdown(self.file_path, data, output_path)

            messagebox.showinfo("Success", "File exported successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = TOCApp(root)
    root.mainloop()