# 🧪 Laboratorio 6 — Separar configuración de la aplicación (ConfigMaps y Secrets)

📍 **Tema**: Configuración en Kubernetes
⏱️ **Duración estimada**: 60–75 minutos
🔑 **Conceptos clave**: `ConfigMap`, `Secret`, `env`, `volumeMounts`

---

## 🧭 Estructura general del laboratorio

```
lab06-configuracion/
├── 01-namespace.yaml            # Espacio aislado para trabajar
├── 02-configmap.yaml            # Configuración general (no secreta)
├── 03-secret.yaml               # Configuración sensible (API Key)
├── 04-deployment-env.yaml      # Uso de ConfigMap y Secret como variables
└── 05-deployment-mount.yaml    # Uso de ConfigMap y Secret como archivos
```

---

## 🔹 Fase 1 — Preparar el entorno de trabajo

### ✅ Paso 1: Crear un namespace

`01-namespace.yaml`

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: lab-config
```

```bash
kubectl apply -f 01-namespace.yaml
kubectl config set-context --current --namespace=lab-config
```

🔍 **Tip**: En Kubernetes, un `Namespace` es como una carpeta o espacio aislado. Todo lo que hagamos en este laboratorio estará contenido ahí para no mezclar recursos con otros proyectos.

---

## 🔹 Fase 2 — Definir la configuración externa

### ✅ Paso 2: Crear el `ConfigMap`

`02-configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: lab-config
data:
  APP_MODE: "produccion"
  APP_COLOR: "azul"
```

```bash
kubectl apply -f 02-configmap.yaml
```

🔍 **Tip**: Los `ConfigMap` almacenan valores que no son sensibles (colores, modos, rutas, etc.). Ideal para evitar tener esos valores *hardcoded* dentro de la imagen del contenedor.

---

### ✅ Paso 3: Crear el `Secret`

`03-secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: lab-config
type: Opaque
stringData:
  API_KEY: "1234-ABCD-5678"
```

```bash
kubectl apply -f 03-secret.yaml
```

🔍 **Tip**: Los `Secrets` son como los `ConfigMap`, pero pensados para almacenar datos sensibles (API keys, contraseñas...). Kubernetes los guarda codificados en base64, pero no cifrados por defecto (a tener en cuenta en producción).

---

## 🔹 Fase 3 — Usar la configuración como variables de entorno

### ✅ Paso 4: Crear un Deployment que lea las variables

`04-deployment-env.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-env
  namespace: lab-config
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app-env
  template:
    metadata:
      labels:
        app: app-env
    spec:
      containers:
        - name: app
          image: busybox
          command: ["sh", "-c", "env && sleep 3600"]
          env:
            - name: APP_MODE
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: APP_MODE
            - name: APP_COLOR
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: APP_COLOR
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: app-secret
                  key: API_KEY
```

```bash
kubectl apply -f 04-deployment-env.yaml
```

🔍 **Tip**: Aquí estamos usando las variables definidas en el `ConfigMap` y el `Secret` como **variables de entorno** dentro del contenedor, lo cual es muy común. El contenedor puede acceder a ellas usando `os.getenv()` en Python, `$VAR_NAME` en Bash, etc.

---

### 🔎 Validación 1: Comprobar que están disponibles

```bash
kubectl get pods
kubectl exec -it <nombre-del-pod> -- env | grep APP_
kubectl exec -it <nombre-del-pod> -- env | grep API_KEY
```

✅ Deberías ver:

```
APP_MODE=produccion
APP_COLOR=azul
API_KEY=1234-ABCD-5678
```

🔍 **Tip**: Esto demuestra que los valores externos están siendo leídos correctamente por el pod.

---

## 🔹 Fase 4 — Usar configuración como archivos

### ✅ Paso 5: Crear un pod que monte la configuración como archivos

`05-deployment-mount.yaml`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-mount
  namespace: lab-config
spec:
  containers:
    - name: app
      image: busybox
      command: ["sh", "-c", "ls /etc/config && cat /etc/config/APP_MODE && sleep 3600"]
      volumeMounts:
        - name: config-vol
          mountPath: /etc/config
    - name: secret
      image: busybox
      command: ["sh", "-c", "ls /etc/secret && cat /etc/secret/API_KEY && sleep 3600"]
      volumeMounts:
        - name: secret-vol
          mountPath: /etc/secret
  volumes:
    - name: config-vol
      configMap:
        name: app-config
    - name: secret-vol
      secret:
        secretName: app-secret
```

```bash
kubectl apply -f 05-deployment-mount.yaml
```

🔍 **Tip**: Esta vez no usamos variables de entorno, sino que montamos el `ConfigMap` y el `Secret` como archivos en el sistema de archivos del contenedor. Esto es útil si la aplicación espera un archivo `.env`, `.ini` o similar.

---

### 🔎 Validación 2: Leer los archivos montados

```bash
kubectl exec -it app-mount -c app -- ls /etc/config
kubectl exec -it app-mount -c app -- cat /etc/config/APP_MODE

kubectl exec -it app-mount -c secret -- ls /etc/secret
kubectl exec -it app-mount -c secret -- cat /etc/secret/API_KEY
```

✅ Resultado esperado:

```
APP_MODE
azul
API_KEY
1234-ABCD-5678
```

🔍 **Tip**: Los `ConfigMap` y `Secrets` montados como archivos se representan como archivos de solo lectura. Si cambias el contenido, Kubernetes lo actualiza automáticamente.

---

## 🧼 Limpieza final (opcional)

```bash
kubectl delete ns lab-config
```

---

## ✅ Qué ha aprendido el alumno

✔ Qué es un `ConfigMap` y cómo declararlo.
✔ Qué es un `Secret` y por qué es importante.
✔ Dos formas de inyectar configuración externa en pods:

* Como variables de entorno.
* Como archivos montados en rutas específicas.
