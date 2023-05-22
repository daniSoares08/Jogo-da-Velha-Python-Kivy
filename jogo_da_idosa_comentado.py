# Importando classes necessárias do módulo Kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout

# Definição da classe principal do jogo
class Jogo_da_Idosa(App):
    def build(self):
        # Configuração inicial do jogo
        self.title = 'Jogo da Velha'  # Título da janela do jogo
        self.grid = GridLayout(cols=3, spacing=10, padding=10)  # Grade onde os botões serão colocados
        self.botoes = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Representação do tabuleiro do jogo
        self.jogador = 'X'  # Define o jogador padrão como 'X'
        self.game_over = False  # Inicializa a variável que verifica se o jogo acabou
        self.movimentos = 0  # Contador de movimentos
        self.placar_x = 0  # Contagem de vitórias do jogador 'X'
        self.placar_o = 0  # Contagem de vitórias do jogador 'O'

        # Cria os botões na grade
        for row in range(3):
            for col in range(3):
                button = Button(font_size=40)
                button.bind(on_press=self.click_botao)  # Vincula o evento de pressionar o botão ao método on_button_click
                button.background_color = (0.6, 0.8, 0.8, 1)  # Define a cor de fundo do botão
                self.grid.add_widget(button)  # Adiciona o botão à grade
                self.botoes[row][col] = button  # Adiciona o botão à matriz que representa o tabuleiro

        # Cria o botão de reset
        botao_reset = Button(text='Reset', size_hint=(0.25, 0.3), font_size=25, color=(0, 0, 0, 1))
        botao_reset.bind(on_press=self.reset_jogo)  # Vincula o evento de pressionar o botão ao método reset_game

        # Cria os labels do placar
        placar_x = Label(text='Jogador X: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))
        placar_o = Label(text='Jogador O: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))

        # Cria o layout do placar
        layout_placar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        layout_placar.add_widget(placar_x)
        layout_placar.add_widget(placar_o)

        # Cria o layout do jogo
        layout_jogo = BoxLayout(orientation='vertical')
        layout_jogo.add_widget(self.grid)

        # Cria um layout centralizado para o botão de reset
        layout_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.25))
        layout_anchor.add_widget(botao_reset)

        # Adiciona o layout do placar e do botão de reset ao layout do jogo
        layout_jogo.add_widget(layout_placar)
        layout_jogo.add_widget(layout_anchor)

        # Configura a cor de fundo do layout do jogo
        with layout_jogo.canvas.before:
            Color(0.6, 0.8, 0.8, 1)  # Define a cor de fundo do layout
            self.rect = Rectangle(pos=layout_jogo.pos, size=layout_jogo.size)  # Define a posição e o tamanho do retângulo de fundo

        # Vincula os eventos de atualização de posição e tamanho ao método update_rect
        layout_jogo.bind(pos=self.atualiza_retangulo, size=self.atualiza_retangulo)

        # Guarda as referências para os labels do placar
        self.label_x = placar_x
        self.label_o = placar_o

        # Cria o popup de escolha do jogador inicial
        self.popup_inicial = self.popup_escolha_x_o()

        # Retorna o layout principal da aplicação
        return layout_jogo

    def popup_escolha_x_o(self):
        # Criação do pop-up para escolha do jogador inicial
        box = BoxLayout(orientation='vertical')  # Layout principal do pop-up
        botoes = BoxLayout(orientation='horizontal')  # Layout para os botões
        popup = Popup(title='Escolha o jogador inicial', content=box, size_hint=(0.5, 0.5))  # Cria o pop-up

        # Cria os botões de escolha do jogador inicial
        botao_x = Button(text='X')
        botao_x.bind(on_press=lambda x: self.set_jogador_inicial('X', popup))  # Vincula o evento de pressionar o botão ao método set_jogador_inicial
        botoes.add_widget(botao_x)

        botao_o = Button(text='O')
        botao_o.bind(on_press=lambda x: self.set_jogador_inicial('O', popup))  # Vincula o evento de pressionar o botão ao método set_jogador_inicial
        botoes.add_widget(botao_o)

        # Adiciona os widgets ao layout principal do pop-up
        box.add_widget(Label(text='Quem começa jogando?'))  # Adiciona a pergunta
        box.add_widget(botoes)  # Adiciona os botões

        # Retorna o pop-up
        return popup

    def set_jogador_inicial(self, jogador, popup):
        # Define o jogador inicial
        self.jogador = jogador
        popup.dismiss()  # Fecha o pop-up

    def on_start(self):
        # Executa o método ao iniciar o aplicativo
        self.popup_inicial.open()  # Abre o pop-up de escolha do jogador inicial

    def atualiza_retangulo(self, instance, value):
        # Atualiza a posição e o tamanho do retângulo de fundo
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def click_botao(self, button):
        # Executa o método quando um botão é pressionado
        if button.text == '' and not self.game_over:  # Verifica se o botão está vazio e o jogo não acabou
            button.text = self.jogador  # Define o texto do botão para o jogador atual
            row, col = self.encontra_posicao_botao(button)  # Obtém a posição do botão pressionado
            self.botoes[row][col] = button  # Atualiza o botão no tabuleiro
            self.movimentos += 1  # Incrementa a quantidade de movimentos
            self.verificar_ganhador()  # Verifica se há um vencedor
            self.quem_comeca()  # Alterna o jogador
            self.atualizar_cor_botao(button)  # Atualiza o estilo do botão após cada jogada

    def encontra_posicao_botao(self, button):
        # Encontra a posição de um botão no tabuleiro
        for row in range(3):
            for col in range(3):
                if self.botoes[row][col] == button:
                    return row, col  # Retorna a posição do botão

    def quem_comeca(self):
        # Alterna o jogador
        if self.jogador == 'X':
            self.jogador = 'O'
        else:
            self.jogador = 'X'

    def verificar_ganhador(self):
        # Verifica se há um vencedor
        for row in range(3):
            # Verificar linhas
            if self.botoes[row][0].text == self.botoes[row][1].text == self.botoes[row][2].text != '':
                self.declarar_ganhador(self.botoes[row][0].text)

        for col in range(3):
            # Verificar colunas
            if self.botoes[0][col].text == self.botoes[1][col].text == self.botoes[2][col].text != '':
                self.declarar_ganhador(self.botoes[0][col].text)

        # Verificar diagonais
        if self.botoes[0][0].text == self.botoes[1][1].text == self.botoes[2][2].text != '':
            self.declarar_ganhador(self.botoes[0][0].text)
        elif self.botoes[0][2].text == self.botoes[1][1].text == self.botoes[2][0].text != '':
            self.declarar_ganhador(self.botoes[0][2].text)

        # Verificar empate
        if self.movimentos == 9 and not self.game_over:
            self.empate()

    def declarar_ganhador(self, winner):
        # Declara um vencedor
        self.game_over = True  # Define que o jogo acabou
        self.title = f'{winner} venceu!'  # Atualiza o título da janela
        self.desabilitar_botoes()  # Desabilita os botões

        if winner == 'X':
            self.placar_x += 1  # Incrementa a contagem de vitórias para o jogador X
        elif winner == 'O':
            self.placar_o += 1  # Incrementa a contagem de vitórias para o jogador O

        self.label_x.text = f'Jogador X: {self.placar_x}'  # Atualiza o placar do jogador X
        self.label_o.text = f'Jogador O: {self.placar_o}'  # Atualiza o placar do jogador O

    def empate(self):
        # Declara um empate
        self.game_over = True  # Define que o jogo acabou
        self.title = 'Empate!'  # Atualiza o título da janela
        self.desabilitar_botoes()  # Desabilita os botões

    def desabilitar_botoes(self):
        # Desabilita os botões
        for row in range(3):
            for col in range(3):
                self.botoes[row][col].disabled = True

    def reset_jogo(self, instance):
        # Reseta o jogo
        for row in range(3):
            for col in range(3):
                self.botoes[row][col].text = ''  # Limpa o texto dos botões
                self.botoes[row][col].disabled = False  # Habilita os botões
                self.botoes[row][col].background_color = (0.6, 0.8, 0.8, 1)  # Restaura a cor de fundo padrão dos botões
        self.movimentos = 0  # Zera o contador de movimentos
        self.game_over = False  # Define que o jogo não acabou
        self.title = 'Jogo da Velha'  # Restaura o título da janela
        self.popup_inicial.open()  # Reabre o pop-up de escolha do jogador inicial

    def atualizar_cor_botao(self, button):
        # Atualiza o estilo do botão após cada jogada
        if button.text == 'X':
            button.background_color = (0.6, 0.8, 0.8, 1)  # Define a cor de fundo para o jogador X
        elif button.text == 'O':
            button.background_color = (0.8, 0.6, 0.8, 1)  # Define a cor de fundo para o jogador O

# Inicia a aplicação
if __name__ == '__main__':
    Jogo_da_Idosa().run()