Sistema visual del Trabajo Final de Máster (Máster en Ciencia de Datos, UOC) sobre clasificación de la accesibilidad de calles a partir de imágenes aéreas de alta resolución mediante segmentación semántica. Parte de la plantilla LaTeX oficial `TFUOC.cls` en castellano (`\documentclass[IB]{TFUOC}`) y la extiende a gráficos, infografías, diagramas de redes neuronales, diagramas de arquitectura y de código, y a la presentación de la defensa. Todo tiene que parecer salido del mismo documento.

## Principios

- **La memoria manda.** Cualquier pieza (gráfico, diagrama, diapositiva) debe poder insertarse en la memoria sin retoques: fondo `papel`, tipografía Computer Modern, azul `uoc-azul` como único color de identidad fuerte.
- **El color significa algo.** Cada familia de color tiene un único significado: `acc-*` es la clase de accesibilidad de un tramo, `seg-*` es una clase de segmentación, `serie-*` distingue modelos o experimentos, `nn-*` y `arq-*` tipos de bloque en diagramas. No mezclar familias en una misma figura salvo que la figura relacione ambas cosas (p. ej. máscara → clase de tramo).
- **Nunca solo color.** Toda clase, serie o estado lleva también una palabra, un patrón o una forma de marcador. Las figuras se imprimirán y las leerán personas con daltonismo.
- **Sobrio y académico.** Sin degradados, sombras, emojis ni esquinas redondeadas grandes. Rectángulos rectos (`radius-0`) para todo lo que es identidad; `radius-sm`/`radius-md` solo en nodos de diagramas.

## Tono y redacción

- Todo en castellano: memoria, ejes, leyendas, pies, diagramas y diapositivas. La clase rotula «Capítulo», «Figura», «Índice de figuras» y (por defecto) «Cuadro»; `\usepackage[tabla]{tfm-estilo}` cambia a «Tabla». Elige una y úsala también en el texto.
- Términos técnicos sin traducción asentada en inglés y en cursiva la primera vez: *encoder*, *skip connection*, *ground truth*; los consolidados, en castellano: segmentación semántica, red neuronal, conjunto de validación, época, pérdida.
- Pies de figura en frase completa, mayúscula inicial y punto final: «Figura 4.1: IoU por clase en el conjunto de validación.». Cada figura se cita en el texto antes de aparecer («como muestra la figura 4.1»).
- Todo eje lleva título y unidades entre paréntesis: «Distancia (m)», «Pérdida (u.a.)», «Época». Métricas con su sigla estándar: IoU, mIoU, F1; «precisión» y «exhaustividad (recall)».
- Nombres de clases de accesibilidad fijos: **Accesible · Practicable · Deficiente · No accesible · Sin datos**. No inventar sinónimos.
- **Coma decimal** y espacio fino como separador de millares: 0,82; 12 500 m. Dos decimales para métricas; porcentajes con espacio: 37 %. `tfm-estilo` ya pone la coma en pgfplots; en matplotlib, ver `tfm.mplstyle`. Los valores de las vistas previas son de ejemplo, nunca resultados.
- Identificadores de código (clases, funciones, variables) tal como están en el repositorio, en `\texttt{}`.

## Color

