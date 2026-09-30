# Kit del sistema visual del TFM

Sistema visual completo para el Trabajo Final de Máster (UOC, Máster en Ciencia de Datos): colores accesibles, tipografía, componentes visuales (gráficos, diagramas, tablas) y documentación de principios de diseño.

## Archivos del sistema

| Archivo | Qué es |
|---------|--------|
| `DESIGN_SYSTEM_GUIDE.md` | Principios de diseño, colores, tipografía, componentes y casos de uso. **Lee esto primero**. |
| `tokens.json` | Datos completos (colores hex, tamaños, espaciados) para importar en herramientas. |
| `latex/tfm-estilo.sty` | Paquete LaTeX con colores, estilos de TikZ y componentes. |
| `latex/beamerthemeUOCTFM.sty` | Tema Beamer para la presentación de defensa. |
| `ejemplo_uso.tex` + `.pdf` | Ejemplos prácticos de cada componente LaTeX. |
| `python/tfm.mplstyle` | Estilo matplotlib para gráficos en Jupyter. |
| `python/paletas.py` | Paletas de color y utilidades Python (máscaras, superponer). |
| `fuentes/` | Computer Modern (CMU) en .ttf y .woff2 para instalar. |

## Primeros pasos

### Memoria LaTeX

1. **Copiar el estilo:** `latex/tfm-estilo.sty` junto a `TFUOC.cls` en tu proyecto Overleaf.
2. **Cargar en tu `.tex`:** justo después de `\documentclass[IB]{TFUOC}`, añade:
   ```latex
   \usepackage{tfm-estilo}           % o [tabla] para rotular "Tabla" en vez de "Cuadro"
   ```
3. **Compilar:** pdflatex → dos pasadas (Overleaf: automático).
4. **Consultar ejemplos:** abre `ejemplo_uso.pdf`, busca el componente que necesites y copia el bloque de `ejemplo_uso.tex`.

### Presentación Beamer

```latex
\documentclass[aspectratio=169]{beamer}
\usepackage[spanish]{babel}
\usetheme{UOCTFM}
\logouoc{noulogo.png}
```

Copia `beamerthemeUOCTFM.sty` y `noulogo.png` junto a tu `.tex`.

### Python & Jupyter

```python
import matplotlib.pyplot as plt
from paletas import ACC, SEG, CMAP_SEG, CMAP_SEC, superponer_mascara
plt.style.use("tfm.mplstyle")
fig.savefig("figuras/perdida.pdf")   # guardar al ancho final, en PDF
```

Locale español: `import locale; locale.setlocale(locale.LC_NUMERIC, "es_ES.UTF-8")`

## Componentes LaTeX

### Gráficos

| Qué visualizar | Componente | En LaTeX |
|---|---|---|
| Comparación entre clases o modelos | Barras (vertical/horizontal, agrupado/apilado) | Ver `ejemplo_uso.pdf` apartado 1.9 |
| Evolución temporal o perfiles | Líneas | Ver `ejemplo_uso.pdf` apartado 1.10 |
| Composición de un total | Circular o anillo | Ver `ejemplo_uso.pdf` apartado 1.11 |
| Matriz de confusión | Matriz de calor | Usar `acc-*` o `serie-*` con escala secuencial |
| Real vs. Predicho | Dispersión + diagonal + banda | Ver `error-*` en `DESIGN_SYSTEM_GUIDE.md` |

### Diagramas

| Diagrama | Cuándo usarlo | En LaTeX |
|---|---|---|
| **Pipeline** | Explicar la arquitectura general | Bloques TikZ, `arq-modulo`, `arq-datos` |
| **Flujo** | Orden de pasos y decisiones | `flujo-decision` para rombos |
| **Red neuronal** | Capas del modelo | Bloques TikZ con `nn-*` (conv, pool, up, atención) |
| **Secuencia** | Llamadas entre componentes | Ver `ejemplo_uso.pdf` apartado 1.13 |
| **Esquema conceptual** | Taxonomía o relaciones | Ver `ejemplo_uso.pdf` apartado 1.12 |
| **Clases** | Diseño del código | Bloques `arq-modulo` |
| **Estados** | Flujo de tareas o secciones | `\estado{pendiente|en-curso|revision|completado|bloqueado}` |
| **Kanban** | Seguimiento de trabajo | Ver `ejemplo_uso.pdf` apartado 1.15 |
| **Cronograma (Gantt)** | Planificación temporal | Ver `ejemplo_uso.pdf` apartado 1.16 |

### Tablas y contenido

