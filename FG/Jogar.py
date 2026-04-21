import pygame
import random

pygame.init()


largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Foguete Blaze")

branco = (255, 255, 255)
preto = (0, 0, 0)
vermelho = (255, 0, 0)


nave_img = pygame.image.load("assets/Foguete Blaze.png")
asteroide_img = pygame.image.load("assets/asteroide_screen.png")
fundo_img = pygame.image.load("assets/Espaçosideral_screen.jpg")
tiro_img = pygame.image.load("assets/MIÍSSIL.gif")
monstro_img = pygame.image.load("assets/MONSTRO.png")  # Imagem do monstro


alexandre_img = pygame.image.load("assets/Alexandre.jpg")
silvia_img = pygame.image.load("assets/Silvia.jpg")
dani_img = pygame.image.load("assets/Dani.jpg")


nave_img = pygame.transform.scale(nave_img, (50, 50))
asteroide_img = pygame.transform.scale(asteroide_img, (50, 50))
fundo_img = pygame.transform.scale(fundo_img, (largura, altura))
tiro_img = pygame.transform.scale(tiro_img, (10, 20))
monstro_img = pygame.transform.scale(monstro_img, (80, 80))  # Escala do monstro


alexandre_img = pygame.transform.scale(alexandre_img, (80, 80))
silvia_img = pygame.transform.scale(silvia_img, (80, 80))
dani_img = pygame.transform.scale(dani_img, (80, 80))
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = nave_img
        self.rect = self.image.get_rect()
        self.rect.centerx = largura // 2
        self.rect.bottom = altura - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura:
            self.rect.right = largura


class Asteroide(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        pygame.sprite.Sprite.__init__(self)
        self.image = asteroide_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8) * velocidade_base
        self.speedx = random.randrange(-3, 3) * velocidade_base

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (
            self.rect.top > altura + 10
            or self.rect.left < -25
            or self.rect.right > largura + 20
        ):
            self.rect.x = random.randrange(largura - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)


class Projeteil(pygame.sprite.Sprite):
    def __init__(self, nave):
        pygame.sprite.Sprite.__init__(self)
        self.image = tiro_img  # Usa a imagem carregada
        self.rect = self.image.get_rect()
        self.rect.centerx = nave.rect.centerx
        self.rect.top = nave.rect.top
        self.speedy = -10  # Velocidade do projétil

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()  # Remove o projétil quando ele sai da tela


class Monstro(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        pygame.sprite.Sprite.__init__(self)
        self.image = monstro_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura - self.rect.width)
        self.rect.y = random.randrange(-150, -80)
        self.speedy = random.randrange(1, 3) * velocidade_base  # Mais lento que asteroides
        self.speedx = random.choice([-2, 2]) * velocidade_base  # Movimento lateral
        self.health = 3  # Vida do monstro (quantos tiros aguenta)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Reverter direção ao atingir as bordas
        if self.rect.left < 0 or self.rect.right > largura:
            self.speedx *= -1

        if self.rect.top > altura + 10:
            self.rect.x = random.randrange(largura - self.rect.width)
            self.rect.y = random.randrange(-150, -80)
            self.speedy = random.randrange(1, 3)
            self.speedx = random.choice([-2, 2])

    def tomar_dano(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()  # Remove o monstro se a vida acabar
            return True  # Indica que o monstro foi destruído
        return False  # Indica que o monstro ainda está vivo


# Classe Base para os Bosses (Alexandre, Silvia, Dani)
class Boss(pygame.sprite.Sprite):
    def __init__(self, img, velocidade_base):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura - self.rect.width)
        self.rect.y = random.randrange(-150, -80)
        self.speedy = random.randrange(1, 3) * velocidade_base
        self.speedx = random.choice([-2, 2]) * velocidade_base
        self.health = 5  # Mais vida que o monstro normal

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Reverter direção ao atingir as bordas
        if self.rect.left < 0 or self.rect.right > largura:
            self.speedx *= -1

        if self.rect.top > altura + 10:
            self.rect.x = random.randrange(largura - self.rect.width)
            self.rect.y = random.randrange(-150, -80)
            self.speedy = random.randrange(1, 3)
            self.speedx = random.choice([-2, 2])

    def tomar_dano(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False


class Alexandre(Boss):
    def __init__(self, velocidade_base):
        super().__init__(alexandre_img, velocidade_base)
        

class Silvia(Boss):
    def __init__(self, velocidade_base):
        super().__init__(silvia_img, velocidade_base)


class Dani(Boss):
    def __init__(self, velocidade_base):
        super().__init__(dani_img, velocidade_base)


class ContadorAsteroides:
    def __init__(self):
        self.total_destruidos = 0

    def incrementa(self):
        self.total_destruidos += 1

    def resetar(self):
        self.total_destruidos = 0

    def obter_total(self):
        return self.total_destruidos


def exibir_placar(surf, texto, tamanho, x, y):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, branco)
    texto_rect = texto_surface.get_rect()
    texto_rect.midtop = (x, y)
    surf.blit(texto_surface, texto_rect)


