"""Ventana de escritorio para editar el blog y cargar los ejemplos de Oracle."""
import os
import tkinter as tk
from tkinter import ttk

from tema import aplicar, aviso, PANEL, NEON, TEXTO

from neo4j.exceptions import AuthError, ConstraintError, DriverError, Neo4jError

from modelo import BASE, URI, USUARIO, conectar
from servicio import BlogService
from cuentas import SesionCaducada
from portada import Portada, Redaccion


PESTANAS = {
    "Usuario": ("Usuarios", ("nombre", "correo")),
    "Categoria": ("Categorías", ("nombre", "slug")),
    "Etiqueta": ("Etiquetas", ("nombre", "slug")),
    "Articulo": ("Artículos", ("titulo", "autor", "categorias", "etiquetas", "cuerpo", "publicar")),
    "Comentario": ("Comentarios", ("articulo", "autor", "cuerpo")),
}
CAMPOS = {
    "estado": "Estado", "nombre": "Nombre", "correo": "Correo", "slug": "Enlace corto",
    "titulo": "Título", "autor": "Usuario (ID)", "articulo": "Artículo (ID)",
    "categorias": "Categorías (IDs separados por comas)",
    "etiquetas": "Etiquetas (IDs separados por comas)",
    "cuerpo": "Texto", "publicar": "Publicado", "id": "ID", "fecha": "Fecha",
}


