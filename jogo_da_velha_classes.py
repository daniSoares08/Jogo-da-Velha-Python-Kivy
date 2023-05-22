from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout


class JogoDaVelhaApp(App):
    def build(self):
        self.title = 'Jogo da Velha'
        self.tabuleiro = Tabuleiro()
        self.jogador = Jogador('X')
        self.game_over = False
        self.movimentos = 0

        layout_jogo = BoxLayout(orientation='vertical')

        self.grid = GridLayout(cols=3, spacing=10, padding=10)
        self.botoes = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Representa o tabuleiro

        for row in range(3):
            for col in range(3):
                button = Button(font_size=40)
                button.bind(on_press=self.click_botao)
                button.background_color = (0.6, 0.8, 0.8, 1)
                self.grid.add_widget(button)
                self.botoes[row][col] = button

        layout_jogo.add_widget(self.grid)

        botao_reset = Button(text='Reset', size_hint=(0.25, 0.3), font_size=25, color=(0, 0, 0, 1))
        botao_reset.bind(on_press=self.reset_game)
        
        placar_x = Label(text='Jogador X: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))
        placar_o = Label(text='Jogador O: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))

        layout_placar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        layout_placar.add_widget(placar_x)
        layout_placar.add_widget(placar_o)
        layout_jogo.add_widget(layout_placar)

        layout_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.25))
        layout_anchor.add_widget(botao_reset)
        layout_jogo.add_widget(layout_anchor)

        with layout_jogo.canvas.before:
            Color(0.6, 0.8, 0.8, 1)  # Define a cor de fundo do layout
            self.rect = Rectangle(pos=layout_jogo.pos, size=layout_jogo.size)

        layout_jogo.bind(pos=self.atualiza_retangulo, size=self.atualiza_retangulo)

        self.label_x = placar_x
        self.label_o = placar_o

        self.popup_inicial = self.popup_escolha_x_o()

        return layout_jogo

    def popup_escolha_x_o(self):
        box = BoxLayout(orientation='vertical')
        botoes = BoxLayout(orientation='horizontal')
        popup = Popup(title='Escolha o jogador inicial', content=box, size_hint=(0.5, 0.5))

        botao_x = Button(text='X')
        botao_x.bind(on_press=lambda x: self.set_jogador_inicial('X', popup))
        botoes.add_widget(botao_x)

        botao_o = Button(text='O')
        botao_o.bind(on_press=lambda x: self.set_jogador_inicial('O', popup))
        botoes.add_widget(botao_o)

        box.add_widget(Label(text='Quem começa jogando?'))
        box.add_widget(botoes)

        return popup

    def set_jogador_inicial(self, jogador, popup):
        if self.jogador is None:
            self.jogador = Jogador(jogador)
        else:
            self.jogador.identificador = jogador
        popup.dismiss()

    def on_start(self):
        self.popup_inicial.open()

    def atualiza_retangulo(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def click_botao(self, button):
        if button.text == '' and not self.game_over:
            button.text = self.jogador.identificador
            row, col = self.encontra_posicao_botao(button)
            self.tabuleiro.marcar_posicao(row, col, self.jogador.identificador)
            self.movimentos += 1
            self.verificar_ganhador()
            self.quem_comeca()
            self.atualiza_cor_botao(button)  # Atualiza o estilo do botão após cada jogada

    def encontra_posicao_botao(self, button):
        for row in range(3):
            for col in range(3):
                if self.botoes[row][col] == button:
                    return row, col

    def quem_comeca(self):
        self.jogador.trocar_jogador()

    def verificar_ganhador(self):
        if self.tabuleiro.verificar_vitoria(self.jogador.identificador):
            self.declarar_ganhador(self.jogador.identificador)
        elif self.movimentos == 9 and not self.game_over:
            self.empate()

    def declarar_ganhador(self, winner):
        self.game_over = True
        self.title = f'{winner} venceu!'
        self.desabilitar_botoes()

        if winner == 'X':
            self.jogador.incrementar_placar()
        elif winner == 'O':
            self.jogador.incrementar_placar()

        self.label_x.text = f'Jogador X: {self.jogador.placar_x}'
        self.label_o.text = f'Jogador O: {self.jogador.placar_o}'

    def empate(self):
        self.game_over = True
        self.title = 'Empate!'
        self.desabilitar_botoes()

    def desabilitar_botoes(self):
        for row in range(3):
            for col in range(3):
                self.botoes[row][col].disabled = True

    def reset_game(self, instance):
        self.game_over = False
        self.movimentos = 0
        self.title = 'Jogo da Velha'

        self.tabuleiro.resetar()
        for row in range(3):
            for col in range(3):
                self.botoes[row][col].text = ''
                self.botoes[row][col].disabled = False
                self.atualiza_cor_botao(self.botoes[row][col])  # Atualiza o estilo de cada botão
        self.popup_inicial.open()

    def atualiza_cor_botao(self, button):
        if button.text == 'X':
            button.background_color = (0, 0, 1, 1)
        elif button.text == 'O':
            button.background_color = (0, 1, 0, 1)
        else:
            button.background_color = (1, 1, 1, 1)

    def on_stop(self):
        self.reset_game(None)

    def on_pause(self):
        return True

    def on_resume(self):
        self.reset_game(None)


class Tabuleiro:
    def __init__(self):
        self.grid = [['', '', ''], ['', '', ''], ['', '', '']]

    def marcar_posicao(self, row, col, identificador):
        self.grid[row][col] = identificador

    def verificar_vitoria(self, identificador):
        for row in range(3):
            # Verificar linhas
            if self.grid[row][0] == self.grid[row][1] == self.grid[row][2] == identificador != '':
                return True

        for col in range(3):
            # Verificar colunas
            if self.grid[0][col] == self.grid[1][col] == self.grid[2][col] == identificador != '':
                return True

        # Verificar diagonais
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == identificador != '':
            return True
        elif self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == identificador != '':
            return True

        return False

    def resetar(self):
        self.grid = [['', '', ''], ['', '', ''], ['', '', '']]


class Jogador:
    def __init__(self, identificador):
        self.identificador = identificador
        self.placar_x = 0
        self.placar_o = 0

    def trocar_jogador(self):
        if self.identificador == 'X':
            self.identificador = 'O'
        else:
            self.identificador = 'X'

    def incrementar_placar(self):
        if self.identificador == 'X':
            self.placar_x += 1
        elif self.identificador == 'O':
            self.placar_o += 1


if __name__ == '__main__':
    JogoDaVelhaApp().run()
