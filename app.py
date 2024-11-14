import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import SQLfunctions
from SQLfunctions import BDConection, BDDataRemovers, BDHandler
import threading
import sys
import os


class Application(object):
    # encerrar app
    def close(self):
        ancenterer = messagebox.askokcancel(title='Confirmation',
                                            message='Realmente deseja sair?')
        if ancenterer:
            # encerrando a thread do timer
            self.counting = False
            self.app.destroy()

    # Construtor, vai ser executado ao iniciar a aplicação pela primeira vez.
    # Neste método devemos inicializar todo o esqueleto da aplicação
    def __init__(self, app):
        self.app = app
        self.nomeApp = "MediSync"
        # Variável que controla a thread de timer. False para desligar o timer
        self.counting = True
        # Inicializando o timer
        self.initTimer()
        self.menu()
        self.app.protocol("WM_DELETE_WINDOW", self.close)
        self.app.mainloop()

    def menu(self):
        self.app.title(self.nomeApp)
        # trocando icone do app
        icone = tk.PhotoImage(file='icons/icone app.png')
        self.app.iconphoto(True, icone)
        self.app["bg"] = "#26a599"
        self.app.maxsize(width=self.app.winfo_screenwidth(),
                         height=self.app.winfo_screenheight())
        self.app.minsize(width=1280, height=1024)
        self.app.geometry("1280x1024")
        self.app.resizable(True, True)
        self.app.state("zoomed")
        ###### centralizando a janela ######
        # POSSUI UM PROBLEMA: QND VC AUMENTA O TAMANHO ELE NAO ATUALIZARÁ PARA RECENTRALIZAR
        ######## dimensões ########
        largura = 1280
        altura = 1024
        ######## resolução ########
        largura_screen = self.app.winfo_screenwidth()
        altura_screen = self.app.winfo_screenheight()
        ######## posição ########
        posx = largura_screen/2 - largura/2
        posy = altura_screen/2 - altura/2
        ######## geometry ########
        self.app.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))

        # Iniciando os Widgets dessa Janela
        self.widgets()

    def initTimer(self):
        self.timer = 0
        self.thread1 = threading.Thread(target=self.timercount)
        self.thread1.start()

    def timercount(self):
        while self.counting:
            hora = time.strftime("%H:%M")
            self.relogio = time.strftime("%H:%M\n%a, %B %d")
            if hora != self.timer:
                self.timer = hora
                self.widgets()
        sys.exit()

    def widgets(self):
        ######### 1 - CONFIGURANDO OS COMPONENTES ##############

        ##### label destaque reologio e nome do app#####
        self.quadrado = tk.Label(self.app, bg="#22958a")

        ##### RELOGIO #####
        # Label relógio
        self.frameHora = tk.Label(self.app, text=self.relogio, bg="#22958a", fg='#e1fada',
                                  anchor='center', font=('Comic Sans MS', 35, 'bold'))

        ### Label aleatoria pedida pelo xandao###
        self.xandao = tk.Label(self.app, text=f" Seja bem vindo ao {self.nomeApp}\nOrganize sua clínica de forma mais eficiente.", bg="#22958a",
                               fg='#e1fada', anchor='center', font=('Comic Sans MS', 35, 'bold'))

        ####### CADASTRO PACIENTE #######
        # Label paciente
        self.desc01 = tk.Label(self.app, text="Cadastrar um Paciente!", bg='#e1fada',
                               fg='#26a599', anchor='center', font=('Comic Sans MS', 14, "bold"))
        # Imagem paciente
        btn1 = tk.PhotoImage(file="icons/paciente.png", master=self.app)
        btn1 = btn1.subsample(2, 2)
        img1 = tk.Label(self.app, image=btn1)
        img1.image = btn1
        # Botão Lembrete
        self.botao1 = tk.Button(self.app, image=btn1, bd=0, highlightthickness=0,
                                bg='#26a599', command=lambda: self.mudarJanela(self.janelaPaciente, self.app))
        # passar o mouse emcima do botão
        self.botao1.bind("<Enter>", lambda e1,
                         b1=self.botao1: self.on_enter(e1, b1))
        self.botao1.bind("<Leave>", lambda e1,
                         b1=self.botao1: self.on_leave(e1, b1))

        ####### CADASTRO CONSULTA #######
        # Label Consulta
        self.desc02 = tk.Label(self.app, text="Cadastrar Uma Consulta", bg='#e1fada',
                               fg='#26a599', anchor='center', font=('Comic Sans MS', 14, "bold"))
        # Imagem consulta
        btn2 = tk.PhotoImage(file="icons/consulta.png", master=self.app)
        btn2 = btn2.subsample(2, 2)
        img2 = tk.Label(self.app, image=btn2)
        img2.image = btn2
        # Botão Consulta
        self.consulta = tk.Button(self.app, image=btn2, bd=0, highlightthickness=0,
                                  bg='#26a599', command=lambda: self.mudarJanela(self.janelaConsulta, self.app))
        # passar o mouse emcima do botão
        self.consulta.bind("<Enter>", lambda e2,
                           b2=self.consulta: self.on_enter(e2, b2))
        self.consulta.bind("<Leave>", lambda e2,
                           b2=self.consulta: self.on_leave(e2, b2))

        ####### CADASTRO funcionario #######
        # Label funcionario
        self.desc03 = tk.Label(self.app, text="Cadastrar um funcionario! ", bg='#e1fada',
                               fg='#26a599', anchor='center', font=('Comic Sans MS', 14, "bold"))
        # Imagem Funcionario
        btn3 = tk.PhotoImage(file="icons/medico.png", master=self.app)
        btn3 = btn3.subsample(2, 2)
        img3 = tk.Label(self.app, image=btn3)
        img3.image = btn3
        # Botão Funcionario
        self.botao3 = tk.Button(self.app, image=btn3, bd=0, highlightthickness=0,
                                bg='#26a599', command=lambda: self.mudarJanela(self.janelaFuncionario, self.app))
        # passar o mouse emcima do botão
        self.botao3.bind("<Enter>", lambda e3,
                         b3=self.botao3: self.on_enter(e3, b3))
        self.botao3.bind("<Leave>", lambda e3,
                         b3=self.botao3: self.on_leave(e3, b3))

        ####################################################
        ######### 2 - EXIBINDO OS COMPONENTES ##############
        ##### label destaque reologio e nome do app#####
        self.quadrado.place(relx=0.005, rely=0.01,
                            relwidth=0.989, relheight=0.36)
        ### Relogio###
        self.frameHora.place(relx=0.275, rely=0.01,
                             relwidth=0.45, relheight=0.18)
        ### xandao##
        self.xandao.place(relx=0.005, rely=0.195,
                          relwidth=0.989, relheight=0.16)
        ### Paciente###
        self.desc01.place(relx=0.069625, rely=0.76,
                          relwidth=0.2405, relheight=0.04)
        ### Consulta###
        self.desc02.place(relx=0.37975, rely=0.76,
                          relwidth=0.2405, relheight=0.04)
        ### Funcionario###
        self.desc03.place(relx=0.689875, rely=0.76,
                          relwidth=0.2405, relheight=0.04)

        # Botões
        ### Paciente###
        self.botao1.place(relx=0.12625, rely=0.564,
                          relwidth=0.125, relheight=0.182)
        ### Consulta###
        self.consulta.place(relx=0.4375, rely=0.564,
                            relwidth=0.125, relheight=0.182)
        ### Funcionario###
        self.botao3.place(relx=0.74675, rely=0.564,
                          relwidth=0.125, relheight=0.182)

    ###### Funçoes do cursor ######
    def on_enter(self, event, button):
        # Mudando a cor de fundo do botão ao passar o mouse
        button.config(bg='#e1fada')  # Altera a cor de fundo ao passar o mouse

    def on_leave(self, event, button):
        # Restaurando a cor de fundo do botão ao sair
        button.config(bg='#26a599')  # Restaura a cor de fundo original

    def mudarJanela(self, abrir, fechar):

        if fechar == self.app:
            abrir()
        # A tela a ser fechada é qualquer outra
        # Nesse caso a principal deverá ser aberta
        else:
            # destruindo a atual
            fechar.destroy()

    # função que visualiza as tabelas do Db
    def frameVisPaciente(self):
        self.vispaciente = tk.Toplevel(self.app)
        self.vispaciente.grab_set()  # Impede interação com a janela principal
        self.vispaciente.title("LISTA DE PACIENTES CADASTRADOS")
        self.vispaciente["bg"] = "#26a599"
        self.vispaciente.maxsize(width=self.vispaciente.winfo_screenwidth(),
                                 height=self.vispaciente.winfo_screenheight())
        self.vispaciente.minsize(width=700, height=600)
        self.vispaciente.resizable(False, False)
        # centralizando a janela
        # dimensões
        largura = 700
        altura = 600
        # resolução
        largura_screen = self.vispaciente.winfo_screenwidth()
        altura_screen = self.vispaciente.winfo_screenheight()
        # posição
        posx = largura_screen/2 - largura/2
        posy = altura_screen/2 - altura/2
        # geometry
        self.vispaciente.geometry('%dx%d+%d+%d' %
                                  (largura, altura, posx, posy))

        ####### CRIANDO Treeview para exbir a tabela do banco ######
        # criando um estilo para alterar as cores do treevieww
        # Criando um estilo personalizado
        style = ttk.Style()
        # Mudar para o tema 'clam' que permite customizações
        style.theme_use('clam')
        style.configure("Custom.Treeview",
                        background="#165F58",  # Cor de fundo das células
                        foreground="#e1fada",    # Cor do texto
                        fieldbackground="#22958a",  # Cor de fundo ao selecionar
                        rowheight=30)          # Altura das linhas

        style.configure("Custom.Treeview.Heading",
                        background="#e1fada", foreground="#22958a")
        # criando a coluna
        self.labelTv = ttk.Treeview(self.vispaciente, columns=('id', 'nome', 'email', 'telefone', 'cpf', 'dataNascimento'),
                                    show='headings', style="Custom.Treeview")
        # adicionando o tamanho das colunas
        self.labelTv.column('id', minwidth=0, width=30,  anchor="center")
        self.labelTv.column('nome', minwidth=0, width=40, anchor="center")
        self.labelTv.column('email', minwidth=0, width=50, anchor="center")
        self.labelTv.column('telefone', minwidth=0, width=50, anchor="center")
        self.labelTv.column('cpf', minwidth=0, width=40, anchor="center")
        self.labelTv.column('dataNascimento', minwidth=0, width=80, anchor="center")
        # nomeando as colunas a ser exibidas
        self.labelTv.heading('id', text='ID', anchor="center")
        self.labelTv.heading('nome', text='NOME', anchor="center")
        self.labelTv.heading('email', text='EMAIL', anchor="center")
        self.labelTv.heading('telefone', text='TELEFONE', anchor="center")
        self.labelTv.heading('cpf', text='CPF', anchor="center")
        self.labelTv.heading('dataNascimento', text='DATA DE NASCIMENTO', anchor="center")
        self.labelTv.pack(fill = "both", expand= True)

        pacientes = BDHandler.visualizar_pacientes()
        if pacientes:
            for paciente in pacientes:
                self.labelTv.insert("", "end", values=paciente)
        ####### CRIANDO COMPONENTES VISUAIS ######

        # explicação pagina
        # label espec
        self.quadrado = tk.Label(self.vispaciente, text="PACIENTES CADASTRADOS", bg="#22958a", fg='white',
                                 font=('Comic Sans MS', 18, "bold"), anchor="center")

        # BOTÃO VOLTAR
        # Imagem voltar
        btnVoltar = tk.PhotoImage(file="icons/home.png", master=self.app)
        btnVoltar = btnVoltar.subsample(2, 2)
        img2 = tk.Label(self.app, image=btnVoltar)
        img2.image = btnVoltar
        # atribuindo comando
        self.voltar = tk.Button(self.vispaciente, image=btnVoltar, bg='#26a599', fg='white', bd=0,
                                command=lambda: self.mudarJanela(self.app, self.vispaciente))

        # BOTÃO deletar
        # Imagem deletar
        btndelet = tk.PhotoImage(file="icons/delete.png", master=self.app)
        btndelet = btndelet.subsample(2, 2)
        img2 = tk.Label(self.app, image=btndelet)
        img2.image = btndelet
        # atribuindo comando
        self.deletar = tk.Button(self.vispaciente, image=btndelet, bg='#26a599', fg='white', bd=0,
                                 command=lambda: self.deletar_pacientes(self.labelTv))

        ### mudando a cor do botão ao passar cursor###
        self.voltar.bind("<Enter>", lambda e,
                         b=self.voltar: self.on_enter(e, b))
        self.voltar.bind("<Leave>", lambda e,
                         b=self.voltar: self.on_leave(e, b))
        self.deletar.bind("<Enter>", lambda e1,
                          b1=self.deletar: self.on_enter(e1, b1))
        self.deletar.bind("<Leave>", lambda e1,
                          b1=self.deletar: self.on_leave(e1, b1))

        ####### DESENHANDO OS COMPONENTES NA TELA ############
        ######## geometry tk.Labels ########
        self.quadrado.place(relx=0.005, rely=0.01, relwidth=0.989, relheight=0.1)
        self.labelTv.place(relx=0.05, rely=0.1585, relwidth=0.89, relheight=0.6664)
        ######## geometry  botões ########
        self.deletar.place(relx=0.1666, rely=0.8875, relwidth=0.25, relheight=0.1)
        self.voltar.place(relx=0.5766, rely=0.8875, relwidth=0.25, relheight=0.1)

    # função que visualiza as tabelas do Db
    def frameVisConsulta(self):
        self.visConsulta = tk.Toplevel(self.app)
        self.visConsulta.grab_set()  # Impede interação com a janela principal
        self.visConsulta.title("LISTA DE CONSULTAS CADASTRADAS")
        self.visConsulta["bg"] = "#26a599"
        self.visConsulta.maxsize(width=self.visConsulta.winfo_screenwidth(),
                                 height=self.visConsulta.winfo_screenheight())
        self.visConsulta.minsize(width=700, height=600)
        self.visConsulta.resizable(False, False)
        # centralizando a janela
        # dimensões
        largura = 700
        altura = 600
        # resolução
        largura_screen = self.visConsulta.winfo_screenwidth()
        altura_screen = self.visConsulta.winfo_screenheight()
        # posição
        posx = largura_screen/2 - largura/2
        posy = altura_screen/2 - altura/2
        # geometry
        self.visConsulta.geometry('%dx%d+%d+%d' %
                                  (largura, altura, posx, posy))

        ####### CRIANDO Treeview para exbir a tabela do banco ######
        # criando um estilo para alterar as cores do treevieww
        # Criando um estilo personalizado
        style = ttk.Style()
        # Mudar para o tema 'clam' que permite customizações
        style.theme_use('clam')
        style.configure("Custom.Treeview",
                        background="#165F58",  # Cor de fundo das células
                        foreground="#e1fada",    # Cor do texto
                        fieldbackground="#22958a",  # Cor de fundo ao selecionar
                        rowheight=30)          # Altura das linhas

        style.configure("Custom.Treeview.Heading",
                        background="#e1fada", foreground="#22958a")
        # criando a coluna
        self.labelTv = ttk.Treeview(self.visConsulta, columns=('id', 'nomeDoutor', 'nomePaciente', 'valorConsulta', 'descricao',
                                                               'dataConsulta', 'horaConsulta'),
                                    show='headings', style="Custom.Treeview")
        # adicionando o tamanho das colunas
        self.labelTv.column('id', minwidth=0, width=30, anchor="center")
        self.labelTv.column('nomeDoutor', minwidth=0, width=60, anchor="center")
        self.labelTv.column('nomePaciente', minwidth=0, width=60, anchor="center")
        self.labelTv.column('valorConsulta', minwidth=0, width=70, anchor="center")
        self.labelTv.column('descricao', minwidth=0, width=50, anchor="center")
        self.labelTv.column('dataConsulta', minwidth=0, width=50, anchor="center")
        self.labelTv.column('horaConsulta', minwidth=0, width=30, anchor="center")
        # nomeando as colunas a ser exibidas
        self.labelTv.heading('id', text='ID')

        self.labelTv.heading('nomeDoutor', text='NOME DOUTOR', anchor="center")
        self.labelTv.heading('nomePaciente', text='NOME PACIENTE', anchor="center")
        self.labelTv.heading('valorConsulta', text='VALOR DA CONSULTA', anchor="center")
        self.labelTv.heading('descricao', text='DESCRIÇÂO', anchor="center")
        self.labelTv.heading('dataConsulta', text='DATA DA CONSULTA', anchor="center")
        self.labelTv.heading('horaConsulta', text='HORA DA CONSULTA', anchor="center")
        
        consultas = BDHandler.visualizar_agenda()
        if consultas:
            for consulta in consultas:
                self.labelTv.insert("", "end", values=consulta)
        ####### CRIANDO COMPONENTES VISUAIS ######

        # explicação pagina
        # label espec
        self.quadrado = tk.Label(self.visConsulta, text="CONSULTAS CADASTRADAS", bg="#22958a", fg='white',
                                 font=('Comic Sans MS', 18, "bold"), anchor="center")

        # BOTÃO VOLTAR
        # Imagem voltar
        btnVoltar = tk.PhotoImage(file="icons/home.png", master=self.app)
        btnVoltar = btnVoltar.subsample(2, 2)
        img2 = tk.Label(self.app, image=btnVoltar)
        img2.image = btnVoltar
        # atribuindo comando
        self.voltar = tk.Button(self.visConsulta, image=btnVoltar, bg='#26a599', fg='white', bd=0,
                                command=lambda: self.mudarJanela(self.app, self.visConsulta))

        # BOTÃO deletar
        # Imagem deletar
        btndelet = tk.PhotoImage(file="icons/delete.png", master=self.app)
        btndelet = btndelet.subsample(2, 2)
        img2 = tk.Label(self.app, image=btndelet)
        img2.image = btndelet
        # atribuindo comando
        self.deletar = tk.Button(self.visConsulta, image=btndelet, bg='#26a599', fg='white', bd=0,
                                 command=lambda: self.deletar_consultas(self.labelTv))

        ### mudando a cor do botão ao passar cursor###
        self.voltar.bind("<Enter>", lambda e,
                         b=self.voltar: self.on_enter(e, b))
        self.voltar.bind("<Leave>", lambda e,
                         b=self.voltar: self.on_leave(e, b))
        self.deletar.bind("<Enter>", lambda e1,
                          b1=self.deletar: self.on_enter(e1, b1))
        self.deletar.bind("<Leave>", lambda e1,
                          b1=self.deletar: self.on_leave(e1, b1))

        ####### DESENHANDO OS COMPONENTES NA TELA ############
        ######## geometry tk.Labels ########
        self.quadrado.place(relx=0.005, rely=0.01, relwidth=0.989, relheight=0.1)
        self.labelTv.place(relx=0.025, rely=0.1585, relwidth=0.95, relheight=0.6664)
        ######## geometry  botões ########
        self.deletar.place(relx=0.1666, rely=0.8875, relwidth=0.25, relheight=0.1)
                           
        self.voltar.place(relx=0.5766, rely=0.8875, relwidth=0.25, relheight=0.1)                 

    # função que visualiza as tabelas do Db
    def frameVisFuncionario(self):
        self.visFuncionario = tk.Toplevel(self.app)
        self.visFuncionario.grab_set()  # Impede interação com a janela principal
        self.visFuncionario.title("LISTA DE FUNCIONARIOS CADASTRADOS")
        self.visFuncionario["bg"] = "#26a599"
        self.visFuncionario.maxsize(width=self.visFuncionario.winfo_screenwidth(),
                                    height=self.visFuncionario.winfo_screenheight())
        self.visFuncionario.minsize(width=700, height=600)
        self.visFuncionario.resizable(False, False)
        # centralizando a janela
        # dimensões
        largura = 700
        altura = 600
        # resolução
        largura_screen = self.visFuncionario.winfo_screenwidth()
        altura_screen = self.visFuncionario.winfo_screenheight()
        # posição
        posx = largura_screen/2 - largura/2
        posy = altura_screen/2 - altura/2
        # geometry
        self.visFuncionario.geometry(
            '%dx%d+%d+%d' % (largura, altura, posx, posy))

        ####### CRIANDO Treeview para exbir a tabela do banco ######
        # criando um estilo para alterar as cores do treevieww
        # Criando um estilo personalizado
        style = ttk.Style()
        # Mudar para o tema 'clam' que permite customizações
        style.theme_use('clam')
        style.configure("Custom.Treeview",
                        background="#165F58",  # Cor de fundo das células
                        foreground="#e1fada",    # Cor do texto
                        fieldbackground="#22958a",  # Cor de fundo ao selecionar
                        rowheight=30)          # Altura das linhas

        style.configure("Custom.Treeview.Heading",
                        background="#e1fada", foreground="#22958a")
        # criando a coluna
        self.labelTv = ttk.Treeview(self.visFuncionario, columns=('id', 'nomeDoutor', 'email', 'telefone', 'crm', 'dataNascimento', 'cpf'),
                                    show='headings', style="Custom.Treeview")
        # adicionando o tamanho das colunas
        self.labelTv.column('id', minwidth=0, width=30, anchor="center")
        self.labelTv.column('nomeDoutor', minwidth=0, width=40, anchor="center")
        self.labelTv.column('email', minwidth=0, width=50, anchor="center")
        self.labelTv.column('telefone', minwidth=0, width=50, anchor="center")
        self.labelTv.column('crm', minwidth=0, width=80, anchor="center")
        self.labelTv.column('dataNascimento', minwidth=0, width=80, anchor="center")
        self.labelTv.column('cpf', minwidth=0, width=40, anchor="center")
        
        
        # nomeando as colunas a ser exibidas
        self.labelTv.heading('id', text='ID', anchor="center")

        self.labelTv.heading('nomeDoutor', text='NOME FUNCIONARIO', anchor="center")

        self.labelTv.heading('email', text='EMAIL', anchor="center")

        self.labelTv.heading('telefone', text='TELEFONE', anchor="center")

        self.labelTv.heading('crm', text='CRM', anchor="center")

        self.labelTv.heading('dataNascimento', text='DATA DE NASCIMENTO', anchor="center")

        self.labelTv.heading('cpf', text='CPF', anchor="center")

        funcionarios = BDHandler.visualizar_medicos()
        if funcionarios:
            for funcionario in funcionarios:
                self.labelTv.insert("", "end", values=funcionario)

        ####### CRIANDO COMPONENTES VISUAIS ######

        # explicação pagina
        # label espec
        self.quadrado = tk.Label(self.visFuncionario, text="FUNCIONÁRIOS CADASTRADOS", bg="#22958a", fg='white',
                                 font=('Comic Sans MS', 18, "bold"), anchor="center")

        # BOTÃO VOLTAR
        # Imagem voltar
        btnVoltar = tk.PhotoImage(file="icons/home.png", master=self.app)
        btnVoltar = btnVoltar.subsample(2, 2)
        img2 = tk.Label(self.app, image=btnVoltar)
        img2.image = btnVoltar
        # atribuindo comando
        self.voltar = tk.Button(self.visFuncionario, image=btnVoltar, bg='#26a599', fg='white', bd=0,
                                command=lambda: self.mudarJanela(self.app, self.visFuncionario))

        # BOTÃO deletar
        # Imagem deletar
        btndelet = tk.PhotoImage(file="icons/delete.png", master=self.app)
        btndelet = btndelet.subsample(2, 2)
        img2 = tk.Label(self.app, image=btndelet)
        img2.image = btndelet
        # atribuindo comando
        self.deletar = tk.Button(self.visFuncionario, image=btndelet, bg='#26a599', fg='white', bd=0,
                                 command=lambda: self.deletar_funcionarios(self.labelTv))

        ### mudando a cor do botão ao passar cursor###
        self.voltar.bind("<Enter>", lambda e,
                         b=self.voltar: self.on_enter(e, b))
        self.voltar.bind("<Leave>", lambda e,
                         b=self.voltar: self.on_leave(e, b))
        self.deletar.bind("<Enter>", lambda e1,
                          b1=self.deletar: self.on_enter(e1, b1))
        self.deletar.bind("<Leave>", lambda e1,
                          b1=self.deletar: self.on_leave(e1, b1))

        ####### DESENHANDO OS COMPONENTES NA TELA ############
        ######## geometry tk.Labels ########
        self.quadrado.place(relx=0.005, rely=0.01, relwidth=0.989, relheight=0.1)
        self.labelTv.place(relx=0.025, rely=0.1585, relwidth=0.95, relheight=0.6664)
        ######## geometry  botões ########
        self.deletar.place(relx=0.1666, rely=0.8875, relwidth=0.25, relheight=0.1)
        self.voltar.place(relx=0.5766, rely=0.8875, relwidth=0.25, relheight=0.1)

    # função da janela de inserção de dados do paciente
    def janelaPaciente(self):
        self.framePaciente = tk.Toplevel(self.app)
        self.framePaciente.grab_set()  # Impede interação com a janela principal
        self.framePaciente.title("CADASTRAR PACIENTE")
        self.framePaciente["bg"] = "#26a599"
        self.framePaciente.maxsize(width=self.framePaciente.winfo_screenwidth(),
                                   height=self.framePaciente.winfo_screenheight())
        self.framePaciente.minsize(width=700, height=600)
        self.framePaciente.resizable(False, False)
        # centralizando a janela
        # dimensões
        largura = 700
        altura = 600
        # resolução
        largura_screen = self.framePaciente.winfo_screenwidth()
        altura_screen = self.framePaciente.winfo_screenheight()
        # posição
        posx = largura_screen/2 - largura/2
        posy = altura_screen/2 - altura/2
        # geometry
        self.framePaciente.geometry('%dx%d+%d+%d' %
                                    (largura, altura, posx, posy))

        ####### CRIANDO COMPONENTES VISUAIS ######

        # explicação pagina
        # label espec
        self.quadrado = tk.Label(self.framePaciente, text="CADASTRO DE PACIENTE", bg="#22958a", fg='white',
                                 font=('Comic Sans MS', 18, "bold"), anchor="center")

        # NOME
        # Label NOME
        self.nome = tk.Label(self.framePaciente, text="NOME", bg='#26a599',
                             fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry NOME
        self.entryNome = tk.Entry(self.framePaciente, fg='white', bg='#22958a',
                                  font=('Comic Sans MS', 14, "bold"))

        # EMAIL
        # Label email
        self.email = tk.Label(self.framePaciente, text="EMAIL", bg='#26a599',
                              fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry email
        self.entryEmail = tk.Entry(self.framePaciente,
                                   fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # TELEFONE
        # Label telefone
        self.telefone = tk.Label(self.framePaciente, text="TELEFONE", bg='#26a599',
                                 fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry telefone
        self.entryTelefone = tk.Entry(self.framePaciente,
                                      fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # CPF
        # Label cpf
        self.cpf = tk.Label(self.framePaciente, text="CPF", bg='#26a599',
                            fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry cpf
        self.entryCpf = tk.Entry(self.framePaciente,
                                 fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # DATA DE NASCISMENTO
        # Label Data de nascimento
        self.dNascimento = tk.Label(self.framePaciente, text="NASCIMENTO (DD/MM/AAAA)", bg='#26a599',
                                    fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry Data de nascimento
        self.sbxDia = tk.Spinbox(self.framePaciente, fg='white', bg='#22958a',
                                 font=('Comic Sans MS', 20, "bold"), from_=1, to=31)
        self.sbxMes = tk.Spinbox(self.framePaciente, fg='white', bg='#22958a',
                                 font=('Comic Sans MS', 20, "bold"), from_=1, to=12)
        self.sbxAno = tk.Spinbox(self.framePaciente, fg='white', bg='#22958a',
                                 font=('Comic Sans MS', 20, "bold"), from_=1940, to=2024)

        # BOTÃO VOLTAR
        # Imagem voltar
        btnVoltar = tk.PhotoImage(file="icons/home.png", master=self.app)
        btnVoltar = btnVoltar.subsample(2, 2)
        img2 = tk.Label(self.app, image=btnVoltar)
        img2.image = btnVoltar
        # atribuindo comando
        self.voltar = tk.Button(self.framePaciente, image=btnVoltar, bg='#26a599', fg='white', bd=0,
                                command=lambda: self.mudarJanela(self.app, self.framePaciente))

        # BOTÃO visualização
        # Imagem Visualização
        btnVizu = tk.PhotoImage(file="icons/vizualização.png", master=self.app)
        btnVizu = btnVizu.subsample(2, 2)
        img = tk.Label(self.app, image=btnVizu)
        img.image = btnVizu
        # atribuindo comando
        self.vizualizacao = tk.Button(self.framePaciente, image=btnVizu, bg='#26a599', fg='white', bd=0,
                                      command=lambda: self.mudarJanela(self.frameVisPaciente(), self.framePaciente))

        # BOTÃO salvar
        # Imagem salvar
        btnsalvar = tk.PhotoImage(file="icons/save.png", master=self.app)
        btnsalvar = btnsalvar.subsample(2, 2)
        img1 = tk.Label(self.app, image=btnsalvar)
        img1.image = btnsalvar
        # atribuindo comando
        self.save = tk.Button(self.framePaciente, image=btnsalvar, bg='#26a599', fg='white', bd=0,
                              command=lambda: self.validarFormsPaciente(self.entryNome.get(), self.entryEmail.get(),
                                                                        self.entryTelefone.get(), self.entryCpf.get(),
                                                                        self.sbxDia.get(), self.sbxMes.get(), self.sbxAno.get()))

        ### mudando a cor do botão ao passar cursor###
        self.voltar.bind("<Enter>", lambda e,
                         b=self.voltar: self.on_enter(e, b))
        self.voltar.bind("<Leave>", lambda e,
                         b=self.voltar: self.on_leave(e, b))
        self.vizualizacao.bind("<Enter>", lambda e1,
                               b1=self.vizualizacao: self.on_enter(e1, b1))
        self.vizualizacao.bind("<Leave>", lambda e1,
                               b1=self.vizualizacao: self.on_leave(e1, b1))
        self.save.bind("<Enter>", lambda e2,
                       b2=self.save: self.on_enter(e2, b2))
        self.save.bind("<Leave>", lambda e2,
                       b2=self.save: self.on_leave(e2, b2))

        ####### DESENHANDO OS COMPONENTES NA TELA ############
        ######## geometry tk.Labels ########
        self.quadrado.place(relx=0.005, rely=0.01, relwidth=0.989, relheight=0.1)
        self.nome.place(relx=0.05, rely=0.17916, relwidth=0.40, relheight=0.075)
        self.email.place(relx=0.05, rely=0.32332, relwidth=0.40, relheight=0.075)
        self.telefone.place(relx=0.05, rely=0.467486, relwidth=0.40, relheight=0.075)
        self.cpf.place(relx=0.05, rely=0.61646, relwidth=0.40, relheight=0.075)
        self.dNascimento.place(relx=0.03, rely=0.755806, relwidth=0.5, relheight=0.075)
        ######## geometry  botões ########
        self.save.place(relx=0.05, rely=0.8875, relwidth=0.25, relheight=0.1)
        self.vizualizacao.place(relx=0.375, rely=0.8875,relwidth=0.25, relheight=0.1)
        self.voltar.place(relx=0.7, rely=0.8875, relwidth=0.25, relheight=0.1)

        ######## geometry entry ########
        self.entryNome.place(relx=0.5, rely=0.17916, relwidth=0.40, relheight=0.075)
        self.entryEmail.place(relx=0.5, rely=0.32332, relwidth=0.40, relheight=0.075)
        self.entryTelefone.place(relx=0.5, rely=0.467486, relwidth=0.40, relheight=0.075)
        self.entryCpf.place(relx=0.5, rely=0.61646, relwidth=0.40, relheight=0.075)                    
        self.sbxDia.place(relx=0.52, rely=0.755806, relwidth=0.13, relheight=0.075)               
        self.sbxMes.place(relx=0.663, rely=0.755806, relwidth=0.133, relheight=0.075)                
        self.sbxAno.place(relx=0.8063, rely=0.755806, relwidth=0.13, relheight=0.075)
        ######## focus ########
        self.entryNome.focus_force()
        self.framePaciente.protocol(
            "WM_DELETE_WINDOW", lambda: self.mudarJanela(self.app, self.framePaciente))

    # função para validar se fico faltando digitar algum campo do paciente
    def validarFormsPaciente(self, nome, email, telefone, cpf, dia, mes, ano):
        if (nome == "" or email == "" or telefone == "" or cpf == "" or dia == "" or mes == "" or ano == ""):
            self.app.msgbox = messagebox.showerror(
                title="Error", message="Por favor preencha todos os campos!")
        else:
            """""
            #Formatando a data
            dtNascimento = dia+"/"+mes+"/"+ano
            #adicionando ao demais dados guardados
            #adptar para salvar na tabela do banco
            paciente = {"nome": nome, "horario": horario}
            self.data.append(data)"""
            dtNascimento = ano+"-"+mes+"-"+dia
            check, message = BDHandler.adicionar_paciente(nome, dtNascimento, telefone, email, cpf)
            if check:
                self.app.msgbox = messagebox.showinfo(title="Result", message= message)
                self.mudarJanela(self.app, self.frameFuncionario)
            else:
                self.app.msgbox = messagebox.showerror(title="Deu ruim", message= message)
                self.mudarJanela(self.app, self.frameFuncionario)

    # função de deletar, no banco de dados e visualmente, as informações de um dado paciente
    def deletar_pacientes(self, table):
        selected_item = table.selection()
        if selected_item:
            item = table.item(selected_item)
            id_item = item['values'][0]  # Pegando o ID ou outra chave primária
            checkOpc = messagebox.askokcancel("Comfirmação", "Deseja deletar o item selecionado?")
            deleter, msg = BDDataRemovers.removedor_pacientes(id_item, checkOpc)
            if deleter:
                messagebox.showinfo(title="Sucesso", message=msg)
            else:
                messagebox.showinfo(title="Error", message=msg)
                
        table.delete(selected_item)
    
    # função da janela de inserção de dados da consulta
    def janelaConsulta(self):
        self.frameConsulta = tk.Toplevel(self.app)
        self.frameConsulta.grab_set()  # Impede interação com a janela principal
        self.frameConsulta.title("CADASTRAR CONSULTA")
        self.frameConsulta["bg"] = "#26a599"
        self.frameConsulta.maxsize(width=self.frameConsulta.winfo_screenwidth(),
                                   height=self.frameConsulta.winfo_screenheight())
        self.frameConsulta.minsize(width=700, height=600)
        self.frameConsulta.resizable(False, False)
        # centralizando a janela
        # dimensões
        largura = 700
        altura = 600
        # resolução
        largura_screen = self.frameConsulta.winfo_screenwidth()
        altura_screen = self.frameConsulta.winfo_screenheight()
        # posição
        posx = largura_screen/2 - largura/2
        posy = altura_screen/2 - altura/2
        # geometry
        self.frameConsulta.geometry('%dx%d+%d+%d' %
                                    (largura, altura, posx, posy))
        ####### CRIANDO COMPONENTES VISUAIS ######

        # explicação pagina
        # label CADASTRAR PACIENTE
        self.quadrado = tk.Label(self.frameConsulta, text="CADASTRO DE CONSULTA", bg="#22958a", fg='#e1fada',
                                 font=('Comic Sans MS', 18, "bold"), anchor="center")

        # NOME
        # Label Id Medico
        self.idMedico = tk.Label(self.frameConsulta, text="ID DO DOUTOR", bg='#26a599',
                                   fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry id
        self.entryIdMedico = tk.Entry(self.frameConsulta, fg='white', bg='#22958a',
                                        font=('Comic Sans MS', 14, "bold"))

        # nome
        # Label Id Paciente
        self.idPaciente = tk.Label(self.frameConsulta, text="ID PACIENTE", bg='#26a599',
                                     fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry id
        self.entryIdPaciente = tk.Entry(self.frameConsulta,
                                          fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # valor
        # Label valor consulta
        self.valorconsulta = tk.Label(self.frameConsulta, text="VALOR", bg='#26a599',
                                      fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry consulta
        self.entryValorConsulta = tk.Entry(self.frameConsulta,
                                           fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # descrição
        # Label descrição
        self.descrição = tk.Label(self.frameConsulta, text="DESCRIÇÂO", bg='#26a599',
                                  fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry desc
        self.entryDescrição = tk.Entry(self.frameConsulta,
                                       fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # DATA CONSULTA
        # Label Data da Consulta
        self.dataConsulta = tk.Label(self.frameConsulta, text="DATA (DD/MM/AAAA)", bg='#26a599',
                                     fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry Data de nascimento
        self.sbxDiaConsulta = tk.Spinbox(self.frameConsulta, fg='white', bg='#22958a',
                                         font=('Comic Sans MS', 20, "bold"), from_=1, to=31)
        self.sbxMesConsulta = tk.Spinbox(self.frameConsulta, fg='white', bg='#22958a',
                                         font=('Comic Sans MS', 20, "bold"), from_=1, to=12)
        self.sbxAnoConsulta = tk.Spinbox(self.frameConsulta, fg='white', bg='#22958a',
                                         font=('Comic Sans MS', 20, "bold"), from_=1940, to=2024)

        # HORARIO
        # Label HORARIO CONSULTA
        self.Horario = tk.Label(self.frameConsulta, text="HORARIO (HH:MM)", bg='#26a599',
                                fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry horario
        self.sbxHora = tk.Spinbox(self.frameConsulta, fg='white', bg='#22958a',
                                  font=('Comic Sans MS', 20, "bold"), from_=00, to=23)
        self.sbxMinuto = tk.Spinbox(self.frameConsulta, fg='white', bg='#22958a',
                                    font=('Comic Sans MS', 20, "bold"), from_=00, to=59)

        # BOTÃO VOLTAR
        # Imagem voltar
        btnVoltar = tk.PhotoImage(file="icons/home.png", master=self.app)
        btnVoltar = btnVoltar.subsample(2, 2)
        img2 = tk.Label(self.app, image=btnVoltar)
        img2.image = btnVoltar
        # atribuindo comando
        self.voltar = tk.Button(self.frameConsulta, image=btnVoltar, bg='#26a599', fg='white', bd=0,
                                command=lambda: self.mudarJanela(self.app, self.frameConsulta))

        # BOTÃO vizualização
        # Imagem Vizualização
        btnVizu = tk.PhotoImage(file="icons/vizualização.png", master=self.app)
        btnVizu = btnVizu.subsample(2, 2)
        img = tk.Label(self.app, image=btnVizu)
        img.image = btnVizu
        # atribuindo comando
        self.vizualizacao = tk.Button(self.frameConsulta, image=btnVizu, bg='#26a599', fg='white', bd=0,
                                      command=lambda: self.mudarJanela(self.frameVisConsulta(), self.frameConsulta))

        # BOTÃO salvar
        # Imagem salvar
        btnsalvar = tk.PhotoImage(file="icons/save.png", master=self.app)
        btnsalvar = btnsalvar.subsample(2, 2)
        img1 = tk.Label(self.app, image=btnsalvar)
        img1.image = btnsalvar
        # atribuindo comando
        self.save = tk.Button(self.frameConsulta, image=btnsalvar, bg='#26a599', fg='white', bd=0,
                              command=lambda: self.validarFormsConsulta(self.entryIdMedico.get(), self.entryIdPaciente.get(),
                                                                        self.entryValorConsulta.get(), self.sbxDiaConsulta.get(),
                                                                        self.sbxMesConsulta.get(), self.sbxAnoConsulta.get(),
                                                                        self.sbxHora.get(), self.sbxMinuto.get(), self.entryDescrição.get()))

        ### mudando a cor do botão ao passar cursor###
        self.voltar.bind("<Enter>", lambda e,
                         b=self.voltar: self.on_enter(e, b))
        self.voltar.bind("<Leave>", lambda e,
                         b=self.voltar: self.on_leave(e, b))
        self.vizualizacao.bind("<Enter>", lambda e1,
                               b1=self.vizualizacao: self.on_enter(e1, b1))
        self.vizualizacao.bind("<Leave>", lambda e1,
                               b1=self.vizualizacao: self.on_leave(e1, b1))
        self.save.bind("<Enter>", lambda e2,
                       b2=self.save: self.on_enter(e2, b2))
        self.save.bind("<Leave>", lambda e2,
                       b2=self.save: self.on_leave(e2, b2))

        ####### DESENHANDO OS COMPONENTES NA TELA ############
        ######## geometry tk.Labels ########
        self.quadrado.place(relx=0.005, rely=0.01, relwidth=0.989, relheight=0.1)
        self.idMedico.place(relx=0.05, rely=0.1585, relwidth=0.40, relheight=0.075)
        self.idPaciente.place(relx=0.05, rely=0.2821, relwidth=0.40, relheight=0.075)
        self.valorconsulta.place(relx=0.05, rely=0.4057, relwidth=0.40, relheight=0.075)
        self.descrição.place(relx=0.05, rely=0.5292, relwidth=0.40, relheight=0.075)
        self.dataConsulta.place(relx=0.05, rely=0.6528, relwidth=0.40, relheight=0.075)
        self.Horario.place(relx=0.05, rely=0.7764, relwidth=0.40, relheight=0.075)
        ######## geometry  botões ########
        self.save.place(relx=0.05, rely=0.8875, relwidth=0.25, relheight=0.1)
        self.vizualizacao.place(relx=0.375, rely=0.8875,relwidth=0.25, relheight=0.1)
        self.voltar.place(relx=0.7, rely=0.8875, relwidth=0.25, relheight=0.1)

        ######## geometry entry ########
        self.entryIdMedico.place(
            relx=0.5, rely=0.1585, relwidth=0.40, relheight=0.075)
        self.entryIdPaciente.place(
            relx=0.5, rely=0.2821, relwidth=0.40, relheight=0.075)
        self.entryValorConsulta.place(
            relx=0.5, rely=0.4057, relwidth=0.40, relheight=0.075)
        self.entryDescrição.place(
            relx=0.5, rely=0.5292, relwidth=0.40, relheight=0.075)
        self.sbxDiaConsulta.place(
            relx=0.52, rely=0.6528, relwidth=0.13, relheight=0.075)
        self.sbxMesConsulta.place(
            relx=0.663, rely=0.6528, relwidth=0.133, relheight=0.075)
        self.sbxAnoConsulta.place(
            relx=0.8063, rely=0.6528, relwidth=0.13, relheight=0.075)
        self.sbxHora.place(relx=0.59, rely=0.7764,
                           relwidth=0.13, relheight=0.075)
        self.sbxMinuto.place(relx=0.74, rely=0.7764,
                             relwidth=0.133, relheight=0.075)
        ######## focus ########
        self.entryNomeMedico.focus_force()
        self.frameConsulta.protocol(
            "WM_DELETE_WINDOW", lambda: self.mudarJanela(self.app, self.frameConsulta))

    # função para validar se fico faltando digitar algum campo da consulta
    def validarFormsConsulta(self, idDoutor, idPaciente, valConsulta, dia, mes, ano, hora, minuto, desc):
        if (idDoutor == "" or idPaciente == "" or valConsulta == ""
                or dia == "" or mes == "" or ano == "" or hora == "" or minuto == ""):
            self.app.msgbox = messagebox.showerror(
                title="Error", message="Por favor preencha todos os campos!")
        else:
            """""
            #Formatando a data
            dtNascimento = dia+"/"+mes+"/"+ano
            #adicionando ao demais dados guardados
            #adptar para salvar na tabela do banco
            paciente = {"nome": nome, "horario": horario}
            self.data.append(data)"""
            dtConsulta = ano+"-"+mes+"-"+dia
            horaConsulta = hora+":"+minuto
            check, message = BDHandler.agendar_consulta(idPaciente, idDoutor, dtConsulta, horaConsulta, desc, valConsulta)
            if check:
                self.app.msgbox = messagebox.showinfo(title="Result", message= message)
                self.mudarJanela(self.app, self.frameConsulta)
            else:
                self.app.msgbox = messagebox.showerror(title="Error", message= message)
                self.mudarJanela(self.app, self.frameConsulta)

    # função de deletar, no banco de dados e visualmente, as informações de uma consulta cancelada
    def deletar_consultas(self, table):
        selected_item = table.selection()
        if selected_item:
            item = table.item(selected_item)
            id_item = item['values'][0]  # Pegando o ID ou outra chave primária
            checkOpc = messagebox.askokcancel("Comfirmação", "Deseja deletar o item selecionado?")
            deleter, msg = BDDataRemovers.removedor_consultas(id_item, checkOpc)
            if deleter:
                messagebox.showinfo(title="Sucesso", message=msg)
            else:
                messagebox.showinfo(title="Error", message=msg)
                
        table.delete(selected_item)

    # função da janela de inserção de dados do funcionario 
    def janelaFuncionario(self):
        self.frameFuncionario = tk.Toplevel(self.app)
        self.frameFuncionario.grab_set()  # Impede interação com a janela principal
        self.frameFuncionario.title("CADASTRAR FUNCIONARIO")
        self.frameFuncionario["bg"] = "#26a599"
        self.frameFuncionario.maxsize(width=self.frameFuncionario.winfo_screenwidth(),
                                      height=self.frameFuncionario.winfo_screenheight())
        self.frameFuncionario.minsize(width=700, height=600)
        self.frameFuncionario.resizable(False, False)
        # centralizando a janela
        # dimensões
        largura = 700
        altura = 600
        # resolução
        largura_screen = self.frameFuncionario.winfo_screenwidth()
        altura_screen = self.frameFuncionario.winfo_screenheight()
        # posição
        posx = largura_screen/2 - largura/2
        posy = altura_screen/2 - altura/2
        # geometry
        self.frameFuncionario.geometry(
            '%dx%d+%d+%d' % (largura, altura, posx, posy))

        # explicação pagina
        # label CADASTRAR PACIENTE
        self.quadrado = tk.Label(self.frameFuncionario, text="CADASTRO DE MEDICO", bg="#22958a", fg='#e1fada',
                                 font=('Comic Sans MS', 18, "bold"), anchor="center")

        # NOME
        # Label NOME Medico
        self.nomeMedico = tk.Label(self.frameFuncionario, text="NOME DOUTOR", bg='#26a599',
                                   fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry NOME
        self.entryNomeMedico = tk.Entry(self.frameFuncionario, fg='white', bg='#22958a',
                                        font=('Comic Sans MS', 14, "bold"))

        # email
        # Label email
        self.emailMed = tk.Label(self.frameFuncionario, text=f"EMAIL", bg='#26a599',
                                 fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry email
        self.entryEmailMed = tk.Entry(self.frameFuncionario,
                                      fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # telefone
        # Label telefone
        self.telefoneMed = tk.Label(self.frameFuncionario, text="TELEFONE", bg='#26a599',
                                    fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry telefone
        self.entryTelefoneMed = tk.Entry(self.frameFuncionario,
                                         fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # CRM
        # Label crm
        self.crm = tk.Label(self.frameFuncionario, text="CRM", bg='#26a599',
                            fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry crm
        self.entryCrm = tk.Entry(self.frameFuncionario,
                                 fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # DATA DE NASCISMENTO
        # Label Data de nascimento
        self.dNascimentoMed = tk.Label(self.frameFuncionario, text="NASCIMENTO (DD/MM/AAAA)", bg='#26a599',
                                       fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry Data de nascimento
        self.sbxDiaMed = tk.Spinbox(self.frameFuncionario, fg='white', bg='#22958a',
                                    font=('Comic Sans MS', 20, "bold"), from_=1, to=31)
        self.sbxMesMed = tk.Spinbox(self.frameFuncionario, fg='white', bg='#22958a',
                                    font=('Comic Sans MS', 20, "bold"), from_=1, to=12)
        self.sbxAnoMed = tk.Spinbox(self.frameFuncionario, fg='white', bg='#22958a',
                                    font=('Comic Sans MS', 20, "bold"), from_=1940, to=2024)

        # CPF
        # Label cpf
        self.cpfMed = tk.Label(self.frameFuncionario, text="Cpf", bg='#26a599',
                               fg='white', anchor='center', font=('Comic Sans MS', 16, "bold"))
        # Entry cpf
        self.entryCpfMed = tk.Entry(self.frameFuncionario,
                                    fg='white', bg='#22958a', font=('Comic Sans MS', 14, "bold"))

        # BOTÃO VOLTAR
        # Imagem voltar
        btnVoltar = tk.PhotoImage(file="icons/home.png", master=self.app)
        btnVoltar = btnVoltar.subsample(2, 2)
        img2 = tk.Label(self.app, image=btnVoltar)
        img2.image = btnVoltar
        # atribuindo comando
        self.voltar = tk.Button(self.frameFuncionario, image=btnVoltar, bg='#26a599', fg='white', bd=0,
                                command=lambda: self.mudarJanela(self.app, self.frameFuncionario))

        # BOTÃO vizualização
        # Imagem Vizualização
        btnVizu = tk.PhotoImage(file="icons/vizualização.png", master=self.app)
        btnVizu = btnVizu.subsample(2, 2)
        img = tk.Label(self.app, image=btnVizu)
        img.image = btnVizu
        # atribuindo comando
        self.vizualizacao = tk.Button(self.frameFuncionario, image=btnVizu, bg='#26a599', fg='white', bd=0,
                                      command=lambda: self.mudarJanela(self.frameVisFuncionario(), self.frameFuncionario))

        # BOTÃO salvar
        # Imagem salvar
        btnsalvar = tk.PhotoImage(file="icons/save.png", master=self.app)
        btnsalvar = btnsalvar.subsample(2, 2)
        img1 = tk.Label(self.app, image=btnsalvar)
        img1.image = btnsalvar
        # atribuindo comando
        self.save = tk.Button(self.frameFuncionario, image=btnsalvar, bg='#26a599', fg='white', bd=0,
                              command=lambda: self.validarFormsFuncionario(self.entryNomeMedico.get(), self.entryEmailMed.get(), self.entryTelefoneMed.get(),
                                                                           self.entryCrm.get(), self.sbxDiaMed.get(), self.sbxMesMed.get(),
                                                                           self.sbxAnoMed.get(), self.entryCpfMed.get()))

        ### mudando a cor do botão ao passar cursor###
        self.voltar.bind("<Enter>", lambda e,
                         b=self.voltar: self.on_enter(e, b))
        self.voltar.bind("<Leave>", lambda e,
                         b=self.voltar: self.on_leave(e, b))
        self.vizualizacao.bind("<Enter>", lambda e1,
                               b1=self.vizualizacao: self.on_enter(e1, b1))
        self.vizualizacao.bind("<Leave>", lambda e1,
                               b1=self.vizualizacao: self.on_leave(e1, b1))
        self.save.bind("<Enter>", lambda e2,
                       b2=self.save: self.on_enter(e2, b2))
        self.save.bind("<Leave>", lambda e2,
                       b2=self.save: self.on_leave(e2, b2))

        ####### DESENHANDO OS COMPONENTES NA TELA ############
        ######## geometry tk.Labels ########
        self.quadrado.place(relx=0.005, rely=0.01, relwidth=0.989, relheight=0.1)
        self.nomeMedico.place(relx=0.05, rely=0.15857, relwidth=0.40, relheight=0.075)
        self.emailMed.place(relx=0.05, rely=0.28214, relwidth=0.40, relheight=0.075)
        self.telefoneMed.place(relx=0.05, rely=0.4057, relwidth=0.40, relheight=0.075)
        self.crm.place(relx=0.05, rely=0.5292, relwidth=0.40, relheight=0.075)
        self.dNascimentoMed.place(relx=0.03, rely=0.65285, relwidth=0.5, relheight=0.075)
        self.cpfMed.place(relx=0.05, rely=0.7764, relwidth=0.4, relheight=0.075)

        ######## geometry  botões ########
        self.save.place(relx=0.05, rely=0.8875, relwidth=0.25, relheight=0.1)
        self.vizualizacao.place(relx=0.375, rely=0.8875, relwidth=0.25, relheight=0.1)
        self.voltar.place(relx=0.7, rely=0.8875, relwidth=0.25, relheight=0.1)

        ######## geometry entry ########
        self.entryNomeMedico.place(relx=0.5, rely=0.15857, relwidth=0.40, relheight=0.075)
        self.entryEmailMed.place(relx=0.5, rely=0.28214, relwidth=0.40, relheight=0.075)
        self.entryTelefoneMed.place(relx=0.5, rely=0.4057, relwidth=0.40, relheight=0.075)
        self.entryCrm.place(relx=0.5, rely=0.5292, relwidth=0.40, relheight=0.075)
        self.sbxDiaMed.place(relx=0.52, rely=0.65285, relwidth=0.13, relheight=0.075)
        self.sbxMesMed.place(relx=0.663, rely=0.65285, relwidth=0.133, relheight=0.075)
        self.sbxAnoMed.place(relx=0.8063, rely=0.65285, relwidth=0.13, relheight=0.075)
        self.entryCpfMed.place(relx=0.5, rely=0.7764, relwidth=0.40, relheight=0.075)
        ######## focus ########
        self.entryNomeMedico.focus_force()
        self.frameFuncionario.protocol(
            "WM_DELETE_WINDOW", lambda: self.mudarJanela(self.app, self.frameFuncionario))

    # função para validar se falta digitar um campo do funcionario
    def validarFormsFuncionario(self, nomeDoutor, email, telefone, crm, dia, mes, ano, cpf):
        if (nomeDoutor == "" or email == "" or telefone == ""
                or crm == "" or dia == "" or mes == "" or ano == "" or cpf == ""):
            self.app.msgbox = messagebox.showerror(
                title="Error", message="Por favor preencha todos os campos!")
        else:
            """""
            #Formatando a data
            dtNascimento = dia+"/"+mes+"/"+ano
            #adicionando ao demais dados guardados
            #adptar para salvar na tabela do banco
            paciente = {"nome": nome, "horario": horario}
            self.data.append(data)"""
            dtNascimento = ano+"-"+mes+"-"+dia
            check, message = BDHandler.adicionar_medico(nomeDoutor, email, telefone, crm, dtNascimento, cpf)
            if check:
                self.app.msgbox = messagebox.showinfo(title="Result", message= message)
                self.mudarJanela(self.app, self.frameFuncionario)
            else:
                self.app.msgbox = messagebox.showerror(title="Deu ruim", message= message)
                self.mudarJanela(self.app, self.frameFuncionario)

    # função de deletar, no banco de dados e visualmente, as informações de uma consulta cancelada
    def deletar_funcionarios(self, table):
        selected_item = table.selection()
        if selected_item:
            item = table.item(selected_item)
            id_item = item['values'][0]  # Pegando o ID ou outra chave primária
            checkOpc = messagebox.askokcancel("Comfirmação", "Deseja deletar o item selecionado?")
            deleter, msg = BDDataRemovers.removedor_medicos(id_item, checkOpc)
            if deleter:
                messagebox.showinfo(title="Sucesso", message=msg)
            else:
                messagebox.showinfo(title="Error", message=msg)
                
        table.delete(selected_item)

if __name__ == "__main__":
    app = Application(tk.Tk())
