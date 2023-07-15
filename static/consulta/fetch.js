document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const consulta = new FormData(form);

        // Tentar remover as classes, se adicionadas
        try {
            nome_label.classList.remove('text-danger');
            nome.classList.remove('is-invalid');

            codigo.classList.remove('is-invalid');
            codigo_label.classList.remove('text-danger');
            
        } catch (error) {
            // Tratar possíveis erros
            console.log('Erro ao remover as classes:', error);
        }
        
        // METODO FETCH
        fetch('/consulta', {
            method: 'POST',
            body: consulta
        })

        .then(response => response.json())

        .then(data => {
            if (data.myquery && data.myquery.length > 0){
                not_query.style.display = 'none';
                const tabela = document.querySelector('#show_query table');

                while (tabela.rows.length > 1) {
                    tabela.deleteRow(1);
                }

                for (let i = 0; i < data.myquery.length; i++) {
                    const row = tabela.insertRow();

                    const idCell = row.insertCell();
                    idCell.textContent = data.myquery[i].id;

                    const nomeCell = row.insertCell();
                    nomeCell.textContent = data.myquery[i].nome;

                    const cpfCell = row.insertCell();
                    cpfCell.textContent = data.myquery[i].cpf;

                    const nascCell = row.insertCell();
                    nascCell.textContent = data.myquery[i].data_nascimento;
                }
                show_query.style.display = 'block';
            } else{
                not_query.style.display = 'block';
            }

            if (data.not_integer){
                not_query.style.display = 'none';
                codigo.classList.add('is-invalid');
                codigo_label.classList.add('text-danger');
            }

            if (data.invalid_name){
                not_query.style.display = 'none';
                nome_label.classList.add('text-danger');
                nome.classList.add('is-invalid');
            }



          })

        .catch(error => {
          //console.error('Erro:', error);
        });
        // FIM DO METODO FETCH


    });
});