# CÉREBRO IA

Sistema operacional para criação, análise, revisão e exportação de projetos culturais com apoio de inteligência artificial.

## Funções principais

- Criação guiada de projetos culturais
- Upload de edital e anexos
- Análise de edital por IA
- Texto em blocos para copiar e colar no formulário do edital
- Banco de equipe com dados, documentos, currículos e portfólio
- Planilha orçamentária editável
- Revisão automática para aumentar nota
- Exportação em Word/PDF
- Busca de oportunidades/editais
- Administração de usuários

## Rodar localmente

npm install
npx vercel dev --listen 5174

Acesse:

http://localhost:5174

## Variáveis de ambiente

Crie um arquivo .env.local com:

OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-5.5
APP_URL=http://localhost:5174
