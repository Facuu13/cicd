
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
