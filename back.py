import PySimpleGUI as sg
class Professor:
    def __init__(self, **kwargs) -> None:
        self.nome = kwargs['nome']
        self.area_atuacao = kwargs.pop('area_atuacao', 'ND')
        self.disciplinas = []
        for i in kwargs['disciplinas']:
            self.disciplinas.append(i)
    def contaCarga(self) -> int:
        total = 0
        for i in self.disciplinas:
            total += i.cargaHoraria
        return total
class Disciplina:
    def __init__(self, **kwargs):
        self.nome = kwargs['nome']
        self.cargaHoraria = int(kwargs.pop('carga', 0))

disp1 = Disciplina(nome='MAS',carga=120)
disp2 = Disciplina(nome = 'EAP', carga = 120)
disp3 = Disciplina(nome = 'CSBA', carga = 80)
disp4 = Disciplina(nome='EI',carga=80)
disp5 = Disciplina(nome = 'MS', carga = 120)
disp6 = Disciplina(nome='CAE',carga=120)
disp7 = Disciplina(nome='Ética',carga=60)
disp8 = Disciplina(nome='MSMF',carga=120)
disp9 = Disciplina(nome='QM',carga=80)

prof1 = Professor(nome = 'Karla', area_atuacao = 'Exatas', disciplinas = [disp1, disp5, disp8])
prof2 = Professor(nome = 'Roveredo', area_atuacao = 'Programacao', disciplinas = [disp3, disp6])
prof3 = Professor(nome = 'Mariana', area_atuacao = 'Exatas', disciplinas = [disp2])
prof4 = Professor(nome = 'Glauco', area_atuacao = 'Negocios', disciplinas = [disp4])
prof5 = Professor(nome = 'Fred', area_atuacao = 'Humanas', disciplinas = [disp7])
prof6 = Professor(nome = 'Camila', area_atuacao = 'Exatas', disciplinas = [disp9])
prof7 = Professor(nome='Marli', area_atuacao='Exatas', disciplinas = [disp5,disp8])

carga_h = [60,80,120]
areas_atuac = ['Calculo', 'Programação', 'Negócios', 'Humanas']
professores = [prof1, prof2, prof3, prof4, prof5, prof6, prof7]
disciplinas = [disp1, disp2, disp3, disp4, disp5, disp6, disp7, disp8, disp9]


def nomes(x):
    nomes = []
    for i in x:
        nomes.append(i.nome)
    return nomes

def escolha_disp(x:list):
    import PySimpleGUI as sg
    for i in disciplinas: 
            x.insert(2,[sg.Checkbox(text=f'{i.nome}', key=f'{i.nome}')])
    return x

def get_disc(x:list):
    disci = []
    for i in x:
        disci.append(i.nome)
    return print(disci)
        
def escolha_prof(x:list):
    import PySimpleGUI as sg
    for a in professores:
        x.insert(2, [sg.Checkbox(text = f'{a.nome}', k = f'{a.nome}')])
    return x

def add_disc(x:list):
    nome_disc = sg.Input(k = 'Nome', size = (20,10))
    layout = [
        [sg.Text('Nome'), nome_disc],
        [sg.Combo(values = carga_h, k = 'Carga horaria', default_value='')],
        [sg.Button(button_text = 'Adicionar'), sg.Button('Voltar', k = 'Voltar' )]
    ]

    layout = escolha_prof(layout)
    janela = sg.Window('Adicionar disciplina', layout = layout)
    while True: 
        try:
            eventos , dados = janela.read()
            nome = dados['Nome']
            carga_horaria = dados['Carga horaria']
            if eventos == 'Adicionar':
                x.append(Disciplina(nome = nome, carga = carga_horaria ))
                break
            elif eventos == sg.WIN_CLOSED or eventos == 'Voltar':
                janela.close()
                break
        except TypeError:
                pass

