"""Colores y controles compartidos por las ventanas del blog."""
import tkinter as tk
from tkinter import ttk

FONDO = "#09070c"
PANEL = "#18101f"
CAMPO = "#100b16"
BORDE = "#654479"
NEON = "#df85ff"
TEXTO = "#faf2ff"
SUAVE = "#ccbad8"
SELECCION = "#74329b"
BOTON = "#32213f"


def aplicar(raiz):
    raiz.configure(bg=FONDO)
    estilo = ttk.Style(raiz)
    estilo.theme_use("clam")
    estilo.configure(".", background=FONDO, foreground=TEXTO, bordercolor=BORDE,
                     lightcolor=BORDE, darkcolor=BORDE, focuscolor=NEON,
                     selectbackground=SELECCION, selectforeground=TEXTO)
    estilo.configure("TButton", background=BOTON, padding=(9, 5))
    estilo.map("TButton", background=[("disabled", PANEL), ("pressed", SELECCION), ("active", "#512b68")],
               foreground=[("disabled", "#9d8da8"), ("!disabled", TEXTO)],
               bordercolor=[("focus", NEON), ("active", NEON)])
    estilo.configure("Principal.TButton", background=NEON, foreground=FONDO)
    estilo.map("Principal.TButton", background=[("pressed", "#bc65df"), ("active", "#ebb2ff")],
               foreground=[("!disabled", FONDO)])
    estilo.configure("TEntry", fieldbackground=CAMPO, insertcolor=NEON, padding=4)
    estilo.map("TEntry", fieldbackground=[("readonly", PANEL), ("!disabled", CAMPO)],
               bordercolor=[("focus", NEON)], foreground=[("readonly", SUAVE)])
    estilo.configure("TCheckbutton", indicatorbackground=CAMPO, indicatorforeground=TEXTO)
    estilo.map("TCheckbutton", background=[("active", PANEL)],
               indicatorbackground=[("selected", SELECCION), ("!selected", CAMPO)])
    estilo.configure("TNotebook.Tab", background=PANEL, padding=(10, 6))
    estilo.map("TNotebook.Tab", background=[("selected", SELECCION), ("active", BOTON)],
               foreground=[("selected", TEXTO), ("!selected", SUAVE)])
    estilo.configure("Treeview", background=CAMPO, fieldbackground=CAMPO, foreground=TEXTO)
    estilo.map("Treeview", background=[("selected", SELECCION)], foreground=[("selected", TEXTO)])
    estilo.configure("Treeview.Heading", background=BOTON, foreground=NEON)
    estilo.map("Treeview.Heading", background=[("active", SELECCION)], foreground=[("active", TEXTO)])
    estilo.configure("Vertical.TScrollbar", troughcolor=CAMPO, background=BOTON, arrowcolor=NEON)
    estilo.map("Vertical.TScrollbar", background=[("active", SELECCION), ("pressed", SELECCION)])
    # Los campos de texto y las listas pertenecen a Tk y usan su propia paleta.
    for clase in ("Text", "Listbox"):
        for opcion, valor in {"background": CAMPO, "foreground": TEXTO, "selectBackground": SELECCION,
                              "selectForeground": TEXTO, "highlightBackground": BORDE,
                              "highlightColor": NEON, "highlightThickness": 1, "borderWidth": 0}.items():
            raiz.option_add(f"*{clase}.{opcion}", valor)
    raiz.option_add("*Text.insertBackground", NEON)
    raiz.option_add("*Text.inactiveSelectBackground", BOTON)


def aviso(titulo, mensaje, *, parent, confirmar=False):
    """Comparte el tema en los avisos y conserva la confirmación antes de borrar."""
    ventana = tk.Toplevel(parent)
    ventana.withdraw()
    ventana.title(titulo)
    ventana.transient(parent.winfo_toplevel())
    ventana.configure(bg=FONDO)
    panel = ttk.Frame(ventana, padding=20)
    panel.pack(fill="both", expand=True)
    ttk.Label(panel, text=titulo, foreground=NEON, font=("Segoe UI", 12, "bold")).pack(anchor="w")
    ttk.Label(panel, text=mensaje, wraplength=440, justify="left").pack(anchor="w", pady=(8, 16))
    botones = ttk.Frame(panel)
    botones.pack(anchor="e")
    respuesta = False

    def cerrar(aceptar=False):
        nonlocal respuesta
        respuesta = aceptar
        ventana.destroy()

    if confirmar:
        inicial = ttk.Button(botones, text="Cancelar", command=cerrar)
        inicial.pack(side="left", padx=6)
    aceptar = ttk.Button(botones, text="Confirmar" if confirmar else "Aceptar",
                         command=lambda: cerrar(True), style="Principal.TButton")
    aceptar.pack(side="left")
    foco = inicial if confirmar else aceptar
    ventana.protocol("WM_DELETE_WINDOW", cerrar)
    ventana.bind("<Escape>", lambda _: cerrar())
    ventana.bind("<Return>", lambda _: ventana.focus_get().invoke()
                 if isinstance(ventana.focus_get(), ttk.Button) else cerrar())
    ventana.update_idletasks()
    padre = parent.winfo_toplevel()
    x = padre.winfo_rootx() + (padre.winfo_width() - ventana.winfo_reqwidth()) // 2
    y = padre.winfo_rooty() + (padre.winfo_height() - ventana.winfo_reqheight()) // 2
    ventana.geometry(f"+{max(0, x)}+{max(0, y)}")
    ventana.deiconify()
    ventana.wait_visibility()
    ventana.grab_set()
    foco.focus_set()
    parent.wait_window(ventana)
    return respuesta
