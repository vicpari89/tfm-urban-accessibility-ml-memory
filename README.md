# Identificación y Caracterización de Vías Accesibles mediante Algoritmos de Visión por Computadora

**Trabajo Fin de Máster en Ciencia de Datos** — UOC  
Autor: Víctor Pariente González  
Tutor: Antonio Ruiz Falcó Rojas  
Fecha: Septiembre 2026 - Enero 2027

---

## Descripción breve



---

## Tabla de contenidos

- [Requisitos previos](#requisitos-previos)
- [Instrucciones de construcción](#instrucciones-de-construcción)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Contenido de la memoria](#contenido-de-la-memoria)
- [Resultados principales](#resultados-principales)
- [Código fuente](#código-fuente)
- [Productos generados](#productos-generados)
- [Cómo citar](#cómo-citar)
- [Autores y agradecimientos](#autores-y-agradecimientos)
- [Licencia](#licencia)

---

## Resultados principales

*Actualizar con los resultados finales del trabajo*

---

## Requisitos previos

Para compilar la memoria en LaTeX y trabajar con los ficheros fuente, necesitas:

- **LaTeX distribution** (TeX Live, MiKTeX o MacTeX)
  - En sistemas Ubuntu: `sudo apt-get install texlive-full`

- **latexmk** (gestor automático de compilación)
  - Incluido en la mayoría de distribuciones de LaTeX
  - Si utilizas Visual Studio Code, puedes instalar la extensión LaTeX Workshop.

---

## Instrucciones de construcción

### Generar el PDF de la memoria

```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd tfm-victor-pariente-ciencia-de-datos-uoc

# Compilar el documento
latexmk -pdf TFM_Victor_Pariente_Gonzalez.tex

# El PDF generado estará en: build/TFM_Victor_Pariente_Gonzalez.pdf
```

**Nota**: La primera compilación puede tardar varios minutos mientras LaTeX descarga y procesa todas las dependencias.

### Limpiar caché y archivos temporales

```bash
# Opción 1: limpiar con latexmk
latexmk -C

# Opción 2: limpiar completamente el directorio build
rm -rf build/
mkdir -p build
```

---

## Estructura del repositorio

```
.
├── TFM_Victor_Pariente_Gonzalez.tex         # Documento principal LaTeX
├── capitulos/                               # Capítulos de la memoria
│   ├── 01-introduccion/
│   │   ├── 01-introduccion.tex             # Capítulo: Introducción y motivación
│   │   └── figuras/                        # Figuras específicas de este capítulo
│   ├── 02-01-marco-legal/
│   │   ├── 02-01-marco-legal.tex           # Normativa y requisitos legales
│   │   └── figuras/
│   ├── 02-02-caracteristicas-accesibilidad/
│   │   ├── 02-02-caracteristicas-accesibilidad.tex
│   │   └── figuras/                        # vados.tex, obras.tex, etc.
│   ├── 03-estado-del-arte/
│   ├── 04-arquitectura-del-sistema/
│   ├── 05-diseno-implementacion/
│   ├── 06-resultados-evaluacion/
│   ├── 07-conclusiones-trabajos-futuros/
│   ├── 08-glosario/
│   ├── 09-bibliografia/
│   └── appendix-generative-ai/
├── figuras/                                 # Imágenes globales (no específicas de capítulos)
├── plantilla-uoc/                           # Plantilla LaTeX de UOC
├── build/                                   # Directorio de salida (archivos compilados)
├── referencias.bib                          # Base de datos bibliográfica
└── .latexmkrc                               # Configuración de compilación

```

---

## Contenido de la memoria

### 1. Introducción
Contextualización del problema, motivación y objetivos del trabajo.

### 2. Características de vías accesibles. Marco legal y normativo
Revisión de la normativa legal estatal sobre las vías urbanas accesibles.
Requisitos técnicos de las características de las vías accesibles.

### 3. Estado del arte
Análisis de textos científicos que aborden problemas similares y puedan servir de base para este trabajo.

### 4. Arquitectura del sistema
Descripción del sistema en su conjunto: desde el tratamiento de datos, segentación semántica, clasificación y evaluación.

### 5. Diseño e implementación de los algoritmos
Diagramas de diseño, secuencia y clase con los detalles técnicos de los modelos utilizados, y las estrategias de entrenamiento, predicción y evaluación utilizadas.

### 6. Resultados y evaluación
Resultados de las predicciones y evaluación del rendimiento y precisión.

### 7. Conclusiones y trabajos futuros
Conclusiones y aprendizajes tras la elaboración del proyecto y futuras líneas de investigación o desarrollo.

### 8. Glosario
Diccionario de consulta útil para definiciones de términos y siglas.

### 9. Bibliografía
Listado de todas las referencias utilizadas en la realización del trabajo.

---

## Resultados principales

### Figuras y visualizaciones
Las figuras generadas durante el trabajo se encuentran en el directorio `figuras/`.

---

## Código fuente

El código de los algoritmos estará en repositorios separados específicos:

- **tfm-urban-accessibility-ml**
  - Link: `https://github.com/vicpari89/tfm-urban-accessibility-ml`
  - Descripción: `Repositorio con las transformaciones de datos y los modelos`

*Nota: pendiente de actualizar*

---

## Productos generados

Los siguientes productos/artefactos se encuentran en:

*Nota: pendiente de actualizar*

---

## Cómo citar

Si utilizas este trabajo en tu investigación, por favor cítalo como:

```bibtex
@mastersthesis{pariente2026,
  author = {Pariente González, Víctor},
  title = {Pendiente},
  school = {Universitat Oberta de Catalunya},
  year = {2026},
  month = {September}
}
```

---

## Autores y agradecimientos

**Autor:** Víctor Pariente González

**Tutor:**
- Antonio Ruiz Falcó Rojas

**Agradecimientos:** 

---

## Licencia

Este trabajo está licenciado bajo Creative Commons Atribución (CC BY).

Consulta el archivo de licencia completo en la memoria PDF para más detalles sobre las condiciones de uso y distribución.

---

## Contacto y preguntas

Para preguntas sobre el contenido de este trabajo o colaboraciones futuras:
- Email: vicpari@uoc.edu

---

**Última actualización:** Septiembre 2026
