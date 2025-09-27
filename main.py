from time import sleep
import sounddevice as sd
from pygame import *
init()
mixer.init()
from random import *
window_size = 1200,800
window = display.set_mode(window_size)
clock = time.Clock()
play = True
gravitation = 5
lose = False

sky_background = image.load('img/sky.png')
sky_background = transform.scale(sky_background,window_size)

bird_img1 = image.load('img/bird.png')
bird_img1 = transform.scale(bird_img1,(100,100))

bird_img2 = image.load('img/bird2.png')
bird_img2 = transform.scale(bird_img2,(100,100))

bird_img = bird_img1

bird = Rect(150,window_size[1]//2-100,100,100)

pipes_img = image.load('img/pipes.png')

jump = 'sound/jump.wav'
play_jamp = mixer.Sound(jump)

background_sound = 'sound/background_sound.mp3'
background_sound = mixer.Sound(background_sound)

lose_sound = 'sound/lose.wav'
lose_sound = mixer.Sound(lose_sound)




def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=650):
   pipes = []
   start_x = window_size[0]
   for i in range(count):
       height = randint(min_height, max_height)
       top_pipe = Rect(start_x, 0, pipe_width, height)
       bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
       pipes.extend([top_pipe, bottom_pipe])
       start_x += distance
   return pipes

main_font = font.Font(None,100)

pipes = generate_pipes(150)
score = 0
while True:
    if not lose and not mixer.get_busy():
        background_sound.play(-1)

    for e in event.get():
        if e.type == QUIT:
            quit()
        
    window.blit(sky_background,(0,0))

    window.blit(bird_img,bird)


    for p in pipes[:]:
        if not lose:
            p.x -= 10
            if p.x <= -10:
                pipes.remove(p)
                score += 0.5
        
        scaled_pipe = transform.scale(pipes_img, (p.width, p.height))

        if p.y == 0:
            flipped_pipe = transform.flip(scaled_pipe, False, True)
            window.blit(flipped_pipe, p)
        else:
            window.blit(scaled_pipe, p)
        

        

        
        if bird.colliderect(p):
            background_sound.stop()
            play_jamp.stop()
            lose = True
            if lose and not mixer.get_busy():
                lose_sound.play()
    
    if len(pipes) < 8:
        pipes += generate_pipes(150)

    skore_text = main_font.render(f'{int(score)}',1,'black')
    center_text = window_size[0]//2 - skore_text.get_rect().w
    window.blit(skore_text,(center_text,40))

    display.update()
    clock.tick(60)
    keys = key.get_pressed()

    
        

    
    if keys[K_w] and not lose:
        bird_img = bird_img2
        gravitation = 5
        bird.y -= 15
        try:
            if play:
                play_jamp.play()
                play = False
        except:
            pass
    else:
        bird_img = bird_img1
        gravitation += 1
        bird.y += gravitation   

    for e in event.get():  
        if e.type == KEYUP:
            if e.key == K_w:
                play = True
    

    if keys[K_r] and lose:
        bird.y = window_size[1]//2 - 100
        pipes = generate_pipes(150)
        score = 0
        lose = False

