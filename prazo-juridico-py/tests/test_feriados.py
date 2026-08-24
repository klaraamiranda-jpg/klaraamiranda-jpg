from datetime import date

from prazo_juridico.feriados import (
    carnaval,
    corpus_christi,
    feriados_nacionais,
    pascoa,
    sexta_feira_santa,
)


def test_pascoa_datas_conhecidas():
    assert pascoa(2024) == date(2024, 3, 31)
    assert pascoa(2025) == date(2025, 4, 20)
    assert pascoa(2026) == date(2026, 4, 5)


def test_sexta_feira_santa():
    assert sexta_feira_santa(2024) == date(2024, 3, 29)


def test_carnaval():
    segunda, terca = carnaval(2024)
    assert segunda == date(2024, 2, 12)
    assert terca == date(2024, 2, 13)


def test_corpus_christi():
    assert corpus_christi(2024) == date(2024, 5, 30)


def test_feriados_nacionais_contem_fixos():
    feriados = feriados_nacionais(2024)
    assert date(2024, 1, 1) in feriados
    assert date(2024, 4, 21) in feriados
    assert date(2024, 5, 1) in feriados
    assert date(2024, 9, 7) in feriados
    assert date(2024, 10, 12) in feriados
    assert date(2024, 11, 2) in feriados
    assert date(2024, 11, 15) in feriados
    assert date(2024, 12, 25) in feriados


def test_feriados_nacionais_inclui_moveis_por_padrao():
    feriados = feriados_nacionais(2024)
    assert sexta_feira_santa(2024) in feriados
    assert corpus_christi(2024) in feriados


def test_feriados_nacionais_sem_moveis():
    feriados = feriados_nacionais(2024, incluir_moveis=False)
    assert sexta_feira_santa(2024) not in feriados


def test_carnaval_nao_e_feriado_nacional_automatico():
    segunda, terca = carnaval(2024)
    feriados = feriados_nacionais(2024)
    assert segunda not in feriados
    assert terca not in feriados


def test_consciencia_negra_apenas_a_partir_de_2024():
    assert date(2023, 11, 20) not in feriados_nacionais(2023)
    assert date(2024, 11, 20) in feriados_nacionais(2024)
