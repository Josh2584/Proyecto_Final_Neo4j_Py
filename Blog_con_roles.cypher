// Blog con roles. En Neo4j Desktop selecciona tu base neo4j y ejecuta todo el archivo.
// El esquema y las cuentas corresponden a Proyecto_Neo4j_Py_con_roles.
CREATE CONSTRAINT blog_controlblog_nombre IF NOT EXISTS
FOR (n:ControlBlog) REQUIRE n.nombre IS UNIQUE;

CREATE CONSTRAINT blog_usuario_id IF NOT EXISTS
FOR (n:Usuario) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT blog_usuario_correo IF NOT EXISTS
FOR (n:Usuario) REQUIRE n.correo IS UNIQUE;

CREATE CONSTRAINT blog_categoria_id IF NOT EXISTS
FOR (n:Categoria) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT blog_categoria_nombre IF NOT EXISTS
FOR (n:Categoria) REQUIRE n.nombre IS UNIQUE;

CREATE CONSTRAINT blog_categoria_slug IF NOT EXISTS
FOR (n:Categoria) REQUIRE n.slug IS UNIQUE;

CREATE CONSTRAINT blog_etiqueta_id IF NOT EXISTS
FOR (n:Etiqueta) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT blog_etiqueta_nombre IF NOT EXISTS
FOR (n:Etiqueta) REQUIRE n.nombre IS UNIQUE;

CREATE CONSTRAINT blog_etiqueta_slug IF NOT EXISTS
FOR (n:Etiqueta) REQUIRE n.slug IS UNIQUE;

CREATE CONSTRAINT blog_articulo_id IF NOT EXISTS
FOR (n:Articulo) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT blog_comentario_id IF NOT EXISTS
FOR (n:Comentario) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT blog_login IF NOT EXISTS FOR (u:CuentaBlog) REQUIRE u.login IS UNIQUE;

// [Ejemplos]
// Los datos de ejemplo se cargan juntos si el blog está vacío.
// Las cuentas de prueba creadas previamente por la app pueden conservarse.
MERGE (b:ControlBlog {nombre:'blog'})
SET b.revision = coalesce(b.revision,0) + 1
WITH b WHERE NOT EXISTS {
  MATCH (n) WHERE (n:Usuario AND NOT n:CuentaBlog) OR n:Articulo OR n:Comentario OR n:Categoria OR n:Etiqueta
}

// Usuario
CALL {
  UNWIND [
    {id: 1, nombre: "Julio Cortázar", correo: "julio.cortazar@blog.local"},
    {id: 2, nombre: "Søren Kierkegaard", correo: "soren.kierkegaard@blog.local"},
    {id: 3, nombre: "Ursula K. Le Guin", correo: "ursula.leguin@blog.local"},
    {id: 4, nombre: "Jorge Luis Borges", correo: "jorge.borges@blog.local"},
    {id: 5, nombre: "Simone de Beauvoir", correo: "simone.beauvoir@blog.local"},
    {id: 6, nombre: "Clarice Lispector", correo: "clarice.lispector@blog.local"},
    {id: 7, nombre: "Franz Kafka", correo: "franz.kafka@blog.local"},
    {id: 8, nombre: "Virginia Woolf", correo: "virginia.woolf@blog.local"},
    {id: 9, nombre: "Albert Camus", correo: "albert.camus@blog.local"},
    {id: 10, nombre: "Hannah Arendt", correo: "hannah.arendt@blog.local"},
    {id: 11, nombre: "Octavio Paz", correo: "octavio.paz@blog.local"},
    {id: 12, nombre: "Gabriel García Márquez", correo: "gabriel.marquez@blog.local"},
    {id: 13, nombre: "Toni Morrison", correo: "toni.morrison@blog.local"},
    {id: 14, nombre: "Italo Calvino", correo: "italo.calvino@blog.local"},
    {id: 15, nombre: "Mary Shelley", correo: "mary.shelley@blog.local"},
    {id: 16, nombre: "Emily Dickinson", correo: "emily.dickinson@blog.local"},
    {id: 17, nombre: "James Baldwin", correo: "james.baldwin@blog.local"},
    {id: 18, nombre: "George Orwell", correo: "george.orwell@blog.local"},
    {id: 19, nombre: "Isabel Allende", correo: "isabel.allende@blog.local"},
    {id: 20, nombre: "Fernando Pessoa", correo: "fernando.pessoa@blog.local"},
    {id: 21, nombre: "Chinua Achebe", correo: "chinua.achebe@blog.local"},
    {id: 22, nombre: "Marguerite Yourcenar", correo: "marguerite.yourcenar@blog.local"},
    {id: 23, nombre: "José Saramago", correo: "jose.saramago@blog.local"},
    {id: 24, nombre: "Susan Sontag", correo: "susan.sontag@blog.local"},
    {id: 25, nombre: "Wislawa Szymborska", correo: "wislawa.szymborska@blog.local"},
    {id: 26, nombre: "Naguib Mahfouz", correo: "naguib.mahfouz@blog.local"},
    {id: 27, nombre: "Milan Kundera", correo: "milan.kundera@blog.local"},
    {id: 28, nombre: "Zora Neale Hurston", correo: "zora.hurston@blog.local"},
    {id: 29, nombre: "Rainer Maria Rilke", correo: "rainer.rilke@blog.local"},
    {id: 30, nombre: "Umberto Eco", correo: "umberto.eco@blog.local"}
  ] AS f
  CREATE (:Usuario {id: f.id, nombre: f.nombre, correo: f.correo, creado: datetime()})
}

