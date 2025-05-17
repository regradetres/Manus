// Funções JavaScript para o Sistema de Produção SUS

document.addEventListener('DOMContentLoaded', function() {
  // Inicializa tooltips do Bootstrap
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });

  // Inicializa popovers do Bootstrap
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
  });

  // Função para validação de CNS
  window.validarCNS = function(cns) {
    // Remove caracteres não numéricos
    cns = cns.replace(/\D/g, '');
    
    // Verifica se tem 15 dígitos
    if (cns.length !== 15) {
      return false;
    }
    
    // Algoritmo de validação do CNS
    var soma = 0;
    var resto, dv;
    var pis = cns.substring(0, 11);
    
    for (var i = 0; i < 11; i++) {
      soma += parseInt(pis.charAt(i)) * (15 - i);
    }
    
    resto = soma % 11;
    dv = 11 - resto;
    
    if (dv === 11) {
      dv = 0;
    }
    
    if (dv === 10) {
      soma = 0;
      for (var i = 0; i < 11; i++) {
        soma += parseInt(pis.charAt(i)) * (15 - i);
      }
      soma += 2;
      resto = soma % 11;
      dv = 11 - resto;
      return cns === pis + '001' + dv;
    } else {
      return cns === pis + '000' + dv;
    }
  };

  // Função para validação de CNES
  window.validarCNES = function(cnes) {
    // Remove caracteres não numéricos
    cnes = cnes.replace(/\D/g, '');
    
    // Verifica se tem 7 dígitos
    return cnes.length === 7;
  };

  // Função para busca de procedimentos SIGTAP
  window.buscarProcedimento = function(termo) {
    if (termo.length < 3) {
      return;
    }
    
    fetch('/sigtap/api/procedimentos?busca=' + encodeURIComponent(termo))
      .then(response => response.json())
      .then(data => {
        const resultadosDiv = document.getElementById('resultados-procedimentos');
        resultadosDiv.innerHTML = '';
        
        if (data.procedimentos.length === 0) {
          resultadosDiv.innerHTML = '<p class="text-muted">Nenhum procedimento encontrado.</p>';
          return;
        }
        
        const lista = document.createElement('ul');
        lista.className = 'list-group';
        
        data.procedimentos.forEach(proc => {
          const item = document.createElement('li');
          item.className = 'list-group-item';
          item.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <strong>${proc.codigo}</strong> - ${proc.nome}
              </div>
              <button class="btn btn-sm btn-primary" onclick="selecionarProcedimento('${proc.id}', '${proc.codigo}', '${proc.nome.replace(/'/g, "\\'")}')">
                Selecionar
              </button>
            </div>
          `;
          lista.appendChild(item);
        });
        
        resultadosDiv.appendChild(lista);
      })
      .catch(error => {
        console.error('Erro ao buscar procedimentos:', error);
      });
  };

  // Função para selecionar procedimento
  window.selecionarProcedimento = function(id, codigo, nome) {
    document.getElementById('procedimento_id').value = id;
    document.getElementById('procedimento_codigo').value = codigo;
    document.getElementById('procedimento_nome').value = nome;
    
    // Fecha o modal de busca
    const modal = bootstrap.Modal.getInstance(document.getElementById('modal-busca-procedimento'));
    if (modal) {
      modal.hide();
    }
  };

  // Função para calcular valor baseado no procedimento e quantidade
  window.calcularValor = function() {
    const procedimentoId = document.getElementById('procedimento_id').value;
    const quantidade = document.getElementById('quantidade').value;
    
    if (!procedimentoId || !quantidade) {
      return;
    }
    
    fetch(`/sigtap/api/procedimentos/${procedimentoId}/valor?quantidade=${quantidade}`)
      .then(response => response.json())
      .then(data => {
        document.getElementById('valor_calculado').value = data.valor.toFixed(2);
      })
      .catch(error => {
        console.error('Erro ao calcular valor:', error);
      });
  };

  // Função para confirmar exclusão
  window.confirmarExclusao = function(id, tipo) {
    if (confirm(`Tem certeza que deseja excluir este registro de ${tipo}?`)) {
      window.location.href = `/producao/excluir/${id}`;
    }
  };

  // Função para mostrar/esconder campos condicionais
  const tipoBPA = document.getElementById('tipo_bpa');
  if (tipoBPA) {
    tipoBPA.addEventListener('change', function() {
      const camposCID = document.getElementById('campos-cid');
      if (this.value === 'I') {
        camposCID.classList.remove('d-none');
      } else {
        camposCID.classList.add('d-none');
      }
    });
  }
});
