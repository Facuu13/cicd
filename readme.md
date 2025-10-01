
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

# 🔹 Tema 5: CI con **tests de Python** (pytest)

## 1) Concepto rápido

* En CI, los **tests** se ejecutan automáticamente en cada push/PR.
* Si un test falla, el pipeline marca **FAIL** y te avisa antes de mergear/deployar.
* Herramientas típicas: **pytest** (tests), **coverage** (cobertura), **flake8/ruff** (lint).

---

## 2) Ejemplo real y sencillo

### 📂 Estructura mínima

```
.
├── app.py
├── tests/
│   └── test_app.py
└── .github/
    └── workflows/
        └── ci-python-tests.yml
```

### `app.py` (código a testear)

```python
def sumar(a, b):
    return a + b

def es_par(n):
    return n % 2 == 0
```

### `tests/test_app.py` (pytest)

```python
import app

def test_sumar():
    assert app.sumar(2, 3) == 5

def test_es_par_true():
    assert app.es_par(4) is True

def test_es_par_false():
    assert app.es_par(5) is False
```

> Podés correrlos localmente con:
>
> ```bash
> pip install pytest
> pytest -q
> ```

---

## 3) Workflow CI en GitHub Actions

### `.github/workflows/ci-python-tests.yml`

```yaml
name: CI Python - Tests

on:
  push:
    paths: ["**/*.py", ".github/workflows/ci-python-tests.yml"]
  pull_request:
    paths: ["**/*.py"]

jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout código
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Instalar deps
        run: |
          python -m pip install --upgrade pip
          pip install pytest

      - name: Correr tests
        run: pytest -q
```

👉 ¿Qué hace?

1. Se dispara en cada push/PR que toque archivos `.py`.
2. Levanta un runner Ubuntu.
3. Instala Python + pytest.
4. Corre los tests y muestra el reporte en **Actions**.

---

## 4) (Opcional) Matrix de versiones de Python

Para probar contra múltiples versiones (útil en libs):

```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]

steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

---

## 5) (Opcional) Cobertura y artifact del reporte

Añadí cobertura con `coverage.py` y guardá el HTML como artifact.

```yaml
      - name: Instalar deps (pytest + coverage)
        run: |
          python -m pip install --upgrade pip
          pip install pytest coverage

      - name: Correr tests con cobertura
        run: |
          coverage run -m pytest -q
          coverage html  # genera carpeta htmlcov/

      - name: Subir reporte de cobertura
        uses: actions/upload-artifact@v4
        with:
          name: coverage-html
          path: htmlcov
```

Luego vas a **Actions → (run) → Artifacts** y descargás `coverage-html` para abrir `index.html` localmente.

---

## 6) (Opcional) Lint rápido (calidad de código)

Agregá **ruff** (o flake8) para chequeos estáticos:

```yaml
      - name: Lint (ruff)
        run: |
          pip install ruff
          ruff check .
```

---

## 7) Resumen

* **pytest** valida tu lógica automáticamente.
* **Artifacts** (reporte HTML de cobertura) te dan visibilidad extra.
* **Paths** evitan correr pipelines innecesarios.
* Esto ya es CI “de verdad”: validación automática en cada cambio.

---

# 🔹 Tema 6: Triggers (cuándo corre un pipeline)

En GitHub Actions (y en la mayoría de sistemas CI/CD como GitLab o Jenkins) los pipelines no corren solos, se disparan con **eventos**.

---

## 1) **push**

Se ejecuta cada vez que hacés `git push`.

```yaml
on: [push]
```

### Ejemplo con ramas específicas:

```yaml
on:
  push:
    branches: ["main", "develop"]
```

👉 Corre solo si pusheás a `main` o `develop`.

---

## 2) **pull_request**

Se ejecuta cuando alguien abre un **PR** (pull request).
Muy usado para **validar antes de mergear**.

```yaml
on:
  pull_request:
    branches: ["main"]
```

👉 Antes de fusionar a `main`, se corren tests automáticamente.

---

## 3) **workflow_dispatch**

Permite ejecutar el pipeline **a mano**, desde la interfaz de GitHub.
Ideal para cosas que no querés que se ejecuten siempre.

```yaml
on:
  workflow_dispatch:
```

👉 En la pestaña **Actions** te aparece un botón **“Run workflow”** para lanzarlo cuando quieras.

Incluso podés agregar **inputs** (ej: elegir versión o entorno):

```yaml
on:
  workflow_dispatch:
    inputs:
      env:
        description: "Entorno"
        required: true
        default: "dev"
```

---

## 4) **schedule**

Permite programar pipelines como un **cronjob**.
Ejemplo: correr todas las noches a las 3 AM UTC:

```yaml
on:
  schedule:
    - cron: "0 3 * * *"
```

👉 Muy útil para:

* Correr tests nocturnos.
* Limpiar caches.
* Hacer builds periódicos.

---

## 5) **Otros triggers útiles**

* **release** → cuando creás un release en GitHub.

```yaml
on:
  release:
    types: [published]
```

* **tag push** → cuando subís un tag (ej: `v1.0.0`).

```yaml
on:
  push:
    tags:
      - "v*"
