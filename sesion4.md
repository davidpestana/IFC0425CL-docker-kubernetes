# 📘 Seguridad en Contenedores I

## 🎯 Objetivos de la sesión

* Comprender cómo se consigue el aislamiento en contenedores.
* Aplicar buenas prácticas de seguridad en la gestión de permisos, imágenes y secretos.
* Conocer herramientas para escanear vulnerabilidades.
* Implementar un flujo seguro de construcción y despliegue.

---

## 1️⃣ Namespaces y cgroups: aislamiento de procesos

### Explicación

* **Namespaces**: crean un *espacio aislado* para cada recurso (PID, NET, MNT, UTS, IPC, USER).

  * Ejemplo: cada contenedor ve solo sus procesos y su red.
* **cgroups (control groups)**: limitan y priorizan el uso de recursos (CPU, memoria, I/O).

  * Ejemplo: evitar que un contenedor consuma toda la RAM del host.

### Demo rápida

```bash
# Ver namespaces de un proceso
lsns

# Ver cgroups de un contenedor
docker run -d --name stress --memory=100m busybox sh -c "while true; do :; done"
cat /sys/fs/cgroup/memory/docker/$(docker inspect -f '{{.Id}}' stress)/memory.limit_in_bytes
```

---

## 2️⃣ Gestión de permisos y usuarios dentro del contenedor

### Explicación

* Evitar usar `root` dentro del contenedor.
* Añadir un usuario no privilegiado en el Dockerfile:

```dockerfile
FROM alpine:3.19
RUN adduser -D appuser
USER appuser
CMD ["echo", "Hola desde un usuario seguro"]
```

* Uso de **User Namespaces Remapping** en Docker.

---

## 3️⃣ Escaneo de imágenes y detección de vulnerabilidades

### Herramientas clave

* **Trivy**: escaneo de vulnerabilidades en imágenes, ficheros y dependencias.
* **Dockle**: análisis de buenas prácticas en imágenes (Dockerfile linting de seguridad).

### Demo rápida

```bash
# Instalar Trivy (Linux)
brew install aquasecurity/trivy/trivy   # en macOS
apt install trivy                       # en Linux

# Escanear imagen
trivy image nginx:latest

# Escaneo de buenas prácticas
dockle nginx:latest
```

---

## 4️⃣ Registro de imágenes: DockerHub y registros privados

### Explicación

* Público: DockerHub → cuidado con la exposición.
* Privado: Harbor, AWS ECR, GitHub Container Registry, GitLab Registry.
* Usar `docker login` con tokens, no contraseñas.

### Demo

```bash
# Etiquetar y subir una imagen
docker build -t miapp:1.0 .
docker tag miapp:1.0 registry.gitlab.com/usuario/proyecto/miapp:1.0
docker push registry.gitlab.com/usuario/proyecto/miapp:1.0
```

---

⏸️ **Descanso 30 min**

---

## 5️⃣ Control de acceso y credenciales seguras

### Explicación

* No guardar contraseñas en Dockerfile ni en `docker-compose.yml`.
* Usar **secret managers**:

  * Docker Secrets (Swarm)
  * Kubernetes Secrets
  * HashiCorp Vault / AWS Secrets Manager.
* Principio de mínimo privilegio (RBAC, IAM).

---

## 6️⃣ Gestión segura de volúmenes y secretos

### Puntos clave

* Revisar permisos en volúmenes montados (`read-only` cuando sea posible).
* Evitar montar `/var/run/docker.sock`.
* Usar volúmenes específicos para secretos (ej: certificados TLS).

### Ejemplo en `docker-compose.yml`:

```yaml
version: "3.8"
services:
  web:
    image: nginx:alpine
    volumes:
      - ./html:/usr/share/nginx/html:ro
      - ./certs:/etc/nginx/certs:ro
```

---

## 7️⃣ Laboratorio 4: Crear un flujo seguro de construcción y despliegue

### Objetivo

Construir y desplegar una aplicación con medidas de seguridad.

### Pasos

1. **Construcción segura**

   * Crear un Dockerfile multi-stage.
   * Añadir un usuario no-root.
   * Minimizar dependencias.
2. **Escaneo**

   * Pasar Trivy y Dockle a la imagen.
3. **Registro privado**

   * Subir la imagen a GitHub Container Registry o GitLab Registry.
4. **Despliegue seguro**

   * Lanzar contenedor con usuario limitado.
   * Montar volúmenes solo en lectura.
   * Usar variables de entorno desde `.env` o secretos.

### Dockerfile ejemplo (multi-stage + usuario no-root)

```dockerfile
# Etapa 1: build
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Etapa 2: run
FROM node:18-alpine
RUN adduser -D appuser
USER appuser
WORKDIR /app
COPY --from=build /app/dist ./dist
CMD ["node", "dist/index.js"]
```

### Flujo esperado

* Construir imagen → escanear con Trivy → subir a registro privado → desplegar en contenedor con permisos mínimos y secretos externos.