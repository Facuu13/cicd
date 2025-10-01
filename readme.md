
---

# 🔹 Tema 1: ¿Qué es CI/CD?

### 1. Concepto teórico

* **CI (Continuous Integration)** = Integración Continua.
  Cada vez que subís código a un repositorio (ej: GitHub/GitLab), se ejecutan **automatizaciones**:

  * Compilar el proyecto
  * Correr tests
  * Analizar calidad del código
    👉 Así se detectan errores rápido y no cuando ya está todo desplegado.

* **CD (Continuous Delivery / Deployment)** = Entrega/Despliegue Continuo.
  Después de que el código pasó las pruebas, se **empaqueta y despliega automáticamente** en un entorno (testing, staging o producción).

⚡ Ejemplo de la vida real (sin código todavía):

* Tenés un repo con un firmware o con una web.
* Hacés un `git push origin main`.
* Automáticamente, un sistema (ej: GitHub Actions, GitLab CI, Jenkins) se encarga de:

  1. Compilar el código.
  2. Testearlo.
  3. Subir el binario/imagen Docker/paquete a un servidor.

Esto elimina pasos manuales, reduce errores y acelera el desarrollo.

---

### 2. Ejemplo práctico (nivel súper básico)

Si usás **GitHub**, ya podés probar CI con casi nada:

1. Creá un repo en GitHub con un archivo `hello.py`:

   ```python
   print("Hola Facu desde CI/CD 🚀")
   ```

2. Dentro del repo, creá una carpeta:

   ```
   .github/workflows/
   ```

3. Y dentro un archivo `ci.yml` con esto:

   ```yaml
   name: Mi primer CI

   on: [push]   # cada vez que hago git push

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout código
           uses: actions/checkout@v2

         - name: Instalar Python
           uses: actions/setup-python@v2
           with:
             python-version: "3.11"

         - name: Ejecutar script
           run: python hello.py
   ```

👉 Con solo subir eso a GitHub, cada vez que hagas `git push` se va a ejecutar un **workflow** que corre tu script automáticamente.

---

Esto sería tu **primer pipeline CI/CD**: súper simple pero ya muestra el concepto.

---

# 🔹 Tema 2: CI vs CD (qué cambia y cómo se usan)

### 1. CI (Continuous Integration)

Ya lo viste en el ejemplo anterior:

* Cada vez que hacés `git push`, se corre un **pipeline** que compila o prueba tu código automáticamente.
* Te asegura que el código **siempre se pueda integrar** con la rama principal sin romper nada.

Ejemplo en tu caso:

* Subís un cambio a un módulo en Python o C.
* GitHub Actions compila el código o corre `pytest`.
* Si algo falla, lo ves al toque.

👉 **CI = testear y validar cada cambio automáticamente.**

---

### 2. CD (Continuous Delivery / Continuous Deployment)

Esto es el **paso siguiente**.

* **Continuous Delivery**: después de que pasa CI, el sistema genera un **paquete listo para desplegar** (ej: un `.bin` para un ESP32, una imagen Docker, o un `.deb` para Linux). El despliegue todavía puede ser manual.
* **Continuous Deployment**: va un paso más: además de generar el paquete, lo **publica automáticamente en el entorno final** (servidor, nube, producción).

---

### 3. Ejemplo concreto para vos

Imaginemos que tenés un **firmware para ESP32** y una **app web de monitoreo**:

* **CI**:

  * Se compila el firmware cada vez que hacés un push.
  * Se corren tests unitarios de la app web.

* **CD**:

  * Se genera el `.bin` del firmware y se guarda como **artifact** en GitHub (para que vos o el equipo lo descarguen).
  * Se construye una imagen Docker de la app web y se sube a **Docker Hub**.
  * Incluso se podría desplegar esa imagen automáticamente en un servidor de prueba o producción.

---

### 4. Ejemplo práctico (paso más allá del hello.py)

En vez de solo correr `hello.py`, ahora agregamos un paso de “build + artifact”:

```yaml
name: CI/CD demo

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Compilar código (ejemplo simple)
        run: |
          echo "Compilando..."
          mkdir build
          echo "Soy un binario falso 🚀" > build/firmware.bin

      - name: Guardar artifact
        uses: actions/upload-artifact@v3
        with:
          name: firmware
          path: build/firmware.bin
```

👉 ¿Qué pasa acá?

1. Cada push crea un archivo `firmware.bin`.
2. GitHub lo guarda como **artifact**.
3. Vos podés entrar a la pestaña **Actions** y descargar ese binario.

Ese sería un ejemplo **Continuous Delivery**: siempre tenés un binario listo para bajar.

---

✅ Resumen fácil:

* **CI** = compilo/testeo cada cambio.
* **CD** = genero un paquete/binario listo para usar (y a veces lo despliego solo).

---

# 🔹 Tema 3: Cómo se arma un pipeline de CI/CD

Un **pipeline** es como una receta de cocina:

