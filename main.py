from numpy import diff
import pygame
from random import randint
pygame.init()

window_h=600
window_w=650
player_turn = True
dif = ''

win = pygame.display.set_mode((window_h,window_w))
pygame.display.set_caption("Jogo da velha")
o_image = pygame.image.load('assets/o_image.png')
x_image = pygame.image.load('assets/x_image.png')

mouse_pos = pygame.mouse.get_pos()

matrix=[[0,0,0],[0,0,0],[0,0,0]]

def fonte(size):
    return pygame.font.Font("assets/8-BIT WONDER.TTF", size)

def max_index_2(n):
    if n == 3: return 0
    elif n == 4: return 1
    else: return n

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
            if event.type == pygame.QUIT:pygame.quit()

def tie_f():
    global matrix
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
    global player_turn

    #player [1] = user, player [2] = cpu
    if matrix[a][b] == 0:
        matrix[a][b] = player
        player_turn = not player_turn

    else:
        pop_up_unavailable()

def game_screen():
    win.fill((34,47,50))
    pygame.draw.line(win,(200,100,0),(200,0),(200,600),12)
    pygame.draw.line(win,(200,100,0),(400,0),(400,600),12)
    pygame.draw.line(win,(200,100,0),(0,200),(600,200),12)
    pygame.draw.line(win,(200,100,0),(0,400),(600,400),12)
    pygame.draw.rect(win,(21,17,26), pygame.Rect(0,600,600,650))
    pygame.draw.rect(win,(186,0,0), pygame.Rect(480,600,140,50))
    pygame.draw.rect(win,(0,106,50), pygame.Rect(0,600,360,50))
    txt = fonte(20).render("Sair", True, "white")
    rct = txt.get_rect(center=(540, 625))
    win.blit(txt, rct)
    txt = fonte(20).render("Alterar dificuldade", True, "white")
    rct = txt.get_rect(center=(182, 625))
    win.blit(txt, rct)

    if dif == 'easy':
        txt = fonte(20).render("fac", True, "white")
        rct = txt.get_rect(center=(420, 625))
        win.blit(txt, rct)
    if dif == 'hard':
        txt = fonte(20).render("dif", True, "white")
        rct = txt.get_rect(center=(420, 625))
        win.blit(txt, rct)

    for i in range (3):
        for j in range (3):
            if matrix[i][j] == 1:
                win.blit(o_image,(i*200,j*200))
            if matrix[i][j] == 2:
                win.blit(x_image,(i*200,j*200))
    pygame.display.update()

