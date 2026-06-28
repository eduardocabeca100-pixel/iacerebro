from pathlib import Path

arquivo = Path("index.html")

if not arquivo.exists():
    raise SystemExit("ERRO: não encontrei index.html. Abra o terminal dentro da pasta certa do projeto.")

html = arquivo.read_text(encoding="utf-8")

inicio = "/* PATCH CÉREBRO IA — Equipe + Portfólio avançado */"
fim = "/* FIM PATCH CÉREBRO IA — Equipe + Portfólio avançado */"

patch = r"""
/* PATCH CÉREBRO IA — Equipe + Portfólio avançado */
function teamDefaults(t){
  return {
    id:t.id,
    name:t.name||'Integrante sem nome',
    artisticName:t.artisticName||t.name||'Nome artístico não informado',
    role:t.role||'Função não definida',
    area:t.area||'Artes cênicas',
    cpf:t.cpf||'CPF não informado',
    cnpj:t.cnpj||'',
    birth:t.birth||'',
    age:t.age||calcAge(t.birth)||'',
    city:t.city||'Cidade/UF não informada',
    address:t.address||'Endereço não informado',
    phone:t.phone||'Telefone não informado',
    email:t.email||'E-mail não informado',
    fee:Number(t.fee||0),
    pix:t.pix||'',
    resumeShort:t.resumeShort||'Mini currículo ainda não informado.',
    resume:t.resume||'Currículo completo ainda não informado.',
    portfolioText:t.portfolioText||'Portfólio ainda não informado. Inclua principais espetáculos, projetos, oficinas, apresentações, prêmios, formações e experiências relevantes.',
    linksText:t.linksText||'',
    docsText:t.docsText||'CPF/RG — pendente\nComprovante de residência — pendente\nCurrículo — pendente\nPortfólio — pendente\nCarta de anuência — pendente\nCNPJ/MEI — se houver',
    projectHistory:t.projectHistory||'Histórico de participação ainda não informado.',
    editalFunction:t.editalFunction||t.role||'Função no projeto ainda não detalhada.',
    observations:t.observations||''
  }
}

function calcAge(dateStr){
  if(!dateStr)return '';
  const d=new Date(dateStr);
  if(isNaN(d))return '';
  const now=new Date();
  let age=now.getFullYear()-d.getFullYear();
  const m=now.getMonth()-d.getMonth();
  if(m<0||(m===0&&now.getDate()<d.getDate()))age--;
  return age>0?age:'';
}

function textLines(text){
  return String(text||'').split('\n').map(x=>x.trim()).filter(Boolean)
}

function nl(text){
  return esc(String(text||'')).replace(/\n/g,'<br>')
}

function teamById(id){
  return teamDefaults(state.team.find(x=>x.id===id)||{})
}

function saveTeamObject(obj){
  const i=state.team.findIndex(x=>x.id===obj.id);
  if(i>=0)state.team[i]=obj;
  else state.team.push(obj);
  save();
}

function renderTeam(){
  title('Equipe','Banco completo de integrantes, currículos, portfólios, links e documentos');

  const selected=project().team||[];
  const total=state.team.length;
  const complete=state.team.filter(x=>{
    const t=teamDefaults(x);
    return t.resume && t.portfolioText && t.cpf;
  }).length;

  document.getElementById('app').innerHTML=`
    <div class="grid cols4">
      <div class="metric"><span>Integrantes</span><b>${total}</b></div>
      <div class="metric"><span>No projeto atual</span><b>${selected.length}</b></div>
      <div class="metric"><span>Cadastros completos</span><b>${complete}</b></div>
      <div class="metric"><span>Banco reutilizável</span><b>ON</b></div>
    </div>

    <div class="spacer"></div>

    <div class="card">
      <div class="between">
        <div>
          <h2>Equipe e portfólios</h2>
          <p class="muted">Cada pessoa tem abas de dados, currículo, portfólio, links, documentos, histórico e função no edital.</p>
        </div>
        <button class="btn primary" onclick="teamForm()">+ Adicionar integrante</button>
      </div>

      <div class="spacer"></div>

      <div class="grid cols3">
        ${state.team.map(raw=>{
          const t=teamDefaults(raw);
          const isSel=selected.includes(t.id);
          return `
          <div class="item" style="display:block">
            <div class="between">
              <div>
                <b>${esc(t.name)}</b><br>
                <span class="muted small">${esc(t.artisticName)} • ${esc(t.city)}</span>
              </div>
              <span class="pill ${isSel?'green':'gray'}">${isSel?'selecionado':'banco'}</span>
            </div>

            <div class="row" style="margin:8px 0">
              <span class="pill blue">${esc(t.area)}</span>
              <span class="pill pink">${esc(t.role)}</span>
              <span class="pill amber">${money(t.fee)}</span>
            </div>

            <div class="small muted">
              ${esc(t.resumeShort).slice(0,150)}${t.resumeShort.length>150?'...':''}
            </div>

            <div class="row" style="margin-top:10px">
              <button class="btn sm light" onclick="teamProfile('${t.id}','dados')">Abrir cadastro</button>
              <button class="btn sm light" onclick="teamProfile('${t.id}','portfolio')">Portfólio</button>
              <button class="btn sm primary" onclick="selectTeam('${t.id}')">Selecionar</button>
            </div>
          </div>`
        }).join('')}
      </div>
    </div>`;
}

function teamForm(){
  showModal(`
    <h2>Novo integrante da equipe</h2>
    <p class="muted">Cadastre tudo uma vez: depois o sistema puxa currículo, portfólio, documentos e função para qualquer edital.</p>

    <div class="grid cols2">
      <div class="field"><label>Nome completo</label><input id="tmName" placeholder="Nome civil completo"></div>
      <div class="field"><label>Nome artístico</label><input id="tmArtistic" placeholder="Nome usado no portfólio"></div>

      <div class="field">
        <label>Área de atuação</label>
        <select id="tmArea">
          <option>Artes cênicas</option>
          <option>Teatro</option>
          <option>Dança</option>
          <option>Música</option>
          <option>Audiovisual</option>
          <option>Produção cultural</option>
          <option>Técnica / Som / Luz</option>
          <option>Comunicação</option>
          <option>Prestação de contas</option>
        </select>
      </div>

      <div class="field"><label>Função principal</label><input id="tmRole" placeholder="Ator, direção, produção, técnica..."></div>
      <div class="field"><label>CPF</label><input id="tmCpf" placeholder="000.000.000-00"></div>
      <div class="field"><label>CNPJ / MEI</label><input id="tmCnpj" placeholder="Opcional"></div>
      <div class="field"><label>Data de nascimento</label><input id="tmBirth" type="date"></div>
      <div class="field"><label>Cidade/UF</label><input id="tmCity" placeholder="Jaraguá do Sul/SC"></div>
      <div class="field"><label>Telefone</label><input id="tmPhone" placeholder="(00) 00000-0000"></div>
      <div class="field"><label>E-mail</label><input id="tmEmail" placeholder="email@dominio.com"></div>
      <div class="field"><label>Cachê padrão</label><input id="tmFee" type="number" value="1000"></div>
      <div class="field"><label>PIX / dados de pagamento</label><input id="tmPix" placeholder="Opcional"></div>
    </div>

    <div class="field" style="margin-top:10px">
      <label>Endereço completo</label>
      <input id="tmAddress" placeholder="Rua, número, bairro, cidade, CEP">
    </div>

    <div class="grid cols2" style="margin-top:10px">
      <div class="field"><label>Mini currículo para formulário</label><textarea id="tmResumeShort" placeholder="Versão curta, pronta para colar em edital."></textarea></div>
      <div class="field"><label>Função no projeto / edital</label><textarea id="tmEditalFunction" placeholder="Explique o que essa pessoa fará no projeto."></textarea></div>
      <div class="field"><label>Currículo completo</label><textarea id="tmResume" placeholder="Formação, experiências, projetos, atuação cultural..."></textarea></div>
      <div class="field"><label>Portfólio</label><textarea id="tmPortfolio" placeholder="Espetáculos, apresentações, oficinas, projetos, premiações, links importantes..."></textarea></div>
      <div class="field"><label>Links, um por linha</label><textarea id="tmLinks" placeholder="Instagram: https://...\nYouTube: https://...\nDrive: https://..."></textarea></div>
      <div class="field"><label>Documentos, um por linha</label><textarea id="tmDocs">CPF/RG — pendente
Comprovante de residência — pendente
Currículo — pendente
Portfólio — pendente
Carta de anuência — pendente</textarea></div>
    </div>

    <div class="row" style="margin-top:12px">
      <button class="btn light" onclick="closeModal()">Cancelar</button>
      <button class="btn primary" onclick="addTeam()">Salvar integrante</button>
    </div>
  `)
}

function addTeam(){
  const obj={
    id:'t'+Date.now(),
    name:val('tmName')||'Novo integrante',
    artisticName:val('tmArtistic')||val('tmName')||'Nome artístico',
    area:val('tmArea')||'Artes cênicas',
    role:val('tmRole')||'Função',
    cpf:val('tmCpf')||'CPF não informado',
    cnpj:val('tmCnpj'),
    birth:val('tmBirth'),
    age:calcAge(val('tmBirth')),
    city:val('tmCity')||'Cidade/UF',
    address:val('tmAddress')||'Endereço não informado',
    phone:val('tmPhone')||'Telefone não informado',
    email:val('tmEmail')||'E-mail não informado',
    fee:Number(val('tmFee')||0),
    pix:val('tmPix'),
    resumeShort:val('tmResumeShort')||'Mini currículo ainda não informado.',
    resume:val('tmResume')||'Currículo completo ainda não informado.',
    portfolioText:val('tmPortfolio')||'Portfólio ainda não informado.',
    linksText:val('tmLinks'),
    docsText:val('tmDocs'),
    projectHistory:'Histórico de participação ainda não informado.',
    editalFunction:val('tmEditalFunction')||val('tmRole')||'Função no projeto ainda não detalhada.',
    observations:''
  };

  state.team.push(obj);
  save();
  closeModal();
  renderTeam();
  toast('Integrante cadastrado com portfólio e documentos.');
}

function teamProfile(id,tab='dados'){
  const t=teamById(id);

  const tabs=[
    ['dados','Dados'],
    ['curriculo','Currículo'],
    ['portfolio','Portfólio'],
    ['links','Links'],
    ['docs','Documentos'],
    ['historico','Projetos'],
    ['funcao','Função no edital']
  ];

  showModal(`
    <div class="between">
      <div>
        <h2>${esc(t.name)}</h2>
        <p class="muted">${esc(t.role)} • ${esc(t.area)} • ${esc(t.city)}</p>
      </div>
      <span class="pill green">Cadastro reutilizável</span>
    </div>

    <div class="subchips" style="margin:12px 0">
      ${tabs.map(x=>`<button class="${tab===x[0]?'active':''}" onclick="teamProfile('${t.id}','${x[0]}')">${x[1]}</button>`).join('')}
    </div>

    ${teamTabBody(t,tab)}

    <div class="row" style="margin-top:12px">
      <button class="btn light" onclick="closeModal()">Fechar</button>
      <button class="btn primary" onclick="selectTeam('${t.id}')">Selecionar no projeto atual</button>
      <button class="btn light" onclick="copyTeam('${t.id}','${tab}')">Copiar esta aba</button>
    </div>
  `)
}

function teamTabBody(t,tab){
  if(tab==='dados')return `
    <div class="grid cols2">
      <div class="notice">
        <b>Nome artístico:</b> ${esc(t.artisticName)}<br>
        <b>CPF:</b> ${esc(t.cpf)}<br>
        <b>CNPJ:</b> ${esc(t.cnpj||'Não informado')}<br>
        <b>Nascimento/idade:</b> ${esc(t.birth||'Não informado')} ${t.age?'• '+esc(t.age)+' anos':''}
      </div>
      <div class="notice">
        <b>Telefone:</b> ${esc(t.phone)}<br>
        <b>E-mail:</b> ${esc(t.email)}<br>
        <b>Endereço:</b> ${esc(t.address)}<br>
        <b>Cachê padrão:</b> ${money(t.fee)}
      </div>
    </div>`;

  if(tab==='curriculo')return `
    <div class="grid cols2">
      <div>
        <h3>Mini currículo</h3>
        <div class="notice">${nl(t.resumeShort)}</div>
      </div>
      <div>
        <h3>Currículo completo</h3>
        <div class="notice">${nl(t.resume)}</div>
      </div>
    </div>`;

  if(tab==='portfolio')return `
    <div class="notice">
      <h3>Portfólio artístico/profissional</h3>
      ${nl(t.portfolioText)}
    </div>`;

  if(tab==='links'){
    const links=textLines(t.linksText);
    return `<div class="list">
      ${links.length?links.map(l=>`
        <div class="item">
          <b>${esc(l)}</b>
          <button class="btn sm light" onclick="navigator.clipboard?.writeText('${esc(l).replace(/'/g,"\\'")}');toast('Link copiado.')">Copiar</button>
        </div>`).join(''):'<div class="empty">Nenhum link cadastrado ainda.</div>'}
    </div>`
  }

  if(tab==='docs'){
    const docs=textLines(t.docsText);
    return `<div class="list">
      ${docs.map(d=>`
        <div class="item ${d.toLowerCase().includes('pendente')?'warn':'good'}">
          <b>${esc(d)}</b>
          <span class="pill ${d.toLowerCase().includes('pendente')?'amber':'green'}">${d.toLowerCase().includes('pendente')?'pendente':'ok'}</span>
        </div>`).join('')}
    </div>`
  }

  if(tab==='historico')return `
    <div class="notice">
      <h3>Histórico de projetos</h3>
      ${nl(t.projectHistory)}
    </div>`;

  return `
    <div class="notice">
      <h3>Função dentro do projeto/editais</h3>
      ${nl(t.editalFunction)}
      <br><br>
      <b>Uso prático:</b> este texto pode entrar na ficha técnica, equipe, metodologia ou justificativa de capacidade técnica.
    </div>`;
}

function copyTeam(id,tab){
  const t=teamById(id);

  const map={
    dados:`${t.name}\n${t.artisticName}\nCPF: ${t.cpf}\nCNPJ: ${t.cnpj||'Não informado'}\nCidade: ${t.city}\nE-mail: ${t.email}\nTelefone: ${t.phone}`,
    curriculo:`Mini currículo:\n${t.resumeShort}\n\nCurrículo completo:\n${t.resume}`,
    portfolio:t.portfolioText,
    links:t.linksText,
    docs:t.docsText,
    historico:t.projectHistory,
    funcao:t.editalFunction
  };

  navigator.clipboard?.writeText(map[tab]||t.resume);
  toast('Conteúdo copiado.');
}

function viewResume(id){
  teamProfile(id,'curriculo')
}

function selectTeam(id){
  const p=project();

  if(!p.team)p.team=[];

  if(!p.team.includes(id)){
    p.team.push(id);
    save();
    toast('Integrante selecionado para o projeto atual.');
  }else{
    toast('Este integrante já está no projeto atual.');
  }
}

function tabPortfolio(){
  const p=project();
  const selected=(p.team&&p.team.length?p.team:state.team.map(t=>t.id)).map(teamById);

  return `
  <div class="grid cols2">
    <div class="card">
      <div class="between">
        <div>
          <h2>Portfólio do projeto</h2>
          <p class="muted">Equipe selecionada, currículos, links e materiais para anexar ao edital.</p>
        </div>
        <button class="btn primary sm" onclick="setPage('team')">Gerenciar equipe</button>
      </div>

      <div class="spacer"></div>

      <div class="notice">
        <b>Resumo para edital:</b><br>
        O projeto conta com equipe multidisciplinar vinculada às artes cênicas, produção cultural, execução técnica e gestão administrativa, reunindo trajetórias compatíveis com a realização da proposta e com capacidade de execução das ações previstas.
      </div>

      <div class="row" style="margin-top:10px">
        <button class="btn light sm" onclick="copyProjectTeamPortfolio()">Copiar resumo da equipe</button>
        <button class="btn light sm" onclick="downloadTeamPortfolio()">Exportar portfólio</button>
      </div>
    </div>

    <div class="card">
      <h2>Integrantes vinculados</h2>
      <div class="list">
        ${selected.map(t=>`
          <div class="item">
            <div>
              <b>${esc(t.name)}</b><br>
              <span class="muted small">${esc(t.role)} • ${esc(t.area)}</span>
            </div>
            <div class="row">
              <button class="btn sm light" onclick="teamProfile('${t.id}','portfolio')">Portfólio</button>
              <button class="btn sm light" onclick="teamProfile('${t.id}','curriculo')">Currículo</button>
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  </div>`
}

function copyProjectTeamPortfolio(){
  const p=project();
  const selected=(p.team&&p.team.length?p.team:state.team.map(t=>t.id)).map(teamById);

  const text=selected.map(t=>`${t.name} — ${t.role}
Mini currículo: ${t.resumeShort}
Função no projeto: ${t.editalFunction}
Portfólio: ${t.portfolioText}`).join('\n\n');

  navigator.clipboard?.writeText(text);
  toast('Resumo da equipe copiado.');
}

function downloadTeamPortfolio(){
  const p=project();
  const selected=(p.team&&p.team.length?p.team:state.team.map(t=>t.id)).map(teamById);

  const html='<html><meta charset="utf-8"><body><h1>Portfólio da equipe — '+esc(p.title)+'</h1>'+
    selected.map(t=>'<h2>'+esc(t.name)+'</h2><p><b>Função:</b> '+esc(t.role)+'</p><p><b>Mini currículo:</b><br>'+nl(t.resumeShort)+'</p><p><b>Portfólio:</b><br>'+nl(t.portfolioText)+'</p><p><b>Links:</b><br>'+nl(t.linksText)+'</p>').join('')+
    '</body></html>';

  downloadBlob(new Blob([html],{type:'application/msword'}),'portfolio-equipe-cerebro-ia.doc');
  toast('Portfólio da equipe exportado.');
}
/* FIM PATCH CÉREBRO IA — Equipe + Portfólio avançado */
"""

if inicio in html and fim in html:
    antes = html.split(inicio)[0]
    depois = html.split(fim)[1]
    html = antes + patch + depois
else:
    if "render();" not in html:
        raise SystemExit("ERRO: não encontrei render(); no index.html. Me manda print do final do arquivo.")
    partes = html.rsplit("render();", 1)
    html = partes[0] + patch + "\nrender();" + partes[1]

backup = Path("index.backup-equipe-portfolio.html")
backup.write_text(arquivo.read_text(encoding="utf-8"), encoding="utf-8")
arquivo.write_text(html, encoding="utf-8")

print("✅ Patch aplicado com sucesso.")
print("✅ Backup criado: index.backup-equipe-portfolio.html")
print("✅ Agora atualize o navegador.")
