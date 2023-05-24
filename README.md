Jogo da Velha em Python usando Kivy


Este é um aplicativo simples de Jogo da Velha, feito em Python, utilizando a biblioteca de interface gráfica Kivy. O jogo foi projetado para ser jogado por dois jogadores alternando as jogadas.

Funcionalidades:
A janela principal do jogo exibe um tabuleiro de 3x3 onde os jogadores fazem suas jogadas.
Cada jogador pode jogar com 'X' ou 'O', alternando a cada jogada.
O aplicativo verifica automaticamente se algum dos jogadores ganhou ou se o jogo terminou em empate.
O aplicativo mantém um placar do número de jogos ganhos por cada jogador.
Há um botão "Reset" para reiniciar o jogo a qualquer momento.

Como Jogar:
Quando o jogo é iniciado, um popup aparece perguntando quem irá começar a partida, se o jogador 'X' ou o jogador 'O'.
Cada jogador faz sua jogada por vez, clicando em um dos espaços vazios do tabuleiro para colocar seu marcador ('X' ou 'O').
O jogo continua até que um dos jogadores tenha três de seus marcadores em uma linha (horizontal, vertical ou diagonal) ou até que todas as casas estejam preenchidas, o que é um empate.
Quando um jogador ganha, a mensagem "[Jogador] venceu!" aparece no título da janela e o placar do respectivo jogador é incrementado.
Em caso de empate, a mensagem "Empate!" aparece no título da janela.
Para iniciar uma nova partida, basta clicar no botão "Reset". Um popup irá aparecer novamente para que seja escolhido quem irá começar a nova partida.

Como executar o código:
Para executar o código, você precisará ter Python e a biblioteca Kivy instalados em seu computador. Uma vez instalados, você pode executar o código usando um interpretador Python.

Sobre o código:
O código foi escrito em Python, utilizando o Kivy, uma biblioteca de interface gráfica para Python. O aplicativo é uma subclasse da classe App do Kivy, e a maior parte do código está na implementação do método build() dessa subclasse, que configura a interface do usuário do jogo.
Os métodos adicionais implementam a lógica do jogo, manipulam as ações do usuário (como cliques de botão), atualizam o estado do jogo e verificam as condições de vitória.
