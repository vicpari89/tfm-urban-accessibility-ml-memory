"""arboles.py — árboles de decisión y XGBoost con el sistema visual «Vía Accesible».

Convierte modelos reales en código LaTeX que usa los estilos de tfm-estilo.sty (v1.8)
y dibuja la importancia de variables y la curva de aprendizaje con tfm.mplstyle.

    from arboles import xgb_a_forest, sklearn_a_forest, importancia_pgfplots, \
        tabla_configuracion, importancia, curva_aprendizaje

    print(xgb_a_forest(modelo, arbol=0, nombres=["anchura", "pendiente", ...]))
    print(sklearn_a_forest(arbol_sk, nombres, clases=["Accesible", "Practicable", ...]))

Todo el texto sale con coma decimal y escapado para LaTeX. Pega la salida dentro de
\\begin{figure} ... \\end{figure} (árboles) o de un entorno tabularx (configuración).
"""
from __future__ import annotations

import json
import math

# Colores del sistema (tokens.json)
SERIE = ["#010073", "#006D82", "#C47F00", "#7A3D99"]
SERIE_BASE = "#8A8FA3"
TINTA_SUAVE = "#4A4D5C"
# Nombre de clase -> sufijo acc-* (hojaclase=...) en la escala de accesibilidad
ACC_CLAVE = {
    "accesible": "accesible", "practicable": "practicable", "deficiente": "deficiente",
    "no accesible": "no-accesible", "sin datos": "sin-datos",
}

# Hiperparámetros de XGBoost agrupados como en la tabla del sistema
GRUPOS_XGB = [
    ("Estructura del árbol", ["max_depth", "min_child_weight", "gamma", "max_leaves", "grow_policy", "tree_method"]),
    ("Muestreo", ["subsample", "colsample_bytree", "colsample_bylevel", "colsample_bynode"]),
    ("Regularización", ["reg_lambda", "lambda", "reg_alpha", "alpha", "max_delta_step"]),
    ("Aprendizaje", ["learning_rate", "eta", "n_estimators", "num_boost_round", "early_stopping_rounds"]),
    ("Objetivo y evaluación", ["objective", "num_class", "eval_metric", "scale_pos_weight"]),
]
DESCRIPCION_XGB = {
    "max_depth": "Profundidad máxima de cada árbol",
    "min_child_weight": "Suma mínima de pesos (hessiano) en una hoja",
    "gamma": "Reducción mínima de la pérdida para dividir un nodo",
    "max_leaves": "Número máximo de hojas por árbol",
    "subsample": "Fracción de muestras usada por árbol",
    "colsample_bytree": "Fracción de variables usada por árbol",
    "colsample_bylevel": "Fracción de variables por nivel",
    "colsample_bynode": "Fracción de variables por división",
    "reg_lambda": "Regularización L2 de los pesos de las hojas",
    "lambda": "Regularización L2 de los pesos de las hojas",
    "reg_alpha": "Regularización L1 de los pesos de las hojas",
    "alpha": "Regularización L1 de los pesos de las hojas",
    "learning_rate": "Tasa de aprendizaje ($\\eta$)",
    "eta": "Tasa de aprendizaje ($\\eta$)",
    "n_estimators": "Número máximo de árboles",
    "num_boost_round": "Número máximo de árboles",
    "early_stopping_rounds": "Iteraciones sin mejora antes de parar",
    "objective": "Función objetivo",
    "num_class": "Número de clases",
    "eval_metric": "Métrica de validación",
    "scale_pos_weight": "Peso de la clase positiva",
    "tree_method": "Algoritmo de construcción",
    "grow_policy": "Política de crecimiento",
    "max_delta_step": "Paso máximo de los pesos de las hojas",
}

_ESCAPE = {"\\": "\\textbackslash{}", "_": "\\_", "%": "\\%", "&": "\\&", "#": "\\#",
           "$": "\\$", "{": "\\{", "}": "\\}", "^": "\\^{}", "~": "\\~{}"}


def _esc(texto) -> str:
    return "".join(_ESCAPE.get(c, c) for c in str(texto))


