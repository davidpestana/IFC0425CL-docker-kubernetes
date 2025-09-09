# 🧪 Laboratorio 4: Primeros pasos con Kubernetes

**Objetivo:**
Familiarizarse con los componentes básicos de Kubernetes desplegando pods, servicios y un primer `Deployment` en un clúster local.

**Duración estimada:** 2h – 2h30

---

## 🔹 Fase 1: Preparar entorno

1. **Comprobar instalación de kubectl**

   ```bash
   kubectl version --client
   ```

2. **Iniciar clúster local (ejemplo con Minikube):**

   ```bash
   minikube start
   kubectl get nodes
   ```

   👉 Verificar que el nodo está en estado `Ready`.

---

## 🔹 Fase 2: Desplegar un Pod básico

1. Crear pod `nginx-pod.yaml`:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: nginx-pod
   spec:
     containers:
     - name: nginx
       image: nginx:latest
       ports:
       - containerPort: 80
   ```

2. Aplicar manifiesto:

   ```bash
   kubectl apply -f nginx-pod.yaml
   ```

3. Verificar:

   ```bash
   kubectl get pods
   kubectl describe pod nginx-pod
   ```

---

## 🔹 Fase 3: Crear un Service para exponer el Pod

1. Crear `nginx-service.yaml`:

   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx-service
   spec:
     type: NodePort
     selector:
       app: nginx
     ports:
       - port: 80
         targetPort: 80
         nodePort: 30080
   ```

2. Antes de aplicar, añadir **label** al Pod para que coincida con el selector:

   ```yaml
   metadata:
     name: nginx-pod
     labels:
       app: nginx
   ```

3. Aplicar ambos manifiestos y verificar:

   ```bash
   kubectl apply -f nginx-pod.yaml
   kubectl apply -f nginx-service.yaml
   kubectl get svc
   ```

4. Probar acceso (Minikube):

   ```bash
   minikube service nginx-service
   ```

   👉 Se debe abrir la página de bienvenida de Nginx.

---

## 🔹 Fase 4: Escalar con un Deployment

1. Crear `nginx-deployment.yaml`:

   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
         - name: nginx
           image: nginx:latest
           ports:
           - containerPort: 80
   ```

2. Aplicar y comprobar:

   ```bash
   kubectl apply -f nginx-deployment.yaml
   kubectl get deployments
   kubectl get pods -o wide
   ```

---

## 🔹 Fase 5: Explorar recursos

* Ver logs de un pod:

  ```bash
  kubectl logs <pod_name>
  ```

* Entrar en un contenedor:

  ```bash
  kubectl exec -it <pod_name> -- bash
  ```

* Escalar el Deployment a 5 réplicas:

  ```bash
  kubectl scale deployment nginx-deployment --replicas=5
  kubectl get pods
  ```

---

## 📌 Conclusión

* Se aprendió a desplegar un **Pod** manualmente.
* Se expuso un servicio con **NodePort**.
* Se desplegó y escaló un **Deployment** con múltiples réplicas.
* Se practicaron operaciones básicas de inspección y acceso a pods.