export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Método não permitido" });
  }

  try {
    const body = req.body || {};
    const apiKey = process.env.OPENAI_API_KEY;
    const model = process.env.OPENAI_MODEL || "gpt-5.5";

    if (!apiKey) {
      return res.status(200).json({
        demo: true,
        output: respostaDemo(body),
        message: "OPENAI_API_KEY ainda não configurada. Rodando resposta demo."
      });
    }

    const prompt = montarPrompt(body);

    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        input: prompt,
        text: {
          verbosity: "medium"
        }
      })
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({
        error: "Erro na OpenAI",
        detail: data
      });
    }

    return res.status(200).json({
      output: data.output_text || extrairTexto(data) || "A IA respondeu, mas não retornou texto legível."
    });
  } catch (error) {
    return res.status(500).json({
      error: "Erro interno na rota de IA",
      detail: error.message
    });
  }
}

function montarPrompt(body) {
  const task = body.task || "geral";
  const project = body.project || {};
  const blockName = body.blockName || "";
  const text = body.text || "";
  const question = body.question || "";

  const base = `
Você é a IA especialista do sistema CÉREBRO IA, um SaaS para criação, revisão e aprovação de projetos culturais em editais públicos.

Regras:
- Escreva em português do Brasil.
- Use linguagem profissional de edital cultural.
- Seja objetivo, forte e copiável.
- Não invente dados sensíveis.
- Quando faltar dado, escreva de forma neutra e adaptável.
- Foque em aprovação: clareza, impacto cultural, viabilidade, acessibilidade, contrapartida, orçamento e documentação.
- Não mencione que é uma IA.
- Não use markdown excessivo se o texto for para colar no edital.

Projeto:
${JSON.stringify(project, null, 2)}
`;

  if (task === "improveBlock") {
    return `${base}

Tarefa: melhorar o bloco "${blockName}" para ser colado diretamente em um edital.

Texto atual:
${text}

Entregue somente o texto final melhorado.`;
  }

  if (task === "applyAllFixes") {
    return `${base}

Tarefa: melhorar todos os blocos do projeto abaixo.

Blocos:
${JSON.stringify(body.blocks || {}, null, 2)}

Retorne em JSON puro, sem markdown, neste formato:
{
  "blocks": {
    "Nome do bloco": "texto melhorado"
  },
  "scoreSuggestion": 92,
  "summary": "resumo curto das melhorias aplicadas"
}`;
  }

  if (task === "chat") {
    return `${base}

Pergunta do usuário:
${question}

Responda como consultor de projetos culturais, com orientação prática e aplicável ao projeto.`;
  }

  if (task === "reviewProject") {
    return `${base}

Tarefa: simular uma banca avaliadora.

Avalie o projeto e retorne:
- nota estimada de 0 a 100;
- principais riscos;
- melhorias obrigatórias;
- pontos fortes;
- checklist final.`;
  }

  return `${base}

Tarefa geral:
${question || text || "Ajude a melhorar este projeto cultural."}`;
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

function extrairTexto(data) {
  try {
    return data.output
      ?.flatMap(item => item.content || [])
      ?.map(content => content.text || "")
      ?.join("\n")
      ?.trim();
  } catch {
    return "";
  }
}
