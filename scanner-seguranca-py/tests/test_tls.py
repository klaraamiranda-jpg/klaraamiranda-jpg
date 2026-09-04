from datetime import datetime, timedelta, timezone

from scanner_seguranca.tls import _extrair_nome, _processar_certificado


def test_extrair_nome():
    componentes = (
        (("countryName", "BR"),),
        (("commonName", "exemplo.com.br"),),
    )
    assert _extrair_nome(componentes) == "exemplo.com.br"


def test_extrair_nome_ausente():
    assert _extrair_nome(()) == "desconhecido"


def _certificado_com_validade(delta: timedelta) -> dict:
    validade = datetime.now(timezone.utc) + delta
    return {
        "subject": ((("commonName", "exemplo.com.br"),),),
        "issuer": ((("commonName", "Autoridade Exemplo"),),),
        "notAfter": validade.strftime("%b %d %H:%M:%S %Y GMT"),
    }


def test_processar_certificado_valido():
    certificado = _certificado_com_validade(timedelta(days=30))
    resultado = _processar_certificado(certificado, "TLSv1.3", "exemplo.com.br", 443)

    assert resultado.emitido_para == "exemplo.com.br"
    assert resultado.emitido_por == "Autoridade Exemplo"
    assert 28 <= resultado.dias_para_expirar <= 30
    assert "EXPIRADO" not in str(resultado)


def test_processar_certificado_expirado():
    certificado = _certificado_com_validade(timedelta(days=-5))
    resultado = _processar_certificado(certificado, "TLSv1.2", "exemplo.com.br", 443)

    assert resultado.dias_para_expirar < 0
    assert "EXPIRADO" in str(resultado)


def test_processar_certificado_expirando_em_breve():
    certificado = _certificado_com_validade(timedelta(days=10))
    resultado = _processar_certificado(certificado, "TLSv1.3", "exemplo.com.br", 443)

    assert "expira em breve" in str(resultado)
