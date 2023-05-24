# Importamos as bibliotecas necessárias do Kivy.
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout

# Criamos uma classe para o jogo, que herda de App.
class Jogo_da_Idosa(App):
    # A função 'build' é onde criamos a interface do usuário.
    def build(self):
        # Definimos algumas variáveis para o jogo.
        self.title = 'Jogo da Velha'  # título do aplicativo
        self.grid = GridLayout(cols=3, spacing=10, padding=10)  # grade para o jogo da velha
        self.botoes = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # armazenar os botões para cada posição do jogo
        self.jogador = 'X'  # jogador atual, começa com 'X'
        self.game_over = False  # controle se o jogo acabou
        self.movimentos = 0  # conta o número de movimentos
        self.placar_x = 0  # placar do jogador X
        self.placar_o = 0  # placar do jogador O

        # Criação dos botões do tabuleiro
        for row in range(3):
            for col in range(3):
                button = Button(font_size=40)
                button.bind(on_press=self.click_botao)  # vincula o evento de pressionar o botão à função 'click_botao'
                button.background_color = (0.6, 0.8, 0.8, 1)  # cor do botão
                self.grid.add_widget(button)  # adiciona o botão à grade
                self.botoes[row][col] = button  # armazena o botão na matriz de botões

        # Definição do botão reset
        botao_reset = Button(text='Reset', size_hint=(0.25, 0.3), font_size=25, color=(0, 0, 0, 1))
        botao_reset.bind(on_press=self.reset_game)  # vincula o evento de pressionar o botão à função 'reset_game'

        # Criação do placar para os jogadores X e O.
        placar_x = Label(text='Jogador X: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))
        placar_o = Label(text='Jogador O: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))

        # Adicionando os placares ao layout
        layout_placar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        layout_placar.add_widget(placar_x)
        layout_placar.add_widget(placar_o)

        # Organizando os layouts
        layout_jogo = BoxLayout(orientation='vertical')
        layout_jogo.add_widget(self.grid)

        # Adicionando o botão de reset
        layout_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.25))
        layout_anchor.add_widget(botao_reset)

        layout_jogo.add_widget(layout_placar)
        layout_jogo.add_widget(layout_anchor)

        # Definindo a cor de fundo do layout do jogo.
        with layout_jogo.canvas.before:
            Color(0.6, 0.8, 0.8, 1)
            self.rect = Rectangle(pos=layout_jogo.pos, size=layout_jogo.size)

        layout_jogo.bind(pos=self.atualiza_retangulo, size=self.atualiza_retangulo)

        # Armazenando as referências aos labels dos placares
        self.label_x = placar_x
        self.label_o = placar_o

        # Criação do popup inicial para escolher o jogador inicial.
        self.popup_inicial = self.popup_escolha_x_o()
        
        # Retornando o layout do jogo completo
        return layout_jogo

    # Criação do popup que será usado para o jogador escolher quem começa jogando.
    def popup_escolha_x_o(self):
        box = BoxLayout(orientation='vertical')
        botoes = BoxLayout(orientation='horizontal')
        popup = Popup(title='Escolha o jogador inicial', content=box, size_hint=(0.5, 0.5))

        # Criação dos botões para a escolha do jogador inicial.
        botao_x = Button(text='X')
        botao_x.bind(on_press=lambda x: self.set_jogador_inicial('X', popup))  # A função set_jogador_inicial é chamada quando o botão é pressionado.
        botoes.add_widget(botao_x)

        botao_o = Button(text='O')
        botao_o.bind(on_press=lambda x: self.set_jogador_inicial('O', popup))  # A função set_jogador_inicial é chamada quando o botão é pressionado.
        botoes.add_widget(botao_o)

        box.add_widget(Label(text='Quem começa jogando?'))
        box.add_widget(botoes)

        return popup

    # Define o jogador inicial e fecha o popup.
    def set_jogador_inicial(self, jogador, popup):
        self.jogador = jogador
        popup.dismiss()

    # Inicia o jogo, abrindo o popup para escolha do jogador inicial.
    def start_jogo(self):
        self.popup_inicial.open()

    # Atualiza a posição e tamanho do retângulo de fundo quando a janela é redimensionada.
    def atualiza_retangulo(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # Ação ao clicar no botão do jogo.
    def click_botao(self, button):
        # Apenas processa o clique se o botão estiver vazio e o jogo não tiver acabado.
        if button.text == '' and not self.game_over:
            button.text = self.jogador  # Define o texto do botão para o jogador atual.
            row, col = self.encontra_posicao_botao(button)  # Encontra a posição do botão na grade.
            self.botoes[row][col] = button  # Atualiza o botão na matriz de botões.
            self.movimentos += 1  # Incrementa o contador de movimentos.
            self.verificar_ganhador()  # Verifica se o jogador atual ganhou.
            self.quem_comeca()  # Alterna para o outro jogador.
            self.atualiza_cor_botao(button)  # Atualiza a cor do botão.

    # Encontra a posição de um botão na grade.
    def encontra_posicao_botao(self, button):
        for row in range(3):
            for col in range(3):
                if self.botoes[row][col] == button:
                    return row, col

    # Alterna para o outro jogador.
    def quem_comeca(self):
        if self.jogador == 'X':
            self.jogador = 'O'
        else:
            self.jogador = 'X'

    # Verifica se algum jogador ganhou.
    def verificar_ganhador(self):
        # Verifica cada linha, coluna e diagonal.
        for row in range(3):
            if self.botoes[row][0].text == self.botoes[row][1].text == self.botoes[row][2].text != '':
                self.declarar_ganhador(self.botoes[row][0].text)

        for col in range(3):
            if self.botoes[0][col].text == self.botoes[1][col].text == self.botoes[2][col].text != '':
                self.declarar_ganhador(self.botoes[0][col].text)

        if self.botoes[0][0].text == self.botoes[1][1].text == self.botoes[2][2].text != '':
            self.declarar_ganhador(self.botoes[0][0].text)
        elif self.botoes[0][2].text == self.botoes[1][1].text == self.botoes[2][0].text != '':
            self.declarar_ganhador(self.botoes[0][2].text)

        # Se todos os espaços estiverem preenchidos e ninguém ganhou, declara um empate.
        if self.movimentos == 9 and not self.game_over:
            self.empate()

    # Declara o vencedor e atualiza o placar.
    def declarar_ganhador(self, ganhador):
        self.game_over = True  # O jogo acabou.
        self.title = f'{ganhador} venceu!'  # Atualiza o título da janela.
        self.desabilitar_botoes()  # Desabilita todos os botões.

        # Atualiza o placar do vencedor.
        if ganhador == 'X':
            self.placar_x += 1
        elif ganhador == 'O':
            self.placar_o += 1

        # Atualiza os labels dos placares.
        self.label_x.text = f'Jogador X: {self.placar_x}'
        self.label_o.text = f'Jogador O: {self.placar_o}'

    # Declara um empate.
    def empate(self):
        self.game_over = True  # O jogo acabou.
        self.title = 'Empate!'  # Atualiza o título da janela.
        self.desabilitar_botoes()  # Desabilita todos os botões.

    # Desabilita todos os botões.
    def desabilitar_botoes(self):
        for row in range(3):
            for col in range(3):
                self.botoes[row][col].disabled = True

    # Reseta o jogo para o estado inicial.
    def reset_game(self, instance):
        self.game_over = False  # O jogo não acabou.
        self.movimentos = 0  # Reseta o contador de movimentos.
        self.title = 'Jogo da Velha'  # Reseta o título da janela.

        # Limpa todos os botões e os habilita.
        for row in range(3):
            for col in range(3):
                self.botoes[row][col].text = ''
                self.botoes[row][col].disabled = False
                self.atualiza_cor_botao(self.botoes[row][col])

        # Reabre o popup para escolha do jogador inicial.
        self.popup_inicial.open()

    # Atualiza a cor de um botão.
    def atualiza_cor_botao(self, button):
        if button.text == 'X':
            button.background_color = (0, 0, 1, 1)  # Azul se o botão está com 'X'.
        elif button.text == 'O':
            button.background_color = (1, 0, 0, 1)  # Vermelho se o botão está com 'O'.
        else:
            button.background_color = (1, 1, 1, 1)  # Branco se o botão está vazio.

# Criação da aplicação.
if __name__ == '__main__':
    Jogo_da_Idosa().run()
