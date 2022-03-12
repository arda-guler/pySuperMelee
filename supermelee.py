import pygame as g
import numpy as np

from spaceship import *
from projectile import *
from sound import *

ships = []
projectiles = []

sp_plasma = g.image.load("data/img/projectiles/plasma.png")
sp_missile = g.image.load("data/img/projectiles/missile.png")

# world to screen coordinate converter
def w2s(pos):
    screen_x_mid = 320
    screen_y_mid = 240

    cy = screen_y_mid - pos[1]
    cx = screen_x_mid + pos[0]

    return np.array([cx, cy])

def create_projectile(sender, p_type, target=None):
    global projectiles
    global sp_plasma, sp_missile
    
    if p_type == "plasma":
        p_size = 2
        p_pos = sender.pos + sender.orient_matrix[1] * (sender.size + p_size * 1.5)
        new_proj = projectile(name="plasma",
                              model="Pure Ion Ultra-High Density Plasma Packet",
                              size=p_size,
                              sprite=sp_plasma,
                              damage=5,
                              pos=p_pos,
                              orient=sender.orient,
                              orient_matrix=sender.orient_matrix,
                              speed=300,
                              target=target,
                              homing=False,
                              sounds=[],
                              expire_time=1)

    elif p_type == "missile":
        p_size = 2
        p_pos = sender.pos + sender.orient_matrix[1] * (sender.size + p_size * 1.5)
        new_proj = projectile(name="missile",
                              model="Nuclear Tipped Active Homing Guided Anti-Ship Missile",
                              size=p_size,
                              sprite=sp_missile,
                              damage=15,
                              pos=p_pos,
                              orient=sender.orient,
                              orient_matrix=sender.orient_matrix,
                              speed=50,
                              target=target,
                              homing=True,
                              sounds=[],
                              expire_time=6)
        
    projectiles.append(new_proj)

