# Vía Accesible — kit del sistema visual del TFM

## Contenido
- `latex/tfm-estilo.sty` — colores; gráficos de barras (vertical/horizontal, agrupado/apilado), líneas y circulares; diagramas de flujo, conceptuales, de secuencia, de red, de arquitectura y mapas; estados, Kanban, cronograma (Gantt), recuadros, tablas, código, columnas e imágenes externas.
- `latex/beamerthemeUOCTFM.sty` — tema Beamer para la defensa.
- `ejemplo_uso.tex` + `ejemplo_uso.pdf` — un ejemplo de cada pieza con la plantilla TFUOC.
- `python/tfm.mplstyle` + `python/paletas.py` — mismo estilo para matplotlib (notebooks).
- `fuentes/` — Computer Modern (CMU) en .ttf (instalar en el sistema para matplotlib) y .woff2 (web).
- `tokens.json` — todos los colores, tamaños y espaciados en formato de datos.

## Memoria (LaTeX)
1. Copia `latex/tfm-estilo.sty` en la carpeta de la plantilla, junto a `TFUOC.cls`.
2. En tu `.tex`, justo después de `\documentclass[IB]{TFUOC}`:
   `\usepackage{tfm-estilo}` (o `\usepackage[tabla]{tfm-estilo}` para rotular «Tabla» en vez de «Cuadro»).
3. Compila con pdflatex (dos pasadas). Overleaf: sube el .sty al proyecto.
4. Usa `ejemplo_uso.tex` como chuleta: copia el bloque que necesites.

## Texto a dos columnas
Solo por bloques (la memoria entera a dos columnas rompe la ficha y los gráficos):
```latex
\begin{doscolumnas}[filete=true]            % columnas=3, separacion=6mm, equilibrar=false, titulo={...}
  Texto...
  \begin{figuracolumna} \includegraphics[width=\linewidth]{figuras/x.png} \caption{...} \end{figuracolumna}
\end{doscolumnas}
```
Dentro de columnas usa `figuracolumna`/`tablacolumna` (o `figure*` a todo el ancho).

## Imágenes externas
- Guárdalas en `figuras/` (o `imagenes/`, `graficos/`) junto al .tex.
- `\figuraexterna[0.8\textwidth]{ortofoto.png}{Pie de la figura.}{fig:etiqueta}{IGN (2025), licencia.}`
- Gráficos en PDF vectorial; ortofotos y máscaras en PNG; fotos en JPG. Siempre con fuente y licencia.

## Presentación (Beamer)
Copia los dos .sty y `noulogo.png` de la plantilla:
```latex
\documentclass[aspectratio=169]{beamer}
\usepackage[spanish]{babel}
\usetheme{UOCTFM}
\logouoc{noulogo.png}
```

## Python
```python
import matplotlib.pyplot as plt
from paletas import ACC, SEG, CMAP_SEG, CMAP_SEC, superponer_mascara
plt.style.use("tfm.mplstyle")
fig.savefig("figuras/perdida.pdf")   # al ancho final, en PDF
```
Para la coma decimal: `import locale; locale.setlocale(locale.LC_NUMERIC, "es_ES.UTF-8")`.

## Estados y marcas de borrador
- `\estado{completado}` (pendiente, en-curso, revision, completado, bloqueado) en texto, tablas y Kanban.
- `\estadobloque{revision}{Qué falta}` para marcar partes en borrador; para la entrega:
  `\usepackage[final]{tfm-estilo}` y desaparecen todas.

## Componentes nuevos (ver `ejemplo_uso.pdf`, apartados 1.9–1.18)
Diagrama de flujo, esquema conceptual, estados, Kanban, recuadros, diagrama de secuencia,
barras horizontales/apiladas y líneas verticales, gráfico circular y de anillo, cronograma (Gantt) y mapa de tramos.

## Bibliografía, citas y estado del arte
- `\usepackage[bibliografia]{tfm-estilo}` + `\addbibresource{referencias.bib}` → referencias numeradas (IEEE) por orden de aparición; al final `\printbibliography[heading=bibintoc]`. Compila pdflatex → biber → pdflatex ×2.
- `referencias.bib` trae 5 referencias de ejemplo: compruébalas con la fuente antes de usarlas.
- Citas: `\citadestacada{frase}{fuente}`, `\enquote{…}~\cite{…}`, `citalarga`, `citanorma`, `\traduccionpropia`.
- Estado del arte: `\cumple{si|parcial|no|na}`, `\filapropia`, `\lineatemporal`, estilos PRISMA y `tfmdispersion`.

## Real frente a predicho
`tfmrealpredicho` + `diagonal` + `bandatolerancia`; en tablas `\tolerancia{0.3}`, `\errorval{-0.5}`, `\comparaclase{1}{2}`;
mapas `tramoacierto`/`tramosobre`/`tramosub`. En Python: `paletas.real_vs_predicho(ax, real, pred, tol=0.3)`.

## Notas
`\postit[Autor]{…}` (borrador, se oculta con `final`), `\aclaracion{…}`, `\footnote{…}`, `\notatabla{…}`.

## Listas
Las listas normales ya salen con el estilo (■ – ▪ en viñetas; 1. a) i. en numeradas). Además:
`\begin{codigos}[O]` (O1, O2… también [H], [RF], [P]; referenciables con \label/\ref), `pasos`, `ventajas`,
`inconvenientes`, `comprobacion` (`\item[\hecho]`, `\item[\parcial]`, `\item[\porhacer]`) y `enlinea` → (a), (b) y (c).
