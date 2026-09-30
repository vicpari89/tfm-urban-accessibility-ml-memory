"""Paletas del sistema visual "Vía Accesible" (TFM UOC) para matplotlib.

Uso:
    import matplotlib.pyplot as plt
    from paletas import ACC, SEG, CMAP_SEG, CMAP_SEC, superponer_mascara
    plt.style.use("tfm.mplstyle")
"""
import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# Escala ordinal de accesibilidad (siempre en este orden)
ACC = {
    "Accesible": "#005A8F",
    "Practicable": "#3A93D0",
    "Deficiente": "#C47F00",
    "No accesible": "#B23C00",
    "Sin datos": "#8A8FA3",   # dibújalo con rayado: hatch="///"
}

# Clases de segmentación (índice = posición en la lista)
SEG = {
    "Calzada": "#404040",
    "Acera": "#CCBB44",
    "Paso de peatones": "#EE6677",
    "Vegetación": "#228833",
    "Edificio": "#BBBBBB",
    "Vehículo": "#33BBEE",
    "Obstáculo": "#AA3377",
    "Sombra": "#332288",
}
IGNORADO = 255

# Estados (solo para etiquetas de estado; siempre con texto)
ESTADOS = {
    "Pendiente":   ("#6F7488", "#EBECEE"),   # (borde/glifo, fondo)
    "En curso":    ("#A86B00", "#F3EADB"),
    "En revisión": ("#6A3D9A", "#EAE4F1"),
    "Completado":  ("#0B6E4F", "#DDEBE6"),
    "Bloqueado":   ("#9C2A00", "#F1E1DB"),
}

# Real frente a predicho (misma convención en gráficos, tablas y mapas)
ERROR = {"sobreestima": "#B35806", "subestima": "#2166AC", "acierto": "#7B7E8C", "tolerancia": "#E3FBFF"}

SERIES = ["#010073", "#006D82", "#C47F00", "#7A3D99"]
SERIE_BASE = "#8A8FA3"   # siempre discontinua: linestyle="--"

CMAP_SEG = ListedColormap(list(SEG.values()), name="tfm_seg")
CMAP_SEC = LinearSegmentedColormap.from_list("tfm_sec", ["#FFFFFF", "#010073"])  # matrices de confusión


def superponer_mascara(ax, imagen, mascara, alpha=0.5):
    """Dibuja la ortofoto y encima la máscara de clases (50 % de opacidad)."""
    ax.imshow(imagen)
    m = np.ma.masked_equal(mascara, IGNORADO)
    ax.imshow(m, cmap=CMAP_SEG, vmin=0, vmax=len(SEG) - 1, alpha=alpha, interpolation="nearest")
    ax.set_axis_off()


def leyenda_segmentacion(ax, **kw):
    """Leyenda con muestras bordeadas (acera, edificio y vehículo son claros)."""
    from matplotlib.patches import Patch
    h = [Patch(facecolor=c, edgecolor="#4A4D5C", linewidth=0.6, label=n) for n, c in SEG.items()]
    return ax.legend(handles=h, **kw)


def grafico_circular(ax, valores, etiquetas, colores, hueco=0.0, centro=None):
    """Sectores (hueco=0) o anillo (hueco=0.4). Empieza a las 12 y gira en sentido horario."""
    w = dict(width=1 - hueco, edgecolor="white", linewidth=1.5) if hueco else dict(edgecolor="white", linewidth=1.5)
    total = sum(valores)
    etq = [f"{e}\n{v / total * 100:.0f} %".replace(".", ",") for e, v in zip(etiquetas, valores)]
    ax.pie(valores, labels=etq, colors=colores, startangle=90, counterclock=False,
           wedgeprops=w, textprops=dict(fontsize=8))
    if centro:
        ax.text(0, 0, centro, ha="center", va="center", fontsize=11, fontweight="bold", color="#010073")
    ax.set_aspect("equal")


def real_vs_predicho(ax, real, pred, tol=0.3, unidad="m"):
    """Dispersión real/predicho con diagonal, banda ±tol y errores marcados con ▲/▼."""
    real, pred = np.asarray(real), np.asarray(pred)
    lo, hi = 0, max(real.max(), pred.max()) * 1.05
    x = np.linspace(lo, hi, 2)
    ax.fill_between(x, x - tol, x + tol, color=ERROR["tolerancia"], lw=0, zorder=0)
    ax.axline((0, 0), slope=1, ls="--", color=SERIE_BASE, lw=1)
    d = pred - real
    ok = np.abs(d) <= tol
    ax.scatter(real[ok], pred[ok], s=14, color=SERIES[0], label=f"Dentro de ±{tol:g} {unidad}".replace(".", ","))
    ax.scatter(real[d > tol], pred[d > tol], s=26, marker="^", color=ERROR["sobreestima"], label="Sobreestima")
    ax.scatter(real[d < -tol], pred[d < -tol], s=26, marker="v", color=ERROR["subestima"], label="Subestima")
    ax.set(xlim=(lo, hi), ylim=(lo, hi), aspect="equal",
           xlabel=f"Valor real ({unidad})", ylabel=f"Valor predicho ({unidad})")
    ax.grid(True, axis="both")
    ax.legend(loc="upper left")
