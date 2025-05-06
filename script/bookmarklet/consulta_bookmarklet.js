// NOTE: este arquivo é um módulo async, use com execute_async_script.

(async function(){
    // 1) Aguarda fim de requisições AJAX genérico
    async function waitForAjax(timeout = 15000) {
      const start = Date.now();
      while (document.querySelector('.rich-table-loading')) {
        if (Date.now() - start > timeout) break;
        await new Promise(r => setTimeout(r, 200));
      }
    }
  
    // 2) Simula clique
    function simulateClick(el) {
      el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
    }
  
    // 3) Formata "Chave: Valor"
    function formatRow(row) {
      const cells = row.querySelectorAll('td,th');
      if (cells.length >= 2) {
        return cells[0].textContent.trim().replace(/\s+/g,' ')
             + ': '
             + cells[1].textContent.trim().replace(/\s+/g,' ');
      }
      return row.textContent.trim().replace(/\s+/g,' ');
    }
  
    // 4) Extrai detalhes de #maisDetalhes
    function extractDetails() {
      const container = document.querySelector('#maisDetalhes');
      if (!container) return {};
      const obj = {};
      container.querySelectorAll('dl').forEach(dl =>
        dl.querySelectorAll('dt').forEach(dt => {
          const key = dt.textContent.trim().replace(/\s+/g,' ');
          const dd  = dt.nextElementSibling;
          const val = dd ? dd.textContent.trim().replace(/\s+/g,' ') : '';
          obj[key] = obj[key] ? obj[key] + ' | ' + val : val;
        })
      );
      return obj;
    }
  
    // 5) Extrai movimentos com data
    async function extractMovimentos() {
      const container = document.getElementById('divTimeLine:eventosTimeLineElement')
                     || document.querySelector('[id$="eventosTimeLineElement"]');
      if (!container) return '';
      // espera até ter pelo menos um movimento ou timeout de 5s
      const start = Date.now();
      while (
        container.querySelectorAll('.media.interno .texto-movimento').length === 0 &&
        Date.now() - start < 5000
      ) {
        await new Promise(r => setTimeout(r, 200));
      }
      const result = [];
      let currentDate = '';
      // percorre filhos em ordem
      Array.from(container.children).forEach(el => {
        if (el.classList.contains('media') && el.classList.contains('data')) {
          // atualiza a data corrente
          const dateSpan = el.querySelector('span.data-interna, span.text-muted');
          if (dateSpan) {
            currentDate = dateSpan.textContent.trim().replace(/\s+/g,' ');
          }
        }
        else if (el.classList.contains('media') && el.classList.contains('interno')) {
          // pega todos os movimentos desse bloco
          el.querySelectorAll('.texto-movimento').forEach(span => {
            const mov = span.textContent.trim().replace(/\s+/g,' ');
            result.push(`${currentDate}: ${mov}`);
          });
        }
      });
      return result.join(' | ');
    }
  
    // 6) Extrai primeira célula de uma tabela simples
    function extractFirstCell(sel) {
      const c = document.querySelector(sel + ' td');
      return c ? c.textContent.trim().replace(/\s+/g,' ') : '';
    }
  
    // 7) Extrai características adicionais
    function extractCharacteristics() {
      return Array.from(document.querySelectorAll('td span > div.propertyView')).map(div => {
        const n = div.querySelector('.name label');
        const v = div.querySelector('.value');
        return n && v
          ? n.textContent.trim().replace(/\s+/g,' ')
            + ': '
            + v.textContent.trim().replace(/\s+/g,' ')
          : '';
      });
    }
  
    // 8) Extrai audiências
    async function extractAudiencia() {
      const nav = document.querySelector('#navbar\\:linkAbaAudiencia');
      if (!nav) return [];
      simulateClick(nav);
      await waitForAjax();
      await new Promise(r => setTimeout(r, 300));
      return Array.from(document.querySelectorAll(
        '#processoConsultaAudienciaGridList\\:tb > tr.rich-table-row'
      )).map(row => {
        const cells = Array.from(row.querySelectorAll('td'));
        return {
          'Data prevista':       cells[0]?.innerText.trim().replace(/\s+/g,' ') || '',
          'Tipo de Audiência':   cells[1]?.innerText.trim().replace(/\s+/g,' ') || '',
          'Unidade':             cells[2]?.innerText.trim().replace(/\s+/g,' ') || '',
          'Sala':                cells[3]?.innerText.trim().replace(/\s+/g,' ') || '',
          'Status da Audiência': cells[4]?.innerText.trim().replace(/\s+/g,' ') || ''
        };
      });
    }
  
    // 9) Extrai linhas de abas genéricas (Perícias/Redistribuições)
    async function clickAndExtract(navSel, rowSel) {
      const nav = document.querySelector(navSel);
      if (!nav) return [];
      simulateClick(nav);
      await waitForAjax();
      await new Promise(r => setTimeout(r, 300));
      return Array.from(document.querySelectorAll(rowSel)).map(formatRow);
    }
  
    // Início da execução
    await waitForAjax();
  
    // 1) extrai detalhes
    const details = extractDetails();
  
    // 2) extrai movimentos com data
    const movimentos = await extractMovimentos();
    details['Movimentos'] = movimentos;
  
    // 3) extrai demais campos
    const poloAtivo       = extractFirstCell('#poloAtivo > table tr');
    const poloPassivo     = extractFirstCell('#poloPassivo > table tr');
    const characteristics = extractCharacteristics().join(' | ');
    const audienciaData   = await extractAudiencia();
    const periciasArr     = await clickAndExtract(
      '#navbar\\:linkAbaPericia',
      '#processoPericiaNovaPericiaList\\:tb > tr'
    );
    const redistribsArr   = await clickAndExtract(
      '#navbar\\:linkAbaRedistribuicoes',
      '#historicoRedistribuicaoList\\:tb > tr'
    );
  
    // Montagem do TSV
    const headers = [
      ...Object.keys(details),
      'Polo ativo',
      'Polo passivo',
      'Características',
      'Data prevista',
      'Tipo de Audiência',
      'Unidade',
      'Sala',
      'Status da Audiência',
      'Perícias',
      'Redistribuições'
    ];
  
    const values = [
      ...Object.values(details),
      poloAtivo,
      poloPassivo,
      characteristics,
      ...(audienciaData[0]
          ? Object.values(audienciaData[0])
          : ['','','','','']),
      periciasArr.length   ? periciasArr.join(' | ')   : 'N/A',
      redistribsArr.length ? redistribsArr.join(' | ') : 'N/A'
    ];
  
    return headers.join('\t') + '\n' + values.join('\t');
  })();
  