- Texto de cuerpo en `tinta` sobre `papel`. Texto secundario (ejes, marcas, fuentes) en `tinta-suave`.
- Títulos de capítulo, sección y subsección, cabecera y pie en `uoc-azul` (lo aplica `TFUOC.cls`). El cuerpo, en `tinta`.
- `uoc-gris` solo para el panel de datos de la portada, que genera la clase.
- `uoc-cian` (logotipo) y `uoc-cian-filete` (filetes y bloque del título de la portada) solo como campos o filetes: portada, bloque de infografía, diapositiva de título. Nunca texto cian.
- Fondos suaves: `uoc-cian-suave` para cabeceras de tabla y datos, `uoc-azul-suave` para recuadros destacados. Encima, siempre `tinta` o `uoc-azul`.
- **Escala de accesibilidad (ordinal, apta para daltonismo):** `acc-accesible` → `acc-practicable` → `acc-deficiente` → `acc-no-accesible`, más `acc-sin-datos` con rayado. Es divergente: azules = buena accesibilidad, naranjas = mala; los extremos son oscuros y los centrales claros, así que se distingue también en escala de grises. Texto sobre `acc-accesible` y `acc-no-accesible`: `papel`; sobre `acc-practicable` y `acc-deficiente`: `tinta`.
- **Clases de segmentación:** `seg-calzada`, `seg-acera`, `seg-paso-peatones`, `seg-vegetacion`, `seg-edificio`, `seg-vehiculo`, `seg-obstaculo`, `seg-sombra`. Superpuestas a la ortofoto con 50 % de opacidad y contorno de 1 px del mismo color al 100 %. En leyendas sobre `papel`, cada muestra lleva borde `tinta-suave` de `trazo`. El fondo / ignorado (índice 255) no se pinta.
- **Series de gráficos:** `serie-1` (modelo propuesto), `serie-2`, `serie-3`, `serie-4` y `serie-base` (referencia, siempre discontinua). Cambia también el marcador (●, ■, ▲, ◆) en cada serie. Máximo cuatro series más la base por gráfico.
- **Diagramas de red:** `nn-conv`, `nn-pool`, `nn-up`, `nn-atencion` con borde `uoc-azul`; `nn-skip` discontinuo para conexiones residuales/skip; `nn-salida` con texto `papel`.
- **Estados** (tareas, objetivos, secciones en borrador): `estado-pendiente`, `estado-en-curso`, `estado-revision`, `estado-completado`, `estado-bloqueado`, cada uno con su `-fondo`. Siempre como etiqueta completa: glifo de progreso (○ ◑ ◕ ● ⊗) + texto + color, con texto `tinta` sobre el fondo. Solo para estados: nunca en gráficos.
- **Real frente a predicho:** `error-sobreestima` (naranja, ▲: la predicción excede lo real, falso positivo), `error-subestima` (azul, ▼ o discontinuo: se queda corta, falso negativo), `error-acierto` (gris) y `error-tolerancia` (banda). Misma convención en gráficos, tablas, mapas y máscaras de error; nunca mezclados con `acc-*` o `seg-*` en la misma figura.
- **Diagramas de flujo:** mismas formas que la arquitectura más `flujo-decision` para el rombo de decisión; los algoritmos o modelos van con doble borde sobre `nn-conv`.
- **Diagramas de arquitectura y código:** `arq-modulo` para procesos, módulos y clases; `arq-datos` para datasets, ficheros y modelos entrenados; `arq-externo` (borde `acc-deficiente`) para sistemas externos como PNOA, catastro o el SIG municipal. Flechas en `tinta-suave`.

## Accesibilidad del color

Todas las parejas se han comprobado con el contraste WCAG 2.1 y con simulación de protanopia, deuteranopia y tritanopia (Machado et al., 2009, severidad completa).

