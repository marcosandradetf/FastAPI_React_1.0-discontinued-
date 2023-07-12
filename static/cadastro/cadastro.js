document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form');
  const successMessage = document.getElementById('success-message');
  const homeButton = document.getElementById('home-button');
  const newButton = document.getElementById('new-button');
  const errorElement = document.getElementById('error-message');
  
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const formData = new FormData(form);

    fetch('/cadastro', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
        try {
            if (data.error) {
              const fieldName = Object.keys(data.error)[0];
              const errorMessage = data.error[fieldName];
              const errorElement = document.getElementById(fieldName);

              errorElement.textContent = errorMessage;
              errorElement.classList.add("red");
            } else {
              form.style.display = 'none'; // Oculta o formulário
            }
          } catch (error) {
            form.style.display = 'none'; // Oculta o formulário
            successMessage.style.display = 'block'; // Exibe a mensagem de sucesso
          }
        })
        .catch(error => {
          //console.error('Erro:', error);
        });

  });

  // Ouvinte de evento para o botão "Voltar ao início"
  homeButton.addEventListener('click', () => {
    window.location.href = '/'; // Redireciona para a página inicial
  });

  // Ouvinte de evento para o botão "Fazer outro cadastro"
  newButton.addEventListener('click', () => {
    location.reload(true);
  });
});
