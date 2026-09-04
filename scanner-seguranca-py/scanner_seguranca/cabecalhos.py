"""Verificação de cabeçalhos HTTP relacionados à segurança."""

from __future__ import annotations

import ssl
import urllib.request
from dataclasses import dataclass, field

# Cabeçalhos de segurança recomendados e o que cada um mitiga.
CABECALHOS_RECOMENDADOS: dict[str, str] = {
    "Strict-Transport-Security": "força conexões HTTPS e evita downgrade para HTTP",
    "Content-Security-Policy": "restringe origens de script/estilo, mitigando XSS",
    "X-Content-Type-Options": "evita que o navegador tente adivinhar o tipo de conteúdo (MIME sniffing)",
    "X-Frame-Options": "evita que a página seja carregada dentro de um <iframe> (clickjacking)",
    "Referrer-Policy": "controla quanta informação de referência é enviada a outros sites",
    "Permissions-Policy": "restringe o uso de APIs sensíveis do navegador (câmera, geolocalização etc.)",
}


@dataclass
class ResultadoCabecalhos:
    url: str
    status: int
    cabecalhos: dict[str, str]
    presentes: list[str] = field(default_factory=list)
    ausentes: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        linhas = [f"URL: {self.url}", f"Status HTTP: {self.status}", ""]

        linhas.append("Cabeçalhos de segurança presentes:")
        if self.presentes:
            linhas.extend(f"  [OK] {nome}: {self.cabecalhos[nome]}" for nome in self.presentes)
        else:
            linhas.append("  (nenhum)")

        linhas.append("")
        linhas.append("Cabeçalhos de segurança ausentes:")
        if self.ausentes:
            linhas.extend(
                f"  [FALTA] {nome} — {CABECALHOS_RECOMENDADOS[nome]}" for nome in self.ausentes
            )
        else:
            linhas.append("  (nenhum — todos os recomendados estão presentes)")

        return "\n".join(linhas)


def _normalizar_url(url: str) -> str:
    """Garante que a URL tenha um esquema, assumindo HTTPS por padrão."""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def verificar_cabecalhos(url: str, *, timeout: float = 5.0) -> ResultadoCabecalhos:
    """
    Faz uma requisição GET a `url` e verifica quais cabeçalhos de
    segurança recomendados estão presentes na resposta.
    """
    url = _normalizar_url(url)

    contexto = ssl.create_default_context()
    requisicao = urllib.request.Request(
        url, method="GET", headers={"User-Agent": "scanner-seguranca-py"}
    )
    with urllib.request.urlopen(requisicao, timeout=timeout, context=contexto) as resposta:
        cabecalhos = dict(resposta.getheaders())
        status = resposta.status

    presentes = [nome for nome in CABECALHOS_RECOMENDADOS if nome in cabecalhos]
    ausentes = [nome for nome in CABECALHOS_RECOMENDADOS if nome not in cabecalhos]

    return ResultadoCabecalhos(
        url=url,
        status=status,
        cabecalhos=cabecalhos,
        presentes=presentes,
        ausentes=ausentes,
    )
