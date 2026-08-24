# prazo-juridico-py

Calculadora de prazos processuais conforme o **Código de Processo Civil**
(Lei nº 13.105/2015).

Dado uma data de publicação/intimação e uma quantidade de dias, calcula a
data de vencimento do prazo contando apenas os dias úteis, com base nas
seguintes regras do CPC:

- **Art. 219** — na contagem de prazo em dias, computam-se somente os dias úteis.
- **Art. 224, caput e §3º** — exclui-se o dia da publicação/intimação; a
  contagem começa no primeiro dia útil seguinte.
- **Art. 220** — suspende-se o curso do prazo entre 20 de dezembro e 20 de
  janeiro, inclusive (recesso forense).
- Feriados nacionais (fixos e móveis: Sexta-feira Santa e Corpus Christi)
  são excluídos automaticamente da contagem.

Feriados locais/forenses (de tribunal ou comarca) não são fixos em lei
federal e por isso não entram automaticamente — podem ser informados à
parte, tanto pela biblioteca quanto pela CLI.

> **Nota:** esta ferramenta trata apenas de prazos regidos pelo CPC. Não
> considera regras específicas de outros ramos do processo (trabalhista,
> penal, eleitoral etc.) nem legislação estadual/administrativa.

## Instalação

Requer Python 3.10+. Sem dependências externas.

```bash
cd prazo-juridico-py
pip install -e .
```

## Uso como biblioteca

```python
from datetime import date
from prazo_juridico import calcular_prazo

resultado = calcular_prazo(date(2026, 8, 24), 15)  # 15 dias úteis
print(resultado)
```

```
Publicação/intimação: 24/08/2026
Início da contagem (art. 224, §3º, CPC): 25/08/2026
Prazo: 15 dia(s) útil(eis) (art. 219, CPC)
Vencimento: 15/09/2026
Dias não computados:
  - 29/08/2026: fim de semana
  - 30/08/2026: fim de semana
  - 05/09/2026: fim de semana
  - 06/09/2026: fim de semana
  - 07/09/2026: feriado nacional
  - 12/09/2026: fim de semana
  - 13/09/2026: fim de semana
```

Para informar feriados locais/forenses, ou desativar o recesso forense:

```python
from datetime import date
from prazo_juridico import calcular_prazo

feriados_do_foro = {date(2026, 9, 8)}  # aniversário da comarca, por exemplo

resultado = calcular_prazo(
    date(2026, 8, 24),
    15,
    feriados_extras=feriados_do_foro,
    considerar_recesso=True,
)
```

## Uso pela linha de comando

```bash
python -m prazo_juridico 24/08/2026 15
```

Com feriados locais adicionais (um por linha, formato `DD/MM/AAAA`,
linhas iniciadas com `#` são ignoradas):

```bash
python -m prazo_juridico 24/08/2026 15 --feriados feriados_locais.txt
```

Para ignorar o recesso forense:

```bash
python -m prazo_juridico 24/08/2026 15 --sem-recesso
```

Se instalado com `pip install -e .`, também é possível usar o comando
`prazo-juridico` diretamente, com os mesmos argumentos.

## Testes

```bash
pip install pytest
pytest
```