// Categoria
CALL {
  UNWIND [
    {id: 1, nombre: "Literatura", slug: "literatura"},
    {id: 2, nombre: "Filosofía", slug: "filosofia"},
    {id: 3, nombre: "Cuento", slug: "cuento"},
    {id: 4, nombre: "Ensayo", slug: "ensayo"},
    {id: 5, nombre: "Existencialismo", slug: "existencialismo"},
    {id: 6, nombre: "Poesía", slug: "poesia"},
    {id: 7, nombre: "Narrativa", slug: "narrativa"},
    {id: 8, nombre: "Ciencia ficción", slug: "ciencia-ficcion"},
    {id: 9, nombre: "Memoria", slug: "memoria"},
    {id: 10, nombre: "Sociedad", slug: "sociedad"}
  ] AS f
  CREATE (:Categoria {id: f.id, nombre: f.nombre, slug: f.slug})
}

// Etiqueta
CALL {
  UNWIND [
    {id: 1, nombre: "Realismo mágico", slug: "realismo-magico"},
    {id: 2, nombre: "Laberintos", slug: "laberintos"},
    {id: 3, nombre: "Libertad", slug: "libertad"},
    {id: 4, nombre: "Identidad", slug: "identidad"},
    {id: 5, nombre: "Fantasía", slug: "fantasia"},
    {id: 6, nombre: "Tiempo", slug: "tiempo"},
    {id: 7, nombre: "Soledad", slug: "soledad"},
    {id: 8, nombre: "Memoria", slug: "memoria"},
    {id: 9, nombre: "Viaje", slug: "viaje"},
    {id: 10, nombre: "Lenguaje", slug: "lenguaje"},
    {id: 11, nombre: "Ética", slug: "etica"},
    {id: 12, nombre: "Utopía", slug: "utopia"},
    {id: 13, nombre: "Historia", slug: "historia"},
    {id: 14, nombre: "Poesía", slug: "poesia"},
    {id: 15, nombre: "Ciudad", slug: "ciudad"},
    {id: 16, nombre: "Naturaleza", slug: "naturaleza"},
    {id: 17, nombre: "Lectura", slug: "lectura"},
    {id: 18, nombre: "Sueños", slug: "suenos"}
  ] AS f
  CREATE (:Etiqueta {id: f.id, nombre: f.nombre, slug: f.slug})
}