def _num(x, decimales=2, signo=False) -> str:
    """Número con coma decimal y signo menos tipográfico."""
    if isinstance(x, (int,)) or (isinstance(x, float) and x.is_integer() and abs(x) >= 1000):
        s = f"{int(x):,}".replace(",", "\\,")
    else:
        s = f"{x:.{decimales}f}".replace(".", ",")
    if s.startswith("-"):
        return "$-$" + s[1:]
    return ("+" + s) if signo and x > 0 else s


def _miles(n) -> str:
    return f"{int(n):,}".replace(",", "\\,")


def _claseacc(nombre: str | None):
    if nombre is None:
        return None
    return ACC_CLAVE.get(str(nombre).strip().lower())


# ------------------------------------------------------------------ XGBoost -> forest
def xgb_a_forest(modelo, arbol: int = 0, nombres=None, decimales: int = 2,
                 profundidad_max: int | None = None, info: str | None = "cover",
                 muestra=None, etiquetas=("sí", "no")) -> str:
    """Código forest (estilo tfmarbol) de un árbol de un modelo XGBoost.

    modelo: XGBClassifier/XGBRegressor o Booster.  arbol: índice del árbol (en multiclase,
    el árbol k de la clase c es k * num_class + c).  nombres: nombres legibles de las variables
    (por defecto, booster.feature_names o f0, f1…).  info: "cover", "gain" o None.
    muestra: vector o dict de valores de una observación -> resalta su camino (camino).
    En XGBoost la rama «sí» es «valor < umbral»; la marcada «ausente» recibe los valores nulos.
    """
    booster = modelo.get_booster() if hasattr(modelo, "get_booster") else modelo
    nodo_raiz = json.loads(booster.get_dump(dump_format="json", with_stats=True)[arbol])
    fn = list(booster.feature_names or [])

    def nombre(split):
        if nombres is not None:
            if isinstance(nombres, dict):
                return nombres.get(split, split)
            idx = fn.index(split) if split in fn else int(str(split).lstrip("f"))
            return nombres[idx]
        return split

    def valor(split):
        if muestra is None:
            return None
        if isinstance(muestra, dict):
            return muestra.get(split, muestra.get(nombre(split)))
        idx = fn.index(split) if split in fn else int(str(split).lstrip("f"))
        return muestra[idx]

    lineas = [f"\\etiquetasramas{{{etiquetas[0]}}}{{{etiquetas[1]}}}", "\\begin{forest} tfmarbol"]

    def visita(n, prof, en_camino, sangria, opciones_extra=""):
        pre = "  " * sangria
        opc = opciones_extra + (", camino" if en_camino and muestra is not None else "")
        if "leaf" in n:
            txt = _num(n["leaf"], decimales + 1, signo=True)
            extra = f"\\arbolinfo{{cobertura {_num(n['cover'], 1)}}}" if info == "cover" and "cover" in n else ""
            lineas.append(f"{pre}[{{{txt}}}{extra}{opc}]")
            return
        if profundidad_max is not None and prof >= profundidad_max:
            lineas.append(f"{pre}[{{\\dots}}{opc}]")
            return
        cond = f"{_esc(nombre(n['split']))} \\textless\\ {_num(n['split_condition'], decimales)}"
        if info == "gain" and "gain" in n:
            cond += f"\\arbolinfo{{ganancia {_num(n['gain'], 1)}}}"
        elif info == "cover" and "cover" in n:
            cond += f"\\arbolinfo{{cobertura {_num(n['cover'], 1)}}}"
        lineas.append(f"{pre}[{{{cond}}}{opc}")
        hijos = {h["nodeid"]: h for h in n["children"]}
        v = valor(n["split"])
        va_si = None
        if v is not None:
            va_si = (n["missing"] == n["yes"]) if (v is None or (isinstance(v, float) and math.isnan(v))) else bool(v < n["split_condition"])
        for clave in ("yes", "no"):
            h = hijos[n[clave]]
            aus = ", ausente" if n["missing"] == n[clave] else ""
            sigue = en_camino and va_si is not None and (va_si == (clave == "yes"))
            visita(h, prof + 1, sigue, sangria + 1, aus)
        lineas.append(f"{pre}]")

    visita(nodo_raiz, 0, True, 0)
    lineas.append("\\end{forest}")
    return "\n".join(lineas)