- **Texto ≥ 4.5:1 (AA) en todas las combinaciones de uso:** `tinta` sobre cualquier fondo del sistema (≥ 15:1); `uoc-azul` sobre `papel`, `uoc-cian`, `uoc-cian-suave` y `uoc-azul-suave` (≥ 12:1); `tinta-suave` sobre `papel`, `superficie` y `uoc-cian-suave` (≥ 7.7:1); `papel` sobre `acc-accesible` (7.3:1), `acc-no-accesible` (5.9:1) y `nn-salida` (16.5:1); `tinta` sobre `acc-practicable` (6.3:1), `acc-deficiente` (6.4:1) y `acc-sin-datos` (6.5:1). Nunca `papel` sobre `acc-sin-datos` (3.2:1).
- **Marcas con significado ≥ 3:1 sobre `papel`:** todas las `acc-*`, todas las `serie-*`, `nn-skip`, y las clases `seg-calzada`, `seg-paso-peatones`, `seg-vegetacion`, `seg-obstaculo`, `seg-sombra`.
- **Excepciones controladas:** `seg-acera` (1.9:1), `seg-edificio` (1.9:1) y `seg-vehiculo` (2.2:1) están pensados para verse sobre la ortofoto; sobre `papel` llevan siempre borde `tinta-suave` (8.4:1). `uoc-cian`, `uoc-cian-filete`, `filete` y los rellenos `nn-*`/`arq-*` son campos o fondos, nunca texto ni marcas sueltas.
- **Distinguibles con daltonismo:** dentro de cada paleta (`acc-*`, `serie-*`, `seg-*`, `nn-*`) todas las parejas mantienen ΔE ≥ 15 en visión normal y en las tres simulaciones. La escala de accesibilidad separa azules (buena) de naranjas (mala), eje que se conserva en protanopia y deuteranopia, y además varía en luminosidad.
- **Estados:** texto `tinta` sobre cada `estado-*-fondo` ≥ 16:1; borde y glifo ≥ 3,7:1 sobre su fondo y ≥ 4,4:1 sobre `papel`. Completado (verde azulado) y Bloqueado (rojo teja) se separan también en deuteranopia, y el glifo (lleno frente a cruz) los distingue en gris.
- **Redundancia obligatoria:** color + texto (nombre o número de clase), color + marcador (series) o color + patrón (`acc-sin-datos` rayado; `nn-skip` y `serie-base` discontinuos). Ninguna figura debe depender solo del color.
- **Escala secuencial de un tono** (`papel` → `uoc-azul`) para matrices de confusión y mapas de calor; nunca *jet*/arcoíris. En matplotlib, para mapas continuos, `cividis` (ya por defecto en `tfm.mplstyle`).
- Revisa cada figura final en escala de grises y con un simulador (p. ej. Color Oracle) antes de incluirla.

## Qué componente usar

- **Explicar el sistema:** *Pipeline* (arquitectura de bloques), *DiagramaFlujo* (orden de algoritmos y decisiones), *DiagramaSecuencia* (llamadas entre componentes en una ejecución), *RedNeuronal* (capas del modelo), *DiagramaClases* (diseño del código).
- **Marco teórico y estado del arte:** *EsquemaConceptual*, *Recuadros* (definiciones e hipótesis), *Citas*, *MatrizLiteratura*, *LineaTemporal*, *DiagramaPRISMA*, *GraficoDispersion*.
- **Resultados:** *Tabla*, *GraficoBarras* (comparar modelos o clases; vertical u horizontal, agrupado o apilado), *GraficoLineas* (evolución o perfiles), *GraficoCircular* (composición de un único total), *MatrizConfusion*, *LeyendaSegmentacion*, *EscalaAccesibilidad*, *MapaTramos*.
- **Validación (real frente a predicho):** *ComparacionRealPredicho*, *TablaRealPredicho*, *MapaError*, *MatrizConfusion*.
- **Listas:** *Listas* (viñetas ■ – ▪, numeradas 1. a) i., objetivos e hipótesis codificados O1/H1, pasos, ventajas e inconvenientes, comprobación).
- **Notas y aclaraciones:** *Notas* (post-it de borrador, aclaraciones, notas al pie y de tabla).
- **Planificación y seguimiento:** *Cronograma* (Gantt), *TableroKanban*, *Estados*.
- **Difusión:** *Infografia*, *Diapositiva*.

## Estado del arte: estilo

Recomendaciones de forma (no de contenido) para analizar artículos científicos.

