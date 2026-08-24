"""Interface de linha de comando da calculadora de prazos processuais."""

from __future__ import annotations

import argparse
from datetime import date, datetime

from .calculadora import calcular_prazo


def _parse_data(texto: str) -> date:
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"data inválida: '{texto}' (use o formato DD/MM/AAAA)"
        ) from exc


def _parse_arquivo_feriados(caminho: str) -> set[date]:
    feriados: set[date] = set()
    with open(caminho, encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            try:
                feriados.add(_parse_data(linha))
            except argparse.ArgumentTypeError as exc:
                raise argparse.ArgumentTypeError(f"{caminho}:{numero}: {exc}") from exc
    return feriados


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prazo-juridico",
        description=(
            "Calculadora de prazos processuais conforme o CPC (Lei 13.105/2015): "
            "conta os dias úteis a partir do primeiro dia útil seguinte à "
            "publicação/intimação (art. 224, §3º), excluindo finais de semana, "
            "feriados nacionais (art. 216) e o recesso forense de 20/dez a "
            "20/jan (art. 220)."
        ),
    )
    parser.add_argument(
        "data_publicacao",
        type=_parse_data,
        help="data da publicação/intimação, no formato DD/MM/AAAA",
    )
    parser.add_argument(
        "dias",
        type=int,
        help="quantidade de dias úteis do prazo",
    )
    parser.add_argument(
        "--feriados",
        type=_parse_arquivo_feriados,
        default=None,
        metavar="ARQUIVO",
        dest="feriados_extras",
        help=(
            "arquivo texto com feriados locais/forenses adicionais do "
            "tribunal ou comarca, um por linha, no formato DD/MM/AAAA"
        ),
    )
    parser.add_argument(
        "--sem-recesso",
        action="store_true",
        help="não considerar o recesso forense de 20/dez a 20/jan (art. 220, CPC)",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = construir_parser()
    args = parser.parse_args(argv)

    try:
        resultado = calcular_prazo(
            args.data_publicacao,
            args.dias,
            feriados_extras=args.feriados_extras,
            considerar_recesso=not args.sem_recesso,
        )
    except ValueError as exc:
        parser.error(str(exc))
        return

    print(resultado)


if __name__ == "__main__":
    main()
