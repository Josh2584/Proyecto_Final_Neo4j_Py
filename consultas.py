"""Consultas Cypher para cargar los formularios y las relaciones del blog."""

LISTADOS = {
    "Usuario": "MATCH (n:Usuario) RETURN n.id AS id, n.nombre AS nombre, n.correo AS correo, coalesce(n.bloqueado,false) AS bloqueado ORDER BY id",
    "Categoria": "MATCH (n:Categoria) RETURN n.id AS id, n.nombre AS nombre, n.slug AS slug ORDER BY id",
    "Etiqueta": "MATCH (n:Etiqueta) RETURN n.id AS id, n.nombre AS nombre, n.slug AS slug ORDER BY id",
    "Articulo": """
        MATCH (u:Usuario)-[:ESCRIBIO]->(a:Articulo)
        RETURN a.id AS id, a.titulo AS titulo, a.cuerpo AS cuerpo, u.id AS autor,
               [(a)-[:EN_CATEGORIA]->(c:Categoria) | c.id] AS categorias,
               [(a)-[:TIENE_ETIQUETA]->(e:Etiqueta) | e.id] AS etiquetas,
               a.publicado IS NOT NULL AS publicar, a.publicado AS fecha
        ORDER BY id DESC
    """,
    "Comentario": """
        MATCH (u:Usuario)-[:COMENTO]->(c:Comentario)-[:SOBRE]->(a:Articulo)
        RETURN c.id AS id, a.id AS articulo, u.id AS autor, c.cuerpo AS cuerpo,
               c.creado AS fecha ORDER BY id DESC
    """,
}

# Al editar se reemplazan las asociaciones del artículo en la misma transacción.
LIMPIAR_ARTICULO = """
    MATCH (a:Articulo {id: $id})-[r:ESCRIBIO|EN_CATEGORIA|TIENE_ETIQUETA]-()
    DELETE r
"""
PUBLICACION = """
    MATCH (a:Articulo {id: $id})
    SET a.actualizado = datetime(),
        a.publicado = CASE WHEN $publicar THEN coalesce(a.publicado, datetime()) END
"""
ELIMINAR_ARTICULO = """
    MATCH (a:Articulo {id: $id})
    OPTIONAL MATCH (c:Comentario)-[:SOBRE]->(a)
    WITH a, collect(c) AS comentarios
    FOREACH (c IN comentarios | DETACH DELETE c)
    DETACH DELETE a
"""

# Sólo se muestran artículos publicados y los comentarios de cada conversación.
PORTADA = """
    MATCH (autor:Usuario)-[:ESCRIBIO]->(a:Articulo)
    WHERE a.publicado IS NOT NULL
    OPTIONAL MATCH (lector:Usuario)-[:COMENTO]->(c:Comentario)-[:SOBRE]->(a)
    WITH a, autor, lector, c ORDER BY c.creado, c.id
    RETURN a.id AS id, a.publicado AS fecha, a.titulo AS titulo, a.cuerpo AS cuerpo, autor.nombre AS autor,
           collect(c { .cuerpo, autor: lector.nombre }) AS comentarios
    ORDER BY fecha DESC, id DESC
"""

