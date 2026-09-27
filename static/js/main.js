// main.js - JavaScript geral da aplicação

document.addEventListener('DOMContentLoaded', () => {
    console.log('FinanceFlow inicializado.');
    
    // Marcar link ativo na navegação
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        // Se o href do link for igual ao caminho atual
        if (link.getAttribute('href') === currentPath) {
            link.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
            link.style.borderLeft = '4px solid var(--primary-color)';
        }
    });
});
