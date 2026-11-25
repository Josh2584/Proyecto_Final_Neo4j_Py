"""Operaciones del administrador del blog. Cada cambio se confirma completo."""
import re

from cuentas import autenticar, comprobar, crear_cuentas
from consultas import PORTADA, ELIMINAR_ARTICULO, LIMPIAR_ARTICULO, LISTADOS, PUBLICACION
from modelo import CARPETA, TIPOS


def texto(valor, campo, limite, minimo=1):
    valor = valor.strip()
    if not minimo <= len(valor) <= limite:
        raise ValueError(f"{campo} debe tener entre {minimo} y {limite} caracteres.")
    return valor


def ids(valor):
    """Admite una lista vacía cuando el artículo todavía no tiene clasificación."""
    if not valor.strip():
        return []
    partes = [p.strip() for p in valor.split(",")]
    if any(not re.fullmatch(r"[1-9][0-9]{0,17}", p) for p in partes):
        raise ValueError("Escribe IDs positivos separados por comas.")
    numeros = list(map(int, partes))
    if len(numeros) != len(set(numeros)):
        raise ValueError("Cada ID debe aparecer una sola vez.")
    return numeros


def id_unico(valor):
    resultado = ids(valor)
    if len(resultado) != 1:
        raise ValueError("Selecciona un solo ID de usuario o artículo.")
    return resultado[0]


def validar(tipo, datos):
    if tipo == "Usuario":
        correo = texto(datos["correo"], "Correo", 254).lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", correo):
            raise ValueError("Revisa el correo electrónico.")
        return {"nombre": texto(datos["nombre"], "Nombre", 100), "correo": correo}
    if tipo in ("Categoria", "Etiqueta"):
        limite = 80 if tipo == "Categoria" else 60
        slug = texto(datos["slug"], "Enlace corto", limite).lower()
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
            raise ValueError("El enlace corto admite letras sin acentos, números y guiones.")
        return {"nombre": texto(datos["nombre"], "Nombre", limite), "slug": slug}
    if tipo == "Articulo":
        return {"titulo": texto(datos["titulo"], "Título", 180),
                "cuerpo": texto(datos["cuerpo"], "Contenido", 10000)}
    return {"cuerpo": texto(datos["cuerpo"], "Comentario", 1000, 3)}


def bloquear(tx):
    # Serializa los cambios del blog para asignar IDs y reemplazar relaciones.
    tx.run("""MERGE (b:ControlBlog {nombre: 'blog'})
              SET b.revision = coalesce(b.revision, 0) + 1""").consume()


def enlazar(tx, consulta, **params):
    if tx.run(consulta + " RETURN count(*) AS total", **params).single()["total"] != 1:
        raise ValueError("El ID relacionado no existe. Revisa el usuario, artículo o clasificación.")


