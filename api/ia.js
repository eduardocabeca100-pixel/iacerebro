export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Método não permitido" });
  }

  try {
    const body = req.body || {};
    const apiKey = process.env.GROQ_API_KEY;
    const model = process.env.GROQ_MODEL || "llama-3.3-70b-versatile";

    if (!apiKey) {
      return res.status(200).json({
        demo: true,
        output: respostaDemo(body),
        message: "GROQ_API_KEY ainda não configurada. Rodando resposta demo."
      });
    }

    const messages = montarMensagens(body);

    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        messages,
        temperature: 0.35,
        max_tokens: 2400
      })
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: "Erro no Groq",
        detail: data
      });
    }

    const output = data?.choices?.[0]?.message?.content || "A IA respondeu, mas não retornou texto legível.";

    return res.status(200).json({ output });
  } catch (error) {
    return res.status(500).json({
      error: "Erro interno na rota de IA com Groq",
      detail: error.message
    });
  }
}

function montarMensagens(body) {
  const task = body.task || "chat";
  const project = body.project || {};
  const blockName = body.blockName || "";
  const text = body.text || "";
  const question = body.question || "";

  const system = `
Você é a IA especialista do CÉREBRO IA, um sistema para criação, análise, revisão e exportação de projetos culturais para editais.

Regras:
- Responda sempre em português do Brasil.
- Use linguagem profissional de edital cultural.
- Escreva textos prontos para copiar e colar.
- Seja objetivo, claro e forte.
- Não invente CPF, CNPJ, endereço, nome de documento ou dado sensível.
- Quando faltar dado, escreva de forma neutra e adaptável.
- Foque em aprovação: clareza, impacto cultural, viabilidade, acessibilidade, contrapartida, orçamento e documentação.
- Não diga que é uma IA.
`;

  const contexto = `
Contexto do projeto:
${JSON.stringify(project, null, 2)}
`;

  if (task === "improveBlock") {
    return [
      { role: "system", content: system },
      { role: "user", content: `${contexto}

Melhore o bloco "${blockName}" abaixo para ser colado diretamente em um edital.

Texto atual:
${text}

Entregue somente o texto final melhorado.` }
    ];
  }

  if (task === "applyAllFixes") {
    return [
      { role: "system", content: system },
      { role: "user", content: `${contexto}

Melhore todos os blocos abaixo.

Blocos:
${JSON.stringify(body.blocks || {}, null, 2)}

Retorne em JSON puro, sem markdown, neste formato:
{
  "blocks": {
    "Nome do bloco": "texto melhorado"
  },
  "scoreSuggestion": 92,
  "summary": "resumo curto das melhorias aplicadas"
}` }
    ];
  }

  if (task === "chat") {
    return [
      { role: "system", content: system },
      { role: "user", content: `${contexto}

Pergunta do usuário:
${question}

Responda como consultor de projetos culturais. Seja prático, direto e ajude a resolver o problema dentro do projeto.` }
    ];
  }

  if (task === "reviewProject") {
    return [
      { role: "system", content: system },
      { role: "user", content: `${contexto}

Simule uma banca avaliadora e entregue:
1. Nota estimada de 0 a 100.
2. Pontos fortes.
3. Riscos de reprovação.
4. Melhorias obrigatórias.
5. Checklist final.` }
    ];
  }

  return [
    { role: "system", content: system },
    { role: "user", content: `${contexto}

${question || text || "Ajude a melhorar este projeto cultural."}` }
  ];
}

function respostaDemo(body) {
  if (body.task === "improveBlock") {
    return `${body.text || ""}

Texto aprimorado: A redação foi fortalecida para evidenciar aderência ao edital, relevância cultural, viabilidade técnica, democratização de acesso, acessibilidade e coerência entre metodologia, equipe e orçamento.`;
  }

  if (body.task === "applyAllFixes") {
    const blocks = body.blocks || {};
    const improved = {};

    Object.keys(blocks).forEach((key) => {
      improved[key] = `${blocks[key]}

Aprimoramento aplicado: este bloco foi revisado para ficar mais claro, objetivo, avaliável e alinhado aos critérios do edital.`;
    });

    return JSON.stringify({
      blocks: improved,
      scoreSuggestion: 92,
      summary: "Blocos revisados em modo demonstração."
    });
  }

  if (body.task === "chat") {
    return "Sugiro revisar justificativa, acessibilidade, contrapartida social, coerência do orçamento e documentação da equipe antes do envio.";
  }

  return "Resposta demo do CÉREBRO IA.";
}
