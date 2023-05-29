from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.audio import SoundLoader

class JogoDaVelha(App):
    def build(self):
        self.title = 'Jogo da Velha'
        self.grid = GridLayout(cols=3, spacing=10, padding=10)
        self.botoes = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.jogador = 'X'
        self.game_over = False
        self.movimentos = 0
        self.placar_x = 0
        self.placar_o = 0

        self.background_music = SoundLoader.load("C:/Users/campo/Documents/Projetos Python/CSBA/Jogo da velha\MusicaDeElevador.ogg")
        self.victory_sound = SoundLoader.load("C:/Users/campo/Documents/Projetos Python/CSBA/Jogo da velha/VITORIA.ogg")

        if self.background_music:
            self.background_music.loop = True  # Make the music loop
            self.background_music.play()

        for row in range(3):
            for col in range(3):
                button = Button(font_size=40)
                button.bind(on_press=self.click_botao)
                button.background_color = (0.6, 0.8, 0.8, 1)
                self.grid.add_widget(button)
                self.botoes[row][col] = button

        botao_reset = Button(text='Reset', size_hint=(0.25, 0.3), font_size=25, color=(0, 0, 0, 1))
        botao_reset.bind(on_press=self.reset_game)

        placar_x = Label(text='Jogador X: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))
        placar_o = Label(text='Jogador O: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))

        layout_placar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        layout_placar.add_widget(placar_x)
        layout_placar.add_widget(placar_o)

        layout_jogo = BoxLayout(orientation='vertical')
        layout_jogo.add_widget(self.grid)

        layout_anchor = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.25))
        layout_anchor.add_widget(botao_reset)

        layout_jogo.add_widget(layout_placar)
        layout_jogo.add_widget(layout_anchor)

        with layout_jogo.canvas.before:
            Color(0.6, 0.8, 0.8, 1)
            self.rect = Rectangle(pos=layout_jogo.pos, size=layout_jogo.size)

        layout_jogo.bind(pos=self.atualiza_retangulo, size=self.atualiza_retangulo)

        self.label_x = placar_x
        self.label_o = placar_o

        self.popup_inicial = self.popup_escolha_x_o()
        
        return layout_jogo

    def on_start(self):
        self.start_jogo()

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
        self.jogador = jogador
        popup.dismiss()

    def start_jogo(self):
        self.popup_inicial.open()

    def atualiza_retangulo(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def click_botao(self, button):
        if button.text == '' and not self.game_over:
            button.text = self.jogador
            row, col = self.encontra_posicao_botao(button)
            self.botoes[row][col] = button
            self.movimentos += 1
            self.verificar_ganhador()
            self.quem_comeca()
            self.atualiza_cor_botao(button)

    def encontra_posicao_botao(self, button):
        for row in range(3):
            for col in range(3):
                if self.botoes[row][col] == button:
                    return row, col

    def quem_comeca(self):
        if self.jogador == 'X':
            self.jogador = 'O'
        else:
            self.jogador = 'X'

    def verificar_ganhador(self):
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

        if self.movimentos == 9 and not self.game_over:
            self.empate()

    def declarar_ganhador(self, ganhador):
        self.game_over = True
        self.title = f'{ganhador} venceu!'
        self.desabilitar_botoes()

        if ganhador == 'X':
            self.placar_x += 1
        elif ganhador == 'O':
            self.placar_o += 1

        if self.victory_sound:
            self.victory_sound.play()

        self.label_x.text = f'Jogador X: {self.placar_x}'
        self.label_o.text = f'Jogador O: {self.placar_o}'

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

        for row in range(3):
            for col in range(3):
                self.botoes[row][col].text = ''
                self.botoes[row][col].disabled = False
                self.atualiza_cor_botao(self.botoes[row][col])
        self.popup_inicial.open()

    def atualiza_cor_botao(self, button):
        if button.text == 'X':
            button.background_color = (0, 0, 1, 1)
        elif button.text == 'O':
            button.background_color = (0, 1, 0, 1)
        else:
            button.background_color = (1, 1, 1, 1)

    def parar(self):
        self.reset_game(None)
        if self.background_music:
            self.background_music.stop()

    def pause(self):
        return True

    def voltar(self):
        self.reset_game(None)

if __name__ == '__main__':
    JogoDaVelha().run()