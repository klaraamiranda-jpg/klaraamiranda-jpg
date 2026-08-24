from datetime import date

import pytest

from prazo_juridico.calculadora import (
    calcular_prazo,
    eh_dia_util,
    em_recesso_forense,
    proximo_dia_util,
)


def test_em_recesso_forense():
    assert em_recesso_forense(date(2026, 12, 20)) is True
    assert em_recesso_forense(date(2027, 1, 20)) is True
    assert em_recesso_forense(date(2026, 12, 19)) is False
    assert em_recesso_forense(date(2027, 1, 21)) is False


def test_eh_dia_util_fim_de_semana():
    assert eh_dia_util(date(2026, 8, 22)) is False  # sábado
    assert eh_dia_util(date(2026, 8, 24)) is True  # segunda-feira


def test_eh_dia_util_feriado_nacional():
    assert eh_dia_util(date(2026, 9, 7)) is False  # Independência (segunda-feira)


def test_eh_dia_util_recesso_forense():
    assert eh_dia_util(date(2026, 1, 5)) is False
    assert eh_dia_util(date(2026, 1, 5), considerar_recesso=False) is True


def test_proximo_dia_util_a_partir_de_sabado():
    assert proximo_dia_util(date(2026, 8, 22)) == date(2026, 8, 24)


def test_calcular_prazo_simples_sem_feriados():
    # Segunda-feira 24/08/2026: publicação.
    # Início da contagem: terça 25/08/2026.
    # Prazo de 5 dias úteis (25,26,27,28 e 31 - pula sáb/dom) -> vence 31/08/2026.
    resultado = calcular_prazo(date(2026, 8, 24), 5, considerar_recesso=False)
    assert resultado.inicio_contagem == date(2026, 8, 25)
    assert resultado.vencimento == date(2026, 8, 31)


def test_calcular_prazo_pula_fim_de_semana():
    # Sexta-feira 21/08/2026: publicação. Início: segunda 24/08/2026.
    # Prazo de 1 dia útil -> vence 24/08/2026.
    resultado = calcular_prazo(date(2026, 8, 21), 1)
    assert resultado.inicio_contagem == date(2026, 8, 24)
    assert resultado.vencimento == date(2026, 8, 24)
    # o fim de semana ficou entre a publicação e o início da contagem,
    # não dentro da janela de contagem em si, então não é listado aqui.
    assert resultado.dias_desconsiderados == []


def test_calcular_prazo_considera_recesso_forense():
    # Publicação em 18/12/2026 (sexta). O recesso forense (20/dez a 20/jan)
    # deve empurrar o vencimento para depois de 20/01/2027.
    resultado = calcular_prazo(date(2026, 12, 18), 2)
    assert resultado.vencimento > date(2027, 1, 20)


def test_calcular_prazo_ignora_recesso_quando_desativado():
    com_recesso = calcular_prazo(date(2026, 12, 18), 2)
    sem_recesso = calcular_prazo(date(2026, 12, 18), 2, considerar_recesso=False)
    assert sem_recesso.vencimento < com_recesso.vencimento


def test_calcular_prazo_feriados_extras():
    extras = {date(2026, 8, 26)}  # quarta-feira marcada como feriado local
    resultado = calcular_prazo(
        date(2026, 8, 24), 3, feriados_extras=extras, considerar_recesso=False
    )
    motivos = [d.motivo for d in resultado.dias_desconsiderados]
    assert "feriado local/forense" in motivos


def test_calcular_prazo_dias_invalido():
    with pytest.raises(ValueError):
        calcular_prazo(date(2026, 1, 1), 0)
