class Sistema:
    def __init__(self):
        self.id = []
        self.nome = None
        self.cpf = None
        self.nasc = None

    # funcao para inicio de cadastro
    def cadastro(self, db_nomes, db_cpfs, db_nasc):
        # utilizacao do modulo importado para limpar o terminal quando se volta ao menu inicial
        os.system('clear') or None
        # atribuindo id a cadastro
        self.id.append(len(self.id) + 1)
        # atribuindo index a variavel
        index = len(self.id)

        print('CADASTRO\n')
        # verificacoes de nome, cpf e nascimento
        if self.ver_nome():
            db_nomes.insert(index - 1, self.nome)
            if self.ver_cpf(db_nomes, db_cpfs, db_nasc):
                db_cpfs.insert(index - 1, self.cpf)
                if self.ver_nasc():
                    db_nasc.insert(index - 1, self.nasc)

    # funcao para validar nome
    def verifica_nome_ok(self, nome):
        # se o tamanho do nome for maior que zero
        if len(nome) > 0:
            # iterando sobre o nome informado e verificando se contem letras e espaco
            if all(letras.isalpha() or letras.isspace() for letras in nome):
                # verificando se o nome contem 1 espaco e é maior ou igual a 5
                if nome.count(' ') == 1 and len(nome) >= 5:
                    # atribuindo a posicao do espaco a variavel espaco
                    espaco = nome.find(' ')
                    # atribuindo a posicao da do sobrenome a variavel sobrenome
                    sobrenome = nome[espaco + 1:]
                    # verificando se o sobrenome contem somente letras
                    if sobrenome.isalpha():
                        nome_ok = nome.title()
                        return True, nome_ok
                    else:
                        error_msg = 'O nome deve ser composto por primeiro nome e um único sobrenome (ex: José Silva).'
                        return False, error_msg
                else:
                    error_msg = 'O nome deve ser composto por primeiro nome e um único sobrenome (ex: José Silva).'
                    return False, error_msg
            else:
                error_msg = 'Você digitou números, digite apenas letras!'
                return False, error_msg
        else:
            error_msg = 'Você não digitou nada, digite um nome e um sobrenome.'
            return False, error_msg

    # funcao para verificar o id informado pelo usuario
    def ver_id_ok(self, id):
        # tentando converter o id para inteiro
        try:
            id = int(id)
            # verificar se o id é maior que 0
            if id > 0:
                # verificar se o id é maior ou menor que o banco de dados
                if id <= len(self.id):
                    return True
                else:
                    print('\nRegistro não encontrado!\nO ID Informado foi maior que o número total de cadastros.\n')
                    self.confirmar()
                    return False
            else:
                print(
                    "\nRegistro não encontrado!\nO ID informado foi um número negativo, informe um número inteiro maior que zero.\n")
            self.confirmar()
            return False
        # caso falhe retornar que o id não é um numero ao inves de interromper o funcionamento do codigo
        except ValueError:
            print('\nRegistro não encontrado!\nO ID Informado contém letras digite apenas números.\n')
            self.confirmar()
            return False

    # funcao para verificar cpf
    def ver_cpf_ok(self, cpf):

        # verificando se o cpf está vazio
        if len(cpf) == 0:
            msg = 'Você não digitou nada, digite um CPF.'
            return False, msg

        # verificando se foi digitado letras
        if not cpf.isnumeric():
            msg = "Voce digitou letras, digite apenas números!"
            return False, msg

        # verificando tamanho do cpf
        if not len(cpf) == 11:
            msg = "CPF deve ser composto por 11 dígitos (ex: 99999999999)"
            return False, msg

        cont = 10
        cpf_9d = cpf[0:9]

        sum = 0
        # iterando pelos 9 digitos do cpf
        for d in cpf_9d:
            sum = sum + int(d) * cont
            cont = cont - 1

        # atruibuindo primeiro digito verificador com base no calculo abaixo
        dv_1 = 11 - sum % 11

        # validando primeiro digito verificador
        if dv_1 >= 10:
            dv_1 = "0"
        else:
            dv_1 = str(dv_1)

        cont = 11
        cpf_10d = cpf_9d + dv_1

        sum = 0
        # iterando pelos 10 digitos do cpf ja com o dv
        for d in cpf_10d:
            sum = sum + int(d) * cont
            cont = cont - 1

        # atruibuindo segundo digito verificador com base no calculo abaixo
        dv_2 = 11 - sum % 11

        # validando segundo digito verificador
        if dv_2 >= 10:
            dv_2 = "0"
        else:
            dv_2 = str(dv_2)

        # validando cpf informado
        if cpf[9] == dv_1 and cpf[10] == dv_2:
            # validando a regiao sudeste
            if cpf[8] != '6' and cpf[8] != '7' and cpf[8] != '8':
                cpf_ok = cpf
                return True, cpf_ok
            else:
                msg = 'Infelizmente o sistema ainda não aceita CPFs emitidos na Região Sudeste (ES, MG, RJ e SP).'
                return False, msg

        else:
            msg = 'CPF Inválido'
            return False, msg

    # funcao para verificar data de nascimento
    def ver_nasc_ok(self, d_nas):
        # anos bissextos armazenados
        bissextos = ["1904", "1908", "1912", "1916", "1920", "1924", "1928", "1932", "1936", "1940", "1944", "1948",
                     "1952", "1956", "1960", "1964", "1968", "1972", "1976", "1980", "1984", "1988", "1992", "1996",
                     "2000", "2004"]

        # verificando se foi digitado algo
        if len(d_nas) > 0:
            # verificando se está no formado xx/xx/xxxx
            if len(d_nas) == 10 and d_nas[2] == '/' and d_nas[5] == '/' and d_nas.count(' ') == 0:
                # armazenando a data em variaveis separadas
                s_dia = d_nas[:2]
                s_mes = d_nas[3:5]
                s_ano = d_nas[6:]

                # verificando se cada cada data é digito
                if s_dia.isdigit() and s_mes.isdigit() and s_ano.isdigit():
                    # convertendo para inteiro
                    dia = int(s_dia)
                    mes = int(s_mes)
                    ano = int(s_ano)

                    # verificando se a data está no formado dd/mm/aaaa
                    if 1 <= dia <= 31 and 1 <= mes <= 12 and 1100 <= ano <= 9999:
                        # verificando se o ano está entre 1900 e 2023
                        if 1900 <= ano <= 2023:

                            # verificacao para fevereiro em ano bissexto
                            if str(ano) in bissextos and s_mes == '02':
                                if 1 <= dia <= 29:
                                    nasc_ok = d_nas
                                    return True, nasc_ok
                                else:
                                    msg = 'Dia informado para esse mês está inválido'

                            # verificacao para fevereiro em ano nao bissexto
                            if str(ano) not in bissextos and s_mes == '02':
                                if 1 <= dia <= 28:
                                    nasc_ok = d_nas
                                    return True, nasc_ok
                                else:
                                    msg = 'Dia informado para esse mês está inválido'
                                    return False, msg

                            # verificacao para mes de abril
                            if s_mes == '04':
                                if 1 <= dia <= 30:
                                    nasc_ok = d_nas
                                    return True, nasc_ok
                                else:
                                    msg = 'Dia informado para esse mês está inválido'
                                    return False, msg

                            # verificacao para o ano de 2023
                            if str(ano) == '2023':
                                if 1 <= mes <= 6:
                                    if 1 <= dia <= 22:
                                        nasc_ok = d_nas
                                        return True, nasc_ok
                                    else:
                                        msg = 'Não estamos aceitando cadastros de viajantes do tempo no momento.\nNão insira datas do futuro'
                                        return False, msg

                            # verificacao para demais datas
                            if s_mes != '04' and s_mes != '02' and s_ano != '2023':
                                nasc_ok = d_nas
                                return True, nasc_ok


                        else:
                            msg = 'Somente sao aceitas pessoas nascidas entre 1900 e 2023.'
                            return False, msg

                    else:
                        msg = 'Informe a data de nascimento válida: No formato dd/mm/aaaa (ex: 01/02/1999).'
                        return False, msg

            else:
                msg = 'Informe a data de nascimento: No formato dd/mm/aaaa (ex: 01/02/1999).'
                return False, msg

        else:
            msg = 'Você não digitou nada, informe uma data.'
            return False, msg


