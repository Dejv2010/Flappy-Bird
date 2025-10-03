from time import sleep
import numpy as np
import sounddevice as sd
from pygame import *
init()
mixer.init()
from random import *
window_size = 1200,800
window = display.set_mode(window_size)
clock = time.Clock()
# зміні
play = True
gravitation = 5
lose = False
jump_ = False
control_type = 'voise'

score = 0
wait = 40 

main_font = font.Font(None,100)
menu_font = font.Font(None,50)
info_font = font.Font(None,20)

#мікрофон
fs = 44100
block = 256 
mic_level = 0.0

y_vel = 0.0
gravitation = 0.6
THRESH = 0.01
IMPULSE = -8.0


#
def audio_cb (indata,frames,time,status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms

# images
sky_background = image.load('img/sky.png')
sky_background = transform.scale(sky_background,window_size)

game_background = image.load('img/game over foto.jpg')
game_background = transform.scale(game_background,window_size)

game_background2 = image.load('img/game-over.jpg')
game_background2 = transform.scale(game_background2,window_size)

bird_img1 = image.load('img/bird.png')
bird_img1 = transform.scale(bird_img1,(100,100))

bird_img2 = image.load('img/bird2.png')
bird_img2 = transform.scale(bird_img2,(100,100))

bird_img = bird_img1
pipes_img = image.load('img/pipes.png')

bird = Rect(150,window_size[1]//2-100,100,100)


# sound
jump = 'sound/jump.wav'
play_jamp = mixer.Sound(jump)

game_over_sound = 'sound/fvfyfyfyv.mp3'
game_over_sound = mixer.Sound(game_over_sound)

background_sound = 'sound/background_sound.mp3'
background_sound = mixer.Sound(background_sound)

lose_sound = 'sound/lose.wav'
lose_sound = mixer.Sound(lose_sound)


          




# menu
go = True
start = False
game_pris = 'red'
max_score = 0
speed = 15
up = 15
btn_color = 'green'
show = 'menu'
hard = 'red'
menu = True
control = False
feel = False
center = (window_size[0] / 2 - 100)
x_pos = 200
on = menu_font.render(f'on',1,'black')
off = menu_font.render(f'off',1,'black')


def btn(text,x,y,width=200,height=50,font_=menu_font):
    btn_rect = Rect(x,y,width,height)
    btn_text = text
    btn_text = font_.render(f'{text}',1,'black')
    btn_text_pos =  ((x + 100) - btn_text.get_rect().w//2) , y + 10
    return btn_rect,btn_text,btn_text_pos

def draw_btn(data,color):
    try:
        draw.rect(window,color,data[0],border_radius=15)
        window.blit(data[1],data[2])
    except:
        pass



menu_btn_data = btn('меню',(window_size[0] - 210),5)

back_to_menu = btn('меню',center,x_pos)

menu_exit_data = btn('грати', center ,x_pos)
x_pos += 60
control_btn_data = btn('керування',center,x_pos)
x_pos += 60
feel_btn_data = btn('чутливість',center,x_pos)
x_pos += 60 
hardcore = btn('hardcor',center,x_pos,width=140)

hx,hy = hardcore[2]
hardcore = hardcore[0],hardcore[1],(hx-30,hy)

hardcore_btn = btn('off',hardcore[0].x + 150,x_pos,width=50)
hx,hy = hardcore_btn[2]
hardcore_btn = hardcore_btn[0],hardcore_btn[1],(hx-75,hy)


x_pos += 60 
prais = btn('приз',center,x_pos,width=140)

hx,hy = prais[2]
prais = prais[0],prais[1],(hx-30,hy)

prais_btn = btn('off',prais[0].x + 150,x_pos,width=50)
hx,hy = prais_btn[2]
prais_btn = prais_btn[0],prais_btn[1],(hx-75,hy)

x_pos += 60
info = btn('правила',center,x_pos)
x_pos += 60

max_score_text = btn(f'max point: {max_score}',center - 40,x_pos,width=280)
hx,hy = max_score_text[2]
max_score_text = max_score_text[0],max_score_text[1],(hx+40,hy)


control_x_pos = 260
voise_btn_data = btn('голосом',center,control_x_pos)
control_x_pos += 60
tap_btn_data = btn('пробіл',center,control_x_pos)

feel_y_pos = 260
speed_btn_data = btn('скорість',center - 300,feel_y_pos)
up_btn_data = btn('піднімання',center + 300,feel_y_pos)

slider_up = btn('',up_btn_data[0].x-100,feel_y_pos + 60,400,30)
btn_up = btn('',slider_up[0].x + 190,slider_up[0].y - 10,20,50)


slider_speed = btn('',speed_btn_data[0].x-100,feel_y_pos + 60,400,30)
print(slider_speed)
btn_speed = btn('',slider_speed[0].x + 190,slider_speed[0].y - 10,20,50)


img_info = image.load('img/info.png')
img_info = transform.scale(img_info,(400,300))
info_text = btn('',center-100,260,400,300,info_font)

#game_over

restart = btn('RESTART',center,750)



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
pipes = generate_pipes(150)

game_over = False


with sd.InputStream(samplerate=fs, channels=1, blocksize=block, callback=audio_cb):
    while True:
        if start:
            for p in pipes:
                p.x += 1200
            start = False

        if not lose and not mixer.get_busy():
            background_sound.play(-1)

        for e in event.get():
            if e.type == QUIT:
                quit()
        
        
            
        window.blit(sky_background,(0,0))
        window.blit(bird_img,bird)

        if not game_over:
            for p in pipes[:]:
                if not lose:
                    p.x -= speed

                if p.x <= -100:
                    pipes.remove(p)
                    score += 0.5
                    
                scaled_pipe = transform.scale(pipes_img, (p.width, p.height))

                if p.y == 0:
                    flipped_pipe = transform.flip(scaled_pipe, False, True)
                    window.blit(flipped_pipe, p)
                else:
                    window.blit(scaled_pipe, p)

                if bird.colliderect(p):
                    if hard == 'red':
                        background_sound.stop()
                        play_jamp.stop()
                        lose = True
                        if lose and not mixer.get_busy():
                            lose_sound.play()
                    if hard == 'green':
                       
                        
                        start = True
                        menu = True
                        show = 'game_over'
                        background_sound.stop()
                        play_jamp.stop()
                        lose_sound.stop()
        
        if len(pipes) < 8:
            pipes += generate_pipes(150)



       
        draw_btn(menu_btn_data,'red')

        skore_text = main_font.render(f'{int(score)}',1,'black')
        center_text = window_size[0]//2 - skore_text.get_rect().w
        window.blit(skore_text,(center_text,40))

        display.update()
        clock.tick(60)
        keys = key.get_pressed()
        

        # обробка події та керування пташкою
        if control_type == 'tap':
            if keys[K_SPACE] and not lose and bird.y > 0:
                bird_img = bird_img2
                gravitation = 2
                bird.y -= up
                try:
                    if play:
                        play_jamp.play()
                        play = False
                except:
                    pass
            elif bird.y < 700:
                bird_img = bird_img1
                gravitation += 0.5
                bird.y += gravitation 
        elif control_type == 'voise':
            if mic_level > THRESH and not lose and bird.y > 0:
                bird_img = bird_img2
                gravitation = 2
                bird.y -= up
                try:
                    if play:
                        play_jamp.play()
                        play = False
                except:
                    pass
            elif bird.y < 700:
                bird_img = bird_img1
                gravitation += 0.5
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
        if lose and wait > 1:
            for p in pipes:
                p.x += 15
            wait -= 1
        else:
            lose = False
            wait = 40

        mous = mouse.get_pressed()
        if mous[0]:
            if menu_btn_data[0].collidepoint(mouse.get_pos()):
                menu = True



        # menu
        while menu:
            if game_over:
                window.blit()
            else:
                window.blit(sky_background,(0,0))

            for e in event.get():
                if e.type == QUIT:
                    quit()

            if show == 'menu':
                
                draw_btn(menu_exit_data,'red')
                draw_btn(control_btn_data,btn_color)
                draw_btn(feel_btn_data,btn_color)
                draw_btn(hardcore,btn_color)
                draw_btn(hardcore_btn,hard)
                draw_btn(prais,btn_color)
                draw_btn(prais_btn,game_pris)
                draw_btn(info,btn_color)
                draw_btn(max_score_text,(173, 216, 230))

            if show == 'control':
                draw_btn(back_to_menu,'red')
                if control_type == 'tap':
                    draw_btn(tap_btn_data,btn_color)
                    draw_btn(voise_btn_data,'red')
                else:
                    draw_btn(tap_btn_data,'red')
                    draw_btn(voise_btn_data,btn_color)
            
            if show == 'feel':
                draw_btn(back_to_menu,'red')
                draw_btn(speed_btn_data,'yellow')
                draw_btn(up_btn_data,'yellow')
                draw_btn(slider_speed,btn_color)
                draw_btn(slider_up,btn_color)
                draw_btn(btn_speed,'red')
                draw_btn(btn_up,'red')

                speed = int((btn_speed[0].x - 100)/13)
                if speed < 0:
                    speed = 1
                up = int((btn_up[0].x - 695)/13)
                if up < 0:
                    up = 1


            if show == 'info':
                draw_btn(back_to_menu,'red')
                draw_btn(info_text,(173, 216, 230))
                window.blit(img_info,info_text[0])
                

            if show == 'game_over':
                if game_pris == 'green':
                    window.blit(game_background,(0,0))
                else:
                    window.blit(game_background2,(0,0))
                if go and game_pris == 'green':
                        game_over_sound.play()
                        go = False
                draw_btn(restart,'white')
                


            


            
                


            display.update()
            clock.tick(60)

            mous = mouse.get_pressed()

            if mous[0]:
                sleep(0.2)
                #menu
                if show == 'menu':
                    if menu_exit_data[0].collidepoint(mouse.get_pos()):
                        gravitation = 5
                        menu = False
                        bird.y = window_size[1]//2 - 100
                    if control_btn_data[0].collidepoint(mouse.get_pos()):
                        show = 'control'  
                    
                    if feel_btn_data[0].collidepoint(mouse.get_pos()):
                        show = 'feel'  
                    
                    if info[0].collidepoint(mouse.get_pos()):
                        show = 'info'

                    if hardcore_btn[0].collidepoint(mouse.get_pos()):
                        if hard == 'red':
                            hardcore_btn = hardcore_btn[0],on,hardcore_btn[2]
                            hard = 'green'
                            if hard == 'green':
                                score = 0

                            sleep(0.1)
                        elif hard == 'green':
                            hardcore_btn = hardcore_btn[0],off,hardcore_btn[2]
                            hard = 'red'
                    
                            sleep(0.1)

                    if prais_btn[0].collidepoint(mouse.get_pos()):
                        if game_pris == 'red':
                            prais_btn = prais_btn[0],on,prais_btn[2]
                            game_pris = 'green'
                            
                        
                            sleep(0.1)
                        elif game_pris == 'green':
                            prais_btn = prais_btn[0],off,prais_btn[2]
                            game_pris = 'red'
                          
                            sleep(0.1)

                # control
                if show == 'control':
                    if tap_btn_data[0].collidepoint(mouse.get_pos()):
                        control_type = 'tap'
                    if voise_btn_data[0].collidepoint(mouse.get_pos()):
                        control_type = 'voise'
                # feel
                if show == 'feel':
                    mx,my = mouse.get_pos()
                    if slider_up[0].x + 400 > btn_up[0].x and slider_up[0].x < btn_up[0].x and slider_up[0].x + 400 > mx and slider_up[0].x < mx:
                        btn_up[0].x = mx

                    if slider_speed[0].x + 400 > btn_speed[0].x and slider_speed[0].x < btn_speed[0].x and slider_speed[0].x + 400 > mx and slider_speed[0].x < mx:
                        btn_speed[0].x = mx    

                if back_to_menu[0].collidepoint(mouse.get_pos()):
                    show = 'menu'

                if show == 'game_over':
                    
                    if restart[0].collidepoint(mouse.get_pos()):
                        if max_score < score:
                            max_score = int(score) 
                            max_score_text = max_score_text[0],menu_font.render(f'max point: {max_score}',1,'black'),max_score_text[2]
                        show = 'menu'
                        menu = True
                        go = True
        
        

            
