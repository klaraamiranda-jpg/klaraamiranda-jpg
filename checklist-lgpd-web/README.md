# checklist-lgpd-web

Verificador de conformidade com a **LGPD** (Lei nº 13.709/2018), em uma
única página estática (HTML + CSS + JavaScript puro, sem dependências ou
build).

Apresenta um checklist organizado em 9 eixos temáticos (governança, base
legal, consentimento, direitos dos titulares, segurança da informação,
compartilhamento de dados, encarregado/DPO, resposta a incidentes e
relatório de impacto), com 31 itens ao todo, cada um referenciando o
artigo correspondente da lei.

> **Aviso:** é uma ferramenta educativa/orientativa para autoavaliação.
> Não substitui uma análise jurídica formal de conformidade com a LGPD.

## Funcionalidades

- Pontuação geral e por categoria, com peso maior para itens marcados
  como "essencial" em relação aos "recomendado".
- Filtro para mostrar somente os itens ainda pendentes.
- Exportação do resultado como relatório em texto (`.txt`).
- Respostas salvas no `localStorage` do navegador — nada é enviado a
  nenhum servidor.

## Como usar

Não precisa de instalação nem de servidor: basta abrir o `index.html`
diretamente no navegador.

Se preferir servir via HTTP (por exemplo, para evitar restrições de
`file://` em alguns navegadores):

```bash
cd checklist-lgpd-web
python3 -m http.server 8000
```

E acesse `http://localhost:8000` no navegador.

## Estrutura

- `index.html` — estrutura da página
- `style.css` — estilos (com suporte a modo escuro via `prefers-color-scheme`)
- `checklist.js` — dados do checklist (perguntas, artigos da LGPD, pesos)
- `script.js` — lógica da aplicação (renderização, pontuação, persistência, exportação)
