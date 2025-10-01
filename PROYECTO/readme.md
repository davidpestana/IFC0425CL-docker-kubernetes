# 🏁 Proyecto Final de Curso

**Título**: Despliegue de aplicación multicontenedor en Kubernetes con kind + port-forward

---

## 🎯 Objetivos

* Desplegar en **kind** una aplicación multicontenedor sencilla.
* Separar la **configuración** (ConfigMaps y Secrets) del **código** de la aplicación.
* Versionar las imágenes y demostrar releases alineadas con el pipeline.
* Automatizar el despliegue de forma manual o automática (GitHub Actions/GitOps).
* Validar la monitorización con el **Prometheus Operator**.

---

## 📂 Repositorios

👉 Deberéis trabajar con **dos repositorios separados**:

1. **Repositorio de aplicación**

   * Código fuente (Node.js o Python).
   * Dockerfile(s).
   * Workflow de GitHub Actions:

     * Build de la imagen.
     * Push a GitHub Container Registry (GHCR) con etiquetas versionadas (`v1.0.0`, `v1.0.1`, etc.).

2. **Repositorio de infraestructura**

   * Manifiestos de Kubernetes:

     * Deployments.
     * Services.
     * ConfigMaps.
     * Secrets.
     * PVCs.
   * Manifiestos/values para desplegar el **Prometheus Operator**.
   * Control de despliegues y releases de la aplicación.

---

## 🛠️ Alcance Técnico

### 1. Aplicación Multicontenedor

* La aplicación **no debe evolucionar funcionalmente**.
* Debe mostrar un mensaje simple:

```
Hola Mundo – Fecha: <fecha actual> – v1
```

* La fecha puede consultarse desde la base de datos con `SELECT NOW()` (o equivalente).
* **El foco es la conexión con la base de datos a través de un Service de Kubernetes**, no programar una app compleja.
* Para demostrar releases, basta con **cambios mínimos** en el código:

  * Cambiar `v1` → `v2` en el mensaje.
  * Añadir un `console.log` o `print`.

---

### 2. Configuración

* La configuración y credenciales deben ir separadas del código:

  * **ConfigMaps** → host, puerto DB.
  * **Secrets** → usuario y password DB.
* Nunca incluir credenciales hardcodeadas en el código fuente.

---

### 3. Despliegue en kind

* Recursos Kubernetes:

  * **Deployments** (app y base de datos).
  * **Services ClusterIP** internos (⚠️ no usar NodePort en kind).
  * **PVC** para persistencia de la base de datos.
  * **ConfigMaps/Secrets** para configuración.

* Acceso con **port-forward**:

```bash
kubectl port-forward svc/app 8080:80 -n proyecto
```

Acceso en: 👉 `http://localhost:8080`

---

### 4. Estrategias de despliegue

Tenéis **dos formas de desplegar**:

1. **Manual**

   ```bash
   kubectl apply -f manifests/
   ```

2. **Automático**

   * **CI/CD con GitHub Actions** → build, push y `kubectl apply`.
   * **GitOps con Flux o ArgoCD** → el clúster sincroniza automáticamente el repo de infraestructura.

👉 **La opción ideal es GitOps**, porque asegura que el clúster siempre refleja lo que hay en Git.

---

### 5. Monitorización

* Desplegar el **Prometheus Operator** (`kube-prometheus-stack`).
* Validar:

  * CRDs creados correctamente (`Prometheus`, `ServiceMonitor`, etc.).
  * Recolección de métricas de los pods de la aplicación.
  * Acceso a **Grafana** (via port-forward).
  * Dashboard con métricas básicas:

    * CPU y memoria de los pods.
    * Número de peticiones HTTP al backend.

---

## 📦 Entregables

1. **Repositorio de aplicación**

   * Código fuente.
   * Dockerfile(s).
   * Workflow de GitHub Actions.

2. **Repositorio de infraestructura**

   * Manifiestos Kubernetes.
   * Configuración del Prometheus Operator.

3. **README** con:

   * Pasos de despliegue en kind.
   * Acceso a la app (`kubectl port-forward`).
   * Validación del Prometheus Operator.

4. **Demo final** mostrando:

   * Releases versionadas (`v1`, `v2`).
   * Despliegue funcionando.
   * Dashboard de Grafana con métricas.

---

## 🎤 Presentación Final

Cada grupo debe mostrar en clase:

1. App en `localhost:8080` con **Hola Mundo + fecha + versión**.
2. Imágenes versionadas en GHCR.
3. Despliegue aplicado (manual o GitOps).
4. Prometheus Operator desplegado y en funcionamiento.
5. Dashboard en Grafana con métricas.

---

## ✅ Criterios de Evaluación

* Aplicación básica (`Hola Mundo <fecha> <versión>`).
* Configuración separada con ConfigMaps y Secrets.
* Repos separados: aplicación vs. infraestructura.
* Versionado correcto de imágenes en GHCR.
* Despliegue válido (manual o automático, recomendando GitOps).
* Prometheus Operator funcionando y métricas visibles en Grafana.
* Documentación y demo claras.

---

📌 **Recuerda**:

* La aplicación es solo un **pretexto** para practicar Kubernetes, CI/CD y GitOps.
* El foco está en la **infraestructura, versionado y observabilidad**, no en programar una app compleja.