def desenhar_texto(surf, texto, tamanho, cor, x, y):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect()
    texto_rect.center = (x, y)
    surf.blit(texto_surface, texto_rect)


def carregar_recorde():
    try:
        with open("recorde.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


def salvar_recorde(recorde):
    with open("recorde.txt", "w") as f:
        f.write(str(recorde))


def criar_asteroides(num_asteroides, velocidade_base):
    for i in range(num_asteroides):
        a = Asteroide(velocidade_base)
        todos_sprites.add(a)
        asteroides.add(a)


# Variáveis Globais
clock = pygame.time.Clock()
pontuacao = 0
recorde = carregar_recorde()
game_over = False
running = True
no_menu = True
asteroide_frequencia = 60  # Inicialmente, um asteroide a cada 60 frames
ultimo_asteroide = pygame.time.get_ticks()
max_asteroides = 20
contador_asteroides = ContadorAsteroides()
dificuldade = 1  # Nível de dificuldade padrão
monstros = pygame.sprite.Group()  # Grupo para os monstros
monstro_frequencia = 7000  # Um monstro a cada 7 segundos (em milissegundos)
bosses = pygame.sprite.Group()  # Grupo para os chefes
boss_frequencia = 10000  # Um boss a cada 10 segundos (em milissegundos)
ultimo_boss = pygame.time.get_ticks()


# Menu de Dificuldade
def menu_dificuldade(game_state):
    dificuldade = game_state["dificuldade"]
    asteroide_frequencia = game_state["asteroide_frequencia"]
    max_asteroides = game_state["max_asteroides"]
    monstro_frequencia = game_state["monstro_frequencia"]
    boss_frequencia = game_state["boss_frequencia"]

    selecionando_dificuldade = True
    while selecionando_dificuldade:
        tela.blit(fundo_img, (0, 0))
        desenhar_texto(
            tela, "Selecione a Dificuldade", 48, branco, largura // 2, altura // 4
        )
        desenhar_texto(
            tela, "1 - Fácil", 32, branco, largura // 2, altura // 2 - 30
        )
        desenhar_texto(
            tela, "2 - Médio", 32, branco, largura // 2, altura // 2 + 20
        )
        desenhar_texto(
            tela, "3 - Difícil(Rápido)", 32, branco, largura // 2, altura // 2 + 70
        )
        desenhar_texto(
            tela,
            "Pressione a tecla correspondente",
            24,
            branco,
            largura // 2,
            altura * 3 // 4,
        )
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_state["dificuldade"] = 1
                    game_state["asteroide_frequencia"] = 60
                    game_state["max_asteroides"] = 10
                    game_state["monstro_frequencia"] = float("inf")
                    game_state["boss_frequencia"] = float("inf")  # Sem Bosses
                    selecionando_dificuldade = False
                elif event.key == pygame.K_2:
                    game_state["dificuldade"] = 2
                    game_state["asteroide_frequencia"] = 45
                    game_state["max_asteroides"] = 15
                    game_state["monstro_frequencia"] = 7000
                    game_state[
                        "boss_frequencia"
                    ] = 15000  # Bosses aparecem a cada 15 segundos
                    selecionando_dificuldade = False
                elif event.key == pygame.K_3:
                    game_state["dificuldade"] = 3
                    game_state["asteroide_frequencia"] = 30
                    game_state["max_asteroides"] = 20
                    game_state["monstro_frequencia"] = 5000
                    game_state[
                        "boss_frequencia"
                    ] = 10000  # Bosses aparecem a cada 10 segundos
                    selecionando_dificuldade = False

    return game_state


# Menu Inicial
def menu_inicial(game_state):
    global no_menu, running
    no_menu = True
    while no_menu:
        tela.blit(fundo_img, (0, 0))
        desenhar_texto(tela, "Foguete Blaze", 64, branco, largura // 2, altura // 4)
        desenhar_texto(
            tela, "Aperte ESPAÇO para começar", 32, branco, largura // 2, altura // 2
        )
        desenhar_texto(
            tela, "Aperte ESC para sair", 32, branco, largura // 2, (altura // 2) + 50
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    no_menu = False
                    game_state = (
                        menu_dificuldade(game_state)
                    )  # Abre o menu de dificuldade
                    return False  # Indica para não sair do jogo
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
    return True  


# Inicialização do Jogo
def inicializar_jogo(game_state):
    global todos_sprites, asteroides, projeteis, nave, monstros, bosses, contador_asteroides, pontuacao

    todos_sprites = pygame.sprite.Group()
    asteroides = pygame.sprite.Group()
    projeteis = pygame.sprite.Group()
    monstros = pygame.sprite.Group()
    bosses = pygame.sprite.Group()
    nave = Nave()
    todos_sprites.add(nave)

    # Ajustar a criação de asteroides com base na dificuldade
    if game_state["dificuldade"] == 1:
        criar_asteroides(8, 0.5)  # Fácil: 8 asteroides, velocidade base 0.5
    elif game_state["dificuldade"] == 2:
        criar_asteroides(12, 0.75)  # Médio: 12 asteroides, velocidade base 0.75
    elif game_state["dificuldade"] == 3:
        criar_asteroides(16, 1)  # Difícil: 16 asteroides, velocidade base 1

    contador_asteroides = ContadorAsteroides()
    pontuacao = 0


# Função para criar Bosses aleatórios
def criar_boss(velocidade_base):
    boss_type = random.choice(
        ["Alexandre","Silvia", "Dani"]
    )  # Escolhe um boss aleatório
    if boss_type == "Alexandre":
        boss = Alexandre(velocidade_base)
    elif boss_type == "Silvia":
        boss = Silvia(velocidade_base)
    elif boss_type == "Dani":
        boss = Dani(velocidade_base)
    else:
        return 

    todos_sprites.add(boss)
    bosses.add(boss)


# Game State Inicial
game_state = {
    "dificuldade": 1,
    "asteroide_frequencia": 60,
    "max_asteroides": 20,
    "monstro_frequencia": 7000,
    "ultimo_monstro": pygame.time.get_ticks(),
    "boss_frequencia": 10000,
    "ultimo_boss": pygame.time.get_ticks(),
}
running = True

if menu_inicial(game_state):
    running = False

while running:
    inicializar_jogo(game_state)
    game_active = True 
    while game_active:
        clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                running = False  # Encerra o jogo completamente
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    tiro = Projeteil(nave)
                    todos_sprites.add(tiro)
                    projeteis.add(tiro)
                   
                if event.key == pygame.K_ESCAPE:
                    # Retorna ao menu inicial
                    game_active = False  # Encerra o loop do jogo atual
                    inicializar_jogo(game_state)  # Reinicializa o jogo
                    if menu_inicial(game_state):  # Mostra o menu inicial novamente
                        running = False  # Se o jogador sair do menu, encerra o jogo
                    break 

        # Lógica do jogo
        if game_active:
            todos_sprites.update()

            # Criar asteroides
            agora = pygame.time.get_ticks()
            if agora - ultimo_asteroide > asteroide_frequencia:
                ultimo_asteroide = agora
                if len(asteroides) < max_asteroides:
                    a = Asteroide(game_state["dificuldade"] * 0.5)  # Ajusta a velocidade
                    todos_sprites.add(a)
                    asteroides.add(a)

            # Criar monstros
            if (
                game_state["monstro_frequencia"] != float("inf")
                and agora - game_state["ultimo_monstro"]
                > game_state["monstro_frequencia"]
            ):
                game_state["ultimo_monstro"] = agora
                monstro = Monstro(game_state["dificuldade"] * 0.3)  # Ajusta a velocidade 
                todos_sprites.add(monstro)
                monstros.add(monstro)

            # Criar chefes
            if (
                game_state["boss_frequencia"] != float("inf")
                and agora - game_state["ultimo_boss"] > game_state["boss_frequencia"]
            ):
                game_state["ultimo_boss"] = agora
                criar_boss(game_state["dificuldade"] * 0.4)  # Ajusta a velocidade

            # Colisões entre projéteis e asteroides
            colisoes = pygame.sprite.groupcollide(asteroides, projeteis, True, True)
            for colisao in colisoes:
                pontuacao += 10
               
                contador_asteroides.incrementa()
                # Recriar asteroide
                a = Asteroide(game_state["dificuldade"] * 0.5)  # Ajusta a velocidade
                todos_sprites.add(a)
                asteroides.add(a)

            # Colisões entre projéteis e monstros
            colisoes_monstros = pygame.sprite.groupcollide(
                monstros, projeteis, False, True
            )  
            for monstro, projeteis_atingidos in colisoes_monstros.items():
                for projetil in projeteis_atingidos:
                    if monstro.tomar_dano():
                        pontuacao += 50  # Dá mais pontos por destruir monstros
                         # Toca o som de explosão
                        # Criar novo monstro
                        monstro = Monstro(game_state["dificuldade"] * 0.3)  # Ajusta a velocidade
                        todos_sprites.add(monstro)
                        monstros.add(monstro)
                    break  
                    
            # Colisões entre projéteis e chefes
            colisoes_bosses = pygame.sprite.groupcollide(
                bosses, projeteis, False, True
            )  
            for boss, projeteis_atingidos in colisoes_bosses.items():
                for projetil in projeteis_atingidos:
                    if boss.tomar_dano():
                        pontuacao += 100  # Pontuação alta por destruir chefes
                     
                        # Criar novo chefe
                        criar_boss(game_state["dificuldade"] * 0.4)  # Ajusta a velocidade
                    break

            # Colisões entre a nave e asteroides/monstros/chefes
            colisoes_nave = pygame.sprite.spritecollide(
                nave, asteroides, True
            )  # Remove o asteroide
            if colisoes_nave:
                game_active = False  # Fim de jogo
                game_over = True
              

            colisoes_nave_monstros = pygame.sprite.spritecollide(
                nave, monstros, True
            )  # Remove o monstro
            if colisoes_nave_monstros:
                game_active = False  # Fim de jogo
                game_over = True
               
            colisoes_nave_bosses = pygame.sprite.spritecollide(nave, bosses, True)
            if colisoes_nave_bosses:
                game_active = False
                game_over = True
                
            tela.blit(fundo_img, (0, 0))
            todos_sprites.draw(tela)

            # Placar
            exibir_placar(
                tela, "Pontuação: " + str(pontuacao), 32, largura // 2, 10
            )
            exibir_placar(tela, "Recorde: " + str(recorde), 24, largura // 4, 10)
            exibir_placar(
                tela,
                "Asteroides Destruídos: " + str(contador_asteroides.obter_total()),
                24,
                largura * 3 // 4,
                10,
            )

            if pontuacao > recorde:
                recorde = pontuacao
                salvar_recorde(recorde)

            pygame.display.flip()

    if game_over:
        tela.fill(preto)
        desenhar_texto(tela, "GAME OVER", 64, vermelho, largura // 2, altura // 4)
        desenhar_texto(
            tela, "Pontuação: " + str(pontuacao), 32, branco, largura // 2, altura // 2
        )
        desenhar_texto(
            tela,
            "Recorde: " + str(recorde),
            32,
            branco,
            largura // 2,
            altura // 2 + 50,
        )
        desenhar_texto(
            tela,
            "Asteroides Destruídos: " + str(contador_asteroides.obter_total()),
            32,
            branco,
            largura // 2,
            altura // 2 + 100,
        )
        desenhar_texto(
            tela,
            "Pressione qualquer tecla para jogar novamente ou ESC para o menu",
            24,
            branco,
            largura // 2,
            altura // 2 + 150,
        )
        pygame.display.flip()

        aguardando = True
        while aguardando:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    aguardando = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        # Retorna ao menu inicial
                        aguardando = False
                        game_over = False
                        inicializar_jogo(game_state)  # Reinicializa o jogo
                        if menu_inicial(game_state):  # Mostra o menu inicial novamente
                            running = False  # Se o jogador sair do menu, encerra o jogo
                        break 
                    else:
                        aguardando = False
                        game_over = False
                        # Reinicializar o jogo
                        inicializar_jogo(game_state)
                        break

pygame.quit()
