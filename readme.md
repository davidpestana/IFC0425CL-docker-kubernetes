# 📅 Planificación del curso

**IFC0425CL - Entornos Seguros Virtualizados con Docker y Kubernetes (35h)**
Modalidad: Aula Virtual (Teams)
Duración: 9 sesiones

---

## Sesión 1 (4h)

**Introducción y fundamentos de Docker**

* Presentación del curso y entorno de trabajo (Teams, repositorios, laboratorios).
* Virtualización ligera vs. virtualización tradicional.
* Arquitectura de Docker: engine, imágenes, contenedores.
* Comandos básicos (`docker run`, `ps`, `images`, `logs`, `exec`).
* Laboratorio 1: primeros contenedores (nginx, alpine, ubuntu).

⏸️ **Descanso 30 min**

* Gestión de imágenes (pull, push, remove).
* Introducción a redes en Docker.
* Ejercicio guiado: lanzar una aplicación web simple en contenedor.

---

## Sesión 2 (4h)

**Imágenes y entornos multicontenedor**

* Creación de imágenes personalizadas con `Dockerfile`.
* Buenas prácticas en construcción de imágenes.
* Laboratorio 2: construir imagen de aplicación Python/Node simple.

⏸️ **Descanso 30 min**

* Introducción a `docker-compose`.
* Definición de servicios y dependencias en YAML.
* Laboratorio 3: stack multicontenedor (app + base de datos).

---

## Sesión 3 (4h)

**Seguridad en contenedores I**

* Namespaces y cgroups: aislamiento de procesos.
* Gestión de permisos y usuarios dentro del contenedor.
* Escaneo de imágenes y detección de vulnerabilidades (Trivy, Dockle).
* Registro de imágenes: DockerHub, registros privados.

⏸️ **Descanso 30 min**

* Control de acceso y credenciales seguras.
* Gestión segura de volúmenes y secretos.
* Laboratorio 4: crear un flujo seguro de construcción y despliegue.

---

## Sesión 4 (4h)

**Introducción a Kubernetes**

* Arquitectura de Kubernetes: master, worker, etcd, kubelet.
* Recursos básicos: Pod, ReplicaSet, Deployment.
* Laboratorio 5: desplegar pods y deployments en Minikube/Kind.

⏸️ **Descanso 30 min**

* Servicios: ClusterIP, NodePort, LoadBalancer.
* Ejercicio guiado: exponer una aplicación dentro del clúster.

---

## Sesión 5 (4h)

**Configuración en Kubernetes**

* ConfigMaps y Secrets.
* Laboratorio 6: separar configuración de la aplicación.

⏸️ **Descanso 30 min**

* Volúmenes y almacenamiento en Kubernetes.
* Ejercicio práctico: aplicación con volumen persistente.

---

## Sesión 6 (4h)

**Despliegue avanzado de aplicaciones**

* Estrategias de despliegue: rolling update, recreate.
* Escalado manual y automático (HPA).
* Laboratorio 7: despliegue con actualización controlada.

⏸️ **Descanso 30 min**

* Introducción a pipelines CI/CD para Kubernetes (GitHub Actions / GitLab CI).
* Ejercicio guiado: pipeline sencillo de build & deploy.

---

## Sesión 7 (4h)

**Monitorización en Kubernetes**

* Introducción a Prometheus.
* Métricas de clúster y pods.
* Laboratorio 8: desplegar Prometheus en clúster local.

⏸️ **Descanso 30 min**

* Introducción a Grafana y dashboards.
* Ejercicio práctico: visualizar métricas de un despliegue.

---

## Sesión 8 (4h)

**Seguridad en Kubernetes**

* Control de acceso con RBAC.
* Network Policies: segmentación de red.
* Recomendaciones de hardening de clúster.

⏸️ **Descanso 30 min**

* Laboratorio 9: crear usuarios y roles con restricciones.
* Laboratorio 10: aplicar políticas de red.

---

## Sesión 9 (3h)

**Proyecto final y cierre**

* Presentación del proyecto final:

  * Desplegar una aplicación multicontenedor en Kubernetes.
  * Configurar acceso seguro, métricas y políticas básicas.
* Exposición de proyectos por grupos.
* Evaluación de resultados y cierre del curso.

---

👉 Con esta planificación:

* **Horas totales** = 8×4h + 1×3h = **35h**.
* Cada sesión incluye **30 min de descanso**, quedando bloques de trabajo de 1h30–2h.
* Se alterna **teoría aplicada + laboratorio** en cada módulo.