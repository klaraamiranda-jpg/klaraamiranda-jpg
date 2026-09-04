"""Ferramenta básica de diagnóstico de segurança.

Use apenas em sistemas próprios ou com autorização explícita do responsável.
"""

from .cabecalhos import CABECALHOS_RECOMENDADOS, ResultadoCabecalhos, verificar_cabecalhos
from .portas import PORTAS_COMUNS, ResultadoPorta, escanear_portas
from .tls import ResultadoTLS, verificar_certificado

__version__ = "0.1.0"

__all__ = [
    "CABECALHOS_RECOMENDADOS",
    "ResultadoCabecalhos",
    "verificar_cabecalhos",
    "PORTAS_COMUNS",
    "ResultadoPorta",
    "escanear_portas",
    "ResultadoTLS",
    "verificar_certificado",
]
