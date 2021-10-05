"""
Funciones útiles para el computo y registro en el laboratorio de la
ley de Ohm
"""

from typing import List, Tuple
from numbers import Real
from matplotlib.pyplot import plot, style, rcParams, title, xlabel, xticks, ylabel, show, yticks
from pandas import DataFrame
from numpy import floor, polyfit


class ConfiguracionRegistro:
    def __init__(self, voltaje_inicial: Real, escala: Real) -> None:
        self.voltaje_inicial = voltaje_inicial
        self.escala = escala


def registrar_corrientes(corrientes: List[Real], config: ConfiguracionRegistro) -> DataFrame:
    voltajes = generar_voltajes(len(corrientes), config.voltaje_inicial, config.escala)
    return crear_tabla(corrientes, voltajes)


def generar_voltajes(cantidad_corrientes: int, voltaje_inicial: float, escala: float) -> List[Real]:
    voltajes = []
    voltaje = voltaje_inicial
    for _ in range(cantidad_corrientes):
        voltajes.append(voltaje)
        voltaje += escala
    return voltajes


def crear_tabla(corrientes: List[Real], voltajes: List[Real]) -> DataFrame:
    return DataFrame(
        {"I (A)": corrientes, "V (volts)": voltajes},
        index=range(1, len(corrientes) + 1),
    ).rename_axis("Medidas", axis=1)


def graficar(titulo: str, dataframe: DataFrame, color="#3EA6FF") -> None:
    x_axis = "I (A)"
    y_axis = "V (volts)"

    style.use("seaborn-whitegrid")
    xticks(dataframe[x_axis])
    yticks(dataframe[y_axis])
    plot(dataframe[x_axis], dataframe[y_axis], color=color, marker=".", markerfacecolor=color)
    rcParams.update({"figure.figsize": (7, 5), "figure.dpi": 100})
    title(titulo)
    xlabel(x_axis)
    ylabel(y_axis)
    show()


def calcular_resistencia(dataframe: DataFrame) -> Tuple[Real, Real]:
    resitencia_experimental = round_down(polyfit(dataframe["I (A)"], dataframe["V (volts)"], 1)[0], 6)
    resistencia_teorica = dataframe["V (volts)"].iloc[-1] / dataframe["I (A)"].iloc[-1]
    return (resitencia_experimental, resistencia_teorica)


def error_porcentual(aceptado: float, experimental: float) -> str:
    """
    Calcular error porcentual de un resultado experimental obtenido con
    respecto al aceptado
    """
    porcentaje = abs(((aceptado - experimental) / aceptado) * 100)
    return "{:.8f}%".format(porcentaje)


def resultado_experimentacion(*dataframes: DataFrame) -> DataFrame:
    resultados = [calcular_resistencia(d) for d in dataframes]
    experimentales = map(lambda x: x[0], resultados)
    aceptados = map(lambda x: x[1], resultados)
    errores = [error_porcentual(acept, exp) for exp, acept in resultados]

    return DataFrame({
        "Resistencia": [f"R{i+1}" for i in range(len(resultados))],
        "Experimental": experimentales,
        "Teórico": aceptados,
        "Error Porcentual": errores
    })


def round_down(number:float, decimals:int=2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return floor(number)

    factor = 10 ** decimals
    return floor(number * factor) / factor
