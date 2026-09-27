import sys
import os
import ctypes
import tkinter as tk
from tkinter import font

def show_error(message, title="Saturn file converter - Error"):
    """Displays a native Windows error message box if something fails."""
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10 | 0x0)

class RoundedButtonMain(tk.Canvas):
    """Custom Canvas-based button with smooth rounded corners and hover effects."""
    def __init__(self, parent, text, command, font, bg="#202020", fg="#dcdcdc", hover_bg="#3a3a3a", width=None, height=28, radius=6):
        super().__init__(parent, bg=parent["bg"], highlightthickness=0, bd=0)
        self.command = command
        self.bg = bg
        self.hover_bg = hover_bg
        self.fg = fg
        self.text = text
        self.font = font
        self.radius = radius
        
        if width is None:
            width = max(55, len(text) * 9 + 14)
        self.config(width=width, height=height)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
        self.draw(self.bg)

    def draw(self, bg_color):
        self.delete("all")
        w = int(self["width"])
        h = int(self["height"])
        r = self.radius
        
        self.create_arc(0, 0, 2*r, 2*r, start=90, extent=90, fill=bg_color, outline="")
        self.create_arc(w-2*r, 0, w, 2*r, start=0, extent=90, fill=bg_color, outline="")
        self.create_arc(0, h-2*r, 2*r, h, start=180, extent=90, fill=bg_color, outline="")
        self.create_arc(w-2*r, h-2*r, w, h, start=270, extent=90, fill=bg_color, outline="")
        
        self.create_rectangle(r, 0, w-r, h, fill=bg_color, outline="")
        self.create_rectangle(0, r, w, h-r, fill=bg_color, outline="")
        
        self.create_text(w/2, h/2, text=self.text, fill=self.fg, font=self.font)

    def on_enter(self, event):
        self.draw(self.hover_bg)

    def on_leave(self, event):
        self.draw(self.bg)

    def on_click(self, event):
        if self.command:
            self.command()