* Se define en un archivo (ej: YAML en GitHub Actions).
* Tiene **jobs** (trabajos grandes).
* Cada job tiene **steps** (pasos concretos).
* Se ejecutan en un **runner** (máquina virtual o contenedor donde se corren los pasos).

---

## 1. Jobs

* Un **job** es un conjunto de pasos que se ejecutan en una misma máquina virtual.
* Ejemplo: un job de **compilar** y otro job de **testear**.
* Los jobs se pueden correr en paralelo o en secuencia.

```yaml
jobs:
  build:     # primer job
    runs-on: ubuntu-latest
    steps:
      - run: echo "Compilando código"

  test:      # segundo job
    runs-on: ubuntu-latest
    steps:
      - run: echo "Corriendo tests"
```

👉 Cuando hacés push, vas a ver dos cajitas en GitHub Actions: **build** y **test**.

---

## 2. Steps

* Dentro de cada job hay **steps** (pasos).
* Los steps pueden ser:

  * Un comando `run` (ej: `python main.py`)
  * Una **acción reutilizable** (ej: `actions/checkout@v2`)

Ejemplo mini-pipeline:

```yaml
jobs:
  demo:
    runs-on: ubuntu-latest
    steps:
      - name: Primer paso
        run: echo "Hola Facu 🚀"
      - name: Segundo paso
        run: echo "Este es otro paso"
```

---

## 3. Runners

* El **runner** es la máquina donde se ejecuta todo.
* GitHub te da runners listos: Ubuntu, Windows, Mac.
* También podés tener **self-hosted runners** (ej: tu propia PC o un servidor).

Ejemplo:

```yaml
runs-on: ubuntu-latest   # usa un runner Ubuntu en la nube
```

---

## 4. Artifacts

* Un **artifact** es un archivo que se genera en el pipeline y que podés descargar después.
* Ejemplo típico: compilar un binario, guardar logs, exportar un reporte.

```yaml
- name: Generar archivo
  run: echo "Soy un binario falso" > output.bin

- name: Guardar artifact
  uses: actions/upload-artifact@v3
  with:
    name: mi-binario
    path: output.bin
```

👉 Después del pipeline, vas a la pestaña **Actions → Run → Artifacts** y descargás `mi-binario.zip`.

---

## 🧩 Resumen fácil

* **Pipeline** = receta de pasos.
* **Jobs** = tareas grandes (compilar, testear, desplegar).
* **Steps** = pasos concretos dentro de cada tarea.
* **Runner** = la máquina que ejecuta todo.
* **Artifact** = archivo que guardás del pipeline.

---

# 🔹 Tema 4: Ejemplos de Pipelines Sencillos

---

## 🟢 Ejemplo 1: Pipeline con un solo Job

Este es el más básico: cada vez que hago `git push`, se ejecuta un job que imprime algo.

```yaml
name: Ejemplo simple

on: [push]   # se ejecuta cuando hago git push

jobs:
  hola:
    runs-on: ubuntu-latest
    steps:
      - name: Mostrar mensaje
        run: echo "Hola Facu 🚀, este es mi primer pipeline"
```

👉 Qué hace:

1. Cuando hacés `git push`, GitHub corre este workflow.
2. Se levanta una máquina Ubuntu.
3. Ejecuta el comando `echo "Hola Facu 🚀, este es mi primer pipeline"`.
4. Podés ver el resultado en la pestaña **Actions** de tu repo.

---

## 🟡 Ejemplo 2: Pipeline con 2 Jobs en paralelo

Ahora agregamos dos jobs que se ejecutan al mismo tiempo: uno compila y otro testea.

```yaml
name: Ejemplo con 2 jobs

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Compilar código
        run: echo "Compilando proyecto..."

  test:
    runs-on: ubuntu-latest
    steps:
      - name: Ejecutar tests
        run: echo "Corriendo tests..."
```

👉 Qué pasa:

* Job **build** y job **test** se ejecutan en paralelo.
* En la interfaz de GitHub Actions ves **dos cajitas**: cada una con su salida.
* En un proyecto real, el primero podría compilar firmware y el segundo correr unit tests.

---

## 🔵 Ejemplo 3: Pipeline con Artifact

Ahora generamos un archivo (como si fuera un binario de firmware) y lo guardamos.

```yaml
name: Ejemplo con artifact

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Crear archivo binario
        run: |
          mkdir build
          echo "Soy un firmware falso 🚀" > build/firmware.bin

      - name: Guardar artifact
        uses: actions/upload-artifact@v3
        with:
          name: firmware
          path: build/firmware.bin
```

👉 Qué hace:

1. Crea una carpeta `build` y un archivo `firmware.bin`.
2. Lo guarda como **artifact**.
3. Al terminar, vas a **Actions → Run → Artifacts** y lo podés descargar.

En un proyecto real, ahí estaría el `.bin` del ESP32 o una imagen Docker.

---

## 🧩 Resumen

* Con **Ejemplo 1** entendés la mecánica básica.
* Con **Ejemplo 2** ves que podés dividir el trabajo en varios jobs.
* Con **Ejemplo 3** aprendés cómo generar y guardar resultados (artifacts).

---
