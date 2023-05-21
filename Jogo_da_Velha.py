from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.anchorlayout import AnchorLayout

class Jogo_da_Idosa(App):
    def build(self):
        self.title = 'Jogo da Velha'
        self.grid = GridLayout(cols=3, spacing=10, padding=10)
        self.buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Representa o tabuleiro
        self.player = 'X'  # Jogador padrão é X
        self.game_over = False
        self.moves_counter = 0
        self.score_x = 0  # Contagem de vitórias para o jogador X
        self.score_o = 0  # Contagem de vitórias para o jogador O

        for row in range(3):
            for col in range(3):
                button = Button(font_size=40)
                button.bind(on_press=self.on_button_click)
                button.background_color = (0.6, 0.8, 0.8, 1)
                self.grid.add_widget(button)
                self.buttons[row][col] = button

        reset_button = Button(text='Reset', size_hint=(0.25, 0.3), font_size=25, color=(0, 0, 0, 1))
        reset_button.bind(on_press=self.reset_game)

        placar_X = Label(text='Jogador X: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))
        placar_O = Label(text='Jogador O: 0', size_hint=(0.5, 0.1), pos_hint={'top': 0.5}, font_size=20, color=(0, 0, 0, 1))

        score_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        score_layout.add_widget(placar_X)
        score_layout.add_widget(placar_O)

        box_layout = BoxLayout(orientation='vertical')
        box_layout.add_widget(self.grid)

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center', size_hint=(1, 0.25))
        anchor_layout.add_widget(reset_button)

        box_layout.add_widget(score_layout)
        box_layout.add_widget(anchor_layout)

        with box_layout.canvas.before:
            Color(0.6, 0.8, 0.8, 1)  # Define a cor de fundo do layout
            self.rect = Rectangle(pos=box_layout.pos, size=box_layout.size)

        box_layout.bind(pos=self.update_rect, size=self.update_rect)

        self.label_x = placar_X
        self.label_o = placar_O

        return box_layout

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_button_click(self, button):
        if button.text == '' and not self.game_over:
            button.text = self.player
            row, col = self.find_button_position(button)
            self.buttons[row][col] = button
            self.moves_counter += 1
            self.check_winner()
            self.switch_players()
            self.update_button_style(button)  # Atualiza o estilo do botão após cada jogada

    def find_button_position(self, button):
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col] == button:
                    return row, col

    def switch_players(self):
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'

    def check_winner(self):
        for row in range(3):
            # Verificar linhas
            if self.buttons[row][0].text == self.buttons[row][1].text == self.buttons[row][2].text != '':
                self.declare_winner(self.buttons[row][0].text)

        for col in range(3):
            # Verificar colunas
            if self.buttons[0][col].text == self.buttons[1][col].text == self.buttons[2][col].text != '':
                self.declare_winner(self.buttons[0][col].text)

        # Verificar diagonais
        if self.buttons[0][0].text == self.buttons[1][1].text == self.buttons[2][2].text != '':
            self.declare_winner(self.buttons[0][0].text)
        elif self.buttons[0][2].text == self.buttons[1][1].text == self.buttons[2][0].text != '':
            self.declare_winner(self.buttons[0][2].text)

        # Verificar empate
        if self.moves_counter == 9 and not self.game_over:
            self.declare_draw()

    def declare_winner(self, winner):
        self.game_over = True
        self.title = f'{winner} venceu!'
        self.disable_buttons()

        if winner == 'X':
            self.score_x += 1
        elif winner == 'O':
            self.score_o += 1

        self.label_x.text = f'Jogador X: {self.score_x}'
        self.label_o.text = f'Jogador O: {self.score_o}'

    def declare_draw(self):
        self.game_over = True
        self.title = 'Empate!'
        self.disable_buttons()

    def disable_buttons(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].disabled = True

    def reset_game(self, instance):
        self.game_over = False
        self.moves_counter = 0
        self.title = 'Jogo da Velha'

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].text = ''
                self.buttons[row][col].disabled = False
                self.update_button_style(self.buttons[row][col])  # Atualiza o estilo de cada botão

    def update_button_style(self, button):
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

if __name__ == '__main__':
    Jogo_da_Idosa().run()