def add_prof(x:list): 
    nome_prof = sg.Input(key='Nome', size=(20,10))
    layout = [
        [sg.Text('Nome'),nome_prof],
        [sg.Combo(values=areas_atuac, key='Area Atuação',default_value='')],
        [],
        [sg.Button(button_text='Adicionar'), sg.Button('Voltar', key='Voltar')]
    ]
    lt_pop = [
        [sg.Text('Professor adicionado com sucesso!')],
        [sg.Button(button_text='Add Outro', k='Add outro'), sg.Button(button_text='Sair', k='Sair')]
    ]
    popup = sg.Window('Adicionado', layout=lt_pop)
    layout = escolha_disp(layout)
    window = sg.Window(title='Adicionar Professor', layout=layout)
    while True:
        try:
            evento, dados = window.read()
            nome = dados['Nome']
            area_atuac = dados['Area Atuação']
            dados['Disciplinas'] = []
            for i in disciplinas:
                if dados[i.nome] == True:
                    dados['Disciplinas'].append(i)
            if  evento == 'Adicionar':
                x.append(Professor(nome=nome, area_atuacao=area_atuac, disciplinas=dados['Disciplinas']))
                nome_prof.update('')
                for i in disciplinas:
                    y = window.find_element(f'{i.nome}')
                    y.update(False)
                z = window.find_element('Area Atuação')
                z.update('')
                sg.popup('Professor(a) adicionado com sucesso!',title='')
                window.refresh()
            elif evento == sg.WIN_CLOSED or evento == 'Voltar':
                window.close()
                break
        except TypeError:
            pass

def criartxt(pasta):
    texto = []
    for i in professores:
        linha = {}
        disci = []
        for j in i.disciplinas:
            disci.append(j.nome)
        linha['disciplinas'] = disci
        disci_t =''
        for k in linha['disciplinas']:
            if k == linha['disciplinas'][-1]:
                disci_t += f'{k}'
            else:
                disci_t += f'{k}, '
        texto.append(f"{i.nome:<10} | {disci_t:<15} | {i.contaCarga():^5}")
    txt = ''
    for l in texto:
        if l == texto[-1]:
            txt += l
        else:
            txt += f'{l}\n'
    print(txt)
    try:
        file = open(f"{pasta}/DadosProfessor.txt", "x")
        file.write(txt)
    except FileExistsError:
        file = open(f'{pasta}/DadosProfessor.txt', "w")
        file.write(txt)

def profs_lista():
    lt_profs = [
        [sg.Listbox(nomes(professores), enable_events=True, key='profs', change_submits=True, size=(12,5)),sg.Text(f'Area de atuação:\n----', key='area_atuac')],
        [sg.Button('Add Prof'), sg.Button('Excluir Prof')],
        [sg.Exit(button_text='Sair')]
    ]  
    w2 = sg.Window('Lista de Professores', layout=lt_profs, size=(300,300))
    while True:
        evento, dados = w2.read()
        area = w2.find_element('area_atuac')
        profs = w2.find_element('profs')
        if evento == 'profs':
            print(dados['profs'])         
            for i in professores:
                if len(dados['profs']) > 0  and i.nome == dados['profs'][0]:
                    area.update(f'Area de atuação:\n{i.area_atuacao}')
        if evento == 'Sair' or evento == sg.WIN_CLOSED :
            w2.close()
            break
        elif evento == 'Add Prof':
                add_prof(professores)
                combo = w2.find_element('profs')
                combo.update(values=nomes(professores))
                for i in professores:
                    print(i.nome, end=', ')
                w2.refresh()
        elif evento == 'Excluir Prof':
            for i in professores:
                if len(dados['profs']) > 0  and i.nome == dados['profs'][0]:
                        sg.popup(f'Professor(a) {dados["profs"][0]}, excluido(a) com sucesso!',title='Aviso!')
                        professores.remove(i)
                        profs.update(nomes(professores))
                        area.update(f'Area de atuação:\n----')
                        w2.refresh()

