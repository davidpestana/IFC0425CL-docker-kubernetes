# 🧪 Laboratorio 2: Imágenes personalizadas y entornos multicontenedor

**Objetivo:**
Aprender a crear imágenes con `Dockerfile`, comprender buenas prácticas de construcción y desplegar aplicaciones multicontenedor con `docker-compose`.

**Duración estimada:** 2h – 2h30

---

## 🔹 Fase 1: Crear una imagen personalizada

1. **Preparar directorio de trabajo:**

   ```bash
   mkdir lab2_app && cd lab2_app
   ```

2. **Crear archivo `app.py`:**

   ```python
   from flask import Flask
   app = Flask(__name__)

   @app.route('/')
   def hello():
       return "¡Hola desde Docker y Flask!"

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

3. **Crear archivo `requirements.txt`:**

   ```
   flask==2.2.2
   ```

4. **Crear `Dockerfile`:**

   ```dockerfile
   # Imagen base ligera
   FROM python:3.11-slim

   # Directorio de trabajo
   WORKDIR /app

   # Copiar dependencias e instalarlas
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   # Copiar aplicación
   COPY app.py .

   # Exponer puerto
   EXPOSE 5000

   # Comando de arranque
   CMD ["python", "app.py"]
   ```

5. **Construir la imagen:**

   ```bash
   docker build -t flask-app:1.0 .
   ```

6. **Ejecutar contenedor:**

   ```bash
   docker run -d -p 5000:5000 flask-app:1.0
   ```

   👉 Abrir navegador en `http://localhost:5000` para ver el mensaje.

---

## 🔹 Fase 2: Entorno multicontenedor con Docker Compose

1. **Extender aplicación con base de datos (MySQL/Postgres).**
   Crear archivo `docker-compose.yml`:

   ```yaml
   version: "3.9"
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       depends_on:
         - db
     db:
       image: mysql:8.0
       environment:
         MYSQL_ROOT_PASSWORD: rootpass
         MYSQL_DATABASE: testdb
         MYSQL_USER: testuser
         MYSQL_PASSWORD: testpass
       volumes:
         - db_data:/var/lib/mysql
   volumes:
     db_data:
   ```

2. **Levantar el entorno:**

   ```bash
   docker-compose up -d
   ```

3. **Comprobar contenedores:**

   ```bash
   docker ps
   ```

4. **Acceder a la base de datos:**

   ```bash
   docker exec -it lab2_app-db-1 mysql -u testuser -p
   ```

   (password: `testpass`)

---

## 🔹 Fase 3: Gestión del ciclo de vida

1. Detener entorno:

   ```bash
   docker-compose down
   ```

2. Levantar de nuevo (manteniendo datos persistentes):

   ```bash
   docker-compose up -d
   ```

3. Eliminar contenedores y volúmenes:

   ```bash
   docker-compose down -v
   ```

---

## 📌 Conclusión

* Se aprendió a **crear imágenes personalizadas** con `Dockerfile`.
* Se desplegó un **stack multicontenedor** con `docker-compose`.
* Se trabajó con **persistencia de datos en volúmenes**.