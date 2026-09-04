/**
 * Base de perguntas do checklist de conformidade com a LGPD
 * (Lei nº 13.709/2018), organizada por eixo temático.
 *
 * Cada item tem:
 *  - id: identificador estável (usado para salvar o estado)
 *  - texto: a pergunta/afirmação a ser avaliada
 *  - artigo: dispositivo da LGPD relacionado
 *  - peso: "essencial" (2 pontos) ou "recomendado" (1 ponto), usado no cálculo do score
 */
const CHECKLIST = [
  {
    categoria: "Governança e responsabilização",
    artigoBase: "art. 6º e 50",
    itens: [
      {
        id: "gov-politica-privacidade",
        texto: "Existe uma política de privacidade publicada e de fácil acesso para os titulares.",
        artigo: "art. 9º",
        peso: "essencial",
      },
      {
        id: "gov-programa-governanca",
        texto:
          "Há um programa de governança em privacidade, com papéis e responsabilidades definidos.",
        artigo: "art. 50",
        peso: "recomendado",
      },
      {
        id: "gov-treinamento",
        texto: "Colaboradores que lidam com dados pessoais recebem treinamento periódico sobre o tema.",
        artigo: "art. 50",
        peso: "recomendado",
      },
      {
        id: "gov-inventario",
        texto:
          "Existe um inventário/mapeamento dos dados pessoais tratados (o que é coletado, de onde vem, para onde vai).",
        artigo: "art. 37",
        peso: "essencial",
      },
    ],
  },
  {
    categoria: "Base legal e finalidade",
    artigoBase: "art. 6º, 7º e 11",
    itens: [
      {
        id: "base-hipotese-legal",
        texto: "Cada tratamento de dado pessoal tem uma base legal identificada e documentada.",
        artigo: "art. 7º",
        peso: "essencial",
      },
      {
        id: "base-dados-sensiveis",
        texto: "Tratamentos de dados sensíveis (saúde, biometria, origem racial etc.) têm base legal específica.",
        artigo: "art. 11",
        peso: "essencial",
      },
      {
        id: "base-finalidade-especifica",
        texto: "A finalidade de cada tratamento é específica, explícita e informada ao titular.",
        artigo: "art. 6º, I",
        peso: "essencial",
      },
      {
        id: "base-minimizacao",
        texto: "Os dados coletados são adequados e limitados ao mínimo necessário para a finalidade.",
        artigo: "art. 6º, III",
        peso: "recomendado",
      },
    ],
  },
  {
    categoria: "Consentimento",
    artigoBase: "art. 8º e 9º",
    itens: [
      {
        id: "consent-livre-informado",
        texto:
          "Quando usado como base legal, o consentimento é livre, informado e inequívoco, para finalidade determinada.",
        artigo: "art. 8º",
        peso: "essencial",
      },
      {
        id: "consent-registro",
        texto: "O consentimento coletado é registrado e pode ser comprovado posteriormente.",
        artigo: "art. 8º, §2º",
        peso: "essencial",
      },
      {
        id: "consent-revogacao",
        texto: "Existe um mecanismo simples para o titular revogar o consentimento a qualquer momento.",
        artigo: "art. 8º, §5º",
        peso: "essencial",
      },
      {
        id: "consent-sem-clausula-generica",
        texto: "Os textos de consentimento não usam cláusulas genéricas nem termos vagos.",
        artigo: "art. 8º, §4º",
        peso: "recomendado",
      },
    ],
  },
  {
    categoria: "Direitos dos titulares",
    artigoBase: "art. 18 e 19",
    itens: [
      {
        id: "dir-acesso",
        texto: "Existe canal para o titular solicitar confirmação e acesso aos seus dados.",
        artigo: "art. 18, I e II",
        peso: "essencial",
      },
      {
        id: "dir-correcao",
        texto: "Existe processo para correção de dados incompletos, inexatos ou desatualizados.",
        artigo: "art. 18, III",
        peso: "essencial",
      },
      {
        id: "dir-eliminacao",
        texto: "Existe processo para anonimização, bloqueio ou eliminação de dados desnecessários.",
        artigo: "art. 18, IV e VI",
        peso: "essencial",
      },
      {
        id: "dir-portabilidade",
        texto: "Existe processo para portabilidade dos dados a outro fornecedor de produto ou serviço.",
        artigo: "art. 18, V",
        peso: "recomendado",
      },
      {
        id: "dir-prazo-resposta",
        texto: "As solicitações dos titulares são respondidas dentro do prazo regulamentar.",
        artigo: "art. 19",
        peso: "essencial",
      },
    ],
  },
  {
    categoria: "Segurança da informação",
    artigoBase: "art. 46 a 49",
    itens: [
      {
        id: "seg-medidas-tecnicas",
        texto:
          "Existem medidas técnicas de segurança (criptografia, controle de acesso, backups, logs de auditoria).",
        artigo: "art. 46",
        peso: "essencial",
      },
      {
        id: "seg-medidas-administrativas",
        texto: "Existem medidas administrativas de segurança (políticas e normas internas).",
        artigo: "art. 46",
        peso: "recomendado",
      },
      {
        id: "seg-controle-acesso",
        texto: "O acesso a dados pessoais é restrito por perfil/necessidade (privilégio mínimo).",
        artigo: "art. 46",
        peso: "essencial",
      },
      {
        id: "seg-ambientes-teste",
        texto: "Ambientes de teste/desenvolvimento não usam dados reais sem anonimização ou mascaramento.",
        artigo: "art. 6º, VII",
        peso: "recomendado",
      },
    ],
  },
  {
    categoria: "Compartilhamento e transferência de dados",
    artigoBase: "art. 26 e 33",
    itens: [
      {
        id: "comp-contrato-operadores",
        texto:
          "O compartilhamento de dados com terceiros/operadores é feito mediante contrato com cláusulas de proteção de dados.",
        artigo: "art. 39",
        peso: "essencial",
      },
      {
        id: "comp-transferencia-internacional",
        texto: "Transferências internacionais de dados se enquadram em uma das hipóteses do art. 33.",
        artigo: "art. 33",
        peso: "essencial",
      },
      {
        id: "comp-registro-terceiros",
        texto: "Existe um registro atualizado dos operadores e terceiros com quem os dados são compartilhados.",
        artigo: "art. 37",
        peso: "recomendado",
      },
    ],
  },
  {
    categoria: "Encarregado (DPO)",
    artigoBase: "art. 41",
    itens: [
      {
        id: "dpo-indicado",
        texto: "Foi indicado um encarregado (DPO) pelo tratamento de dados pessoais.",
        artigo: "art. 41, caput",
        peso: "essencial",
      },
      {
        id: "dpo-contato-publico",
        texto: "A identidade e o contato do encarregado são divulgados publicamente.",
        artigo: "art. 41, §1º",
        peso: "essencial",
      },
      {
        id: "dpo-canal-titulares",
        texto:
          "O encarregado atua como canal de comunicação entre titulares, ANPD e a organização.",
        artigo: "art. 41, §2º",
        peso: "recomendado",
      },
    ],
  },
  {
    categoria: "Resposta a incidentes de segurança",
    artigoBase: "art. 48",
    itens: [
      {
        id: "inc-plano-resposta",
        texto: "Existe um plano de resposta a incidentes de segurança envolvendo dados pessoais.",
        artigo: "art. 46",
        peso: "essencial",
      },
      {
        id: "inc-comunicacao",
        texto:
          "Existe processo para comunicar incidentes relevantes à ANPD e aos titulares em prazo razoável.",
        artigo: "art. 48",
        peso: "essencial",
      },
      {
        id: "inc-registro-analise",
        texto: "Incidentes são registrados e analisados (causas, impacto, medidas corretivas).",
        artigo: "art. 48, §1º",
        peso: "recomendado",
      },
    ],
  },
  {
    categoria: "Relatório de Impacto à Proteção de Dados",
    artigoBase: "art. 38",
    itens: [
      {
        id: "ripd-realizado",
        texto:
          "Foi elaborado (ou está previsto) um Relatório de Impacto à Proteção de Dados (RIPD) para operações de alto risco.",
        artigo: "art. 38",
        peso: "recomendado",
      },
    ],
  },
];

const PESOS = { essencial: 2, recomendado: 1 };