def main():
    global ships, projectiles

    print("\nCONTROLS:")
    print("Player A: Arrow keys to move, Enter to shoot.")
    print("Player B: WASD to move, T to shoot.\n")

    panel = g.image.load("data/img/ui/panel.png")
    A_light = g.image.load("data/img/ui/green_light.png")
    B_light = g.image.load("data/img/ui/purple_light.png")
    background = g.image.load("data/img/background/orion_nebula.png")
    
    # initialization
    g.init()
    init_sound()

    # display
    mw = g.display.set_mode((640, 480))
    x_mid = 320
    y_mid = 240
    
    g.display.set_caption("SuperMelee!")
    
    # set icon
    ico = g.image.load("data/img/ships/blue_corvette/blue_corvette_1.png")
    g.display.set_icon(ico)  

    # sounds
    corvette_sounds = {"firing":"plasma",
                       "damage":"alert"}
    
    destroyer_sounds = {"firing":"launch",
                        "damage":"hit"}

    # ships
    s_A = spaceship(name="AFS Frungy",
                    model="X3 Class Corvette",
                    size=7,
                    sprite="blue_corvette",
                    max_crew=50,
                    max_energy=100,
                    accel_rate=17,
                    turn_rate=5,
                    energy_generation=20,
                    projectile="plasma",
                    attack_energy=15,
                    sounds=corvette_sounds,
                    max_speed=48,
                    attack_cooldown=0.2)
    
    s_A.set_pos(np.array([-200.0, 0.0]))

    s_B = spaceship(name="PRM Fwiffo",
                    model="Type-III Destroyer",
                    size=10,
                    sprite="red_destroyer",
                    max_crew=92,
                    max_energy=300,
                    accel_rate=10,
                    turn_rate=0.5,
                    energy_generation=5,
                    projectile="missile",
                    attack_energy=50,
                    sounds=destroyer_sounds,
                    max_speed=20,
                    attack_cooldown=2)

    s_B.set_pos(np.array([200.0, 0.0]))

    ships = [s_A, s_B]

    game_tick = 0
    game_time = 0
    dt = 0.02
    game_active = True
    mw.fill((0,0,0))
    playBGM("bgm")
    
    while game_active:

        # inputs
        for event in g.event.get():
            if event.type == g.QUIT:
                game_active = False

        key_inputs = g.key.get_pressed()

        # ship A controls
        if key_inputs[g.K_LEFT]:
            s_A.rotate(1, dt)
        if key_inputs[g.K_RIGHT]:
            s_A.rotate(-1, dt)
        if key_inputs[g.K_UP]:
            s_A.accel(dt)
        if key_inputs[g.K_RETURN]:
            if s_A.energy > s_A.attack_energy and s_A.current_cooldown <= 0:
                create_projectile(s_A, s_A.projectile)
                s_A.attack()
                if not getChannelBusy(1):
                    playSfx(s_A.sounds["firing"], 1)

        # ship B controls
        if key_inputs[g.K_a]:
            s_B.rotate(1, dt)
        if key_inputs[g.K_d]:
            s_B.rotate(-1, dt)
        if key_inputs[g.K_w]:
            s_B.accel(dt)
        if key_inputs[g.K_t]:
            if s_B.energy > s_B.attack_energy and s_B.current_cooldown <= 0:
                create_projectile(s_B, s_B.projectile, s_A)
                s_B.attack()
                if not getChannelBusy(2):
                    playSfx(s_B.sounds["firing"], 2)

        # update
        for proj in projectiles:
            proj.update_pos(dt)
            proj.home_on_target()
            expired = proj.update_expiration(dt)
            if expired:
                projectiles.remove(proj)
            else:
                for ship in ships:
                    collided = proj.check_collision(ship)
                    if collided:
                        ship.damage(proj.damage)
                        projectiles.remove(proj)
                        
                        if ship == s_A:
                            if not getChannelBusy(3):
                                playSfx(ship.sounds["damage"], 3)
                        else:
                            if not getChannelBusy(4):
                                playSfx(ship.sounds["damage"], 4)
                                
                        break
                
        for ship in ships:
            ship.update_pos(dt)
            ship.update_energy(dt)

        # render
        mw.blit(background, [0,0])
        
        for ship in ships:
            screen_pos = w2s(ship.pos) - np.array([8, 8])
            mw.blit(ship.get_texture(), screen_pos)

        for proj in projectiles:
            screen_pos = w2s(proj.pos)
            mw.blit(proj.get_texture(), screen_pos)

        mw.blit(panel, [0,0])
        crew_lights_A = max(int(s_A.crew/15),0)
        crew_lights_B = max(int(s_B.crew/15),0)
        energy_lights_A = max(int(s_A.energy/50),0)
        energy_lights_B = max(int(s_B.energy/50),0)

        for i in range(crew_lights_A):
            light_pos = [14 + i*16, 428]
            mw.blit(A_light, light_pos)

        for i in range(crew_lights_B):
            light_pos = [14 + i*16, 438]
            mw.blit(B_light, light_pos)

        for i in range(energy_lights_A):
            light_pos = [446 + i*16, 428]
            mw.blit(A_light, light_pos)

        for i in range(energy_lights_B):
            light_pos = [446 + i*16, 438]
            mw.blit(B_light, light_pos)

        if s_A.crew <= 0 and s_B.crew > 0:
            print("Player B wins!")
            g.time.wait(5000)
            game_active = False
        elif s_A.crew > 0 and s_B.crew <= 0:
            print("Player A wins!")
            g.time.wait(5000)
            game_active = False
        elif s_A.crew <= 0 and s_B.crew <= 0:
            print("Everybody dies!")
            g.time.wait(5000)
            game_active = False

        g.display.update()

        if game_tick % 100 == 0:
            pass
            #print(s_A.energy)
            
        g.time.wait(20)
        game_tick += 1
        game_time += dt

main()
g.quit()
