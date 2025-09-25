## 🧩 Fase 7 — Escalado automático con HPA + generación de carga

### 🎯 Objetivos

* Configurar un **HPA** sobre el `Deployment`.
* Usar **metrics-server** (ya instalado) para monitorizar uso de CPU.
* Generar carga real para disparar el escalado automático.
* Observar cómo aumentan las réplicas y se distribuye la carga.

---

## 🔧 Consideraciones importantes

* La imagen `jocatalin/kubernetes-bootcamp` **no consume mucha CPU** con tráfico HTTP.
* El autoscaling solo responde al **uso real de CPU**, no al número de peticiones.
* Se recomienda simular carga con `while true; curl ...` desde varios pods o terminales.

---

## ✅ Paso 1 — Crear el HPA

### 📄 `06-hpa.yaml`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: bootcamp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kubernetes-bootcamp
  minReplicas: 2
  maxReplicas: 6
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 30
```

📌 Puedes ajustar `averageUtilization` a un valor bajo (30%) para que escale fácilmente.

---

### ▶️ Aplicar

```bash
kubectl apply -f manifests/06-hpa.yaml
kubectl get hpa
```

---

## 🧪 OPCIÓN A — Generar carga desde el exterior (port-forward + stress script)

### ✅ Ventaja: sin pods extra.

### ▶️ Hacer port-forward

```bash
kubectl port-forward svc/kubernetes-bootcamp 8080:80
```

### 📄 Script: `scripts/stress-local.sh`

```bash
#!/bin/bash
while true; do
  curl -s http://localhost:8080 > /dev/null
done
```

### ▶️ Ejecutar en 4–5 terminales a la vez:

```bash
bash scripts/stress-local.sh
```

🧠 Esto genera carga real sobre el pod → consume CPU → activa HPA.

---

## 🧪 OPCIÓN B — Generar carga dentro del clúster (Pods `curl` en bucle)

### ✅ Ventaja: más realista, sin exponer puertos.

### 📄 `07-stress-pod.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: stress-curl
spec:
  containers:
    - name: stress
      image: curlimages/curl
      command: ["/bin/sh", "-c"]
      args:
        - |
          while true; do
            curl -s http://kubernetes-bootcamp > /dev/null
          done
```

🧠 Puedes crear varios de estos pods (`stress-curl-1`, `stress-curl-2`, etc.).

---

### ▶️ Aplicar

```bash
kubectl apply -f manifests/07-stress-pod.yaml
```

---

## 📈 Monitorizar el escalado

```bash
kubectl get hpa -w
kubectl get pods -l app=bootcamp -w
```

Verás cómo el número de réplicas sube progresivamente.

---

## 🧼 Limpieza (opcional)

```bash
kubectl delete hpa bootcamp-hpa
kubectl delete pod stress-curl
kubectl delete -f manifests/
```
