"""Cuentas de prueba y comprobación de sesiones del blog."""
import hashlib
import hmac
import secrets
from dataclasses import dataclass


class SesionCaducada(PermissionError):
    """El usuario debe identificarse de nuevo."""


@dataclass(frozen=True)
class Sesion:
    usuario: str
    rol: str
    version: int


def huella(clave, sal):
    return hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal), 600_000).hex()


def crear_cuentas(tx, ultimo_ejemplo):
    """Reserva los IDs del SQL para permitir cargar los ejemplos después del primer acceso."""
    tx.run("""MATCH (b:ControlBlog {nombre:'blog'})
              OPTIONAL MATCH (u:Usuario)
              WITH b, coalesce(max(u.id), 0) AS ultimo
              SET b.Usuario = reduce(m = $reserva, n IN [ultimo, coalesce(b.Usuario, 0)] |
                                     CASE WHEN n > m THEN n ELSE m END)""", reserva=ultimo_ejemplo).consume()
    for login, rol in (("admin", "administrador"), ("escritor", "escritor"), ("lector", "lector")):
        if tx.run("MATCH (u:CuentaBlog {login:$login}) RETURN u.id", login=login).single():
            continue
        sal = secrets.token_hex(16)
        tx.run("""MATCH (b:ControlBlog {nombre:'blog'})
                  SET b.Usuario = b.Usuario + 1
                  CREATE (:CuentaBlog:Usuario {id:b.Usuario, login:$login, rol:$rol,
                    nombre:$login, creado:datetime(), correo:$correo, sal:$sal,
                    huella:$huella, bloqueado:false, version:0})""",
               login=login, rol=rol, correo=f"{login}@demo.blog.local", sal=sal,
               huella=huella(login + "123", sal)).consume()


def autenticar(tx, login, clave):
    fila = tx.run("""MATCH (u:CuentaBlog {login:$login})
                     RETURN u.sal AS sal, u.huella AS huella, u.rol AS rol,
                            u.version AS version, u.bloqueado AS bloqueado""", login=login).single()
    if not fila or not hmac.compare_digest(huella(clave, fila["sal"]), fila["huella"]):
        raise ValueError("Usuario o contraseña incorrectos.")
    if fila["bloqueado"]:
        raise ValueError("Esta cuenta está bloqueada.")
    return Sesion(login, fila["rol"], fila["version"])


def comprobar(tx, sesion, roles):
    if sesion is None:
        raise SesionCaducada("Inicia sesión para continuar.")
    fila = tx.run("""MATCH (u:CuentaBlog {login:$login, version:$version, bloqueado:false})
                     RETURN u.id AS id, u.rol AS rol""",
                  login=sesion.usuario, version=sesion.version).single()
    if not fila:
        raise SesionCaducada("La sesión dejó de estar activa. Vuelve a identificarte.")
    if fila["rol"] not in roles:
        raise PermissionError("Tu cuenta no tiene permiso para esa acción.")
    return fila["id"]
