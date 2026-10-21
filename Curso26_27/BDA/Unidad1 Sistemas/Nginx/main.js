/**
 * NGINX Masterclass — Interactive Utilities
 * IES San Vicente — Big Data & IA
 */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Copy Buttons on all code blocks
  const copyButtons = document.querySelectorAll('.btn-copy');
  
  copyButtons.forEach(button => {
    button.addEventListener('click', async () => {
      const codeBlock = button.closest('.code-block');
      if (!codeBlock) return;
      
      const codeElement = codeBlock.querySelector('pre code') || codeBlock.querySelector('pre');
      if (!codeElement) return;
      
      const textToCopy = codeElement.innerText;
      
      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalHTML = button.innerHTML;
        button.innerHTML = `
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          ¡Copiado!
        `;
        button.style.background = 'var(--primary)';
        button.style.color = '#042111';
        
        setTimeout(() => {
          button.innerHTML = originalHTML;
          button.style.background = '';
          button.style.color = '';
        }, 2200);
      } catch (err) {
        console.error('Error al copiar al portapapeles:', err);
      }
    });
  });

  // Sticky navbar shadow on scroll
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
});
