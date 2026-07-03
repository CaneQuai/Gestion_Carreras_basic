import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

# ── palette ──
P_BG        = "#1a1a2e"
P_SURFACE   = "#16213e"
P_CARD      = "#1c2541"
P_BORDER    = "#2a3a5c"
P_ACCENT    = "#e94560"
P_GOLD      = "#f5c518"
P_MUTED     = "#8899aa"
P_TEXT      = "#eef0f4"
P_WHITE     = "#ffffff"
FONT        = ("Segoe UI", 10)
FONT_B      = ("Segoe UI", 10, "bold")
FONT_S      = ("Segoe UI", 9)
FONT_SUB    = ("Segoe UI", 12, "bold")
FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_HERO   = ("Segoe UI", 24, "bold")


def config_styles():
    s = ttk.Style()
    s.theme_use("clam")

    s.configure(".", background=P_BG, foreground=P_TEXT, font=FONT, fieldbackground=P_CARD)
    s.map(".", background=[("active", P_SURFACE)])

    s.configure("TFrame", background=P_BG)
    s.configure("TButton",
                background=P_ACCENT, foreground=P_WHITE, font=FONT_B,
                borderwidth=0, focusthickness=0, focuscolor="none")
    s.map("TButton",
          background=[("active", "#ff6b81"), ("pressed", "#c0392b")])

    s.configure("Secondary.TButton", background=P_BORDER, foreground=P_TEXT)
    s.map("Secondary.TButton",
          background=[("active", "#3a4a6c"), ("pressed", "#2a3a5c")])

    s.configure("Danger.TButton", background="#6c1a1a", foreground=P_TEXT)
    s.map("Danger.TButton",
          background=[("active", "#8a2222"), ("pressed", "#5a1414")])

    s.configure("Card.TFrame", background=P_CARD, relief="flat")
    s.configure("Surface.TFrame", background=P_SURFACE)

    s.configure("TLabel", background=P_BG, foreground=P_TEXT, font=FONT)
    s.configure("Surface.TLabel", background=P_SURFACE, foreground=P_TEXT, font=FONT)
    s.configure("Card.TLabel", background=P_CARD, foreground=P_TEXT, font=FONT)
    s.configure("Header.TLabel", background=P_SURFACE, foreground=P_GOLD, font=FONT_TITLE)
    s.configure("Sub.TLabel", background=P_BG, foreground=P_GOLD, font=FONT_SUB)
    s.configure("Muted.TLabel", background=P_BG, foreground=P_MUTED, font=FONT_S)
    s.configure("White.TLabel", background=P_CARD, foreground=P_WHITE, font=FONT_B)

    s.configure("TLabelframe", background=P_BG, foreground=P_GOLD, bordercolor=P_BORDER,
                lightcolor=P_BORDER, darkcolor=P_BORDER, font=FONT_B)
    s.configure("TLabelframe.Label", background=P_BG, foreground=P_GOLD, font=FONT_B)

    s.configure("TEntry", fieldbackground=P_CARD, foreground=P_TEXT, bordercolor=P_BORDER,
                lightcolor=P_BORDER, darkcolor=P_BORDER)
    s.map("TEntry", fieldbackground=[("focus", "#1e2d4a")])

    s.configure("Treeview",
                background=P_CARD, foreground=P_TEXT, fieldbackground=P_CARD,
                borderwidth=0, rowheight=30)
    s.map("Treeview", background=[("selected", P_ACCENT)], foreground=[("selected", P_WHITE)])
    s.configure("Treeview.Heading",
                background=P_BORDER, foreground=P_TEXT, font=FONT_B, borderwidth=0)
    s.map("Treeview.Heading", background=[("active", "#3a4a6c")])

    s.configure("TScrollbar", background=P_BORDER, bordercolor=P_BORDER,
                arrowcolor=P_TEXT, troughcolor=P_BG)
    s.map("TScrollbar", background=[("active", "#3a4a6c")])

    s.configure("TSeparator", background=P_BORDER)


