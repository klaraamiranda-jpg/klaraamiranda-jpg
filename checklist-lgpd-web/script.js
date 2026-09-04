/**
 * Lógica do verificador de conformidade com a LGPD.
 * Todo o estado é salvo no localStorage do navegador — nada é enviado
 * para nenhum servidor.
 */
(function () {
  "use strict";

  const CHAVE_ARMAZENAMENTO = "checklist-lgpd-web:respostas";

  const elCategorias = document.getElementById("categorias");
  const elScoreValor = document.getElementById("score-valor");
  const elScoreBarra = document.getElementById("score-barra");
  const elScoreResumo = document.getElementById("score-resumo");
  const elFiltroPendentes = document.getElementById("filtro-pendentes");
  const elBotaoReset = document.getElementById("botao-reset");
  const elBotaoExportar = document.getElementById("botao-exportar");
  const elAtualizadoEm = document.getElementById("atualizado-em");

  let respostas = carregarRespostas();
  let somentePendentes = false;

  function carregarRespostas() {
    try {
      const bruto = localStorage.getItem(CHAVE_ARMAZENAMENTO);
      return bruto ? JSON.parse(bruto) : {};
    } catch (erro) {
      console.warn("Não foi possível ler o armazenamento local:", erro);
      return {};
    }
  }

  function salvarRespostas() {
    try {
      localStorage.setItem(CHAVE_ARMAZENAMENTO, JSON.stringify(respostas));
    } catch (erro) {
      console.warn("Não foi possível salvar no armazenamento local:", erro);
    }
  }

  function todosOsItens() {
    return CHECKLIST.flatMap((grupo) => grupo.itens);
  }

  function calcularScore() {
    const itens = todosOsItens();
    let pontosObtidos = 0;
    let pontosTotais = 0;

    for (const item of itens) {
      const peso = PESOS[item.peso] || 1;
      pontosTotais += peso;
      if (respostas[item.id]) {
        pontosObtidos += peso;
      }
    }

    const percentual = pontosTotais === 0 ? 0 : Math.round((pontosObtidos / pontosTotais) * 100);

    const porCategoria = CHECKLIST.map((grupo) => {
      let obtidos = 0;
      let totais = 0;
      for (const item of grupo.itens) {
        const peso = PESOS[item.peso] || 1;
        totais += peso;
        if (respostas[item.id]) obtidos += peso;
      }
      return {
        categoria: grupo.categoria,
        percentual: totais === 0 ? 0 : Math.round((obtidos / totais) * 100),
        concluidos: grupo.itens.filter((item) => respostas[item.id]).length,
        total: grupo.itens.length,
      };
    });

    return { percentual, porCategoria, marcados: itens.filter((i) => respostas[i.id]).length, total: itens.length };
  }

  function nivelDoScore(percentual) {
    if (percentual >= 80) return { rotulo: "Bom nível de conformidade", classe: "score-alto" };
    if (percentual >= 50) return { rotulo: "Conformidade parcial", classe: "score-medio" };
    return { rotulo: "Atenção: conformidade baixa", classe: "score-baixo" };
  }

  function renderizarScore() {
    const { percentual, porCategoria, marcados, total } = calcularScore();
    const nivel = nivelDoScore(percentual);

    elScoreValor.textContent = percentual + "%";
    elScoreValor.className = "score-valor " + nivel.classe;
    elScoreBarra.style.width = percentual + "%";
    elScoreBarra.className = "score-barra-preenchida " + nivel.classe;
    elScoreResumo.textContent = `${nivel.rotulo} — ${marcados} de ${total} itens atendidos.`;

    return porCategoria;
  }

  function criarItem(item, grupo) {
    const li = document.createElement("li");
    li.className = "item";
    li.dataset.itemId = item.id;

    const label = document.createElement("label");
    label.className = "item-label";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = Boolean(respostas[item.id]);
    checkbox.addEventListener("change", () => {
      respostas[item.id] = checkbox.checked;
      salvarRespostas();
      atualizarTudo();
    });

    const textoWrapper = document.createElement("span");
    textoWrapper.className = "item-texto";

    const texto = document.createElement("span");
    texto.textContent = item.texto;

    const meta = document.createElement("span");
    meta.className = "item-meta";
    const badgePeso = document.createElement("span");
    badgePeso.className = "badge badge-" + item.peso;
    badgePeso.textContent = item.peso === "essencial" ? "Essencial" : "Recomendado";
    const badgeArtigo = document.createElement("span");
    badgeArtigo.className = "badge badge-artigo";
    badgeArtigo.textContent = "LGPD, " + item.artigo;

    meta.appendChild(badgePeso);
    meta.appendChild(badgeArtigo);

    textoWrapper.appendChild(texto);
    textoWrapper.appendChild(meta);

    label.appendChild(checkbox);
    label.appendChild(textoWrapper);
    li.appendChild(label);

    return li;
  }

  function renderizarCategorias(porCategoria) {
    elCategorias.innerHTML = "";

    CHECKLIST.forEach((grupo, indice) => {
      const infoCategoria = porCategoria[indice];

      const itensVisiveis = somentePendentes
        ? grupo.itens.filter((item) => !respostas[item.id])
        : grupo.itens;

      if (somentePendentes && itensVisiveis.length === 0) {
        return;
      }

      const secao = document.createElement("section");
      secao.className = "categoria";

      const cabecalho = document.createElement("div");
      cabecalho.className = "categoria-cabecalho";

      const titulo = document.createElement("h2");
      titulo.textContent = grupo.categoria;

      const progresso = document.createElement("span");
      progresso.className = "categoria-progresso";
      progresso.textContent = `${infoCategoria.concluidos}/${infoCategoria.total} · ${infoCategoria.percentual}%`;

      cabecalho.appendChild(titulo);
      cabecalho.appendChild(progresso);

      const lista = document.createElement("ul");
      lista.className = "lista-itens";
      itensVisiveis.forEach((item) => lista.appendChild(criarItem(item, grupo)));

      secao.appendChild(cabecalho);
      secao.appendChild(lista);
      elCategorias.appendChild(secao);
    });

    if (somentePendentes && elCategorias.children.length === 0) {
      const vazio = document.createElement("p");
      vazio.className = "estado-vazio";
      vazio.textContent = "Nenhum item pendente — todos os pontos avaliados foram marcados.";
      elCategorias.appendChild(vazio);
    }
  }

  function atualizarTudo() {
    const porCategoria = renderizarScore();
    renderizarCategorias(porCategoria);
    elAtualizadoEm.textContent = "Última alteração: " + new Date().toLocaleString("pt-BR");
  }

  function resetarRespostas() {
    const confirmar = window.confirm(
      "Isso vai apagar todas as respostas marcadas neste navegador. Deseja continuar?"
    );
    if (!confirmar) return;
    respostas = {};
    salvarRespostas();
    atualizarTudo();
  }

  function gerarTextoRelatorio() {
    const { percentual, marcados, total } = calcularScore();
    const linhas = [];
    linhas.push("Relatório de conformidade com a LGPD (Lei nº 13.709/2018)");
    linhas.push("Gerado em: " + new Date().toLocaleString("pt-BR"));
    linhas.push(`Pontuação geral: ${percentual}% (${marcados}/${total} itens atendidos)`);
    linhas.push("");

    CHECKLIST.forEach((grupo) => {
      linhas.push(`## ${grupo.categoria}`);
      grupo.itens.forEach((item) => {
        const marcado = respostas[item.id] ? "[x]" : "[ ]";
        linhas.push(`${marcado} (${item.peso}, LGPD ${item.artigo}) ${item.texto}`);
      });
      linhas.push("");
    });

    linhas.push(
      "Aviso: este relatório é uma autoavaliação orientativa e não substitui" +
        " uma análise jurídica formal de conformidade com a LGPD."
    );

    return linhas.join("\n");
  }

  function exportarRelatorio() {
    const texto = gerarTextoRelatorio();
    const blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const data = new Date().toISOString().slice(0, 10);
    link.href = url;
    link.download = `relatorio-lgpd-${data}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  elFiltroPendentes.addEventListener("change", () => {
    somentePendentes = elFiltroPendentes.checked;
    atualizarTudo();
  });

  elBotaoReset.addEventListener("click", resetarRespostas);
  elBotaoExportar.addEventListener("click", exportarRelatorio);

  atualizarTudo();
})();