// Articulo
CALL {
  UNWIND [
    {id: 1, autor: 1, titulo: "La ciudad que cambia al ser narrada", cuerpo: "Una ciudad no es solo sus calles: también es la versión que cada caminante recuerda. Al escribirla, el narrador descubre que la esquina de ayer ya pertenece a otro mapa."},
    {id: 2, autor: 2, titulo: "Elegir incluso cuando nadie observa", cuerpo: "La elección cotidiana no necesita testigos para tener peso. La responsabilidad aparece precisamente cuando dejamos de buscar una respuesta cómoda fuera de nosotros."},
    {id: 3, autor: 3, titulo: "Imaginación como herramienta de futuro", cuerpo: "La imaginación no huye del mundo: ensaya maneras distintas de habitarlo. Una historia puede abrir preguntas que un manual todavía no sabe formular."},
    {id: 4, autor: 4, titulo: "El archivo y sus infinitas posibilidades", cuerpo: "Toda biblioteca promete orden, pero cada lector inventa un recorrido. Entre dos estantes puede aparecer una pregunta que transforma el sentido del catálogo entero."},
    {id: 5, autor: 5, titulo: "Escribir desde la propia experiencia", cuerpo: "La experiencia personal no es una habitación cerrada. Cuando se cuenta con honestidad, encuentra hilos que la unen con las preguntas de otras personas."},
    {id: 6, autor: 6, titulo: "Cuaderno de lectura: Clarice Lispector", cuerpo: "Texto original de demostración. Clarice Lispector propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 7, autor: 7, titulo: "Cuaderno de lectura: Franz Kafka", cuerpo: "Texto original de demostración. Franz Kafka propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 8, autor: 8, titulo: "Cuaderno de lectura: Virginia Woolf", cuerpo: "Texto original de demostración. Virginia Woolf propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 9, autor: 9, titulo: "Cuaderno de lectura: Albert Camus", cuerpo: "Texto original de demostración. Albert Camus propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 10, autor: 10, titulo: "Cuaderno de lectura: Hannah Arendt", cuerpo: "Texto original de demostración. Hannah Arendt propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 11, autor: 11, titulo: "Cuaderno de lectura: Octavio Paz", cuerpo: "Texto original de demostración. Octavio Paz propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 12, autor: 12, titulo: "Cuaderno de lectura: Gabriel García Márquez", cuerpo: "Texto original de demostración. Gabriel García Márquez propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 13, autor: 13, titulo: "Cuaderno de lectura: Toni Morrison", cuerpo: "Texto original de demostración. Toni Morrison propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 14, autor: 14, titulo: "Cuaderno de lectura: Italo Calvino", cuerpo: "Texto original de demostración. Italo Calvino propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 15, autor: 15, titulo: "Cuaderno de lectura: Mary Shelley", cuerpo: "Texto original de demostración. Mary Shelley propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 16, autor: 16, titulo: "Cuaderno de lectura: Emily Dickinson", cuerpo: "Texto original de demostración. Emily Dickinson propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 17, autor: 17, titulo: "Cuaderno de lectura: James Baldwin", cuerpo: "Texto original de demostración. James Baldwin propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 18, autor: 18, titulo: "Cuaderno de lectura: George Orwell", cuerpo: "Texto original de demostración. George Orwell propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 19, autor: 19, titulo: "Cuaderno de lectura: Isabel Allende", cuerpo: "Texto original de demostración. Isabel Allende propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 20, autor: 20, titulo: "Cuaderno de lectura: Fernando Pessoa", cuerpo: "Texto original de demostración. Fernando Pessoa propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 21, autor: 21, titulo: "Cuaderno de lectura: Chinua Achebe", cuerpo: "Texto original de demostración. Chinua Achebe propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 22, autor: 22, titulo: "Cuaderno de lectura: Marguerite Yourcenar", cuerpo: "Texto original de demostración. Marguerite Yourcenar propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 23, autor: 23, titulo: "Cuaderno de lectura: José Saramago", cuerpo: "Texto original de demostración. José Saramago propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 24, autor: 24, titulo: "Cuaderno de lectura: Susan Sontag", cuerpo: "Texto original de demostración. Susan Sontag propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 25, autor: 25, titulo: "Cuaderno de lectura: Wislawa Szymborska", cuerpo: "Texto original de demostración. Wislawa Szymborska propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 26, autor: 26, titulo: "Cuaderno de lectura: Naguib Mahfouz", cuerpo: "Texto original de demostración. Naguib Mahfouz propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 27, autor: 27, titulo: "Cuaderno de lectura: Milan Kundera", cuerpo: "Texto original de demostración. Milan Kundera propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 28, autor: 28, titulo: "Cuaderno de lectura: Zora Neale Hurston", cuerpo: "Texto original de demostración. Zora Neale Hurston propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 29, autor: 29, titulo: "Cuaderno de lectura: Rainer Maria Rilke", cuerpo: "Texto original de demostración. Rainer Maria Rilke propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."},
    {id: 30, autor: 30, titulo: "Cuaderno de lectura: Umberto Eco", cuerpo: "Texto original de demostración. Umberto Eco propone una reflexión sobre la lectura, la memoria y la conversación entre ideas."}
  ] AS f
  MATCH (u:Usuario {id: f.autor})
  CREATE (u)-[:ESCRIBIO]->(:Articulo {id: f.id, titulo: f.titulo, cuerpo: f.cuerpo,
      creado: datetime(), actualizado: datetime(),
      publicado: datetime('2024-01-01T00:00:00Z') + duration({days: toInteger(rand()*1096)})})
}

// Comentario
CALL {
  UNWIND [
    {id: 1, articulo: 1, autor: 4, cuerpo: "La idea de que el relato transforma el espacio resulta muy sugerente."},
    {id: 2, articulo: 2, autor: 5, cuerpo: "Una reflexión clara sobre la responsabilidad de decidir."},
    {id: 3, articulo: 3, autor: 6, cuerpo: "Las historias son una forma poderosa de explorar alternativas."},
    {id: 4, articulo: 1, autor: 2, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 5, articulo: 2, autor: 3, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 6, articulo: 3, autor: 4, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 7, articulo: 4, autor: 5, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 8, articulo: 5, autor: 6, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 9, articulo: 6, autor: 7, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 10, articulo: 7, autor: 8, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 11, articulo: 8, autor: 9, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 12, articulo: 9, autor: 10, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 13, articulo: 10, autor: 11, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 14, articulo: 11, autor: 12, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 15, articulo: 12, autor: 13, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 16, articulo: 13, autor: 14, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 17, articulo: 14, autor: 15, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 18, articulo: 15, autor: 16, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 19, articulo: 16, autor: 17, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 20, articulo: 17, autor: 18, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 21, articulo: 18, autor: 19, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 22, articulo: 19, autor: 20, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 23, articulo: 20, autor: 21, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 24, articulo: 21, autor: 22, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 25, articulo: 22, autor: 23, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 26, articulo: 23, autor: 24, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 27, articulo: 24, autor: 25, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 28, articulo: 25, autor: 26, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 29, articulo: 26, autor: 27, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 30, articulo: 27, autor: 28, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 31, articulo: 28, autor: 29, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 32, articulo: 29, autor: 30, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 33, articulo: 30, autor: 1, cuerpo: "Comentario de lectura: este artículo abre una conversación interesante."},
    {id: 34, articulo: 1, autor: 8, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 35, articulo: 2, autor: 9, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 36, articulo: 3, autor: 10, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 37, articulo: 4, autor: 11, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 38, articulo: 5, autor: 12, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 39, articulo: 6, autor: 13, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 40, articulo: 7, autor: 14, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 41, articulo: 8, autor: 15, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 42, articulo: 9, autor: 16, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 43, articulo: 10, autor: 17, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 44, articulo: 11, autor: 18, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 45, articulo: 12, autor: 19, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 46, articulo: 13, autor: 20, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 47, articulo: 14, autor: 21, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 48, articulo: 15, autor: 22, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 49, articulo: 16, autor: 23, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 50, articulo: 17, autor: 24, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 51, articulo: 18, autor: 25, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 52, articulo: 19, autor: 26, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 53, articulo: 20, autor: 27, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 54, articulo: 21, autor: 28, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 55, articulo: 22, autor: 29, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 56, articulo: 23, autor: 30, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 57, articulo: 24, autor: 1, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 58, articulo: 25, autor: 2, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 59, articulo: 26, autor: 3, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 60, articulo: 27, autor: 4, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 61, articulo: 28, autor: 5, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 62, articulo: 29, autor: 6, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."},
    {id: 63, articulo: 30, autor: 7, cuerpo: "Me parece valioso relacionar esta idea con otras lecturas del blog."}
  ] AS f
  MATCH (u:Usuario {id: f.autor}), (a:Articulo {id: f.articulo})
  CREATE (u)-[:COMENTO]->(:Comentario {id: f.id, cuerpo: f.cuerpo,
      creado: datetime()})-[:SOBRE]->(a)
}

// categorias
CALL {
  UNWIND [
    {articulo: 1, destino: 1},
    {articulo: 1, destino: 3},
    {articulo: 1, destino: 4},
    {articulo: 2, destino: 2},
    {articulo: 2, destino: 5},
    {articulo: 3, destino: 1},
    {articulo: 3, destino: 3},
    {articulo: 3, destino: 6},
    {articulo: 4, destino: 4},
    {articulo: 4, destino: 7},
    {articulo: 5, destino: 4},
    {articulo: 5, destino: 5},
    {articulo: 5, destino: 8},
    {articulo: 6, destino: 6},
    {articulo: 6, destino: 9},
    {articulo: 7, destino: 7},
    {articulo: 7, destino: 10},
    {articulo: 8, destino: 1},
    {articulo: 8, destino: 8},
    {articulo: 9, destino: 2},
    {articulo: 9, destino: 9},
    {articulo: 10, destino: 3},
    {articulo: 10, destino: 10},
    {articulo: 11, destino: 1},
    {articulo: 11, destino: 4},
    {articulo: 12, destino: 2},
    {articulo: 12, destino: 5},
    {articulo: 13, destino: 3},
    {articulo: 13, destino: 6},
    {articulo: 14, destino: 4},
    {articulo: 14, destino: 7},
    {articulo: 15, destino: 5},
    {articulo: 15, destino: 8},
    {articulo: 16, destino: 6},
    {articulo: 16, destino: 9},
    {articulo: 17, destino: 7},
    {articulo: 17, destino: 10},
    {articulo: 18, destino: 1},
    {articulo: 18, destino: 8},
    {articulo: 19, destino: 2},
    {articulo: 19, destino: 9},
    {articulo: 20, destino: 3},
    {articulo: 20, destino: 10},
    {articulo: 21, destino: 1},
    {articulo: 21, destino: 4},
    {articulo: 22, destino: 2},
    {articulo: 22, destino: 5},
    {articulo: 23, destino: 3},
    {articulo: 23, destino: 6},
    {articulo: 24, destino: 4},
    {articulo: 24, destino: 7},
    {articulo: 25, destino: 5},
    {articulo: 25, destino: 8},
    {articulo: 26, destino: 6},
    {articulo: 26, destino: 9},
    {articulo: 27, destino: 7},
    {articulo: 27, destino: 10},
    {articulo: 28, destino: 1},
    {articulo: 28, destino: 8},
    {articulo: 29, destino: 2},
    {articulo: 29, destino: 9},
    {articulo: 30, destino: 3},
    {articulo: 30, destino: 10}
  ] AS f
  MATCH (a:Articulo {id: f.articulo}), (c:Categoria {id: f.destino})
  CREATE (a)-[:EN_CATEGORIA]->(c)
}

// etiquetas
CALL {
  UNWIND [
    {articulo: 1, destino: 1},
    {articulo: 1, destino: 6},
    {articulo: 2, destino: 2},
    {articulo: 2, destino: 3},
    {articulo: 2, destino: 7},
    {articulo: 3, destino: 3},
    {articulo: 3, destino: 5},
    {articulo: 3, destino: 8},
    {articulo: 4, destino: 2},
    {articulo: 4, destino: 4},
    {articulo: 4, destino: 9},
    {articulo: 5, destino: 4},
    {articulo: 5, destino: 5},
    {articulo: 5, destino: 10},
    {articulo: 6, destino: 6},
    {articulo: 6, destino: 11},
    {articulo: 7, destino: 7},
    {articulo: 7, destino: 12},
    {articulo: 8, destino: 8},
    {articulo: 8, destino: 13},
    {articulo: 9, destino: 9},
    {articulo: 9, destino: 14},
    {articulo: 10, destino: 10},
    {articulo: 10, destino: 15},
    {articulo: 11, destino: 11},
    {articulo: 11, destino: 16},
    {articulo: 12, destino: 12},
    {articulo: 12, destino: 17},
    {articulo: 13, destino: 13},
    {articulo: 13, destino: 18},
    {articulo: 14, destino: 1},
    {articulo: 14, destino: 14},
    {articulo: 15, destino: 2},
    {articulo: 15, destino: 15},
    {articulo: 16, destino: 3},
    {articulo: 16, destino: 16},
    {articulo: 17, destino: 4},
    {articulo: 17, destino: 17},
    {articulo: 18, destino: 5},
    {articulo: 18, destino: 18},
    {articulo: 19, destino: 1},
    {articulo: 19, destino: 6},
    {articulo: 20, destino: 2},
    {articulo: 20, destino: 7},
    {articulo: 21, destino: 3},
    {articulo: 21, destino: 8},
    {articulo: 22, destino: 4},
    {articulo: 22, destino: 9},
    {articulo: 23, destino: 5},
    {articulo: 23, destino: 10},
    {articulo: 24, destino: 6},
    {articulo: 24, destino: 11},
    {articulo: 25, destino: 7},
    {articulo: 25, destino: 12},
    {articulo: 26, destino: 8},
    {articulo: 26, destino: 13},
    {articulo: 27, destino: 9},
    {articulo: 27, destino: 14},
    {articulo: 28, destino: 10},
    {articulo: 28, destino: 15},
    {articulo: 29, destino: 11},
    {articulo: 29, destino: 16},
    {articulo: 30, destino: 12},
    {articulo: 30, destino: 17}
  ] AS f
  MATCH (a:Articulo {id: f.articulo}), (e:Etiqueta {id: f.destino})
  CREATE (a)-[:TIENE_ETIQUETA]->(e)
}

CALL {
  UNWIND [
    {id: 31, login: "admin", rol: "administrador", correo: "admin@demo.blog.local", sal: "ea629f7eaaa7f892e0cb735338289f46", huella: "dca9cfcb6c38c1458567ac2a10a8e7a0d24ef6126f21745660b806dcc78e28cc"},
    {id: 32, login: "escritor", rol: "escritor", correo: "escritor@demo.blog.local", sal: "a5e539de0efb4df6b2cb68623a14b0fa", huella: "684b8d291efff33f8dac29776985c627b5fe2a5081d1690a0f3a758909dd2059"},
    {id: 33, login: "lector", rol: "lector", correo: "lector@demo.blog.local", sal: "ec35be237346c3c1777af7cfff33743c", huella: "48315f0053ec09dd347c10ea4607e6af0719ee7c8e8b234d45a8ecc6360c033e"}
  ] AS f
  MERGE (u:CuentaBlog {login:f.login})
  ON CREATE SET u:Usuario, u.id=f.id, u.nombre=f.login, u.rol=f.rol,
                u.correo=f.correo, u.sal=f.sal, u.huella=f.huella,
                u.bloqueado=false, u.version=0, u.creado=datetime()
}

WITH b MATCH (n:Usuario) WITH b, max(n.id) AS ultimo
SET b.Usuario = CASE WHEN b.Usuario > ultimo THEN b.Usuario ELSE ultimo END

WITH b MATCH (n:Categoria) WITH b, max(n.id) AS ultimo
SET b.Categoria = CASE WHEN b.Categoria > ultimo THEN b.Categoria ELSE ultimo END

WITH b MATCH (n:Etiqueta) WITH b, max(n.id) AS ultimo
SET b.Etiqueta = CASE WHEN b.Etiqueta > ultimo THEN b.Etiqueta ELSE ultimo END

WITH b MATCH (n:Articulo) WITH b, max(n.id) AS ultimo
SET b.Articulo = CASE WHEN b.Articulo > ultimo THEN b.Articulo ELSE ultimo END

WITH b MATCH (n:Comentario) WITH b, max(n.id) AS ultimo
SET b.Comentario = CASE WHEN b.Comentario > ultimo THEN b.Comentario ELSE ultimo END
RETURN "Carga inicial completada" AS estado;

// [Resumen]
// Totales de la base seleccionada.
RETURN COUNT { (:Usuario) } AS usuarios,
       COUNT { (:CuentaBlog) } AS cuentas,
       COUNT { (:Articulo) } AS articulos,
       COUNT { (:Comentario) } AS comentarios,
       COUNT { (:Categoria) } AS categorias,
       COUNT { (:Etiqueta) } AS etiquetas;
