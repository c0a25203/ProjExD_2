import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    x, y = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        x = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        y = False
    return x, y

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        old_kk_rct = kk_rct.copy()
        for key, mv in DELTA.items():
            if key_lst[key]:
                kk_rct.move_ip(mv)
        x, y = check_bound(kk_rct)
        if not x:
            kk_rct.x = old_kk_rct.x
        if not y:
            kk_rct.y = old_kk_rct.y
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        x, y = check_bound(bb_rct)
        if not x:
            vx *= -1
        if not y:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
