# 📂 Recursos para el Proyecto Final

Este documento contiene **propuestas de aplicación mínima** en **Node.js** y **Ruby**, listas para contenerizar y desplegar en Kubernetes.
👉 Son **ejemplos**: el foco del proyecto no está en programar, sino en **aplicar buenas prácticas de contenedorización, despliegue y operaciones**.

---

## 🚀 Node.js – Express + PostgreSQL

**app.js**

```javascript
const express = require('express');
const { Client } = require('pg');

const app = express();
const PORT = process.env.PORT || 80;

// Configuración vía variables de entorno (vendrán de ConfigMaps/Secrets en Kubernetes)
const client = new Client({
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
});

client.connect().then(() => console.log("✅ Conectado a DB"))
  .catch(err => {
    console.error("❌ Error de conexión:", err);
    process.exit(1);
  });

app.get('/', async (req, res) => {
  try {
    const result = await client.query('SELECT NOW()');
    res.send(`Hola Mundo – Fecha: ${result.rows[0].now} – ${process.env.APP_VERSION || "v1"}`);
  } catch (err) {
    res.status(500).send("Error consultando DB");
  }
});

app.listen(PORT, () => {
  console.log(`🚀 Servidor escuchando en puerto ${PORT}`);
});
```

**package.json**

```json
{
  "name": "hola-mundo-db",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.1"
  }
}
```

**Dockerfile**

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 80
CMD ["node", "app.js"]
```

---

## 💎 Ruby – Sinatra + PostgreSQL

**app.rb**

```ruby
require 'sinatra'
require 'pg'

set :bind, '0.0.0.0'
set :port, 80

get '/' do
  begin
    conn = PG.connect(
      host: ENV['DB_HOST'],
      dbname: ENV['DB_NAME'],
      user: ENV['DB_USER'],
      password: ENV['DB_PASS']
    )
    result = conn.exec("SELECT NOW();")
    fecha = result[0]['now']
    conn.close
    "Hola Mundo – Fecha: #{fecha} – #{ENV['APP_VERSION'] || 'v1'}"
  rescue PG::Error => e
    status 500
    "Error conectando a DB: #{e.message}"
  end
end
```

**Gemfile**

```ruby
source "https://rubygems.org"

gem "sinatra"
gem "pg"
```

**Dockerfile**

```dockerfile
FROM ruby:3.2-alpine

WORKDIR /app

# Dependencias necesarias para pg
RUN apk add --no-cache build-base postgresql-dev

COPY Gemfile Gemfile.lock ./
RUN bundle install

COPY . .

EXPOSE 80
CMD ["ruby", "app.rb"]
```

---

## 🔑 Variables de entorno esperadas

Las aplicaciones esperan estas variables (se deben inyectar mediante **ConfigMaps** y **Secrets** en Kubernetes):

* `DB_HOST` → Host de la base de datos.
* `DB_NAME` → Nombre de la base de datos.
* `DB_USER` → Usuario de la base de datos (Secret).
* `DB_PASS` → Password de la base de datos (Secret).
* `APP_VERSION` → Versión de la aplicación (`v1`, `v2`, …).

---

📌 **Nota:**
Este código es **propuesta de referencia**. Podéis adaptarlo si queréis, pero el foco del proyecto está en:

* Contenerizar y publicar las imágenes en un registry.
* Separar configuración con ConfigMaps/Secrets.
* Desplegar en Kubernetes con buenas prácticas.
* Gestionar releases y monitorización.
