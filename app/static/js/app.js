document.addEventListener('DOMContentLoaded', function () {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alertEl) {
    setTimeout(() => {
      if (alertEl && alertEl.parentNode) {
        alertEl.remove();
      }
    }, 4000);
  });

  const cards = document.querySelectorAll('.card');
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 80}ms`;
    card.style.animation = 'fadeInUp 0.5s ease forwards';
  });
});

const style = document.createElement('style');
style.textContent = `
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;
document.head.appendChild(style);
