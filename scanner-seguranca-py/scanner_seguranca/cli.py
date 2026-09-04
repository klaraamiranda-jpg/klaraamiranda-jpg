"""Interface de linha de comando do scanner de segurança."""

from __future__ import annotations

import argparse
import socket

from .cabecalhos import verificar_cabecalhos
from .portas import escanear_portas
from .tls import verificar_certificado

AVISO = (
    "Use esta ferramenta apenas em sistemas próprios ou com autorização explícita\n"
    "do responsável. Escanear hosts de terceiros sem permissão pode violar a\n"
    "legislação de crimes cibernéticos e os termos de uso do provedor."
)


def _parse_portas(texto: str) -> list[int]:
    portas: list[int] = []
    for parte in texto.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "-" in parte:
            inicio, fim = parte.split("-", 1)
            portas.extend(range(int(inicio), int(fim) + 1))
        else:
            portas.append(int(parte))
    return portas


def _cmd_portas(args: argparse.Namespace) -> None:
    resultados = escanear_portas(args.host, args.portas, timeout=args.timeout)
    abertas = [r for r in resultados if r.aberta]
    print(f"Varredura de portas em {args.host} ({len(resultados)} porta(s) verificada(s))")
    if not abertas:
        print("Nenhuma porta aberta encontrada entre as verificadas.")
        return
    for resultado in abertas:
        servico = f" ({resultado.servico})" if resultado.servico else ""
        print(f"  {resultado.porta}/tcp aberta{servico}")


def _cmd_cabecalhos(args: argparse.Namespace) -> None:
    resultado = verificar_cabecalhos(args.url, timeout=args.timeout)
    print(resultado)


def _cmd_tls(args: argparse.Namespace) -> None:
    resultado = verificar_certificado(args.host, args.porta, timeout=args.timeout)
    print(resultado)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scanner-seguranca",
        description=(
            "Ferramenta básica de diagnóstico de segurança: varredura de portas TCP,\n"
            "verificação de cabeçalhos HTTP de segurança e checagem de certificado TLS.\n\n"
            + AVISO
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    p_portas = subparsers.add_parser("portas", help="varredura de portas TCP em um host")
    p_portas.add_argument("host", help="host ou IP a verificar")
    p_portas.add_argument(
        "--portas",
        type=_parse_portas,
        default=None,
        metavar="LISTA",
        help="portas a verificar, ex.: 22,80,443 ou 1-1024 (padrão: portas comuns)",
    )
    p_portas.add_argument("--timeout", type=float, default=1.0, help="timeout por porta, em segundos")
    p_portas.set_defaults(func=_cmd_portas)

    p_cabecalhos = subparsers.add_parser(
        "cabecalhos", help="verifica cabeçalhos HTTP de segurança de uma URL"
    )
    p_cabecalhos.add_argument("url", help="URL a verificar (ex.: https://exemplo.com.br)")
    p_cabecalhos.add_argument("--timeout", type=float, default=5.0)
    p_cabecalhos.set_defaults(func=_cmd_cabecalhos)

    p_tls = subparsers.add_parser("tls", help="verifica o certificado TLS de um host")
    p_tls.add_argument("host", help="host a verificar")
    p_tls.add_argument("--porta", type=int, default=443)
    p_tls.add_argument("--timeout", type=float, default=5.0)
    p_tls.set_defaults(func=_cmd_tls)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = construir_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except (TimeoutError, socket.timeout):
        parser.error("tempo limite excedido ao conectar ao alvo.")
    except OSError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