class BlogService:
    def __init__(self, driver, base):
        self.driver = driver
        self.base = base
        self.identidad = None

    def preparar(self):
        """Instala las restricciones antes del primer alta o carga de datos."""
        esquema, _ = self._script_blog()
        with self.driver.session(database=self.base) as sesion:
            for orden in re.split(r";[ \t]*(?:\n|$)", esquema):
                if orden.strip():
                    sesion.run(orden).consume()

            def iniciar(tx):
                bloquear(tx)
                crear_cuentas(tx, 30)  # Los usuarios de ejemplo ocupan los IDs del 1 al 30.
            sesion.execute_write(iniciar)

    def entrar(self, login, clave):
        self.salir()
        with self.driver.session(database=self.base) as s:
            self.identidad = s.execute_read(autenticar, login.strip().lower(), clave)
        return self.identidad

    def salir(self):
        self.identidad = None

    def _operar(self, roles, escritura, operacion, *args):
        def ejecutar(tx):
            if escritura:
                bloquear(tx)
            usuario = comprobar(tx, self.identidad, roles)
            return operacion(tx, usuario, *args)
        with self.driver.session(database=self.base) as s:
            ejecutar_tx = s.execute_write if escritura else s.execute_read
            return ejecutar_tx(ejecutar)

    def listar(self, tipo):
        return self._operar(("administrador",), False,
                            lambda tx, _: tx.run(LISTADOS[tipo]).data())

    @staticmethod
    def _script_blog():
        """Query ejecuta todo el archivo. La aplicación carga los ejemplos a petición."""
        script = (CARPETA / "Blog_con_roles.cypher").read_text(encoding="utf-8-sig")
        esquema, resto = script.split("// [Ejemplos]\n", 1)
        ejemplos, _ = resto.split("// [Resumen]\n", 1)
        return esquema, ejemplos.strip().removesuffix(";")

    def cargar_ejemplos(self):
        _, ejemplos = self._script_blog()

        def cargar(tx, _):
            if tx.run(ejemplos).single() is None:
                raise ValueError("La carga inicial requiere un blog vacío. Ya hay registros.")

        self._operar(("administrador",), True, cargar)

    def portada(self):
        return self._operar(("lector", "escritor", "administrador"), False,
                            lambda tx, _: tx.run(PORTADA).data())

    def publicar(self, titulo, cuerpo):
        def crear(tx, usuario):
            datos = dict(titulo=titulo, cuerpo=cuerpo, autor=str(usuario), publicar=True,
                         categorias="", etiquetas="")
            return self._guardar(tx, "Articulo", None, validar("Articulo", datos), datos)
        return self._operar(("escritor", "administrador"), True, crear)

    def comentar(self, articulo, cuerpo):
        def crear(tx, usuario):
            fila = tx.run("MATCH (a:Articulo {id:$id}) WHERE a.publicado IS NOT NULL RETURN a.id",
                          id=articulo).single()
            if not fila:
                raise ValueError("La publicación ya no está disponible.")
            datos = dict(articulo=str(articulo), autor=str(usuario), cuerpo=cuerpo)
            return self._guardar(tx, "Comentario", None, validar("Comentario", datos), datos)
        return self._operar(("lector", "escritor", "administrador"), True, crear)

    def cambiar_bloqueo(self, ident, bloqueado):
        def cambiar(tx, usuario):
            if ident == usuario:
                raise ValueError("Tu cuenta de administración debe permanecer activa.")
            fila = tx.run("""MATCH (u:Usuario {id:$id})
                             SET u.bloqueado = $estado, u.version = coalesce(u.version, 0) + 1
                             RETURN u.id""", id=ident, estado=bloqueado).single()
            if not fila:
                raise ValueError("El usuario ya no existe.")
        self._operar(("administrador",), True, cambiar)

    def guardar(self, tipo, ident, datos):
        if tipo not in TIPOS:
            raise ValueError("Tipo de registro desconocido.")
        propiedades = validar(tipo, datos)
        return self._operar(("administrador",), True,
                            lambda tx, _: self._guardar(tx, tipo, ident, propiedades, datos))

    @staticmethod
    def _guardar(tx, tipo, ident, propiedades, datos):
        nuevo = ident is None
        if nuevo:
            ident = tx.run(f"""MATCH (b:ControlBlog {{nombre:'blog'}})
                               SET b.{tipo} = coalesce(b.{tipo}, 0) + 1
                               RETURN b.{tipo} AS id""").single()["id"]
            tx.run(f"CREATE (n:{tipo} {{id: $id}})", id=ident).consume()
            if tipo in ("Usuario", "Articulo", "Comentario"):
                tx.run(f"MATCH (n:{tipo} {{id: $id}}) SET n.creado = datetime()", id=ident).consume()
        fila = tx.run(f"MATCH (n:{tipo} {{id: $id}}) SET n += $props RETURN n.id",
                      id=ident, props=propiedades).single()
        if fila is None:
            raise ValueError("El registro ya no existe.")
        if tipo == "Articulo":
            BlogService._relaciones_articulo(tx, ident, datos)
        elif tipo == "Comentario" and nuevo:
            enlazar(tx, """MATCH (u:Usuario {id: $autor}), (a:Articulo {id: $articulo}),
                                 (c:Comentario {id: $id})
                           CREATE (u)-[:COMENTO]->(c)-[:SOBRE]->(a)""",
                    id=ident, autor=id_unico(datos["autor"]), articulo=id_unico(datos["articulo"]))
        return ident

    @staticmethod
    def _relaciones_articulo(tx, ident, datos):
        tx.run(LIMPIAR_ARTICULO, id=ident).consume()
        enlazar(tx, """MATCH (u:Usuario {id: $autor}), (a:Articulo {id: $id})
                       CREATE (u)-[:ESCRIBIO]->(a)""", id=ident, autor=id_unico(datos["autor"]))
        for campo, tipo, relacion in (("categorias", "Categoria", "EN_CATEGORIA"),
                                      ("etiquetas", "Etiqueta", "TIENE_ETIQUETA")):
            for destino in ids(datos[campo]):
                enlazar(tx, f"""MATCH (a:Articulo {{id: $id}}), (d:{tipo} {{id: $destino}})
                                CREATE (a)-[:{relacion}]->(d)""", id=ident, destino=destino)
        tx.run(PUBLICACION, id=ident, publicar=datos["publicar"]).consume()

    def eliminar(self, tipo, ident):
        if tipo not in TIPOS:
            raise ValueError("Tipo de registro desconocido.")
        self._operar(("administrador",), True, lambda tx, _: self._eliminar(tx, tipo, ident))

    @staticmethod
    def _eliminar(tx, tipo, ident):
        registro = tx.run(f"MATCH (n:{tipo} {{id: $id}}) RETURN EXISTS {{ (n)--() }} AS vinculado, n:CuentaBlog AS cuenta",
                          id=ident).single()
        if registro is None:
            raise ValueError("El registro ya no existe.")
        if registro["cuenta"]:
            raise ValueError("Para suspender una cuenta de acceso utiliza Bloquear.")
        if tipo == "Usuario" and registro["vinculado"]:
            raise ValueError("Este usuario tiene artículos o comentarios en el blog.")
        orden = ELIMINAR_ARTICULO if tipo == "Articulo" else f"MATCH (n:{tipo} {{id:$id}}) DETACH DELETE n"
        tx.run(orden, id=ident).consume()
