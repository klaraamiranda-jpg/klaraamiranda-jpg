"""Cálculo de feriados nacionais usados na contagem de prazos processuais."""

from __future__ import annotations

from datetime import date, timedelta

# Feriados nacionais de data fixa (Lei nº 10.607/2002, art. 1º).
FERIADOS_FIXOS: tuple[tuple[int, int], ...] = (
    (1, 1),    # Confraternização Universal
    (4, 21),   # Tiradentes
    (5, 1),    # Dia do Trabalho
    (9, 7),    # Independência do Brasil
    (10, 12),  # Nossa Senhora Aparecida
    (11, 2),   # Finados
    (11, 15),  # Proclamação da República
    (12, 25),  # Natal
)

# Dia Nacional de Zumbi e da Consciência Negra: feriado nacional desde 2024
# (Lei nº 14.759/2023).
ANO_INICIO_CONSCIENCIA_NEGRA = 2024


def pascoa(ano: int) -> date:
    """Data da Páscoa no ano informado (algoritmo de Gauss/Meeus)."""
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(ano, mes, dia)


def sexta_feira_santa(ano: int) -> date:
    """Sexta-feira da Paixão (dois dias antes da Páscoa)."""
    return pascoa(ano) - timedelta(days=2)


def carnaval(ano: int) -> tuple[date, date]:
    """Segunda e terça-feira de carnaval."""
    terca = pascoa(ano) - timedelta(days=47)
    segunda = terca - timedelta(days=1)
    return segunda, terca


def corpus_christi(ano: int) -> date:
    """Corpus Christi (60 dias após a Páscoa)."""
    return pascoa(ano) + timedelta(days=60)


def feriados_nacionais(ano: int, *, incluir_moveis: bool = True) -> set[date]:
    """
    Retorna o conjunto de feriados nacionais do ano informado.

    Inclui os feriados de data fixa e, quando `incluir_moveis` for
    verdadeiro (padrão), a Sexta-feira Santa e o Corpus Christi.
    Carnaval não é feriado nacional por lei (é ponto facultativo), por
    isso não entra automaticamente; use `carnaval()` e o parâmetro
    `feriados_extras` das funções de cálculo de prazo se o tribunal em
    questão o tratar como feriado forense.
    """
    feriados = {date(ano, mes, dia) for mes, dia in FERIADOS_FIXOS}
    if ano >= ANO_INICIO_CONSCIENCIA_NEGRA:
        feriados.add(date(ano, 11, 20))
    if incluir_moveis:
        feriados.add(sexta_feira_santa(ano))
        feriados.add(corpus_christi(ano))
    return feriados