| Componente | Uso |
|---|---|
| **Tablas** | `booktabs` (sin líneas verticales), cabecera sobre `uoc-cian-suave` |
| **Dos columnas** | Solo bloques: `\begin{doscolumnas}[filete=true]` (no toda la memoria) |
| **Recuadros** | Definiciones e hipótesis; usa `\aclaracion{}` o `\recuadro{}` |
| **Notas** | `\postit[Autor]{…}` (desaparece con `\usepackage[final]{tfm-estilo}`) |
| **Listas** | Viñetas automáticas (■–▪); `\pasos`, `\ventajas`, `\inconvenientes` |
| **Código** | `listings` o `minted` con estilo `tfmcodigo` |

### Imágenes externas

```latex
\figuraexterna[0.8\textwidth]{ortofoto.png}{Pie de la figura.}{fig:etiqueta}{IGN (2025), licencia.}
```

- Ubicación: `figuras/`, `imagenes/` o `graficos/` junto al `.tex`.
- Formatos: gráficos en **PDF** vectorial; ortofotos y máscaras en **PNG**; fotos en **JPG**. Siempre con fuente y licencia.
- Mosaicos: usa `subfigure` con columnas iguales (paquete `subcaption`, ya cargado).

## Referencias y estado del arte

### Configurar bibliografía

```latex
\usepackage[bibliografia]{tfm-estilo}
\addbibresource{referencias.bib}
% al final del documento:
\printbibliography[heading=bibintoc]
```

Compila: pdflatex → biber → pdflatex ×2 (en Overleaf es automático).

### Componentes para referencias

| Tarea | Comando |
|---|---|
| Cita estándar | `\cite{ref}` (número IEEE tras autor o frase: «Xie et al. [1]») |
| Cita textual | `\enquote{…}~\cite{…}` |
| Cita de norma | `\citanorma{ref}` |
| Traducción propia | `\traduccionpropia` |
| Matriz de literatura | `\cumple{si|parcial|no|na}` + `\filapropia` |
| Línea temporal | `\lineatemporal` |
| Diagrama PRISMA | Ver `ejemplo_uso.pdf` apartado 1.14 |

## Validación y borrador

| Marca | Usos | Comando |
|---|---|---|
| **Estados** | Completado, pendiente, en revisión… | `\estado{completado}` |
| **Bloque de borrador** | Marcar secciones incompletas | `\estadobloque{revision}{Qué falta}` |
| **Post-it** | Notas temporales (desaparece con `final`) | `\postit[Autor]{…}` |
| **Aclaración** | Llamada de atención | `\aclaracion{…}` |

Para ocultar borradores en la entrega: `\usepackage[final]{tfm-estilo}`

## Colores y tipografía

Consulta la **sección «Color» y «Tipografía»** en `DESIGN_SYSTEM_GUIDE.md` para:
- Cuándo usar cada color de accesibilidad (`acc-*`), segmentación (`seg-*`), serie (`serie-*`) y estado.
- Familias tipográficas (serif para memoria, sans para figuras).
- Contraste WCAG 2.1 y daltonismo: todas las parejas de color están validadas.
- Redundancia obligatoria: color + texto, color + marcador, color + patrón.

## Cómo añadir un componente nuevo

1. **Define el principio:** ¿qué visualiza? (proceso, estado, comparación…)
2. **Sigue la escalera de color:**
   - ¿Existe una familia (`acc-*`, `seg-*`, `serie-*`) con el mismo significado? Reutiliza.
   - ¿Es nuevo? Crea la paleta en `tokens.json` con contraste ≥ 4.5:1 (WCAG AA).
   - Valida en gris y con Color Oracle (protanopia, deuteranopia, tritanopia).
3. **Define el trazo:** línea, marcador, patrón o glifo para redundancia de color.
4. **Implementa en LaTeX:** añade estilos TikZ a `latex/tfm-estilo.sty`.
5. **Documenta:** añade comando, ejemplo en `ejemplo_uso.tex` y entrada en `DESIGN_SYSTEM_GUIDE.md`.
6. **Prueba:** compila con `pdflatex` ×2 y verifica en pantalla + impreso.

## Propuesta: Documentación interactiva en HTML

El sistema actual (Markdown + LaTeX + JSON) es sólido, pero un **sitio HTML interactivo** facilitaría:

✓ **Visualización de colores** con código hex, contraste real y simulación de daltonismo  
✓ **Tipografía en acción** con tamaños y espaciados interactivos  
✓ **Galería de componentes** con ejemplos renderizados (no solo capturas PDF)  
✓ **Copiar/pegar fácil** de código LaTeX y valores de tokens  
✓ **Búsqueda** por componente o caso de uso  

### Alternativa lazy (sin HTML por ahora)
- **GitHub Pages + Markdown** con rendered tokens.json
- **Print friendly** de DESIGN_SYSTEM_GUIDE.md
- Script Python para exportar paleta a Figma/Adobe Color

¿Quieres que cree la versión HTML, o te parece mejor mejorar otro aspecto primero?