# ------------------------------------------------------------------ scikit-learn -> forest
def sklearn_a_forest(arbol, nombres, clases=None, decimales: int = 2,
                     profundidad_max: int | None = None, info: str | None = "n",
                     muestra=None, etiquetas=("sí", "no")) -> str:
    """Código forest de un DecisionTreeClassifier/Regressor de scikit-learn.

    Rama «sí» = «variable ≤ umbral» (convención de scikit-learn). Si las clases se llaman como
    la escala de accesibilidad (Accesible, Practicable, Deficiente, No accesible, Sin datos),
    las hojas se colorean con hojaclase; si no, van en arbol-hoja con el nombre de la clase.
    info: "n" (muestras), "impureza" o None.  muestra: vector de una observación -> camino.
    """
    t = arbol.tree_
    es_clasificador = hasattr(arbol, "classes_")
    if clases is None and es_clasificador:
        clases = [str(c) for c in arbol.classes_]
    lineas = [f"\\etiquetasramas{{{etiquetas[0]}}}{{{etiquetas[1]}}}", "\\begin{forest} tfmarbol"]

    def texto_info(i):
        if info == "n":
            return f"\\arbolinfo{{n = {_miles(t.n_node_samples[i])}}}"
        if info == "impureza":
            return f"\\arbolinfo{{impureza {_num(float(t.impurity[i]), 3)}}}"
        return ""

    def visita(i, prof, en_camino, sangria):
        pre = "  " * sangria
        opc = ", camino" if (en_camino and muestra is not None) else ""
        hoja = t.children_left[i] == t.children_right[i]
        if hoja or (profundidad_max is not None and prof >= profundidad_max and not hoja):
            if hoja and es_clasificador:
                nombre = clases[int(t.value[i][0].argmax())]
                clave = _claseacc(nombre)
                opc = (f", hojaclase={clave}" if clave else "") + opc
                txt = _esc(nombre)
            elif hoja:
                txt = _num(float(t.value[i][0][0]), decimales)
            else:
                txt = "\\dots"
            lineas.append(f"{pre}[{{{txt}}}{texto_info(i) if hoja else ''}{opc}]")
            return
        cond = f"{_esc(nombres[t.feature[i]])} $\\leq$ {_num(float(t.threshold[i]), decimales)}"
        lineas.append(f"{pre}[{{{cond}}}{texto_info(i)}{opc}")
        va_izq = None if muestra is None else bool(muestra[t.feature[i]] <= t.threshold[i])
        visita(t.children_left[i], prof + 1, en_camino and va_izq is True, sangria + 1)
        visita(t.children_right[i], prof + 1, en_camino and va_izq is False, sangria + 1)
        lineas.append(f"{pre}]")

    visita(0, 0, True, 0)
    lineas.append("\\end{forest}")
    return "\n".join(lineas)


# ------------------------------------------------------------------ Importancia y configuración en LaTeX
def _puntuaciones(modelo, tipo="gain", nombres=None):
    booster = modelo.get_booster() if hasattr(modelo, "get_booster") else modelo
    sc = booster.get_score(importance_type=tipo)
    fn = list(booster.feature_names or [])
    total = sum(sc.values()) or 1.0
    salida = []
    for k, v in sc.items():
        if nombres is not None:
            idx = fn.index(k) if k in fn else int(str(k).lstrip("f"))
            k = nombres[idx]
        salida.append((k, v / total))
    return sorted(salida, key=lambda kv: kv[1], reverse=True)


def importancia_pgfplots(modelo, tipo: str = "gain", top: int = 10, nombres=None,
                         ancho: str = "0.8\\linewidth") -> str:
    """Código pgfplots (estilo tfmimportancia) con la importancia normalizada (suma 1)."""
    datos = _puntuaciones(modelo, tipo, nombres)[:top]
    etiquetas = ",".join("{" + _esc(k) + "}" for k, _ in datos)
    coords = " ".join(f"({v:.4f},{{{_esc(k)}}})" for k, v in datos)
    eje = {"gain": "Ganancia media (normalizada)", "weight": "Número de divisiones (normalizado)",
           "cover": "Cobertura media (normalizada)", "total_gain": "Ganancia total (normalizada)"}.get(tipo, tipo)
    alto = max(3.0, 0.6 * len(datos) + 1.2)
    return (f"\\begin{{tikzpicture}}\n\\begin{{axis}}[tfmimportancia, width={ancho}, height={alto:.1f}cm,\n"
            f"    xlabel={{{eje}}}, symbolic y coords={{{etiquetas}}}]\n"
            f"  \\addplot coordinates {{{coords}}};\n\\end{{axis}}\n\\end{{tikzpicture}}")