def prompt_target_extension():
    """Pops up a compact gradient window to pick conversion format."""
    selected_ext: list[str | None] = [None]
    
    root = tk.Tk()
    root.title("Saturn file converter")
    root.geometry("480x485")
    root.overrideredirect(True)
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . center')
    
    available_fonts = font.families()
    fira_family = "Fira Sans" if "Fira Sans" in available_fonts else ("FiraSans" if "FiraSans" in available_fonts else "Segoe UI")
    
    base_font = (fira_family, 10)
    bold_font = (fira_family, 10, "bold")
    title_font = (fira_family, 11, "bold")
    
    bg_dark = "#141414"
    top_gradient_color = "#1c1c1c"
    border_color = "#555555"
    text_color = "#dcdcdc"
    
    canvas = tk.Canvas(root, width=480, height=485, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    def draw_gradient(event=None):
        canvas.delete("grad")
        for i in range(485):
            nr = int(45 + (10 - 45) * (i / 485))
            ng = int(45 + (10 - 45) * (i / 485))
            nb = int(45 + (10 - 45) * (i / 485))
            color = f"#{nr:02x}{ng:02x}{nb:02x}"
            canvas.create_line(0, i, 480, i, fill=color, tags="grad")

    canvas.bind("<Configure>", draw_gradient)

    container = tk.Frame(canvas, bg=bg_dark)
    container.place(x=0, y=0, width=480, height=485)

    title_bar = tk.Frame(container, bg=top_gradient_color, height=28)
    title_bar.pack(fill=tk.X, side=tk.TOP)
    title_bar.pack_propagate(False)

    title_lbl = tk.Label(title_bar, text="   Saturn file converter", bg=top_gradient_color, fg=text_color, font=base_font)
    title_lbl.pack(side=tk.LEFT, pady=2)

    def close_window():
        root.destroy()

    close_btn = tk.Button(title_bar, text="✕", bg=top_gradient_color, fg=text_color, activebackground="#ff5f56", 
                          activeforeground="#ffffff", relief="flat", bd=0, command=close_window, font=base_font, width=3)
    close_btn.pack(side=tk.RIGHT, fill=tk.Y)

    drag_data = {"x": 0, "y": 0}
    def start_move(event):
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def do_move(event):
        deltax = event.x - drag_data["x"]
        deltay = event.y - drag_data["y"]
        root.geometry(f"+{root.winfo_x() + deltax}+{root.winfo_y() + deltay}")

    title_bar.bind("<Button-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)
    title_lbl.bind("<Button-1>", start_move)
    title_lbl.bind("<B1-Motion>", do_move)

    content_frame = tk.Frame(container, bg=bg_dark)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

    tk.Label(content_frame, text="Select Target Conversion Format:", bg=bg_dark, fg=text_color, font=title_font).pack(anchor="w", pady=(0, 4))

    categories = {
        "Images": [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".ico", ".gif"],
        "Documents & Data": [".pdf", ".docx", ".txt", ".json", ".csv", ".xlsx", ".html", ".md"],
        "Media (Audio/Video)": [".mp4", ".mkv", ".avi", ".mp3", ".wav", ".flac"],
        "Archives": [".zip", ".tar.gz", ".7z"]
    }
    
    def set_and_close(ext):
        selected_ext[0] = ext
        root.destroy()

    def create_section(parent, title):
        outer = tk.Frame(parent, bg=bg_dark, bd=0)
        outer.pack(fill=tk.X, pady=2, padx=0)
        lbl = tk.Label(outer, text=title, bg=bg_dark, fg=text_color, font=bold_font)
        lbl.pack(anchor="w", padx=2, pady=(1, 1))
        grid_f = tk.Frame(outer, bg=bg_dark)
        grid_f.pack(fill=tk.X, padx=0, pady=(0, 2))
        return grid_f

    for cat_name, exts in categories.items():
        g_frame = create_section(content_frame, cat_name)
        for i, ext in enumerate(exts):
            b = RoundedButtonMain(g_frame, text=ext, font=base_font, width=54, height=26, radius=6,
                                  command=lambda e=ext: set_and_close(e))
            b.grid(row=i//4, column=i%4, padx=3, pady=2, sticky="ew")

    custom_outer = tk.Frame(content_frame, bg=bg_dark, bd=0)
    custom_outer.pack(fill=tk.X, pady=2, padx=0)
    
    tk.Label(custom_outer, text="Custom / Other Extension", bg=bg_dark, fg=text_color, font=bold_font).pack(anchor="w", padx=2, pady=(1, 1))
    
    sub_f = tk.Frame(custom_outer, bg=bg_dark)
    sub_f.pack(fill=tk.X, padx=0, pady=(0, 2))
    
    def submit_custom():
        val = entry.get().strip()
        if val:
            if not val.startswith("."):
                val = "." + val
            selected_ext[0] = val.lower()
        root.destroy()

    convert_btn = RoundedButtonMain(sub_f, text="Convert", font=base_font, width=75, height=26, radius=6,
                                    command=submit_custom)
    convert_btn.pack(side=tk.RIGHT, padx=(6, 0))

    entry_border = tk.Frame(sub_f, bg=border_color, bd=0)
    entry_border.pack(side=tk.LEFT, fill=tk.X, expand=True)
    entry_inner = tk.Frame(entry_border, bg="#1a1a1a")
    entry_inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
    
    entry = tk.Entry(entry_inner, bg="#1a1a1a", fg=text_color, insertbackground=text_color, 
                     relief="flat", bd=0, font=base_font)
    entry.pack(fill=tk.BOTH, expand=True, padx=6, ipady=3)
    entry.insert(0, ".odt")
        
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
    
    return selected_ext[0]

def action_universal_convert(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("The target file no longer exists.")
        
    target_ext = prompt_target_extension()
    if not target_ext:
        return 
        
    directory, filename = os.path.split(file_path)
    name, current_ext = os.path.splitext(filename)
    
    if target_ext == current_ext.lower():
        raise ValueError("Source and target extensions cannot be identical.")
        
    out_filepath = os.path.join(directory, f"{name}_converted{target_ext}")

    image_exts = ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.ico', '.gif']
    if target_ext in image_exts:
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                if target_ext in ['.jpg', '.jpeg'] and img.mode in ('RGBA', 'LA'):
                    img = img.convert('RGB')
                img.save(out_filepath)
            return
        except ImportError:
            raise ImportError("Pillow library is required for image conversions. Run 'pip install Pillow' in your terminal.")

    try:
        with open(file_path, 'rb') as src, open(out_filepath, 'wb') as dst:
            while chunk := src.read(1024 * 1024):
                dst.write(chunk)
    except Exception as e:
        raise RuntimeError(f"Conversion failed: {str(e)}")

def main():
    if len(sys.argv) < 2:
        return
    file_path = sys.argv[1]
    try:
        action_universal_convert(file_path)
    except Exception as e:
        show_error(str(e))

if __name__ == "__main__":
    main()