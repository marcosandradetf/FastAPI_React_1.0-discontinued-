document.addEventListener('DOMContentLoaded', () => {
    const ativar_busca_nome = document.getElementById('ativar_busca_nome');
    const ativar_busca_id = document.getElementById('ativar_busca_id');
    const menu_opcoes = document.getElementById('opcao');
    const btn_decisao = document.getElementById('decisao');
    const show_query = document.getElementById('show_query');
    const not_query = document.getElementById('not_query');
    const nome = document.getElementById('nome');
    const nome_label = document.getElementById('nome_label');
    const codigo = document.getElementById('codigo');
    const codigo_label = document.getElementById('codigo_label');

    ativar_busca_nome.addEventListener('click', () => {
        const busca_nome = document.getElementById('busca_nome');
        menu_opcoes.style.display = 'none';
        busca_nome.style.display = 'block';
        btn_decisao.style.display = 'block';
    });

    ativar_busca_id.addEventListener('click', () => {
        const busca_id = document.getElementById('busca_id');
        menu_opcoes.style.display = 'none';
        busca_id.style.display = 'block';
        btn_decisao.style.display = 'block';
    });

});