- **Bibliografía numerada por orden de aparición**, como pide la UOC ([7]): `\usepackage[bibliografia]{tfm-estilo}` carga biblatex + biber con estilo IEEE, `\addbibresource{referencias.bib}` en el preámbulo y `\printbibliography[heading=bibintoc]` en el capítulo de bibliografía (sustituye a la lista manual). Compila con pdflatex → biber → pdflatex ×2 (en Overleaf es automático).
- **Gestor de referencias:** Zotero (con Better BibTeX) o JabRef exportando un `.bib`; incluye DOI siempre que exista y, para webs, URL y fecha de consulta (`urldate`).
- **Citas en el texto:** el número va tras el autor o la afirmación: «Xie et al. [1] proponen…», «…mejora el mIoU [3], [5]». No uses el número como sujeto («[1] propone»). Varias referencias seguidas se agrupan ([3]–[5]).
- **Nombres de métodos** con la grafía original del artículo (SegFormer, DeepLabV3+, U-Net), en redonda, no en `\texttt`; el mismo nombre en texto, tablas y gráficos.
- **Paráfrasis antes que cita textual.** Textual solo para definiciones y normas (*Citas*).
- **Una pieza visual por pregunta:**
  - ¿Qué hay y en qué se diferencia? → *MatrizLiteratura* (criterios ●◐○, trabajo propio en la última fila).
  - ¿Cómo ha evolucionado? → *LineaTemporal*.
  - ¿Cómo se agrupan los enfoques? → *EsquemaConceptual* como taxonomía.
  - ¿Qué compromiso hay entre precisión y coste? → *GraficoDispersion*.
  - ¿Cómo se buscaron los artículos? → *DiagramaPRISMA* (bases de datos, cadena de búsqueda y fecha en el texto).
  - ¿Cuánto se publica por año? → *GraficoBarras* vertical.
- **Resultados de otros artículos:** compáralos solo si usan el mismo dataset y la misma métrica, y dilo en el pie. Las figuras de otros autores se rehacen con este sistema y se indica «Fuente: adaptado de [n]».
- **Cierre de cada bloque** con una *Aclaración* o un *Recuadro* de tipo hipótesis que conecte el hueco detectado con tu trabajo.

## Tipografía

- Una sola superfamilia: **Computer Modern** (la de LaTeX). `serif` para la memoria, `sans` para todo lo que va dentro de una figura (ejes, nodos, leyendas) y en diapositivas, `mono` para código.
- Estilos de memoria: `capitulo`, `seccion`, `subseccion`, `cuerpo`, `pie-figura`, `nota`, `cabecera`. Los tamaños equivalen a la clase `report` a 12 pt; el texto ocupa 17 cm de ancho (`\textwidth` de `TFUOC.cls`).
- Dentro de las figuras: `figura-titulo`, `figura-eje`, `figura-dato`, `diagrama-nodo`. Exporta las figuras al ancho final (hasta 17 cm; lo habitual, 0,8\textwidth ≈ 13,5 cm) para que 9–10 pt en la figura sean 9–10 pt en la página; no escales figuras hechas a otro tamaño.
- Listas: viñeta cuadrada `uoc-azul` en el primer nivel y raya `tinta-suave` en el segundo; números en `uoc-azul`. Lo aplica `tfm-estilo` a todas las listas (componente *Listas*).
- Código en `codigo`, sobre `superficie`, sin numeración de color.
- Diapositivas: `slide-titulo` en `uoc-azul`, `slide-cuerpo` en `tinta`, `cifra` para un único dato destacado.

## Espaciado, trazos y forma

- Escala de espaciado de 4 px: `space-1`, `space-2`, `space-3`, `space-4`, `space-6`, `space-8`, `space-12`.
- Trazos: `trazo-fino` para rejillas y \midrule, `trazo` para bordes y flechas, `trazo-grueso` para series y \toprule/\bottomrule, `trazo-cabecera` para los filetes cian.
- Maquetación a una columna (17 cm). Bloques concretos a dos o tres columnas con `doscolumnas` (ver componente *DosColumnas*); nunca la memoria entera a dos columnas.
- Tablas con booktabs: sin líneas verticales, cabecera sobre `uoc-cian-suave` opcional, mejor valor de cada columna en negrita.
- Gráficos: sin marco superior ni derecho, rejilla horizontal en `rejilla`, leyenda dentro del área si cabe, fuera a la derecha si no.

## Logotipo e imágenes

