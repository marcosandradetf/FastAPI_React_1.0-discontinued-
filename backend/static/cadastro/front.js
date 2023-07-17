document.addEventListener('DOMContentLoaded', () => {
  const inputs = document.querySelectorAll('input');

  inputs.forEach(input => {
    input.addEventListener('input', () => {
      const fieldName = input.getAttribute('name');
      const errorElement = document.getElementById(`${fieldName}_label`);

      errorElement.textContent = '';
    });
  });
});