# funcao para exibir cadastro
def exibir_cadastro(self, db_nomes, db_cpfs, db_nasc):
    # limpando terminal
    os.system('clear') or None
    print('\nCADASTROS\n')
    # iterando sobre os cadastros e fazendo print
    for id, nome, cpf, nasc in zip(self.id, db_nomes, db_cpfs, db_nasc):
        print(f'ID: {id}')
        print(f'Nome: {nome}')
        print(f'CPF: {cpf}')
        print(f'Data de Nascimento: {nasc}\n')


# funcao generica para confirmar
def confirmar(self):
    input('<ENTER> PARA CONTINUAR')


# funcao para alterar cpf
def altera_cpf(self, nome, cpf, nasc):
    # loop da funcao
    while True:
        # limpando terminal
        os.system('clear') or None
        # exibindo cadastro
        self.exibir_cadastro(nome, cpf, nasc)
        id = input("Informe o ID do cadastro que deseja alterar o CPF: ")

        # verificando se o id é valido atraves da funcao abaixo
        if self.ver_id_ok(id):
            # limpando o terminal
            os.system('clear') or None
            # convertendo o id em index
            id = int(id) - 1
            # exibindo o cadastro conforme o id convertido
            print('Cadastro para alteração de CPF\n')
            print(f'ID: {self.id[id]}')
            print(f'Nome: {nome[id]}')
            print(f'CPF: {cpf[id]}')
            print(f'Data de Nascimento: {nasc[id]}\n')
            # solicitando confirmação
            confirmar = input('<ENTER> para confirmar ou digite outra tecla para cancelar: \n')
            # caso confirmado
            if confirmar == '':
                print('Informe o novo cpf')
                # chamando a funcao para validar cpf e se validar, altera-se
                if self.ver_cpf(nome, cpf, nasc):
                    cpf[id] = self.cpf
                    input('\nCPF alterado <ENTER> para continuar')
                break
            else:
                input('Alteração cancelada pelo usuário <ENTER> para continuar')
                break


