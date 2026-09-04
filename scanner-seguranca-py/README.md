# scanner-seguranca-py

Ferramenta básica de diagnóstico de segurança, em Python puro (sem
dependências externas). Três verificações simples e comuns em uma
primeira avaliação de exposição de um sistema:

- **Varredura de portas TCP** (`portas`) — verifica quais portas de um
  host aceitam conexão, entre uma lista de portas comuns ou uma lista
  informada.
- **Cabeçalhos HTTP de segurança** (`cabecalhos`) — verifica se uma URL
  responde com cabeçalhos recomendados (`Content-Security-Policy`,
  `Strict-Transport-Security`, `X-Frame-Options` etc.) e explica o que
  cada um mitiga.
- **Certificado TLS** (`tls`) — verifica protocolo, emissor e validade do
  certificado apresentado por um host.

> ## ⚠️ Uso responsável
>
> Use esta ferramenta **apenas em sistemas próprios ou com autorização
> explícita** do responsável pelo sistema. Escanear hosts de terceiros
> sem permissão pode violar a legislação de crimes cibernéticos (no
> Brasil, entre outras normas, a Lei nº 12.737/2012) e os termos de uso
> de provedores de hospedagem/nuvem. Esta ferramenta é passiva (não
> explora vulnerabilidades) e serve apenas como um diagnóstico inicial
> — não substitui uma avaliação de segurança profissional.

## Instalação

Requer Python 3.10+. Sem dependências externas.

```bash
cd scanner-seguranca-py
pip install -e .
```

## Uso pela linha de comando

```bash
# varre as portas comuns de um host
python -m scanner_seguranca portas meusite.com.br

# varre uma lista/intervalo específico de portas
python -m scanner_seguranca portas 192.168.0.10 --portas 22,80,443,8000-8010

# verifica cabeçalhos de segurança de uma URL
python -m scanner_seguranca cabecalhos https://meusite.com.br

# verifica o certificado TLS de um host
python -m scanner_seguranca tls meusite.com.br
```

Se instalado com `pip install -e .`, também é possível usar o comando
`scanner-seguranca` diretamente, com os mesmos argumentos.

## Uso como biblioteca

```python
from scanner_seguranca import escanear_portas, verificar_cabecalhos, verificar_certificado

resultados = escanear_portas("meusite.com.br", [22, 80, 443])
for r in resultados:
    print(r.porta, "aberta" if r.aberta else "fechada", r.servico)

cabecalhos = verificar_cabecalhos("https://meusite.com.br")
print(cabecalhos.presentes, cabecalhos.ausentes)

certificado = verificar_certificado("meusite.com.br")
print(certificado)
```

## Testes

```bash
pip install pytest
pytest
```

Os testes usam apenas servidores locais (`127.0.0.1`), sem depender de
rede externa.
