import pygame 
import random
import os 


pygame.init()

WIDTH, HEIGHT = 500, 600 
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("firma2")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

player_img = pygame.image.load(os.path.abspath("C:\\Users\ПК\\Desktop\\Python Codes\\pygame-game-game-\\player_ball.png"))
block_img = pygame.image.load(os.path.abspath("C:\\Users\ПК\\Desktop\\Python Codes\\pygame-game-game-\\bratok.png"))
background_img = pygame.image.load(os.path.abspath("C:\\Users\\ПК\\Desktop\\Python Codes\\pygame-game-game-\\zombie_siti.jpg"))

player_size = 50
block_width, block_height  = 50, 50 

def change_color(image, color):
    colored_image = image.copy()
    colored_image.fill(color, special_flags=pygame.BLEND_MULT)
    return colored_image

player_img = change_color(player_img, (255, 255, 255))
block_img = change_color(block_img, (255, 255, 255))

background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
player_img = pygame.transform.scale(player_img, (player_size, player_size))
block_img = pygame.transform.scale(block_img, (block_width, block_height))

score = 0
font = pygame.font.SysFont("Arial", 30)
console_font = pygame.font.SysFont("Courier New", 20)
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def show_game_over():
    draw_text(f"Гра завершена! Фінальний рахунок:{score}", WIDTH // 9, HEIGHT // 3, WHITE)
    draw_text("R = рестарт гри, Q = вихід з гри",WIDTH // 7, HEIGHT // 2, WHITE)    
    
    


def start_game():
    global score 
    
    blocks = []
    score = 0
    level = 1
    blocks_per_level = 1
    player_x = WIDTH // 2 - player_size // 2 
    player_y = HEIGHT - player_size - 10
    player_speed = 5
    block_speed = 3
    
    clock = pygame.time.Clock()
    
    console_active = False
    console_text = ""
    
    
    running = True 
    while running:
        screen.blit(background_img, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKQUOTE:
                    console_active = not console_active
                if console_active:
                    if event.key == pygame.K_RETURN:
                        parts = console_text.split()
                        if len(parts) > 0:
                            cmd = parts[0].lower()
                            if cmd == "quit":
                                running = False
                            elif cmd == "speed" and len(parts) > 1:
                                try: player_speed = int(parts[1]) 
                                except: pass
                            elif cmd == "block" and len(parts) > 1:
                                try: block_speed = int(parts[1]) 
                                except: pass    
                            elif cmd == "level" and len(parts) > 1:
                                try: level = int(parts[1]) 
                                except: pass       
                        console_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        console_text = console_text[:-1]
                    elif event.key != pygame.K_ESCAPE:
                        console_text += event.unicode        
                    
        
        
        if console_active:
            overlay = pygame.Surface((WIDTH, 120))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            input_surf = console_font.render(f"> {console_text}", True, (0, 255, 0))
            screen.blit(input_surf, (10, 10))
            
            help_surf = console_font.render("Available cmds: speed [val], block [val]", True, (200, 200, 200))
            help_surf2 = console_font.render("                level [val], quit", True, (200, 200, 200))
            screen.blit(help_surf, (10, 50))
            screen.blit(help_surf2, (10, 75))

            pygame.display.flip()
            continue            
                    
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_x > 0: 
            player_x -= player_speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x < WIDTH - player_size: 
            player_x += player_speed
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player_y > 0:
            player_y -= player_speed
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player_y < HEIGHT - player_size:
            player_y += player_speed
        
        if len(blocks) < blocks_per_level:
            block_x = random.randint(0, WIDTH - block_width)
            block_y = -block_height
            blocks.append([block_x, block_y])
        
        for block in blocks:
            block[1] += block_speed
            if block[1] > HEIGHT:
                blocks.remove(block)
        
        for block in blocks:
            if (player_x < block[0] + block_width and 
                player_x + player_size > block[0] and 
                player_y < block[1] + block_height and
                player_y + player_size > block[1]):
                show_game_over()
                pygame.display.flip()
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            waiting_for_input = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                start_game()
                                waiting_for_input = False
                            elif event.key == pygame.K_q:
                               running = False
                               waiting_for_input = False   
                break 
        
                                 
        score += 1
        if score % 99 == 0:
            level += 1
            block_speed += 1 
            blocks_per_level += 0.5
            player_speed += 1.5
            
            
            
                   
                                        
        
        screen.blit(player_img, (player_x, player_y))
        
        for block in blocks:
            screen.blit(block_img, (block[0], block[1]))
            
        draw_text(f"Рахунок: {score}", 10, 10, BLACK)
        draw_text(f"Рівень: {level}", 10, 40, BLACK)
        
        pygame.display.flip()
        clock.tick(30)


















running = True 
while running:
    start_game()
    pygame.quit()
    
    