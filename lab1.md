# 🧪 Laboratorio 1: Primeros pasos con Docker

**Objetivo:**
Familiarizarse con la ejecución de contenedores básicos, gestión de imágenes y exploración de entornos aislados.

**Duración estimada:** 1h – 1h30

---

## 🔹 Fase 1: Verificar instalación de Docker

1. Comprobar versión de Docker:

   ```bash
   docker --version
   docker info
   ```

   👉 Confirma que el motor está instalado y en ejecución.

---

## 🔹 Fase 2: Ejecutar el primer contenedor

1. Lanzar un contenedor básico de prueba:

   ```bash
   docker run hello-world
   ```

   * Observa cómo Docker descarga la imagen y ejecuta un proceso.
   * Explica el flujo: búsqueda local → DockerHub → descarga → ejecución.

2. Ejecutar un contenedor interactivo con Linux:

   ```bash
   docker run -it alpine sh
   ```

   * Explorar dentro del contenedor:

     ```bash
     uname -a
     cat /etc/os-release
     ```
   * Salir con `exit`.

---

## 🔹 Fase 3: Gestión de contenedores

1. Listar contenedores activos:

   ```bash
   docker ps
   ```
2. Listar todos los contenedores (incluidos los detenidos):

   ```bash
   docker ps -a
   ```
3. Eliminar un contenedor terminado:

   ```bash
   docker rm <ID>
   ```
4. Ejecutar un contenedor en segundo plano:

   ```bash
   docker run -d nginx
   ```

   * Verificar estado: `docker ps`
   * Parar contenedor: `docker stop <ID>`
   * Eliminarlo: `docker rm <ID>`

---

## 🔹 Fase 4: Gestión de imágenes

1. Listar imágenes descargadas:

   ```bash
   docker images
   ```
2. Descargar explícitamente una imagen:

   ```bash
   docker pull ubuntu:22.04
   ```
3. Eliminar una imagen:

   ```bash
   docker rmi ubuntu:22.04
   ```

---

## 🔹 Fase 5: Publicar un servicio local

1. Lanzar un contenedor **Nginx** en el puerto 8080:

   ```bash
   docker run -d -p 8080:80 nginx
   ```

2. Abrir navegador en `http://localhost:8080`
   👉 Se debe ver la página de bienvenida de Nginx.

3. Detener y eliminar el contenedor:

   ```bash
   docker stop <ID>
   docker rm <ID>
   ```

---

## 📌 Conclusión

* Docker facilita el despliegue rápido de aplicaciones en contenedores.
* Se aprendió a **crear, listar, detener y eliminar** contenedores.
* Se desplegó el primer servicio accesible en red (Nginx).