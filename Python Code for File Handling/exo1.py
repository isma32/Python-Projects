# file_manager_gui.py
import csv
import io
import os
import sys
from tkinter import (
    Tk, Text, Menu, Scrollbar, Toplevel, StringVar, BooleanVar,
    END, INSERT, WORD, BOTH, RIGHT, Y, LEFT, X, N, S, E, W
)
from tkinter import filedialog, messagebox, simpledialog, ttk

APP_NAME = "Tiny Text/CSV Editor"
RECENT_LIMIT = 7
FIND_TAG = "find_match"
CSV_PRETTY_TAG = "csv_pretty"

class EditorApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title(APP_NAME)
        self.filename = None
        self.recent_files = []

        # CSV pretty-print state
        self.csv_pretty_view = BooleanVar(value=True)
        self.csv_delimiter = StringVar(value=",")
        self.csv_quotechar = StringVar(value='"')

        # Text area + scrollbar
        self.text = Text(root, wrap=WORD, undo=True, font=("Consolas", 11))
        self.scroll = Scrollbar(root, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.grid(row=0, column=0, sticky=N+S+E+W)
        self.scroll.grid(row=0, column=1, sticky=N+S)

        # Status bar
        self.status = ttk.Label(root, anchor="w", relief="sunken")
        self.status.grid(row=1, column=0, columnspan=2, sticky=E+W)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Menus
        self._build_menus()

        # Text tags
        self.text.tag_config(FIND_TAG, background="#ffe58f")

        # Shortcuts
        root.bind("<Control-n>", lambda e: self.new_file())
        root.bind("<Control-o>", lambda e: self.open_file())
        root.bind("<Control-s>", lambda e: self.save_file())
        root.bind("<Control-Shift-S>", lambda e: self.save_file_as())
        root.bind("<Control-f>", lambda e: self.open_find_dialog())
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        self._set_status("Ready. New document.")

    # ---------- UI & Menus ----------
    def _build_menus(self):
        menubar = Menu(self.root)

        # File menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        filemenu.add_command(label="Open…", accelerator="Ctrl+O", command=self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        filemenu.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        filemenu.add_separator()
        self.recent_menu = Menu(filemenu, tearoff=0)
        self._rebuild_recent_menu()
        filemenu.add_cascade(label="Open Recent", menu=self.recent_menu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="File", menu=filemenu)

        # Edit menu
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Find…", accelerator="Ctrl+F", command=self.open_find_dialog)
        editmenu.add_separator()
        editmenu.add_command(label="Undo", command=lambda: self._safe_text_edit("undo"))
        editmenu.add_command(label="Redo", command=lambda: self._safe_text_edit("redo"))
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=lambda: self.text.event_generate("<<Cut>>"))
        editmenu.add_command(label="Copy", command=lambda: self.text.event_generate("<<Copy>>"))
        editmenu.add_command(label="Paste", command=lambda: self.text.event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edit", menu=editmenu)

        # CSV menu
        csvmenu = Menu(menubar, tearoff=0)
        csvmenu.add_checkbutton(
            label="Pretty view for CSV (align columns)",
            variable=self.csv_pretty_view,
            command=self._maybe_reformat_csv
        )
        csvmenu.add_separator()
        csvmenu.add_command(label="Set delimiter…", command=self._set_delimiter)
        csvmenu.add_command(label="Set quote character…", command=self._set_quotechar)
        menubar.add_cascade(label="CSV", menu=csvmenu)

        # Help menu
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self._about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)

    def _rebuild_recent_menu(self):
        self.recent_menu.delete(0, END)
        if not self.recent_files:
            self.recent_menu.add_command(label="(empty)", state="disabled")
            return
        for path in self.recent_files[:RECENT_LIMIT]:
            display = path if len(path) <= 60 else "…" + path[-59:]
            self.recent_menu.add_command(
                label=display,
                command=lambda p=path: self._open_path(p)
            )
        self.recent_menu.add_separator()
        self.recent_menu.add_command(label="Clear list", command=self._clear_recent)

    # ---------- File actions ----------
    def new_file(self):
        if not self._maybe_confirm_unsaved():
            return
        self.text.delete("1.0", END)
        self.text.edit_reset()
        self.filename = None
        self._clear_highlights()
        self._set_title()
        self._set_status("New document.")

    def open_file(self):
        if not self._maybe_confirm_unsaved():
            return
        path = filedialog.askopenfilename(
            title="Open",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        self._open_path(path)

    def _open_path(self, path):
        try:
            with open(path, "r", encoding="utf-8", newline="") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")
            return

        self.text.delete("1.0", END)
        self.text.insert("1.0", content)
        self.text.edit_reset()
        self.filename = path
        self._clear_highlights()
        self._set_title(os.path.basename(path))
        self._set_status(f"Opened: {path}")
        self._push_recent(path)

        # If CSV and pretty view is on, format it
        if path.lower().endswith(".csv") and self.csv_pretty_view.get():
            self._format_csv_buffer_pretty()

    def save_file(self):
        if self.filename is None:
            return self.save_file_as()
        return self._save_to_path(self.filename)

    def save_file_as(self):
        default_ext = ".csv" if (self.filename or "").lower().endswith(".csv") else ".txt"
        path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=default_ext,
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return False
        ok = self._save_to_path(path)
        if ok:
            self.filename = path
            self._set_title(os.path.basename(path))
            self._push_recent(path)
        return ok

    def _save_to_path(self, path):
        try:
            # If saving as CSV while in pretty view, we should try to save raw CSV if possible.
            content = self.text.get("1.0", END)
            if path.lower().endswith(".csv") and self.csv_pretty_view.get():
                # Best-effort: if current content aligns like a table (multiple spaces),
                # we will convert consecutive spaces to a single delimiter,
                # unless we detect actual commas already.
                if "," not in content:
                    rows = []
                    for line in content.splitlines():
                        if not line.strip():
                            rows.append([])
                            continue
                        # split on runs of 2+ spaces or tabs
                        chunks = [c for c in _split_columns(line)]
                        rows.append(chunks)
                    content = _rows_to_csv(rows, delimiter=self.csv_delimiter.get(), quotechar=self.csv_quotechar.get())

            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(content.rstrip("\n"))  # no trailing newline storm
            self._set_status(f"Saved: {path}")
            self.text.edit_modified(False)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")
            return False

    # ---------- Find ----------
    def open_find_dialog(self):
        self._clear_highlights()

        dlg = Toplevel(self.root)
        dlg.title("Find")
        dlg.transient(self.root)
        dlg.resizable(False, False)
        dlg.grab_set()

        term_var = StringVar()
        nocase_var = BooleanVar(value=True)
        whole_var = BooleanVar(value=False)

        ttk.Label(dlg, text="Find what:").grid(row=0, column=0, padx=8, pady=(10, 4), sticky="w")
        entry = ttk.Entry(dlg, textvariable=term_var, width=36)
        entry.grid(row=0, column=1, padx=8, pady=(10, 4))
        entry.focus()

        ttk.Checkbutton(dlg, text="Match case", variable=nocase_var, onvalue=False, offvalue=True).grid(row=1, column=0, padx=8, pady=2, sticky="w")
        ttk.Checkbutton(dlg, text="Whole word", variable=whole_var).grid(row=1, column=1, padx=8, pady=2, sticky="w")

        btns = ttk.Frame(dlg)
        btns.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(btns, text="Find All", command=lambda: (self._find_all(term_var.get(), nocase_var.get(), whole_var.get()), dlg.destroy())).pack(side=LEFT, padx=6)
        ttk.Button(btns, text="Cancel", command=dlg.destroy).pack(side=LEFT, padx=6)

        dlg.bind("<Return>", lambda e: (self._find_all(term_var.get(), nocase_var.get(), whole_var.get()), dlg.destroy()))
        dlg.bind("<Escape>", lambda e: dlg.destroy())

    def _find_all(self, needle: str, nocase: bool, whole_word: bool):
        self._clear_highlights()
        if not needle:
            return
        start = "1.0"
        hits = 0
        while True:
            idx = self.text.search(
                needle,
                start,
                nocase=1 if nocase else 0,
                stopindex=END,
                regexp=1 if whole_word else 0,
            ) if whole_word else self.text.search(needle, start, nocase=1 if nocase else 0, stopindex=END)
            if not idx:
                break
            if whole_word:
                # When using regexp, the match is the whole thing; tag from idx to idx+length
                end = f"{idx}+{len(self.text.get(idx, f'{idx} lineend'))}c"  # fallback
                # Better: compute end using match length by re-searching exact span
                # but Text.search doesn't give span. We'll approximate:
                end = f"{idx}+{len(needle)}c"
            else:
                end = f"{idx}+{len(needle)}c"
            self.text.tag_add(FIND_TAG, idx, end)
            hits += 1
            start = end
        if hits:
            first_idx = self.text.index(f"{FIND_TAG}.first")
            self.text.see(first_idx)
        messagebox.showinfo("Find", f"Occurrences found: {hits}")

    def _clear_highlights(self):
        self.text.tag_remove(FIND_TAG, "1.0", END)

    # ---------- CSV helpers ----------
    def _maybe_reformat_csv(self):
        if not (self.filename or "").lower().endswith(".csv"):
            return
        if self.csv_pretty_view.get():
            self._format_csv_buffer_pretty()
        else:
            # reload raw file to avoid losing commas/spaces from pretty formatting
            try:
                with open(self.filename, "r", encoding="utf-8", newline="") as f:
                    content = f.read()
                self.text.delete("1.0", END)
                self.text.insert("1.0", content)
                self.text.edit_reset()
                self._set_status("Switched to raw CSV view.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not revert to raw CSV:\n{e}")

    def _format_csv_buffer_pretty(self):
        """Read current buffer as CSV and render as fixed-width columns."""
        content = self.text.get("1.0", END)
        try:
            rows = list(csv.reader(io.StringIO(content), delimiter=self.csv_delimiter.get() or ",", quotechar=(self.csv_quotechar.get() or '"')))
            if not rows:
                return
            # compute widths
            widths = []
            for r in rows:
                if len(r) > len(widths):
                    widths.extend([0] * (len(r) - len(widths)))
                for i, cell in enumerate(r):
                    widths[i] = max(widths[i], len(cell))
            lines = []
            for r in rows:
                padded = [(r[i] if i < len(r) else "").ljust(widths[i]) for i in range(len(widths))]
                lines.append("  ".join(padded))
            pretty = "\n".join(lines)
            self.text.delete("1.0", END)
            self.text.insert("1.0", pretty)
            self.text.edit_reset()
            self._set_status("Pretty-rendered CSV (readable columns). Saving as .csv will try to preserve raw structure.")
        except Exception as e:
            # If parsing failed, keep raw content
            self._set_status(f"CSV parse error (showing raw): {e}")

    def _set_delimiter(self):
        delim = simpledialog.askstring("CSV Delimiter", "Enter a single-character delimiter (e.g., , ; \\t):", initialvalue=self.csv_delimiter.get())
        if delim is None:
            return
        if delim.lower() == "\\t":
            delim = "\t"
        if len(delim) != 1:
            messagebox.showerror("Invalid", "Delimiter must be exactly one character.")
            return
        self.csv_delimiter.set(delim)
        self._maybe_reformat_csv()

    def _set_quotechar(self):
        quote = simpledialog.askstring("CSV Quote Character", "Enter a single-character quote (e.g., \"):", initialvalue=self.csv_quotechar.get())
        if quote is None:
            return
        if len(quote) != 1:
            messagebox.showerror("Invalid", "Quote character must be exactly one character.")
            return
        self.csv_quotechar.set(quote)
        self._maybe_reformat_csv()

    # ---------- Utilities ----------
    def _safe_text_edit(self, action):
        try:
            getattr(self.text, action)()
        except Exception:
            pass

    def _push_recent(self, path):
        path = os.path.abspath(path)
        if path in self.recent_files:
            self.recent_files.remove(path)
        self.recent_files.insert(0, path)
        del self.recent_files[RECENT_LIMIT:]
        self._rebuild_recent_menu()

    def _clear_recent(self):
        self.recent_files.clear()
        self._rebuild_recent_menu()

    def _set_title(self, name=None):
        title = APP_NAME if not name else f"{name} — {APP_NAME}"
        self.root.title(title)

    def _set_status(self, text):
        self.status.config(text=text)

    def _maybe_confirm_unsaved(self):
        if self.text.edit_modified():
            resp = messagebox.askyesnocancel("Unsaved changes", "You have unsaved changes. Save them?")
            if resp is None:  # Cancel
                return False
            if resp:          # Yes
                if not self.save_file():
                    return False
        return True

    def on_close(self):
        if not self._maybe_confirm_unsaved():
            return
        self.root.destroy()

    def _about(self):
        messagebox.showinfo(
            "About",
            f"{APP_NAME}\n\nA lightweight Tkinter editor for .txt & .csv with Find and CSV pretty view."
        )


# ---------- Helpers outside the class ----------

def _split_columns(line: str):
    """
    Split a monospaced table row on runs of >=2 spaces or tabs.
    Keep single spaces inside tokens.
    """
    cols = []
    current = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch == "\t":
            # treat tab as a column break
            cols.append("".join(current).rstrip())
            current = []
            i += 1
            # skip consecutive tabs
            while i < n and line[i] == "\t":
                i += 1
            continue
        if ch == " ":
            # count run
            j = i
            while j < n and line[j] == " ":
                j += 1
            run = j - i
            if run >= 2:
                cols.append("".join(current).rstrip())
                current = []
                i = j
                # skip extra spaces beyond the run
                while i < n and line[i] == " ":
                    i += 1
                continue
            else:
                current.append(" ")
                i += 1
        else:
            current.append(ch)
            i += 1
    cols.append("".join(current).rstrip())
    # Trim trailing empties that result from long space runs at EOL
    while cols and cols[-1] == "":
        cols.pop()
    return cols

def _rows_to_csv(rows, delimiter=",", quotechar='"'):
    output = io.StringIO()
    writer = csv.writer(output, delimiter=delimiter or ",", quotechar=quotechar or '"', lineterminator="\n")
    for r in rows:
        writer.writerow(r)
    return output.getvalue()

def main():
    root = Tk()
    try:
        # Prefer native-looking widgets when available
        root.call("tk", "scaling", 1.2)
        style = ttk.Style()
        if sys.platform.startswith("win"):
            style.theme_use("winnative")
        else:
            style.theme_use(style.theme_use())
    except Exception:
        pass
    EditorApp(root)
    root.minsize(700, 450)
    root.mainloop()

if __name__ == "__main__":
    main()