config_styles()


def card(parent, text):
    f = ttk.Frame(parent, style="Surface.TFrame")
    f.pack(fill=tk.X, pady=(0, 12))
    ttk.Label(f, text=text, style="Header.TLabel").pack(pady=(14, 6))
    ttk.Separator(parent, orient="horizontal").pack(fill=tk.X, padx=4)
    return f


class VertScroll(ttk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, style="TFrame", **kw)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, bg=P_BG, highlightthickness=0)
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw", tags="inner")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll.grid(row=0, column=1, sticky="ns")

    def content(self):
        return self.inner


class ModalRegistrar(tk.Toplevel):
    def __init__(self, parent, corredores):
        super().__init__(parent)
        self.corredores = corredores
        self.title("Registrar Corredores")
        self.geometry("580x520")
        self.resizable(False, False)
        self.configure(bg=P_BG)
        self.transient(parent)
        self.grab_set()

        c = simpledialog.askinteger("Cantidad", "¿Cuántos corredores vas a registrar?",
                                   parent=self, minvalue=1, maxvalue=50)
        if not c:
            self.destroy()
            return
        self.cant = c
        self.entries = []

        card(self, f"🏁 REGISTRAR {c} CORREDOR(ES)")

        vs = VertScroll(self)
        vs.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 6))
        body = vs.content()

        for i in range(c):
            g = ttk.LabelFrame(body, text=f"🚗 Corredor {i+1}", padding=10)
            g.grid(row=i, column=0, padx=2, pady=5, sticky="ew")
            g.columnconfigure(1, weight=1)

            ttk.Label(g, text="Conductor:", style="Card.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=3)
            e1 = ttk.Entry(g); e1.grid(row=0, column=1, sticky="ew", pady=3)

            ttk.Label(g, text="Auto:", style="Card.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=3)
            e2 = ttk.Entry(g); e2.grid(row=1, column=1, sticky="ew", pady=3)

            ttk.Label(g, text="Apuesta ($):", style="Card.TLabel").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=3)
            e3 = ttk.Entry(g); e3.grid(row=2, column=1, sticky="ew", pady=3)

            self.entries.append((e1, e2, e3))

        btns = ttk.Frame(self)
        btns.pack(fill=tk.X, pady=(6, 12))
        ttk.Button(btns, text="✅ Guardar", command=self.guardar).pack(side=tk.LEFT, padx=(20, 5), expand=True, ipadx=12)
        ttk.Button(btns, text="Cancelar", command=self.destroy, style="Secondary.TButton").pack(side=tk.RIGHT, padx=(5, 20), expand=True, ipadx=12)

    def guardar(self):
        for i, (e1, e2, e3) in enumerate(self.entries):
            c = e1.get().strip()
            a = e2.get().strip()
            try:
                ap = float(e3.get().strip())
            except ValueError:
                messagebox.showerror("Error", f"Corredor {i+1}: monto inválido")
                return
            if not c:
                messagebox.showerror("Error", f"Corredor {i+1}: nombre vacío")
                return
            if not a:
                messagebox.showerror("Error", f"Corredor {i+1}: auto vacío")
                return
            self.corredores.append({"conductor": c, "auto": a, "apuesta": ap})
        messagebox.showinfo("Listo", f"{self.cant} corredor(es) guardados ✅")
        self.destroy()


class ModalVerCorredores(tk.Toplevel):
    def __init__(self, parent, corredores):
        super().__init__(parent)
        self.title("Ver Corredores")
        self.geometry("680x440")
        self.resizable(True, True)
        self.configure(bg=P_BG)
        self.transient(parent)
        self.grab_set()

        card(self, f"📋 CORREDORES ({len(corredores)})")

        c = ttk.Frame(self, padding=(18, 6))
        c.pack(fill=tk.BOTH, expand=True)

        cols = ("conductor", "auto", "apuesta")
        t = ttk.Treeview(c, columns=cols, show="headings", height=14)
        t.heading("conductor", text="Conductor")
        t.heading("auto", text="Auto")
        t.heading("apuesta", text="Apuesta")
        t.column("conductor", width=240, minwidth=140)
        t.column("auto", width=240, minwidth=140)
        t.column("apuesta", width=120, minwidth=80, anchor="e")

        for cr in corredores:
            t.insert("", tk.END, values=(cr["conductor"], cr["auto"], f"${cr['apuesta']:.2f}"))

        s = ttk.Scrollbar(c, orient=tk.VERTICAL, command=t.yview)
        t.configure(yscrollcommand=s.set)
        t.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        s.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(self, text="Cerrar", command=self.destroy, style="Secondary.TButton").pack(pady=(8, 14), ipadx=24)


class ModalCarrera(tk.Toplevel):
    def __init__(self, parent, corredores):
        super().__init__(parent)
        self.title("Carrera")
        self.geometry("460x400")
        self.resizable(False, False)
        self.configure(bg=P_BG)
        self.transient(parent)
        self.grab_set()

        if not corredores:
            ttk.Label(self, text="😕 No hay corredores registrados",
                      font=FONT_SUB).pack(expand=True)
            ttk.Button(self, text="Cerrar", command=self.destroy, style="Secondary.TButton").pack(pady=12)
            return

        ganador = random.choice(corredores)

        card(self, "🏁 CARRERA FINALIZADA 🏁")

        body = ttk.Frame(self, style="Card.TFrame")
        body.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        ttk.Label(body, text="🏆", font=("Segoe UI", 40),
                  background=P_CARD).pack(pady=(16, 0))
        ttk.Label(body, text="GANADOR", font=FONT_HERO,
                  foreground=P_GOLD, background=P_CARD).pack()

        sep = ttk.Separator(body, orient="horizontal")
        sep.pack(fill=tk.X, padx=24, pady=10)

        info = ttk.Frame(body, style="Card.TFrame")
        info.pack(pady=6)
        for lbl, val in [("Conductor", ganador["conductor"]),
                         ("Auto", ganador["auto"]),
                         ("Apuesta", f"${ganador['apuesta']:.2f}")]:
            r = ttk.Frame(info, style="Card.TFrame")
            r.pack(pady=4)
            ttk.Label(r, text=f"{lbl}:", font=FONT_B,
                      foreground=P_GOLD, background=P_CARD).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(r, text=val, font=("Segoe UI", 11),
                      background=P_CARD).pack(side=tk.LEFT)

        ttk.Button(self, text="Cerrar", command=self.destroy, style="Secondary.TButton").pack(pady=(6, 16), ipadx=24)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Carreras")
        self.root.geometry("480x460")
        self.root.resizable(False, False)
        self.root.configure(bg=P_BG)

        self.corredores = []

        card(self.root, "🏎 SISTEMA DE CARRERAS 🏎")

        ttk.Label(self.root,
                  text="Bienvenido al sistema de gestión de carreras",
                  style="Muted.TLabel",
                  font=("Segoe UI", 10)).pack(pady=(0, 18))

        btns = ttk.Frame(self.root)
        btns.pack(expand=True)

        items = [
            ("🏁 Registrar Corredores", self.registrar, "TButton"),
            ("📋 Ver Corredores", self.ver_corredores, "TButton"),
            ("🏆 Iniciar Carrera", self.iniciar_carrera, "TButton"),
            ("🚪 Salir", self.root.quit, "Danger.TButton"),
        ]
        for txt, cmd, st in items:
            ttk.Button(btns, text=txt, command=cmd, style=st, width=30).pack(pady=5, ipadx=4, ipady=5)

    def registrar(self):
        ModalRegistrar(self.root, self.corredores)

    def ver_corredores(self):
        if not self.corredores:
            messagebox.showinfo("Sin datos", "No hay corredores registrados")
            return
        ModalVerCorredores(self.root, self.corredores)

    def iniciar_carrera(self):
        ModalCarrera(self.root, self.corredores)

    def run(self):
        self.root.mainloop()
