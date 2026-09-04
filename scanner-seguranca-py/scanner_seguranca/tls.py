"""Verificação básica do certificado TLS de um host."""

from __future__ import annotations

import socket
import ssl
from dataclasses import dataclass
from datetime import datetime, timezone

DIAS_ALERTA_EXPIRACAO = 15


@dataclass
class ResultadoTLS:
    host: str
    porta: int
    protocolo: str
    emitido_para: str
    emitido_por: str
    valido_ate: datetime
    dias_para_expirar: int

    def __str__(self) -> str:
        aviso = ""
        if self.dias_para_expirar < 0:
            aviso = " (EXPIRADO)"
        elif self.dias_para_expirar <= DIAS_ALERTA_EXPIRACAO:
            aviso = " (expira em breve)"
        return (
            f"Host: {self.host}:{self.porta}\n"
            f"Protocolo: {self.protocolo}\n"
            f"Emitido para: {self.emitido_para}\n"
            f"Emitido por: {self.emitido_por}\n"
            f"Válido até: {self.valido_ate:%d/%m/%Y}{aviso}"
        )


def _extrair_nome(componentes) -> str:
    """Extrai o commonName de uma estrutura subject/issuer de getpeercert()."""
    partes = dict(par[0] for par in componentes)
    return partes.get("commonName", "desconhecido")


def _processar_certificado(
    certificado: dict, protocolo: str, host: str, porta: int
) -> ResultadoTLS:
    emitido_para = _extrair_nome(certificado.get("subject", ()))
    emitido_por = _extrair_nome(certificado.get("issuer", ()))
    valido_ate = datetime.strptime(certificado["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(
        tzinfo=timezone.utc
    )
    dias_para_expirar = (valido_ate - datetime.now(timezone.utc)).days

    return ResultadoTLS(
        host=host,
        porta=porta,
        protocolo=protocolo or "desconhecido",
        emitido_para=emitido_para,
        emitido_por=emitido_por,
        valido_ate=valido_ate,
        dias_para_expirar=dias_para_expirar,
    )


def verificar_certificado(host: str, porta: int = 443, *, timeout: float = 5.0) -> ResultadoTLS:
    """Conecta em `host:porta` via TLS e reporta dados do certificado apresentado."""
    contexto = ssl.create_default_context()
    with socket.create_connection((host, porta), timeout=timeout) as sock:
        with contexto.wrap_socket(sock, server_hostname=host) as ssock:
            certificado = ssock.getpeercert()
            protocolo = ssock.version()

    return _processar_certificado(certificado, protocolo, host, porta)
