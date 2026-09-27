// charts.js - Lida especificamente com a biblioteca Chart.js no Dashboard

document.addEventListener('DOMContentLoaded', () => {
    
    // Verifica se estamos na página que tem o canvas do gráfico
    const pieCanvas = document.getElementById('expensesPieChart');
    if (!pieCanvas) return; // Se não estiver na página, sai do script

    // 1. Faz requisição (Fetch API) para a rota /api/chart-data
    const period = typeof currentPeriod !== 'undefined' ? currentPeriod : 'month';
    fetch(`/api/chart-data?period=${period}`)
        .then(response => response.json()) // Converte a resposta pra JSON
        .then(data => {
            
            // Se não houver dados, exibe uma mensagem
            if (data.pie_chart.data.length === 0) {
                const container = pieCanvas.parentElement;
                pieCanvas.style.display = 'none';
                
                const msg = document.createElement('p');
                msg.className = 'empty-state';
                msg.textContent = 'Sem despesas neste mês para gerar o gráfico.';
                container.appendChild(msg);
                return;
            }

            // 2. Cria o gráfico usando o Chart.js
            const ctx = pieCanvas.getContext('2d');
            
            new Chart(ctx, {
                type: 'doughnut', // Tipo "rosquinha" (pizza com furo no meio)
                data: {
                    labels: data.pie_chart.labels, // Nomes das categorias
                    datasets: [{
                        data: data.pie_chart.data,     // Valores das despesas
                        backgroundColor: data.pie_chart.colors, // Cores das categorias
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom', // Coloca a legenda embaixo
                        },
                        tooltip: {
                            callbacks: {
                                // Formata o valor na tooltip (aquele balãozinho ao passar o mouse)
                                label: function(context) {
                                    let label = context.label || '';
                                    if (label) {
                                        label += ': ';
                                    }
                                    if (context.parsed !== null) {
                                        label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed);
                                    }
                                    return label;
                                }
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Erro ao carregar os dados do gráfico:', error);
        });
});
