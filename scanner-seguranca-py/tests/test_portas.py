import socket
import threading

from scanner_seguranca.portas import escanear_portas


def _porta_livre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_escanear_portas_detecta_porta_aberta_e_fechada():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("127.0.0.1", 0))
    servidor.listen(1)
    porta_aberta = servidor.getsockname()[1]

    def aceitar_conexoes():
        try:
            while True:
                conexao, _ = servidor.accept()
                conexao.close()
        except OSError:
            pass

    thread = threading.Thread(target=aceitar_conexoes, daemon=True)
    thread.start()

    try:
        porta_fechada = _porta_livre()  # criada e liberada, ninguém escuta nela

        resultados = escanear_portas(
            "127.0.0.1", [porta_aberta, porta_fechada], timeout=0.5
        )
        por_porta = {r.porta: r.aberta for r in resultados}

        assert por_porta[porta_aberta] is True
        assert por_porta[porta_fechada] is False
    finally:
        servidor.close()


def test_escanear_portas_lista_vazia():
    assert escanear_portas("127.0.0.1", []) == []