class Editor(ttk.Frame):
    """La tabla y el formulario comparten el ID del registro seleccionado."""

    def __init__(self, padre, app, tipo):
        super().__init__(padre, padding=12)
        self.app = app
        self.tipo = tipo
        self.campos = PESTANAS[tipo][1]
        self.entradas = {}
        self.filas = {}
        self.ident = None
        form = ttk.Frame(self)
        form.pack(fill="x")
        form.columnconfigure(1, weight=1)
        for i, campo in enumerate(self.campos):
            ttk.Label(form, text=CAMPOS[campo]).grid(row=i, column=0, sticky="nw", padx=(0, 10), pady=3)
            if campo == "cuerpo":
                widget = tk.Text(form, height=4, wrap="word", font="TkTextFont")
            elif campo == "publicar":
                self.publicar = tk.BooleanVar()
                widget = ttk.Checkbutton(form, variable=self.publicar)
            else:
                widget = ttk.Entry(form)
            widget.grid(row=i, column=1, sticky="ew", pady=2)
            self.entradas[campo] = widget
        acciones = ttk.Frame(self)
        acciones.pack(fill="x", pady=8)
        for nombre, accion in (("Nuevo", self.limpiar), ("Guardar", self.guardar), ("Eliminar", self.eliminar)):
            ttk.Button(acciones, text=nombre, command=accion).pack(side="left", padx=(0, 6))

        columnas = ["id", *self.campos]
        if tipo == "Usuario":
            columnas.append("estado")
            for nombre, estado in (("Bloquear", True), ("Desbloquear", False)):
                ttk.Button(acciones, text=nombre, command=lambda b=estado: self.bloquear(b)).pack(side="left", padx=3)
        if tipo == "Articulo":
            columnas = ["id", "titulo", "autor", "categorias", "fecha"]
        elif tipo == "Comentario":
            columnas.append("fecha")
        panel = ttk.Frame(self)
        panel.pack(fill="both", expand=True)
        self.tabla = ttk.Treeview(panel, columns=columnas, show="headings", selectmode="browse")
        for col in columnas:
            titulo = {"autor": "Usuario", "articulo": "Artículo", "categorias": "Categorías"}.get(col, CAMPOS[col])
            self.tabla.heading(col, text=titulo)
            self.tabla.column(col, width=52 if col == "id" else 155, stretch=col != "id")
        barra = ttk.Scrollbar(panel, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar(self, filas, nombres):
        self.limpiar()
        self.tabla.delete(*self.tabla.get_children())
        self.filas = {str(f["id"]): f for f in filas}
        for clave, fila in self.filas.items():
            vista = dict(fila)
            if "bloqueado" in fila:
                vista["estado"] = "Bloqueado" if fila["bloqueado"] else "Activo"
            for campo, tipo in (("autor", "Usuario"), ("articulo", "Articulo")):
                if campo in fila:
                    vista[campo] = nombres[tipo].get(fila[campo], fila[campo])
            if "categorias" in fila:
                vista["categorias"] = ", ".join(nombres["Categoria"][i] for i in sorted(fila["categorias"]))
            if "fecha" in fila:
                vista["fecha"] = str(fila["fecha"])[:16].replace("T", " ") if fila["fecha"] else "Borrador"
            self.tabla.insert("", "end", iid=clave, values=[vista[c] for c in self.tabla["columns"]])

    def rellenar(self, fila):
        for campo, widget in self.entradas.items():
            valor = fila.get(campo, "")
            if campo == "cuerpo":
                widget.delete("1.0", "end")
                widget.insert("1.0", valor)
            elif campo == "publicar":
                self.publicar.set(bool(valor))
            else:
                widget.configure(state="normal")
                widget.delete(0, "end")
                if isinstance(valor, list):
                    valor = ", ".join(map(str, sorted(valor)))
                widget.insert(0, valor)
                # Un comentario conserva el autor y el artículo al que respondía.
                if fila and self.tipo == "Comentario" and campo in ("autor", "articulo"):
                    widget.configure(state="readonly")

    def seleccionar(self, _evento=None):
        elegidos = self.tabla.selection()
        if elegidos:
            fila = self.filas[elegidos[0]]
            self.ident = fila["id"]
            self.rellenar(fila)

    def limpiar(self):
        self.ident = None
        self.tabla.selection_remove(*self.tabla.selection())
        self.rellenar({})

    def guardar(self):
        datos = {}
        for campo, widget in self.entradas.items():
            if campo == "cuerpo":
                datos[campo] = widget.get("1.0", "end-1c")
            elif campo == "publicar":
                datos[campo] = self.publicar.get()
            else:
                datos[campo] = widget.get()
        ident = self.app.servicio.guardar(self.tipo, self.ident, datos)
        self.app.actualizar(f"Registro {ident} guardado.")

    def bloquear(self, estado):
        if self.ident is None:
            raise ValueError("Selecciona un usuario de la tabla.")
        accion = "bloquear" if estado else "desbloquear"
        if aviso("Moderar usuario", f"¿Quieres {accion} a {self.filas[str(self.ident)]['nombre']}?", parent=self, confirmar=True):
            self.app.servicio.cambiar_bloqueo(self.ident, estado)
            self.app.actualizar("Estado de usuario actualizado.")

    def eliminar(self):
        if self.ident is None:
            aviso("Eliminar", "Selecciona un registro de la tabla.", parent=self)
            return
        mensaje = f"¿Eliminar el registro {self.ident}?"
        if self.tipo == "Articulo":
            mensaje += " También se eliminarán sus comentarios."
        if aviso("Eliminar", mensaje, parent=self, confirmar=True):
            self.app.servicio.eliminar(self.tipo, self.ident)
            self.app.actualizar("Registro eliminado.")


class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        aplicar(self)
        self.title("El cuaderno · Blog")
        self.geometry("1000x720")
        self.servicio = None
        self.estado = tk.StringVar()
        self.config = {k: tk.StringVar(value=v) for k, v in (
            ("URI", URI), ("Base", BASE), ("Usuario Neo4j", USUARIO),
            ("Contraseña Neo4j", os.getenv("NEO4J_PASSWORD", "")))}
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.inicio()

    def pagina(self):
        for widget in self.winfo_children():
            widget.destroy()

    def inicio(self):
        self.pagina()
        tarjeta = tk.Frame(self, bg=PANEL, highlightbackground=NEON, highlightthickness=1, padx=42, pady=28)
        tarjeta.place(relx=.5, rely=.5, anchor="center")
        tk.Label(tarjeta, text="El cuaderno", font=("Georgia", 26), fg=NEON,
                 bg=PANEL).pack(anchor="w")
        tk.Label(tarjeta, text="Iniciar sesión", font=("Segoe UI", 13), fg=TEXTO,
                 bg=PANEL).pack(anchor="w", pady=(6, 16))
        self.login = tk.StringVar()
        self.clave = tk.StringVar()
        for campo, var in (("Usuario", self.login), ("Contraseña", self.clave)):
            tk.Label(tarjeta, text=campo, fg=TEXTO, bg=PANEL).pack(anchor="w")
            entrada = ttk.Entry(tarjeta, textvariable=var, width=38,
                                show="*" if var is self.clave else "")
            entrada.pack(fill="x", pady=(2, 10))
            entrada.bind("<Return>", lambda _: self.entrar())
            if var is self.login:
                entrada.focus_set()
        ttk.Button(tarjeta, text="Entrar", command=self.entrar, style="Principal.TButton").pack(fill="x")
        if self.servicio is None:
            opciones = ttk.Frame(tarjeta, padding=8)
            def alternar():
                if opciones.winfo_manager():
                    opciones.pack_forget()
                else:
                    opciones.pack(fill="x")
            ttk.Button(tarjeta, text="Configurar conexión Neo4j", command=alternar).pack(pady=(10, 0))
            for i, (campo, var) in enumerate(self.config.items()):
                ttk.Label(opciones, text=campo).grid(row=i, column=0, sticky="w", pady=2)
                ttk.Entry(opciones, textvariable=var, show="*" if campo.startswith("Contraseña") else ""
                          ).grid(row=i, column=1)

    def entrar(self):
        if not self.login.get().strip() or not self.clave.get():
            raise ValueError("Escribe tu usuario y contraseña del blog.")
        if self.servicio is None:
            valores = {k: v.get() for k, v in self.config.items()}
            if not valores["Contraseña Neo4j"]:
                raise ValueError("Abre Configurar conexión Neo4j e introduce la contraseña de tu instancia.")
            driver = conectar(valores["URI"].strip(), valores["Usuario Neo4j"].strip(), valores["Contraseña Neo4j"])
            servicio = BlogService(driver, valores["Base"].strip())
            try:
                servicio.preparar()
                servicio.entrar(self.login.get(), self.clave.get())
            except Exception:
                driver.close()
                raise
            self.servicio = servicio
            self.config["Contraseña Neo4j"].set("")
        else:
            self.servicio.entrar(self.login.get(), self.clave.get())
        self.clave.set("")
        self.panel()

    def panel(self):
        self.pagina()
        cuenta = self.servicio.identidad
        barra = ttk.Frame(self, padding=12)
        barra.pack(fill="x")
        ttk.Label(barra, text="El cuaderno", foreground=NEON, font=("Georgia", 20)).pack(side="left")
        ttk.Label(barra, text=f"{cuenta.usuario} · {cuenta.rol}").pack(side="left", padx=18)
        ttk.Button(barra, text="Cerrar sesión", command=self.salir).pack(side="right")
        ttk.Button(barra, text="Actualizar", command=self.actualizar).pack(side="right", padx=6)
        self.libro = ttk.Notebook(self)
        self.libro.pack(fill="both", expand=True, padx=12, pady=6)
        self.portada = Portada(self.libro, self)
        self.libro.add(self.portada, text="Leer y comentar")
        if cuenta.rol in ("administrador", "escritor"):
            self.libro.add(Redaccion(self.libro, self), text="Publicar")
        self.editores = {}
        if cuenta.rol == "administrador":
            ttk.Button(barra, text="Cargar ejemplos", command=self.ejemplos).pack(side="right")
            for tipo, (titulo, _) in PESTANAS.items():
                editor = Editor(self.libro, self, tipo)
                self.libro.add(editor, text=titulo)
                self.editores[tipo] = editor
        ttk.Label(self, textvariable=self.estado, padding=(12, 6)).pack(anchor="w")
        self.actualizar()

    def salir(self):
        self.servicio.salir()
        self.inicio()

    def ejemplos(self):
        self.servicio.cargar_ejemplos()
        self.actualizar("Ejemplos cargados.")

    def actualizar(self, mensaje=""):
        self.portada.cargar()
        if self.editores:
            datos = {tipo: self.servicio.listar(tipo) for tipo in PESTANAS}
            nombres = {tipo: {f["id"]: f[campo] for f in datos[tipo]}
                       for tipo, campo in (("Usuario", "nombre"), ("Articulo", "titulo"), ("Categoria", "nombre"))}
            for tipo, editor in self.editores.items():
                editor.cargar(datos[tipo], nombres)
        self.estado.set(mensaje)

    def report_callback_exception(self, tipo, error, traza):
        """Traduce los errores habituales que llegan desde los botones de Tk."""
        if isinstance(error, SesionCaducada):
            self.salir()
            detalle = str(error)
        elif isinstance(error, PermissionError):
            detalle = str(error)
        elif isinstance(error, AuthError):
            detalle = "Revisa el usuario y la contraseña de la instancia."
        elif isinstance(error, ConstraintError):
            detalle = "Ya existe un registro con ese correo, nombre, enlace o ID."
        elif isinstance(error, (DriverError, Neo4jError, OSError)):
            detalle = f"Revisa la instancia, URI, base y permisos. {error}"
        elif isinstance(error, ValueError):
            detalle = str(error)
        else:
            return super().report_callback_exception(tipo, error, traza)
        aviso("Blog · Neo4j", detalle, parent=self)

    def cerrar(self):
        if self.servicio:
            self.servicio.driver.close()
        self.destroy()


def main():
    Ventana().mainloop()
