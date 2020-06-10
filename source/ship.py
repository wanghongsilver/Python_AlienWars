import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """飞船类创建"""
    def __init__(self,ai_settings,screen):
        """初始化飞船并设置其初始位置"""
        super(Ship,self).__init__()
        self.screen = screen

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('../images/myship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings

        #将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)
        #移动标志
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and (self.rect.centerx < self.ai_settings.screen_width):\
            self.center += self.ai_settings.ship_speed_factor
             
        if self.moving_left and (self.rect.centerx > 0):
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.center = self.screen_rect.centerx