def ai_turn_hard():
    if player_turn == False:

        #detectar possiveis jogadas vitoriosas
        for i in range (3):
            for j in range (3):
                if matrix[i][j] == 2:
                    if matrix[max_index_2(i+1)][max_index_2(j)] == 2 and matrix[max_index_2(i+2)][max_index_2(j)] == 0:
                        select(max_index_2(i+2),max_index_2(j),2)
                        return 0
                    if matrix[max_index_2(i-1)][max_index_2(j)] == 2 and matrix[max_index_2(i-2)][max_index_2(j)] == 0:
                        select(max_index_2(i-2),max_index_2(j),2)
                        return 0
                    if matrix[max_index_2(i)][max_index_2(j+1)] == 2 and matrix[max_index_2(i)][max_index_2(j+2)] == 0:
                        select(max_index_2(i),max_index_2(j+2),2)
                        return 0
                    if matrix[max_index_2(i)][max_index_2(j-1)] == 2 and matrix[max_index_2(i)][max_index_2(j-2)] == 0:
                        select(max_index_2(i),max_index_2(j-2),2)
                        return 0

        if matrix[1][1] == 0 and ((matrix[0][0] == 2 and matrix[2][2] == 2) or (matrix[2][0] == 2 and matrix[0][2] == 2)):
            select(1,1,2)
            return 0
        for i in range(2):
            for j in range(2):
                if matrix[1][1] == 2 and matrix[2*i][2*j] == 2 and matrix[2-(2*i)][2-(2*j)] == 0:
                    select(2-(2*i),2-(2*j),2)
                    return 0

        #impedir vitorias do usuario
        for i in range (3):
            for j in range (3):
                if matrix[i][j] == 1:
                    if matrix[max_index_2(i+1)][max_index_2(j)] == 1 and matrix[max_index_2(i+2)][max_index_2(j)] == 0:
                        select(max_index_2(i+2),max_index_2(j),2)
                        return 0
                    if matrix[max_index_2(i-1)][max_index_2(j)] == 1 and matrix[max_index_2(i-2)][max_index_2(j)] == 0:
                        select(max_index_2(i-2),max_index_2(j),2)
                        return 0
                    if matrix[max_index_2(i)][max_index_2(j+1)] == 1 and matrix[max_index_2(i)][max_index_2(j+2)] == 0:
                        select(max_index_2(i),max_index_2(j+2),2)
                        return 0
                    if matrix[max_index_2(i)][max_index_2(j-1)] == 1 and matrix[max_index_2(i)][max_index_2(j-2)] == 0:
                        select(max_index_2(i),max_index_2(j-2),2)
                        return 0

        if matrix[1][1] == 0 and ((matrix[0][0] == 1 and matrix[2][2] == 1) or (matrix[2][0] == 1 and matrix[0][2] == 1)):
            select(1,1,2)
            return 0
        for i in range(2):
            for j in range(2):
                if matrix[1][1] == 1 and matrix[2*i][2*j] == 1 and matrix[2-(2*i)][2-(2*j)] == 0:
                    select(2-(2*i),2-(2*j),2)
                    return 0

        #caso nenhuma das funcoes acima retorne uma possivel jogada:

        if ((matrix[0][0] == 1 and matrix[2][2] == 1) or (matrix[2][0] == 1 and matrix[0][2] == 1)) and matrix[1][1] == 2:
            if matrix[0][1] == 0:
                select(0,1,2)
                return 0
            if matrix[1][0] == 0:
                select(1,0,2)
                return 0
            if matrix[2][1] == 0:
                select(2,1,2)
                return 0
            if matrix[1][2] == 0:
                select(1,2,2)
                return 0

        if matrix[1][1] == 1:  
            for i in range(2):
                for j in range(2):
                    if matrix[2*i][2*j] == 0:
                        select(2*i,2*j,2)
                        return 0

        for i in range(2):
            for j in range(2):
                if matrix[2*i][2*j] == 1 and matrix[1][1] == 0:
                    select(1,1,2)
                    return 0
                   

        for i in range(2):
            for j in range(2):
                if matrix[2*i][2*j] == 0:
                    select(2*i,2*j,2)
                    return 0

        while True:
            a = randint(0,2)
            b = randint(0,2)
            if matrix[a][b] == 0:
                select(a,b,2)
                return 0

def ai_turn_easy():
    if player_turn == False:
        while True:
            a = randint(0,2)
            b = randint(0,2)
            if matrix[a][b] == 0:
                select(a,b,2)
                return 0

def game(difficulty):
    global player_turn
    while True:
        pygame.time.delay(50)


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if int(event.pos[1]//200) > 2:
                    if int(event.pos[0]//200) == 2:
                        pygame.quit()
                    else:
                        return 0
                elif player_turn == True:
                    selected_x = int(event.pos[0]//200)
                    selected_y = int(event.pos[1]//200)
                    select(selected_x,selected_y,1)


            if event.type == pygame.QUIT:pygame.quit()

        game_screen()
        detect_winner()
        if difficulty == 'easy':
            ai_turn_easy()
        if difficulty == 'hard':
            ai_turn_hard()

def set_difficulty():
    global dif
    while True:
        win.fill((30,30,50))
        pygame.time.delay(50)

        pygame.draw.rect(win,(10,10,10), pygame.Rect(30,300,160,100))
        pygame.draw.rect(win,(10,10,10), pygame.Rect(220,300,160,100))
        pygame.draw.rect(win,(10,10,10), pygame.Rect(410,300,160,100))
        txt = fonte(20).render("Escolha a dificuldade", True, "white")
        rct = txt.get_rect(center=(300, 180))
        win.blit(txt,rct)

        txt = fonte(20).render("facil", True, "white")
        rct = txt.get_rect(center=(110, 350))
        win.blit(txt,rct)

        txt = fonte(20).render("medio", True, "white")
        rct = txt.get_rect(center=(300, 350))
        win.blit(txt,rct)

        txt = fonte(12).render("(em breve)", True, "white")
        rct = txt.get_rect(center=(300, 375))
        win.blit(txt,rct)

        txt = fonte(20).render("dificil", True, "white")
        rct = txt.get_rect(center=(490, 350))
        win.blit(txt,rct)


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if int(event.pos[0]//200) == 2:
                    dif = 'hard'
                    return 0
                if int(event.pos[0]//200) == 0:
                    dif = 'easy'
                    return 0
            if event.type == pygame.QUIT:pygame.quit()


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
            if event.type == pygame.MOUSEBUTTONDOWN: return 0
            if event.type == pygame.QUIT:pygame.quit()

main()
while True:
    set_difficulty()
    game(dif)