# funcao para alterar sobrenomes
def altera_sobrenomes(self, nome, cpf, nasc):
    # loop da funcao
    while True:
        # exibicao de cadastro
        self.exibir_cadastro(nome, cpf, nasc)
        print("Informe os ID's dos cadastros que terão os sobrenomes trocados")
        # solicitando os ids para troca de cadastro
        id_1 = input("Informe o primeiro ID: ")
        id_2 = input("Informe o segundo ID: ")
        # armazenando os ids informados
        ids = [id_1, id_2]

        # validando os ids informado atraves da funcao abaixo
        if self.ver_id_ok(id_1) and self.ver_id_ok(id_2):
            # limpando terminal
            os.system('clear') or None
            print('\nOs cadastros a seguir terão os sobrenomes trocados:\n')
            # iterando sobre os ids informados e exibindo os cadastros
            for i in range(2):
                # convertendo os ids em index
                ids[i] = int(ids[i]) - 1
                # exibindo
                print(f'ID: {self.id[ids[i]]}')
                print(f'Nome: {nome[ids[i]]}')
                print(f'CPF: {cpf[ids[i]]}')
                print(f'Data de Nascimento: {nasc[ids[i]]}\n')

            confirmar = input('<ENTER> para confirmar troca ou digite outra tecla para cancelar: ')

            # solicitando que confirme a troca de sobrenome
            if confirmar == '':
                # armazenando os nomes e sobrenomes
                nomes = []
                sobrenomes = []
                # iterando sobre os nomes e sobrenomes
                for i in range(len(nome)):
                    # pegando os nomes
                    nome_ = nome[i].split()[0]
                    # pegando os sobrenomes
                    sobrenome_ = nome[i].split()[-2:]
                    # armazenando
                    nomes.append(nome_)
                    sobrenomes.append(sobrenome_[1])

                # fazendo a troca dos sobrenomes
                nome[int(id_1) - 1] = nomes[int(id_1) - 1] + ' ' + sobrenomes[int(id_2) - 1]
                nome[int(id_2) - 1] = nomes[int(id_2) - 1] + ' ' + sobrenomes[int(id_1) - 1]

            else:
                input('\nAlteração cancelada pelo usuário <ENTER> para continuar')
            break


# funcao de remocao de cadastro
def remove_cadastro(self, nome, cpf, nasc):
    # loop da funcao
    while True:
        self.exibir_cadastro(nome, cpf, nasc)
        id = input("Informe o ID do cadastro a ser removido: ")

        # validando o id informado atraves da funcao abaixo
        if self.ver_id_ok(id):
            # limpando terminal
            os.system('clear') or None
            # convertendo id em index
            id = int(id) - 1
            # exebindo cadastro que sera excluido
            print('O cadastro a seguir será excluído\n')
            print(f'ID: {self.id[id]}')
            print(f'Nome: {nome[id]}')
            print(f'CPF: {cpf[id]}')
            print(f'Data de Nascimento: {nasc[id]}\n')

            # solicitando confirmação
            confirmar = input('<ENTER> para confirmar ou digite outra tecla para cancelar: ')
            # caso o usuario confirme
            if confirmar == '':
                # excluindo o cadastro
                del self.id[id]
                del nome[id]
                del nasc[id]
                # iterando sobre os ids
                for i in range(len(self.id)):
                    # se o algum id for menor ou igual o id informado
                    if self.id[i] <= id:
                        continue
                    # corregindo os ids apos a exclusao
                    self.id[i] = self.id[i] - 1
                input('\nCadastro removido <ENTER> para continuar')
                break
            else:
                input('\nExclusão cancelada pelo usuário <ENTER> para continuar')
                break
