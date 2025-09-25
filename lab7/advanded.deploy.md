# 🧪 Laboratorio 7 — Rolling Update y Rollback con ClusterIP (vía YAML)

> 📦 Basado en la imagen: `docker.io/jocatalin/kubernetes-bootcamp`
> 🔧 Todo se gestiona con manifiestos YAML, **no con `kubectl set` ni `kubectl expose`**
> 🌐 Comunicación interna usando un `Pod tester` y un `Service` tipo `ClusterIP`

---

## 🧱 Estructura del proyecto

```
lab07-rolling-update/
├── manifests/
│   ├── 01-deployment-v1.yaml
│   ├── 02-service-clusterip.yaml
│   ├── 03-deployment-v2.yaml
│   ├── 04-deployment-v10.yaml  # versión rota
│   ├── 05-tester.yaml
```

---

## 🧩 Fase 1 – Despliegue inicial v1 con Service ClusterIP

### 🎯 Objetivo:

* Desplegar `v1` del bootcamp con 3 réplicas.
* Crear un `Service` interno tipo `ClusterIP`.

---

### 📄 `01-deployment-v1.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-bootcamp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bootcamp
  strategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: bootcamp
    spec:
      containers:
        - name: kubernetes-bootcamp
          image: docker.io/jocatalin/kubernetes-bootcamp:v1
          ports:
            - containerPort: 8080
```

---

### 📄 `02-service-clusterip.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: kubernetes-bootcamp
spec:
  selector:
    app: bootcamp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

---

### ▶️ Aplicar

```bash
kubectl apply -f manifests/01-deployment-v1.yaml
kubectl apply -f manifests/02-service-clusterip.yaml
```

---

## 🧩 Fase 2 – Crear un tester interno para comprobar la app

### 🎯 Objetivo:

* Usar un `Pod` temporal que pruebe el acceso a través del `Service`.

---

### 📄 `05-tester.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: curl-tester
spec:
  containers:
    - name: curl
      image: curlimages/curl
      command: ["sleep", "3600"]
```

### ▶️ Aplicar y entrar

```bash
kubectl apply -f manifests/05-tester.yaml
kubectl exec -it curl-tester -- sh
```

### ✅ Validar desde dentro del clúster:

```bash
curl http://kubernetes-bootcamp
```

Deberías recibir algo como:

```txt
Hello Kubernetes bootcamp! | Running on: kubernetes-bootcamp-xxxxx | v=1
```

---

## 🧩 Fase 3 – Rolling update a versión v2

### 🎯 Objetivo:

* Cambiar a imagen `v2`
* Observar reemplazo progresivo de pods

---

### 📄 `03-deployment-v2.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-bootcamp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bootcamp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: bootcamp
    spec:
      containers:
        - name: kubernetes-bootcamp
          image: docker.io/jocatalin/kubernetes-bootcamp:v2
          ports:
            - containerPort: 8080
```

---

### ▶️ Aplicar

```bash
kubectl apply -f manifests/03-deployment-v2.yaml
kubectl rollout status deployment kubernetes-bootcamp
```

---

### ✅ Verificar desde el tester

```bash
kubectl exec -it curl-tester -- sh
# Ejecuta varias veces:
curl http://kubernetes-bootcamp
```

🧠 Deberías ver varias respuestas tipo:

```
... | v=1
... | v=2
```

Al finalizar el rollout, todas serán `v=2`.

---

## 🧩 Fase 4 – Despliegue erróneo con imagen inexistente

### 🎯 Objetivo:

* Simular fallo al hacer deploy de una versión inexistente (`v10`)
* Ver efecto en los pods

---

### 📄 `04-deployment-v10.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kubernetes-bootcamp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bootcamp
  strategy:
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: bootcamp
    spec:
      containers:
        - name: kubernetes-bootcamp
          image: docker.io/jocatalin/kubernetes-bootcamp:v10
          ports:
            - containerPort: 8080
```

---

### ▶️ Aplicar

```bash
kubectl apply -f manifests/04-deployment-v10.yaml
kubectl rollout status deployment kubernetes-bootcamp
```

---

### 🧪 Ver estado

```bash
kubectl get pods
kubectl describe pods | grep -A 5 "Events"
```

Verás errores tipo `ImagePullBackOff`.

---

## 🧩 Fase 5 – Rollback a la versión estable

### 🎯 Objetivo:

* Revertir al último estado funcional (`v2`) usando `rollout undo`

---

### ▶️ Ejecutar rollback

```bash
kubectl rollout undo deployment kubernetes-bootcamp
```

---

### ✅ Verificar desde el tester

```bash
kubectl exec -it curl-tester -- sh
curl http://kubernetes-bootcamp
```

Todas las respuestas deberían volver a ser `v=2`.

---

## 🧼 Fase 6 – Limpieza

```bash
kubectl delete -f manifests/
kubectl delete pod curl-tester
```