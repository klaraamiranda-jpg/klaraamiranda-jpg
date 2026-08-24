"""
Contagem de prazos processuais conforme o Código de Processo Civil
(Lei nº 13.105/2015).

Regras aplicadas:

- Art. 219: na contagem de prazo em dias, computam-se somente os dias úteis.
- Art. 224, caput: exclui-se o dia do começo (a data da publicação/intimação)
  e inclui-se o dia do vencimento.
- Art. 224, §3º: a contagem tem início no primeiro dia útil seguinte ao da
  publicação/intimação.
- Art. 220: suspende-se o curso do prazo processual entre 20 de dezembro e
  20 de janeiro, inclusive (recesso forense).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, timedelta

from .feriados import feriados_nacionais


def em_recesso_forense(data: date) -> bool:
    """Art. 220, CPC: suspende-se o prazo entre 20/dez e 20/jan, inclusive."""
    return (data.month == 12 and data.day >= 20) or (data.month == 1 and data.day <= 20)


def eh_dia_util(
    data: date,
    *,
    feriados_extras: Iterable[date] | None = None,
    considerar_nacionais: bool = True,
    considerar_recesso: bool = True,
) -> bool:
    """
    Indica se `data` é dia útil para fins processuais: não é sábado, domingo,
    feriado nacional nem dia de recesso forense (art. 220, CPC).

    `feriados_extras` permite informar feriados locais/forenses do
    tribunal ou comarca, que variam por localidade e não são calculados
    automaticamente.
    """
    if data.weekday() >= 5:  # sábado (5) ou domingo (6)
        return False
    if considerar_recesso and em_recesso_forense(data):
        return False
    if considerar_nacionais and data in feriados_nacionais(data.year):
        return False
    if feriados_extras and data in feriados_extras:
        return False
    return True


def _motivo_nao_util(
    data: date,
    feriados_extras: Iterable[date],
    considerar_nacionais: bool,
    considerar_recesso: bool,
) -> str:
    if data.weekday() >= 5:
        return "fim de semana"
    if considerar_recesso and em_recesso_forense(data):
        return "recesso forense (art. 220, CPC)"
    if considerar_nacionais and data in feriados_nacionais(data.year):
        return "feriado nacional"
    if feriados_extras and data in feriados_extras:
        return "feriado local/forense"
    return "dia não útil"


def proximo_dia_util(
    data: date,
    *,
    feriados_extras: Iterable[date] | None = None,
    considerar_nacionais: bool = True,
    considerar_recesso: bool = True,
) -> date:
    """Retorna o primeiro dia útil a partir de (e incluindo) `data`."""
    extras = set(feriados_extras or ())
    while not eh_dia_util(
        data,
        feriados_extras=extras,
        considerar_nacionais=considerar_nacionais,
        considerar_recesso=considerar_recesso,
    ):
        data += timedelta(days=1)
    return data


@dataclass
class DiaDesconsiderado:
    """Um dia dentro do intervalo do prazo que não foi computado, e o motivo."""

    data: date
    motivo: str


@dataclass
class ResultadoPrazo:
    data_publicacao: date
    dias_uteis: int
    inicio_contagem: date
    vencimento: date
    dias_desconsiderados: list[DiaDesconsiderado] = field(default_factory=list)

    def __str__(self) -> str:
        linhas = [
            f"Publicação/intimação: {self.data_publicacao:%d/%m/%Y}",
            f"Início da contagem (art. 224, §3º, CPC): {self.inicio_contagem:%d/%m/%Y}",
            f"Prazo: {self.dias_uteis} dia(s) útil(eis) (art. 219, CPC)",
            f"Vencimento: {self.vencimento:%d/%m/%Y}",
        ]
        if self.dias_desconsiderados:
            linhas.append("Dias não computados:")
            linhas.extend(
                f"  - {dia.data:%d/%m/%Y}: {dia.motivo}" for dia in self.dias_desconsiderados
            )
        return "\n".join(linhas)


def calcular_prazo(
    data_publicacao: date,
    dias_uteis: int,
    *,
    feriados_extras: Iterable[date] | None = None,
    considerar_nacionais: bool = True,
    considerar_recesso: bool = True,
) -> ResultadoPrazo:
    """
    Calcula o vencimento de um prazo processual contado em dias úteis.

    `data_publicacao` é a data da publicação/intimação que dá início ao
    prazo. `dias_uteis` é a quantidade de dias úteis do prazo (por
    exemplo, 15 para uma contestação).
    """
    if dias_uteis <= 0:
        raise ValueError("O prazo em dias úteis deve ser maior que zero.")

    extras = set(feriados_extras or ())

    def util(dia: date) -> bool:
        return eh_dia_util(
            dia,
            feriados_extras=extras,
            considerar_nacionais=considerar_nacionais,
            considerar_recesso=considerar_recesso,
        )

    inicio = proximo_dia_util(
        data_publicacao + timedelta(days=1),
        feriados_extras=extras,
        considerar_nacionais=considerar_nacionais,
        considerar_recesso=considerar_recesso,
    )

    desconsiderados: list[DiaDesconsiderado] = []
    atual = inicio
    contados = 0
    while True:
        if util(atual):
            contados += 1
            if contados == dias_uteis:
                break
        else:
            desconsiderados.append(
                DiaDesconsiderado(
                    atual,
                    _motivo_nao_util(atual, extras, considerar_nacionais, considerar_recesso),
                )
            )
        atual += timedelta(days=1)

    return ResultadoPrazo(
        data_publicacao=data_publicacao,
        dias_uteis=dias_uteis,
        inicio_contagem=inicio,
        vencimento=atual,
        dias_desconsiderados=desconsiderados,
    )
