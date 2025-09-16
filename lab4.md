# 🧪 Laboratorio 3: Seguridad en contenedores e imágenes

**Objetivo:**
Aprender a analizar imágenes en busca de vulnerabilidades, aplicar buenas prácticas de seguridad y gestionar secretos de forma correcta.

**Duración estimada:** 2h

---

## 🔹 Fase 1: Namespaces y aislamiento de procesos

1. Ejecutar un contenedor con usuario root (por defecto):

   ```bash
   docker run -it ubuntu:22.04 bash
   whoami
   ```

   👉 Observar que dentro del contenedor se ejecuta como **root**.

2. Salir y ejecutar contenedor como usuario limitado:

   ```bash
   docker run -it --user 1000:1000 ubuntu:22.04 bash
   whoami
   ```

   👉 Diferencia de permisos entre root vs usuario sin privilegios.

---

## 🔹 Fase 2: Escaneo de imágenes

1. Instalar **Trivy** (si no está disponible en el entorno):

   ```bash
   sudo apt-get install -y wget apt-transport-https gnupg lsb-release
   
   wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
   echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | \
     sudo tee /etc/apt/sources.list.d/trivy.list
   
   sudo apt-get update
   sudo apt-get install -y trivy

   ```

2. Escanear imagen oficial de Nginx:

   ```bash
   trivy image nginx:latest
   ```

3. Escanear la imagen personalizada creada en **Lab 2** (`flask-app:1.0`):

   ```bash
   trivy image flask-app:1.0
   ```

4. Identificar vulnerabilidades críticas/altas y discutir mitigaciones (ejemplo: usar imágenes `-slim` o `distroless`).

---

## 🔹 Fase 3: Gestión segura de credenciales

1. Ejecutar contenedor con variable de entorno (poco seguro):

   ```bash
   docker run -e DB_PASSWORD=SuperSecret mysql:8.0
   ```

   👉 Verificar que las variables quedan expuestas con:

   ```bash
   docker inspect <container_id> | grep DB_PASSWORD
   ```

2. Usar **Docker Secrets** (cuando se trabaja con Docker Swarm) o simular gestión segura:

   * Crear archivo `db_password.txt` con contenido `SuperSecret`.
   * Montarlo como volumen:

     ```bash
     docker run -d \
       -v $(pwd)/db_password.txt:/run/secrets/db_password:ro \
       nginx
     ```

   👉 Dentro del contenedor, el secreto queda disponible en `/run/secrets/db_password`.

---

## 🔹 Fase 4: Buenas prácticas en imágenes

1. Comparar tamaños de imágenes:

   ```bash
   docker pull python:3.11
   docker pull python:3.11-slim
   docker pull gcr.io/distroless/python3
   docker images | grep python
   ```

   👉 Mostrar diferencias de tamaño y superficie de ataque.

2. Reconstruir la imagen del **Lab 2** usando `python:3.11-slim` para mejorar seguridad.

---

## 📌 Conclusión

* Se entendió cómo **namespaces y usuarios** refuerzan el aislamiento.
* Se aprendió a **escanear imágenes** y detectar vulnerabilidades.
* Se revisaron métodos de **gestión de secretos más seguros** que variables de entorno.
* Se introdujeron **buenas prácticas de hardening** en construcción de imágenes.

---

💡 Para hacerlo más evaluable, puedo prepararte una **rúbrica de entrega** con 3 capturas obligatorias:

1. Resultado de `trivy` en `nginx:latest`.
2. Inspección mostrando la diferencia entre secreto en ENV y secreto en fichero.
3. Comparativa de tamaños de imágenes `python`.
