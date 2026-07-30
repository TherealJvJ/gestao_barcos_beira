/* ================================================================
   Sistema de Gestão de Barcos — INTRANSMAR Beira
   main.js — Interações e Utilitários
   ================================================================ */

/* === Sidebar Mobile === */
function abrirSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebar-overlay');
    if (sidebar) {
        sidebar.classList.add('open');
        if (overlay) overlay.classList.add('visible');
        document.body.style.overflow = 'hidden';
    }
}

function fecharSidebar() {
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebar-overlay');
    if (sidebar) {
        sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('visible');
        document.body.style.overflow = '';
    }
}

// Fechar sidebar com tecla Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        fecharSidebar();
        fecharDropdown();
    }
});

/* === Dropdown do Utilizador === */
function toggleDropdown() {
    var menu = document.getElementById('dropdown-menu');
    var btn = document.querySelector('.user-btn');
    if (!menu) return;
    var isOpen = menu.classList.contains('open');
    if (isOpen) {
        fecharDropdown();
    } else {
        menu.classList.add('open');
        if (btn) btn.setAttribute('aria-expanded', 'true');
    }
}

function fecharDropdown() {
    var menu = document.getElementById('dropdown-menu');
    var btn = document.querySelector('.user-btn');
    if (menu) menu.classList.remove('open');
    if (btn) btn.setAttribute('aria-expanded', 'false');
}

// Fechar dropdown ao clicar fora
document.addEventListener('click', function(e) {
    var dropdown = document.getElementById('user-dropdown');
    if (dropdown && !dropdown.contains(e.target)) {
        fecharDropdown();
    }
});

/* === Confirmação de Logout === */
function confirmarLogout(url) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: 'Terminar Sessão?',
            text: 'Irá sair do sistema. Deseja continuar?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#CC3E3E',
            cancelButtonColor: '#6B8C9A',
            confirmButtonText: '<i class="bi bi-box-arrow-right"></i> Sair',
            cancelButtonText: 'Cancelar',
            reverseButtons: true,
            customClass: { popup: 'swal-compact' }
        }).then(function(result) {
            if (result.isConfirmed) {
                window.location.href = url;
            }
        });
        return false;
    }
    return true;
}

/* === Confirmações SweetAlert2 === */
function confirmarAprovacao(url) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: 'Aprovar Embarcação?',
            text: 'A embarcação será aprovada e poderá receber documentos oficiais.',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#1F9E6E',
            cancelButtonColor: '#6B8C9A',
            confirmButtonText: 'Sim, Aprovar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then(function(result) {
            if (result.isConfirmed) { window.location.href = url; }
        });
    } else {
        if (confirm('Aprovar Embarcação?\nA embarcação será aprovada e poderá receber documentos oficiais.')) {
            window.location.href = url;
        }
    }
}

function confirmarRejeicao(url) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: 'Rejeitar Embarcação?',
            text: 'A embarcação será rejeitada. Esta acção pode ser revertida posteriormente.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#CC3E3E',
            cancelButtonColor: '#6B8C9A',
            confirmButtonText: 'Sim, Rejeitar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then(function(result) {
            if (result.isConfirmed) { window.location.href = url; }
        });
    } else {
        if (confirm('Rejeitar Embarcação?\nA embarcação será rejeitada. Esta acção pode ser revertida posteriormente.')) {
            window.location.href = url;
        }
    }
}

function confirmarDesactivacao(url, nome) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: 'Alterar Estado?',
            html: 'Deseja alterar o estado do utilizador <strong>' + nome + '</strong>?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#D97B40',
            cancelButtonColor: '#6B8C9A',
            confirmButtonText: 'Sim, Alterar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then(function(result) {
            if (result.isConfirmed) { window.location.href = url; }
        });
    } else {
        if (confirm('Alterar Estado?\nDeseja alterar o estado do utilizador ' + nome + '?')) {
            window.location.href = url;
        }
    }
}

function confirmarEliminar(url, item) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: 'Eliminar Registo?',
            html: 'Tem a certeza que pretende eliminar <strong>' + item + '</strong>? Esta acção é irreversível.',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#CC3E3E',
            cancelButtonColor: '#6B8C9A',
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then(function(result) {
            if (result.isConfirmed) { window.location.href = url; }
        });
    } else {
        if (confirm('Eliminar Registo?\nTem a certeza que pretende eliminar ' + item + '? Esta acção é irreversível.')) {
            window.location.href = url;
        }
    }
}

/* === Toast Notifications === */
function mostrarToast(mensagem, tipo) {
    if (typeof Swal === 'undefined') return;
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3500,
        timerProgressBar: true,
    });
    Toast.fire({ icon: tipo || 'success', title: mensagem });
}

/* === Auto-dismiss Django Messages === */
document.addEventListener('DOMContentLoaded', function() {
    var alerts = document.querySelectorAll('.alert-custom');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            setTimeout(function() {
                if (alert.parentNode) alert.parentNode.removeChild(alert);
            }, 350);
        }, 5500);
    });
});

/* === CSRF Token para AJAX === */
function getCSRFToken() {
    var cookie = document.cookie.split(';').find(function(c) {
        return c.trim().startsWith('csrftoken=');
    });
    return cookie ? cookie.split('=')[1] : '';
}

/* === Pesquisa em Tabela === */
function filtrarTabela(inputId, tabelaId) {
    var input = document.getElementById(inputId);
    var tabela = document.getElementById(tabelaId);
    if (!input || !tabela) return;

    input.addEventListener('input', function() {
        var filtro = this.value.toLowerCase().trim();
        var linhas = tabela.querySelectorAll('tbody tr');
        var count = 0;
        linhas.forEach(function(linha) {
            var texto = linha.textContent.toLowerCase();
            var visivel = texto.includes(filtro);
            linha.style.display = visivel ? '' : 'none';
            if (visivel) count++;
        });
        // Mostrar contagem
        var countEl = document.getElementById('resultado-contagem');
        if (countEl) {
            countEl.textContent = count + (count === 1 ? ' resultado' : ' resultados');
        }
    });
}

/* === Imprimir Relatório === */
function imprimirRelatorio() {
    window.print();
}

/* === Gráfico Doughnut === */
function criarGraficoDoughnut(canvasId, labels, dados, cores) {
    var ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: dados,
                backgroundColor: cores || ['#0A6B8A', '#1F9E6E', '#D97B40', '#CC3E3E', '#2A7EC8'],
                borderWidth: 3,
                borderColor: '#fff',
                hoverBorderWidth: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '62%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 16,
                        font: { size: 12, family: 'Inter' },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            }
        }
    });
}

/* === Gráfico de Barras === */
function criarGraficoBarras(canvasId, labels, dados, cor) {
    var ctx = document.getElementById(canvasId);
    if (!ctx) return null;
    var cores = Array.isArray(cor) ? cor : [cor || '#0A6B8A'];
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total',
                data: dados,
                backgroundColor: Array.isArray(cor) ? cor : '#0A6B8A',
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1, font: { size: 11 } },
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 12 } }
                }
            }
        }
    });
}

/* === Inicialização Geral === */
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar pesquisa de tabela
    filtrarTabela('busca-tabela', 'tabela-dados');

    // Resize handler: fechar sidebar se janela ficar grande
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992) {
            fecharSidebar();
        }
    });
});

// Forçar recarregamento se a página for carregada a partir do cache de histórico (botão Voltar/Avançar)
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});
