import os
import sys
import pygame as pg
import random
import time


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


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する。

    引数:
        screen: ゲーム画面のSurface

    戻り値:
        なし
    """
    black = pg.Surface((WIDTH, HEIGHT))
    black.fill((0, 0, 0))
    black.set_alpha(150)
    font = pg.font.Font(None, 80)
    gameover_img = font.render("Game Over", True, (255, 255, 255))

    kk_img = pg.transform.rotozoom(
        pg.image.load("fig/8.png"), 0, 0.9
    )
    kkl_rct = kk_img.get_rect()
    kkl_rct.center = (WIDTH // 2 - 190, HEIGHT // 2)

    kkr_rct = kk_img.get_rect()
    kkr_rct.center = (WIDTH // 2 + 190, HEIGHT // 2)
      
    black.blit(gameover_img, gameover_img.get_rect( 
        center=(WIDTH // 2, HEIGHT // 2) 
    )) 

    black.blit(kk_img, kkl_rct)
    black.blit(kk_img, kkr_rct)

    screen.blit(black, (0, 0))
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の大きさと加速度のリストを作成する。

    戻り値:
    爆弾Surfaceのリストと加速度のリスト
    """
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        pg.draw.circle(bb_img,(255, 0, 0),(10 * r, 10 * r),10 * r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動方向に対応したこうかとん画像の辞書を作成する。

    戻り値:
        移動量タプルをキー、こうかとん画像Surfaceを値とする辞書
    """
    kk_img = pg.image.load("fig/3.png")

    kk_dict = {
    (0, 0): pg.transform.rotozoom(kk_img, 0, 0.9),
    (+5, 0): pg.transform.rotozoom(kk_img, 180, 0.9),   # 右
    (+5, -5): pg.transform.rotozoom(kk_img, 135, 0.9),  # 右上
    (0, -5): pg.transform.rotozoom(kk_img, 270, 0.9),   # 上
    (-5, -5): pg.transform.rotozoom(kk_img, 315, 0.9),  # 左上
    (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9),     # 左
    (-5, +5): pg.transform.rotozoom(kk_img, 45, 0.9),   # 左下
    (0, +5): pg.transform.rotozoom(kk_img, 90, 0.9),    # 下
    (+5, +5): pg.transform.rotozoom(kk_img, 225, 0.9),  # 右下
}

    return kk_dict

kk_imgs = get_kk_imgs()
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

    bb_imgs, bb_accs = init_bb_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_img = kk_imgs[tuple(sum_mv)]
        old_kk_rct = kk_rct.copy()
        kk_rct.move_ip(sum_mv)
        
        x, y = check_bound(kk_rct)
        if not x:
            kk_rct.x = old_kk_rct.x
        if not y:
            kk_rct.y = old_kk_rct.y
        screen.blit(kk_img, kk_rct)
        
        avx = vx * bb_accs[min(tmr // 500, 9)]
        avy = vy * bb_accs[min(tmr // 500, 9)]

        bb_img = bb_imgs[min(tmr // 500, 9)]

        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height

        bb_rct.move_ip(avx, avy)
        x, y = check_bound(bb_rct)
        if not x:
            vx *= -1
        if not y:
            vy *= -1
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
