"""Varredura básica de portas TCP (varredura de conexão / connect scan)."""

from __future__ import annotations

import socket
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

# Portas comumente associadas a serviços de rede, usadas como padrão
# quando nenhuma lista específica é informada.
PORTAS_COMUNS: dict[int, str] = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-alt",
    8443: "HTTPS-alt",
    27017: "MongoDB",
}


@dataclass
class ResultadoPorta:
    porta: int
    aberta: bool
    servico: str | None = None


def _checar_porta(host: str, porta: int, timeout: float) -> ResultadoPorta:
    try:
        with socket.create_connection((host, porta), timeout=timeout):
            return ResultadoPorta(porta, True, PORTAS_COMUNS.get(porta))
    except (OSError, socket.timeout):
        return ResultadoPorta(porta, False, PORTAS_COMUNS.get(porta))


def escanear_portas(
    host: str,
    portas: Iterable[int] | None = None,
    *,
    timeout: float = 1.0,
    max_threads: int = 50,
) -> list[ResultadoPorta]:
    """
    Verifica quais portas TCP de `host` aceitam conexão.

    Se `portas` não for informado, usa a lista de portas comuns
    (`PORTAS_COMUNS`). Use apenas em hosts próprios ou com autorização
    explícita para o teste.
    """
    alvo_portas = list(portas) if portas is not None else list(PORTAS_COMUNS)
    if not alvo_portas:
        return []

    resultados: list[ResultadoPorta] = []
    with ThreadPoolExecutor(max_workers=min(max_threads, len(alvo_portas))) as executor:
        futuros = {
            executor.submit(_checar_porta, host, porta, timeout): porta for porta in alvo_portas
        }
        for futuro in as_completed(futuros):
            resultados.append(futuro.result())

    resultados.sort(key=lambda r: r.porta)
    return resultados
