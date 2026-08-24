"""Calculadora de prazos processuais conforme o CPC (Lei nº 13.105/2015)."""

from .calculadora import (
    DiaDesconsiderado,
    ResultadoPrazo,
    calcular_prazo,
    eh_dia_util,
    em_recesso_forense,
    proximo_dia_util,
)
from .feriados import carnaval, corpus_christi, feriados_nacionais, pascoa, sexta_feira_santa

__version__ = "0.1.0"

__all__ = [
    "DiaDesconsiderado",
    "ResultadoPrazo",
    "calcular_prazo",
    "eh_dia_util",
    "em_recesso_forense",
    "proximo_dia_util",
    "carnaval",
    "corpus_christi",
    "feriados_nacionais",
    "pascoa",
    "sexta_feira_santa",
]