```

👉 Esto es clave en proyectos de firmware: podés compilar y generar el binario **solo cuando marcás una versión**.

---

## 🧩 Ejemplo práctico con varios triggers juntos

```yaml
on:
  push:
    branches: ["main", "develop"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:
  schedule:
    - cron: "0 3 * * *"
```

Este workflow corre cuando:

* Hacés push a `main` o `develop`.
* Hacés un PR hacia `main`.
* Lo corrés a mano.
* O se ejecuta automáticamente todos los días a las 3 AM UTC.

---

✅ Resumen rápido:

* `push` → cada vez que subís cambios.
* `pull_request` → antes de mergear.
* `workflow_dispatch` → manual.
* `schedule` → programado (cron).
* `release` / `tags` → versiones y entregas.

---

# 📝 Machete CI/CD para entrevistas

## 🔹 ¿Qué es CI/CD?

* **CI (Continuous Integration):**
  Cada vez que alguien hace `git push`, el sistema compila y corre tests automáticamente → detecta errores rápido.
* **CD (Continuous Delivery/Deployment):**
  Después de CI, el sistema empaqueta (ej: binario, imagen Docker) y lo deja listo para desplegar o lo despliega directo.

👉 CI = integrar sin romper.
👉 CD = entregar rápido y de forma confiable.

---

## 🔹 Componentes básicos de un pipeline

* **Workflow:** el archivo YAML que define el pipeline.
* **Job:** una tarea grande (build, test, deploy).
* **Step:** comandos dentro de un job (ej: `pip install`, `pytest`).
* **Runner:** máquina donde corre (Ubuntu, Windows, Mac, o self-hosted).
* **Artifact:** archivo generado (ej: binario `.bin`, reporte de cobertura).

---

## 🔹 Triggers comunes

* `push` → cada vez que subís cambios.
* `pull_request` → validar antes de mergear.
* `workflow_dispatch` → correrlo manualmente.
* `schedule` → programado (cron).
* `release` / `tags` → cuando creás una versión nueva.

---

## 🔹 Ejemplo ultra simple (Python hello)

```yaml
name: CI Python

on: [push]

jobs:
  python-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: "3.11"
      - run: python hello.py
```

---

## 🔹 Ejemplo con tests (pytest)

```yaml
- name: Instalar dependencias
  run: pip install pytest

- name: Correr tests
  run: pytest -q python_app/tests
```

---

## 🔹 Ejemplo con artifact

```yaml
- run: echo "Soy un firmware falso 🚀" > firmware.bin
- uses: actions/upload-artifact@v3
  with:
    name: firmware
    path: firmware.bin
```

---

## 🔹 Ejemplo con paths

```yaml
on:
  push:
    paths:
      - "python_app/**"   # solo si cambia código Python
```

---

## 🔹 Cómo lo explicar en 30 segundos

*"CI/CD son prácticas para automatizar compilación, pruebas y despliegues.
En CI, cada push dispara un pipeline que corre tests o compila el código.
En CD, ese resultado se empaqueta y se entrega automáticamente (como binarios o imágenes Docker).
Yo armé pipelines con GitHub Actions, configurando jobs que ejecutan scripts de Python y C, con filtros por paths y artifacts descargables. También sé usar triggers como push, PR o manual dispatch."*

---
¡De una, Facu! 🙌
Te armo el **machete de Docker básico** — mismo estilo que el de CI/CD, para que tengas lo fundamental bien claro y listo para entrevistas o práctica.

---

# 🐳 Machete Docker para entrevistas

## 🔹 ¿Qué es Docker?

* Plataforma para **empaquetar aplicaciones en contenedores**.
* Un **contenedor** incluye tu app + dependencias + librerías + sistema base → corre igual en cualquier entorno.
* Diferencia con una **VM**: la VM emula todo un sistema operativo → más pesado. Docker usa el kernel del host → más liviano y rápido.

👉 Frase corta: *“Docker asegura que mi aplicación corra igual en mi PC, en un server o en la nube.”*

---

## 🔹 Conceptos clave

* **Imagen**: plantilla de solo lectura (ej: `python:3.11`).
* **Contenedor**: instancia en ejecución de una imagen.
* **Dockerfile**: receta para construir imágenes.
* **Registry**: repositorio de imágenes (ej: Docker Hub).

---

## 🔹 Comandos esenciales

```bash
# correr un contenedor simple
docker run hello-world

# correr interactivo con bash
docker run -it ubuntu bash

# listar contenedores en ejecución
docker ps

# listar TODOS los contenedores (incluye los detenidos)
docker ps -a

# detener un contenedor
docker stop <id>

# borrar un contenedor
docker rm <id>

# listar imágenes locales
docker images

# borrar una imagen
docker rmi <id>
```

---

## 🔹 Crear tu propia imagen (Dockerfile mínimo)

**Dockerfile**

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

**app.py**

```python
print("Hola Facu desde Docker 🚀")
```

**Construcción y ejecución**

```bash
docker build -t facu_app .
docker run facu_app
```

👉 Eso genera tu propia imagen (`facu_app`) y la ejecuta como contenedor.

---

## 🔹 Mapear puertos y volúmenes

* Mapear puertos:

```bash
docker run -p 8080:80 nginx
```

👉 accedés en `http://localhost:8080` a Nginx dentro del contenedor.

* Montar volumen:

```bash
docker run -v $(pwd):/app ubuntu
```

👉 compartís tu carpeta actual con `/app` en el contenedor.

---

## 🔹 Casos típicos en entrevistas

1. **Levantar un servicio IoT**:

   ```bash
   docker run -p 1883:1883 eclipse-mosquitto
   ```

   👉 broker MQTT en segundos.

2. **Dashboard Node-RED**:

   ```bash
   docker run -p 1880:1880 nodered/node-red
   ```

   👉 sin instalar nada en tu máquina.

3. **Workflow CI/CD**:

   * GitHub Actions → build de imagen Docker.
   * Push a DockerHub.
   * Deploy automático.

---

## 🔹 Cómo lo explicás en entrevista

*"Docker me permite empaquetar mis apps en contenedores que corren igual en cualquier entorno.
Sé crear imágenes con Dockerfile, correr servicios como Mosquitto o Node-RED en contenedores, mapear puertos y usar volúmenes.
También puedo integrar Docker con CI/CD, para construir y publicar imágenes automáticamente en DockerHub."*

---