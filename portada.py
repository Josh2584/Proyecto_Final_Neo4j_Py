"""Lectura de publicaciones y conversación desde la cuenta conectada."""
import tkinter as tk
from tkinter import ttk

from tema import NEON


class Portada(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, padding=14)
        self.app = app
        self.articulos = []
        self.elegido = None
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)
        ttk.Label(self, text="Publicaciones", foreground=NEON, font=("Georgia", 16)).grid(sticky="w")
        self.titulo = ttk.Label(self, font=("Georgia", 16), wraplength=560)
        self.titulo.grid(row=0, column=1, sticky="w", padx=14)
        self.lista = tk.Listbox(self, exportselection=False, activestyle="none",
                                font=("Segoe UI", 11), width=28)
        self.lista.grid(row=1, column=0, rowspan=3, sticky="nsew", pady=8)
        self.lista.bind("<<ListboxSelect>>", self.leer)
        self.lectura = tk.Text(self, wrap="word", padx=14, pady=12, relief="flat",
                               font=("Georgia", 12), width=44, height=12)
        self.lectura.tag_configure("firma", foreground=NEON, font=("Segoe UI", 10, "bold"))
        self.lectura.grid(row=1, column=1, sticky="nsew", padx=(14, 0), pady=8)
        barra = ttk.Scrollbar(self, command=self.lectura.yview)
        barra.grid(row=1, column=2, sticky="ns", pady=8)
        self.lectura.configure(yscrollcommand=barra.set)
        self.respuesta = tk.Text(self, height=3, width=35, wrap="word", font="TkTextFont")
        self.respuesta.grid(row=2, column=1, sticky="ew", padx=(14, 0))
        self.boton = ttk.Button(self, text="Enviar comentario", command=self.comentar)
        self.boton.grid(row=3, column=1, sticky="e", pady=6)

    def cargar(self):
        self.articulos = self.app.servicio.portada()
        self.lista.delete(0, "end")
        indice = 0
        for i, fila in enumerate(self.articulos):
            self.lista.insert("end", fila["titulo"])
            if fila["id"] == self.elegido:
                indice = i
        if self.articulos:
            self.lista.selection_set(indice)
            self.lista.see(indice)
        self.leer()

    def leer(self, evento=None):
        pos = self.lista.curselection()
        fila = self.articulos[pos[0]] if pos else None
        ident = fila["id"] if fila else None
        if self.elegido != ident:
            self.respuesta.delete("1.0", "end")
        self.elegido = ident
        self.titulo.configure(text=fila["titulo"] if fila else "Aún no hay publicaciones")
        self.boton.configure(state="normal" if fila else "disabled")
        self.lectura.configure(state="normal")
        self.lectura.delete("1.0", "end")
        if fila:
            self.lectura.insert("end", fila["autor"] + "\n\n", "firma")
            self.lectura.insert("end", fila["cuerpo"] + "\n\n")
            self.lectura.insert("end", "Comentarios\n", "firma")
            for c in fila["comentarios"]:
                self.lectura.insert("end", "\n" + c["autor"] + "\n", "firma")
                self.lectura.insert("end", c["cuerpo"] + "\n")
        self.lectura.configure(state="disabled")

    def comentar(self):
        self.app.servicio.comentar(self.elegido, self.respuesta.get("1.0", "end-1c"))
        self.respuesta.delete("1.0", "end")
        self.app.actualizar("Comentario publicado.")


class Redaccion(ttk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, padding=20)
        self.app = app
        ttk.Label(self, text="Nueva publicación", foreground=NEON, font=("Georgia", 18)).pack(anchor="w")
        ttk.Label(self, text="Título").pack(anchor="w", pady=(16, 2))
        self.titulo = ttk.Entry(self)
        self.titulo.pack(fill="x")
        ttk.Label(self, text="Contenido").pack(anchor="w", pady=(12, 2))
        self.cuerpo = tk.Text(self, wrap="word", height=8, font=("Georgia", 12))
        self.cuerpo.pack(fill="both", expand=True)
        ttk.Button(self, text="Publicar", command=self.publicar).pack(anchor="e", pady=8)

    def publicar(self):
        ident = self.app.servicio.publicar(self.titulo.get(), self.cuerpo.get("1.0", "end-1c"))
        self.titulo.delete(0, "end")
        self.cuerpo.delete("1.0", "end")
        self.app.portada.elegido = ident
        self.app.actualizar("Artículo publicado.")
        self.app.libro.select(self.app.portada)
