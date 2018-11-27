import random
import pygame

# 屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60
# 敌机定时器常量
ENEMY_EVENT = pygame.USEREVENT


class GameSprite(pygame.sprite.Sprite):
    """飞机精灵类"""

    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    """游戏背景类"""

    def __init__(self, is_alt=False):

        # 调用父类方法
        super().__init__("./images/background.png")
        # 判断是否为交替图像
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 1、背景图像移动
        super().update()
        # 2、判断图像是否移出屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):

    def __init__(self):
        # 1、调用父类创建敌机精灵，指定图片
        super().__init__("./images/enemy0.png")
        # 2、指定敌机的初始速度1-3
        self.speed = random.randint(1, 3)
        # 3、指定敌机的初始位置
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.rect.bottom = 0

    def update(self):
        # 1、调用父类方法
        super().update()
        # 2、判断是否飞出屏幕，如果是则从精灵组中删除
        if self.rect.y >= SCREEN_RECT.height:
            print("飞出屏幕")
            self.kill()

    def __del__(self):
        # print("敌机销毁 %s" % self.rect)
        pass


class Hero(GameSprite):
    """英雄精灵类"""
    def __init__(self):
        super().__init__("./images/hero1.png",0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0 :
            self.rect.x = SCREEN_RECT.x
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        # print("发射子弹")
        # 一次发射3颗子弹
        for i in (1,2,3):
            bullet = Bullet()
            bullet.rect.bottom = self.rect.y - 30 * i
            bullet.rect.centerx = self.rect.centerx
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵类"""
    def __init__(self):
        super().__init__("./images/bullet2.png",-2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        # print("子弹销毁")
        pass