def disc_list():
    layout = [
        [sg.Listbox(nomes(disciplinas), enable_events = True, k = 'disciplinas',change_submits=True, size = (12,5)), sg.Text(f'Carga horária:\n----', k ='carga_h')],
        [sg.Button('Adicionar disciplina'), sg.Button('Excluir disciplina')],
        [sg.Exit(button_text = 'Sair')]
    ]
    janela = sg.Window('Lista de Disciplinas', layout, size=(300,250))
    while True:
        eventos, dados = janela.read()
        carga_horaria = janela.find_element('carga_h')
        disciplina = janela.find_element('disciplinas')
        #disc = janela.find_element('disciplinas')
        if eventos == 'disciplinas':
            print(dados['disciplinas'])  
            for i in disciplinas:
                if len(dados['disciplinas']) > 0  and i.nome == dados['disciplinas'][0]:
                    carga_horaria.update(f'Carga horária:\n{i.cargaHoraria}')
        elif eventos == 'Sair' or eventos == sg.WIN_CLOSED:
            janela.close()
            break
        elif eventos == 'Adicionar disciplina':
            #add_disc(disciplinas)
            #combo = janela.find_element('disciplinas')
            #combo.update(values = nomes(disciplinas))
            #for i in disciplinas:
            #    print(i.nome, end=', ')
            #janela.refresh()
            print('Gustavo vai fazer')
        elif eventos == 'Excluir disciplina':
            for i in disciplinas:
               if len(dados['disciplinas']) > 0  and i.nome == dados['disciplinas'][0]:
                   sg.popup(f'Disciplina {dados["disciplinas"][0]}, excluido(a) com sucesso!',title = 'Aviso!')
                   disciplinas.remove(i)
                   disciplina.update(nomes(disciplinas))
                   carga_horaria.update(f'Carga horária:\n----')
                   janela.refresh() 

def disps_lista():
    lt_profs = [
        [sg.Listbox(nomes(professores), enable_events=True, key='profs', change_submits=True, size=(12,5)),sg.Text(f'Area de atuação:\n----', key='area_atuac')],
        [sg.Button('Add Prof'), sg.Button('Excluir Prof')],
        [sg.Exit(button_text='Sair')]
    ]  
    w2 = sg.Window('Lista de Professores', layout=lt_profs, size=(300,300))
    while True:
        evento, dados = w2.read()
        area = w2.find_element('area_atuac')
        profs = w2.find_element('profs')
        if evento == 'profs':
            print(dados['profs'])         
            for i in professores:
                if len(dados['profs']) > 0  and i.nome == dados['profs'][0]:
                    area.update(f'Area de atuação:\n{i.area_atuacao}')
        if evento == 'Sair' or evento == sg.WIN_CLOSED :
            w2.close()
            break
        elif evento == 'Add Prof':
                add_prof(professores)
                combo = w2.find_element('profs')
                combo.update(values=nomes(professores))
                for i in professores:
                    print(i.nome, end=', ')
                w2.refresh()
        elif evento == 'Excluir Prof':
            for i in professores:
                if len(dados['profs']) > 0  and i.nome == dados['profs'][0]:
                        sg.popup(f'Professor(a) {dados["profs"][0]}, excluido(a) com sucesso!',title='Aviso!')
                        professores.remove(i)
                        profs.update(nomes(professores))
                        area.update(f'Area de atuação:\n----')
                        w2.refresh()

def relatorio():
    lt = [
        [sg.Text(f'_'*300)],
        [sg.Text('Selecione sua pasta:'), sg.InputText(key = 'TargetFolder'), sg.FolderBrowse('Pesquisar')],
        [sg.Submit(), sg.Exit()]
        ]
    wr = sg.Window('Gerar Relatório', layout=lt, size=(600,100))
    evento, dados = wr.read()
    while True:
        if evento == 'Exit' or evento == sg.WIN_CLOSED:
            wr.close()
            break
        elif evento == 'Submit':
                criartxt(dados['TargetFolder'])
                sg.popup('Relatório criado com sucesso!')
                wr.close()
                break