def tabla_configuracion(params: dict, rangos: dict | None = None, elegidos=None) -> str:
    """Filas LaTeX de la tabla de configuración, agrupadas como en el sistema.

    params: hiperparámetros (p. ej. modelo.get_params() o el dict de xgb.train).
    rangos: rango explorado por hiperparámetro (texto).  elegidos: claves a resaltar con \\mejor.
    Pega la salida dentro de un tabularx de cuatro columnas (ver README del componente).
    """
    rangos = rangos or {}
    elegidos = set(elegidos or [])
    filas, usados = [], set()

    def celda(v):
        if isinstance(v, float):
            return _num(v, 3).rstrip("0").rstrip(",") if "," in _num(v, 3) else _num(v, 3)
        return _esc(v)

    for grupo, claves in GRUPOS_XGB + [("Otros", None)]:
        presentes = [k for k in (claves or [k for k in params if k not in usados])
                     if k in params and params[k] is not None and k not in usados]
        if not presentes:
            continue
        filas.append(f"\\filagrupo{{4}}{{{grupo}}}")
        for k in presentes:
            usados.add(k)
            val = celda(params[k])
            val = f"\\mejor{{{val}}}" if k in elegidos else val
            filas.append(f"\\hiperparam{{{k}}} & {DESCRIPCION_XGB.get(k, '')} & "
                         f"{_esc(rangos.get(k, '--'))} & {val} \\\\")
    return "\n".join(filas)


# ------------------------------------------------------------------ matplotlib
def importancia(modelo, ax=None, tipo: str = "gain", top: int = 10, nombres=None):
    """Barras horizontales de importancia (serie-1), normalizadas, primera arriba."""
    import matplotlib.pyplot as plt
    datos = _puntuaciones(modelo, tipo, nombres)[:top]
    ax = ax or plt.gca()
    ks = [k for k, _ in datos][::-1]
    vs = [v for _, v in datos][::-1]
    ax.barh(ks, vs, color=SERIE[0], height=0.55)
    for y, v in enumerate(vs):
        ax.text(v, y, " " + f"{v:.2f}".replace(".", ","), va="center", fontsize=7, color="#000000")
    ax.set_xlim(0, max(vs) * 1.15 if vs else 1)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.set_xlabel({"gain": "Ganancia media (normalizada)", "weight": "Número de divisiones"}.get(tipo, tipo))
    return ax


def curva_aprendizaje(resultados: dict, metrica: str | None = None, ax=None, mejor: int | None = None,
                      nombres=("Entrenamiento", "Validación")):
    """Curva de la métrica por iteración (modelo.evals_result()).

    El último conjunto evaluado se dibuja como validación (serie-1) y el primero como
    entrenamiento (serie-2). mejor: modelo.best_iteration -> línea de parada temprana.
    """
    import matplotlib.pyplot as plt
    ax = ax or plt.gca()
    conjuntos = list(resultados.keys())
    metrica = metrica or list(resultados[conjuntos[0]].keys())[-1]
    estilos = {conjuntos[0]: dict(color=SERIE[1], marker="None"),
               conjuntos[-1]: dict(color=SERIE[0], marker="None")}
    for conj, nom in zip([conjuntos[-1], conjuntos[0]] if len(conjuntos) > 1 else conjuntos,
                         [nombres[1], nombres[0]] if len(conjuntos) > 1 else [nombres[1]]):
        ax.plot(resultados[conj][metrica], label=nom, **estilos[conj])
    if mejor is not None:
        ax.axvline(mejor, color=TINTA_SUAVE, linestyle="--", linewidth=0.8)
        ax.annotate(f"parada temprana\n(mejor iteración: {mejor})", xy=(mejor, 1), xycoords=("data", "axes fraction"),
                    xytext=(3, -3), textcoords="offset points", va="top", fontsize=7, color=TINTA_SUAVE)
    ax.set_xlabel("Iteración (número de árboles)")
    ax.set_ylabel(metrica)
    ax.legend(loc="center right")
    return ax
