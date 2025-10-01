# 📘 Ejemplos y Recomendaciones para el Proyecto Final

Este documento reúne **ejemplos prácticos y buenas prácticas** para ayudaros a completar el proyecto.
El foco está en la **contenedorización, despliegue y operación de la aplicación**, no en el desarrollo de código complejo.

---

## 🚀 Ejemplos de uso

### 1. Lanzar la aplicación localmente con Docker

```bash
# Construir la imagen
docker build -t hola-mundo:v1 .

# Ejecutar el contenedor conectando a PostgreSQL local
docker run -e DB_HOST=host.docker.internal \
           -e DB_NAME=demo \
           -e DB_USER=user \
           -e DB_PASS=password \
           -e APP_VERSION=v1 \
           -p 8080:80 hola-mundo:v1
```

Acceso en: 👉 [http://localhost:8080](http://localhost:8080)

---

### 2. Acceso a la aplicación en Kubernetes

En **kind**, no se puede usar NodePort directamente.
Acceso mediante **port-forward**:

```bash
kubectl port-forward svc/app 8080:80 -n proyecto
```

Acceso en: 👉 [http://localhost:8080](http://localhost:8080)

---

### 3. Ejemplo de ConfigMap y Secret en Kubernetes

**configmap.yaml**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DB_HOST: "postgres"
  DB_NAME: "demo"
```

**secret.yaml**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_USER: "user"
  DB_PASS: "password"
```

**deployment.yaml (extracto)**

```yaml
envFrom:
  - configMapRef:
      name: app-config
  - secretRef:
      name: app-secret
```

---

### 4. Validación de releases

Para demostrar que el pipeline está alineado con el versionado, bastan cambios mínimos:

* Cambiar el texto de `v1` → `v2` en el mensaje de la app.
* Añadir un log de depuración.
* Crear una nueva etiqueta (`git tag v2.0.0 && git push origin v2.0.0`).

---

## ✅ Recomendaciones

1. **Mantén la aplicación mínima**

   * El foco está en contenerización, despliegue, versionado y monitorización.
   * No inviertas tiempo en lógica de negocio.

2. **Usa ConfigMaps y Secrets**

   * Nunca pongas credenciales hardcodeadas en el código.
   * Esto es parte esencial de las buenas prácticas en Kubernetes.

3. **Versiona las imágenes**

   * Usa siempre etiquetas (`v1`, `v2`, `latest`).
   * Publica las imágenes en GitHub Container Registry (GHCR).

4. **Entrega clara**

   * Incluye un `README` con los pasos de despliegue y validación.
   * Usa capturas de pantalla de Grafana en la demo final.

5. **Automatización**

   * Si usas GitHub Actions, prueba el pipeline antes de la demo.
   * GitOps (ArgoCD o Flux) es lo ideal, pero no obligatorio.

---

## 📖 Enlaces de documentación oficial

* **Docker**

  * [Docker Docs](https://docs.docker.com/)
  * [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)

* **Node.js & Ruby**

  * [Node.js Docs](https://nodejs.org/en/docs/)
  * [Express Docs](https://expressjs.com/)
  * [Ruby Docs](https://www.ruby-lang.org/en/documentation/)
  * [Sinatra Docs](http://sinatrarb.com/documentation.html)

* **PostgreSQL**

  * [PostgreSQL Docs](https://www.postgresql.org/docs/)

* **Kubernetes**

  * [Kubernetes Docs](https://kubernetes.io/docs/home/)
  * [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
  * [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
  * [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
  * [Services](https://kubernetes.io/docs/concepts/services-networking/service/)

* **Prometheus & Grafana**

  * [Prometheus Operator](https://prometheus-operator.dev/)
  * [kube-prometheus-stack (Helm)](https://artifacthub.io/packages/helm/prometheus-community/kube-prometheus-stack)
  * [Grafana Docs](https://grafana.com/docs/)

* **CI/CD & GitOps**

  * [GitHub Actions](https://docs.github.com/en/actions)
  * [GHCR – GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
  * [FluxCD](https://fluxcd.io/)
  * [ArgoCD](https://argo-cd.readthedocs.io/en/stable/)

---
