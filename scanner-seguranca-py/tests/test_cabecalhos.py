import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from scanner_seguranca.cabecalhos import _normalizar_url, verificar_cabecalhos


class _HandlerComAlgunsCabecalhos(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format, *args):  # silencia log de teste
        pass


@pytest.fixture
def servidor_teste():
    servidor = HTTPServer(("127.0.0.1", 0), _HandlerComAlgunsCabecalhos)
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    yield servidor
    servidor.shutdown()
    thread.join()


def test_verificar_cabecalhos_detecta_presentes_e_ausentes(servidor_teste):
    porta = servidor_teste.server_address[1]
    resultado = verificar_cabecalhos(f"http://127.0.0.1:{porta}/")

    assert resultado.status == 200
    assert "X-Content-Type-Options" in resultado.presentes
    assert "X-Frame-Options" in resultado.presentes
    assert "Content-Security-Policy" in resultado.ausentes
    assert "Strict-Transport-Security" in resultado.ausentes


def test_normalizar_url_adiciona_https_por_padrao():
    assert _normalizar_url("exemplo.com.br") == "https://exemplo.com.br"
    assert _normalizar_url("http://exemplo.com.br") == "http://exemplo.com.br"
    assert _normalizar_url("https://exemplo.com.br") == "https://exemplo.com.br"
