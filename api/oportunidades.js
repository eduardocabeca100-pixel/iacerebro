export default async function handler(req, res) {
  if (req.method !== "GET") {
    return res.status(405).json({ error: "Método não permitido" });
  }

  const uf = String(req.query.uf || "SC").toUpperCase();
  const linguagem = String(req.query.linguagem || "Teatro");
  const q = String(req.query.q || "");

  const apiKey = process.env.OPENAI_API_KEY;
  const model = process.env.OPENAI_MODEL || "gpt-5.5";

  if (!apiKey) {
    return res.status(200).json(filtrarBaseDemo(uf, linguagem, q));
  }

  try {
    const prompt = `
Busque oportunidades, editais, prêmios, chamamentos públicos e fomento cultural atualmente abertos ou recentemente publicados no Brasil.

Filtros:
- UF: ${uf}
- Linguagem: ${linguagem}
- Palavra-chave: ${q || "sem palavra-chave"}

Priorize fontes oficiais: Governo Federal, Ministério da Cultura, secretarias estaduais/municipais de cultura, fundações culturais, Mapas Culturais, Prosas e páginas oficiais de editais.

Retorne SOMENTE JSON puro, sem markdown, neste formato:
[
  {
    "id": "op1",
    "title": "nome do edital",
    "uf": "SC ou BR",
    "source": "fonte",
    "lang": "linguagem",
    "value": 10000,
    "deadline": "data ou não informado",
    "url": "link oficial",
    "summary": "resumo curto"
  }
]

Se não encontrar valor ou prazo, use 0 e "não informado".
`;

    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        tools: [{ type: "web_search" }],
        input: prompt,
        text: {
          verbosity: "low"
        }
      })
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(200).json(filtrarBaseDemo(uf, linguagem, q));
    }

    const text = data.output_text || "";
    const parsed = extrairJson(text);

    if (Array.isArray(parsed)) {
      return res.status(200).json(parsed.map((item, index) => ({
        id: item.id || `web-${index + 1}`,
        title: item.title || "Oportunidade cultural",
        uf: item.uf || uf,
        source: item.source || "Fonte pública",
        lang: item.lang || linguagem,
        value: Number(item.value || 0),
        deadline: item.deadline || "não informado",
        url: item.url || "",
        summary: item.summary || ""
      })));
    }

    return res.status(200).json(filtrarBaseDemo(uf, linguagem, q));
  } catch (error) {
    return res.status(200).json(filtrarBaseDemo(uf, linguagem, q));
  }
}

function extrairJson(text) {
  try {
    return JSON.parse(text);
  } catch {}

  try {
    const start = text.indexOf("[");
    const end = text.lastIndexOf("]");
    if (start >= 0 && end > start) {
      return JSON.parse(text.slice(start, end + 1));
    }
  } catch {}

  return null;
}

function filtrarBaseDemo(uf, linguagem, q) {
  const base = [
    {
      id: "demo-sc-1",
      title: "Edital de Fomento às Artes Cênicas — Santa Catarina",
      uf: "SC",
      source: "Base demonstração",
      lang: "Teatro",
      value: 25000,
      deadline: "30/08/2026",
      url: "https://",
      summary: "Oportunidade simulada para testar filtros e criação de projeto."
    },
    {
      id: "demo-br-1",
      title: "Prêmio Cultura Viva — Brasil",
      uf: "BR",
      source: "Base demonstração",
      lang: "Multilinguagem",
      value: 50000,
      deadline: "15/09/2026",
      url: "https://",
      summary: "Oportunidade nacional simulada para testar o radar."
    },
    {
      id: "demo-ms-1",
      title: "Fomento Cultural — Mato Grosso do Sul",
      uf: "MS",
      source: "Base demonstração",
      lang: "Teatro",
      value: 30000,
      deadline: "10/09/2026",
      url: "https://",
      summary: "Oportunidade simulada para Mato Grosso do Sul."
    }
  ];

  return base.filter(item => {
    const ufOk = uf === "TODOS" || item.uf === uf || item.uf === "BR";
    const langOk = linguagem === "Todas" || item.lang === linguagem || item.lang === "Multilinguagem";
    const qOk = !q || item.title.toLowerCase().includes(q.toLowerCase()) || item.summary.toLowerCase().includes(q.toLowerCase());
    return ufOk && langOk && qOk;
  });
}