- Logotipos en el grupo *Logos*, copiados de la plantilla oficial: `uoc-logo-horizontal.png` (= `noulogo.png`, cabecera y diapositivas), `uoc-logo-vertical.png` (= `UOCllarg.png`, portada) y `eimt.png` (pie). Úsalos tal cual, sin recolorear, deformar ni poner sobre fondos que no sean `papel` o `uoc-cian`.
- Ortofotos: sin filtros ni saturación añadida; indica siempre fuente y año con `\fuente{}` bajo la figura («Fuente: ortofoto PNOA, IGN (2025).») y la resolución (cm/píxel).
- Mosaicos (Imagen · Referencia · Predicción) en rejilla de columnas iguales separadas por `space-2`, con la etiqueta de columna en `figura-eje` encima.

## Imágenes y recursos externos

- **Dónde:** guarda cada imagen en una carpeta junto al `.tex` (`figuras/`, `imagenes/` o `graficos/`; `tfm-estilo` ya las busca ahí) y nómbrala sin espacios ni tildes: `ortofoto_area_estudio.png`.
- **Formato:** gráficos y diagramas en **PDF vectorial** (pgfplots, TikZ o `savefig(..., format="pdf")`); ortofotos y máscaras en **PNG** (sin pérdida, recortadas al área útil, ≥ 300 ppp al tamaño impreso); fotografías de campo en **JPG** de calidad alta. Nada de capturas de pantalla de gráficos.
- **Cómo:** `\figuraexterna[ancho]{fichero}{pie}{etiqueta}{fuente y licencia}` crea la figura con pie, etiqueta y línea de fuente. Para mosaicos (Imagen · Referencia · Predicción) usa `subfigure` (paquete `subcaption`, ya cargado) con columnas de igual ancho.
- **Fuente y licencia siempre:** bajo cada imagen ajena, `\fuente{autor/organismo (año), licencia}`, y la referencia completa en la bibliografía. Ortofotos PNOA: cita al IGN/CNIG y la licencia que figure en su centro de descargas; Google, Bing u otros visores tienen condiciones restrictivas: compruébalas antes de usarlas.
- **Adaptar al sistema:** si rehaces un gráfico ajeno, usa los colores `serie-*`/`acc-*`/`seg-*` y la tipografía del sistema, y pon «Fuente: adaptado de …». Una imagen ajena que no puedes rehacer se incluye tal cual, sin recolorear, y se comprueba su legibilidad (texto ≥ 8 pt impreso).
- **Iconos o gráficos de terceros:** solo con licencia libre (CC BY, CC0, OFL) y atribución; el sistema no usa iconos, así que evítalos salvo que aporten información.
- **En este sistema de diseño:** las imágenes de referencia (p. ej. una ortofoto tipo o un logotipo nuevo) se añaden arrastrándolas a la página del sistema o pidiéndomelo; quedan en un grupo de recursos con su nota de uso.

## Iconografía

- No hay set de iconos. En leyendas y diagramas se usan formas geométricas (cuadrado de muestra, marcadores de gráfico, flechas) y texto. No usar emojis ni iconos de terceros en la memoria.

## Uso con LaTeX y Python

- `assets/LaTeX/tfm-estilo.sty` define todos los colores con los mismos nombres que los tokens (`\color{uoc-azul}`, `fill=acc-deficiente`), los estilos TikZ de diagramas (`nnconv`, `nnpool`, `nnup`, `arqmodulo`, `arqdatos`, `flecha`, `skip`…), la lista de ciclos de pgfplots `tfmseries` y el estilo `listings` `tfmcodigo`. Cópialo junto a `TFUOC.cls` y cárgalo después de `\documentclass[IB]{TFUOC}` con `\usepackage{tfm-estilo}` (o `[tabla]`). Probado con la plantilla TFM 2025-2: compila sin conflictos con su `xcolor`, `colortbl` y `babel` en castellano.
- Con `babel` en castellano, escribe superíndices en modo matemático (`$512^2$`) en lugar de `²`: `utf8x` de la plantilla los compone mal dentro de TikZ.
- `assets/LaTeX/beamerthemeUOCTFM.sty` es el tema Beamer para la defensa.
- `assets/Python/tfm.mplstyle` replica colores y tipografía en matplotlib para figuras generadas desde los notebooks (máscaras, curvas de entrenamiento): `plt.style.use('tfm.mplstyle')`.
