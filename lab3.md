# 🧪 Laboratorio 3: Stack multicontenedor (app + base de datos)

### 🎯 Objetivo

* Aprender a usar `docker-compose` para levantar varios servicios que colaboran entre sí.
* Montar una aplicación web (Python/Flask o Node/Express) conectada a una base de datos (MySQL o PostgreSQL).
* Entender cómo definir redes, volúmenes y variables de entorno en YAML.

---

## 1️⃣ Preparación

* Crear carpeta de trabajo `lab03-stack/`.
* Dentro, dos subcarpetas:

  ```
  lab03-stack/
  ├── app/
  │   └── Dockerfile
  │   └── app.py   (si Python) ó index.js (si Node)
  └── docker-compose.yml
  ```
* Verificar que Docker y Docker Compose están instalados:

  ```bash
  docker --version
  docker compose version
  ```

---

## 2️⃣ Aplicación sencilla

### Opción A: Python (Flask)

**app/app.py**

```python
from flask import Flask
import os
import psycopg2

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "testdb"),
            user=os.getenv("POSTGRES_USER", "user"),
            password=os.getenv("POSTGRES_PASSWORD", "pass"),
            host="db"
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        conn.close()
        return f"📦 Hola desde Flask! Hora en DB: {result[0]}"
    except Exception as e:
        return f"Error conectando a DB: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

**app/Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY app.py /app

RUN pip install flask psycopg2-binary

EXPOSE 5000
CMD ["python", "app.py"]
```

---

### Opción B: Node (Express + pg)

**app/index.js**

```js
const express = require("express");
const { Client } = require("pg");

const app = express();

app.get("/", async (req, res) => {
  try {
    const client = new Client({
      host: "db",
      user: process.env.POSTGRES_USER || "user",
      password: process.env.POSTGRES_PASSWORD || "pass",
      database: process.env.POSTGRES_DB || "testdb"
    });
    await client.connect();
    const result = await client.query("SELECT NOW()");
    await client.end();
    res.send("📦 Hola desde Express! Hora en DB: " + result.rows[0].now);
  } catch (err) {
    res.send("Error conectando a DB: " + err);
  }
});

app.listen(8080, () => console.log("Servidor en puerto 8080"));
```

**app/Dockerfile**

```dockerfile
FROM node:20-slim

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY index.js ./
EXPOSE 8080
CMD ["node", "index.js"]
```

**app/package.json**

```json
{
  "name": "lab03-app",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "express": "^4.19.2",
    "pg": "^8.11.3"
  }
}
```

---

## 3️⃣ docker-compose.yml

```yaml
version: "3.9"

services:
  app:
    build: ./app
    ports:
      - "8080:8080"   # si Node
      # - "5000:5000" # si Flask
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: testdb
    depends_on:
      - db

  db:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: testdb
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

## 4️⃣ Ejecución

1. Levantar el stack:

   ```bash
   docker compose up --build
   ```
2. Verificar contenedores:

   ```bash
   docker ps
   ```
3. Probar en navegador:

   * Flask → `http://localhost:5000`
   * Node → `http://localhost:8080`

---

## 5️⃣ Retos adicionales

* **Reto 1**: Añadir un servicio `pgadmin` para administrar PostgreSQL vía web.
* **Reto 2**: Añadir variables en `.env` en lugar de codificarlas en el YAML.
* **Reto 3**: Crear un volumen persistente para que los datos sobrevivan aunque se borre el contenedor DB.

