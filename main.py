import pygame
from random import randint
pygame.init()

window_h=600
window_w=600
rodada = 0
player_turn = True

win = pygame.display.set_mode((window_h,window_w))
pygame.display.set_caption("Jogo da velha")
o_image = pygame.image.load('assets/o_image.png')
x_image = pygame.image.load('assets/x_image.png')

mouse_pos = pygame.mouse.get_pos()

matrix=[[0,0,0],[0,0,0],[0,0,0]]

def fonte(size):
    return pygame.font.Font("assets/8-BIT WONDER.TTF", size)

def pop_up_unavailable():
    pont = True
    while pont:
        pygame.draw.rect(win, "Red", (50,200,500,200))
        ase = fonte(25).render("Posicao indisponivel", True, "White")
        aere = ase.get_rect(center=(310, 300))
        win.blit(ase, aere)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: pont = False
            if event.type == pygame.QUIT:pygame.quit()

def won(winner,s1,s2):
    global matrix
    global rodada
    pont = True
    while pont:

        pygame.draw.line(win,(190,190,190),(s1[0]*200+100,s1[1]*200+100),(s2[0]*200+100,s2[1]*200+100),25)
        pygame.draw.circle(win,(190,190,190),(s1[0]*200+100,s1[1]*200+100),12)
        pygame.draw.circle(win,(190,190,190),(s2[0]*200+100,s2[1]*200+100),12)



        pygame.draw.rect(win, "Green", (125,257,350,30))
        if winner == 1:
            ase = fonte(25).render("Humano venceu", True, "Black")
        elif winner == 2:
            ase = fonte(25).render("Maquina venceu", True, "Black")
        aere = ase.get_rect(center=(300, 270))
        win.blit(ase, aere)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pont = False
                matrix=[[0,0,0],[0,0,0],[0,0,0]]
                rodada = 0
            if event.type == pygame.QUIT:pygame.quit()

def tie_f():
    global matrix
    global rodada
    pont = True
    while pont:
        pygame.draw.rect(win, "purple", (125,257,350,30))

        ase = fonte(25).render("Deu velha", True, "Black")
        aere = ase.get_rect(center=(300, 270))
        win.blit(ase, aere)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                matrix=[[0,0,0],[0,0,0],[0,0,0]]
                rodada = 0
                pont = False
            if event.type == pygame.QUIT:pygame.quit() 

def detect_winner():

    for i in range (3):
        if matrix[i][0] == matrix[i][1] and matrix[i][0] == matrix[i][2] and matrix[i][0] != 0:
            won(matrix[i][0],(i,0),(i,2))
    for i in range (3):
        if matrix[0][i] == matrix[1][i] and matrix[0][i] == matrix[2][i] and matrix[0][i] != 0:
            won(matrix[0][i],(0,i),(2,i))
    if matrix[0][0] == matrix[1][1] and matrix[0][0] == matrix[2][2] and matrix[1][1] != 0:
        won(matrix[1][1],(0,0),(2,2))
    if matrix[2][0] == matrix[1][1] and matrix[2][0] == matrix[0][2] and matrix[1][1] != 0:
        won(matrix[1][1],(2,0),(0,2))
    
    tie = True
    for i in range(3):
        for j in range(3):
            if matrix[i][j] == 0:
                tie = False
    
    if tie == True:
        tie_f()

def select(a,b,player):
    global rodada
    global player_turn

    #player [1] = user, player [2] = cpu
    if matrix[a][b] == 0:
        matrix[a][b] = player
        rodada += 1
        player_turn = not player_turn

    else:
        pop_up_unavailable()

def game_screen():
    win.fill((34,47,50))
    pygame.draw.line(win,(200,100,0),(200,0),(200,600),12)
    pygame.draw.line(win,(200,100,0),(400,0),(400,600),12)
    pygame.draw.line(win,(200,100,0),(0,200),(600,200),12)
    pygame.draw.line(win,(200,100,0),(0,400),(600,400),12)
    for i in range (3):
        for j in range (3):
            if matrix[i][j] == 1:
                win.blit(o_image,(i*200,j*200))
            if matrix[i][j] == 2:
                win.blit(x_image,(i*200,j*200))
    pygame.display.update()

def game():
    global rodada
    global player_turn
    while True:
        pygame.time.delay(50)


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_turn == True:
                    selected_x = int(event.pos[0]//200)
                    selected_y = int(event.pos[1]//200)
                    select(selected_x,selected_y,1)


            if event.type == pygame.QUIT:pygame.quit()

        game_screen()
        detect_winner()

        #artifical inteligence
        #if gamemode == hard:
        if rodada == 0 and player_turn == False:
            select(1,1,2)
        if rodada == 1 and player_turn == False:
            if matrix[0][0] == 1: select(2,2,2)
            if matrix[2][2] == 1: select(0,0,2)
            if matrix[2][0] == 1: select(0,2,2)
            if matrix[0][2] == 1: select(2,0,2)

            if matrix[1][0] == 1 or matrix[0][1] == 1 or matrix[2][1] == 1 or matrix[1][2] == 1: select(1,1,2)

            if matrix[1][1] == 1: select(randint(0,1)*2,randint(0,1)*2,2)
            
        if rodada > 1 and player_turn == False:


            #fazer uma função recursiva para detectar jogadas vitoriosas


            while True:
                a = randint(0,2)
                b = randint(0,2)
                if matrix[a][b] == 0:
                    select(a,b,2)
                    break
                else: continue
                


def main():
    while True:

        pygame.time.delay(50)
        pygame.display.update()
        win.fill((0,0,0))
        MENU_TEXT = fonte(50).render("Jogo da veia", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 100))
        win.blit(MENU_TEXT, MENU_RECT)
        ase = fonte(15).render("Against the machine", True, "grey")
        aere = MENU_TEXT.get_rect(center=(430, 160))
        win.blit(ase, aere)
        pygame.draw.rect(win, (20,50,65), (150,300,300,90))
        ase = fonte(14).render("clique aqui para iniciar", True, "grey")
        aere = MENU_TEXT.get_rect(center=(422, 360))
        win.blit(ase, aere)


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: game()
            if event.type == pygame.QUIT:pygame.quit()

main()
pygame.quit()