import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import  GameStats
from button import Button
from scoreboard import Scoreboard
import game_function as gf

from config_json import  Config

def run_game():
    #初始化pygame 设置和对象
    pygame.init()
    ai_settings = Settings()
    config_js = Config(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #创建Play按钮
    play_button = Button(ai_settings,screen,"Play")


    #创建一个用于存储游戏统计信息的实例,创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)


    #创建一艘飞船
    ship = Ship(ai_settings,screen)

    #创建一个用于存储子弹和外星人的编组
    bullets = Group()
    aliens = Group()

    #创建一个外星人�?
    # alien = Alien(ai_settings,screen)
    gf.create_fleet(ai_settings,screen,ship,aliens)

    #开始游戏主循环
    while True:
        #监视键盘和鼠标事�?
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullents(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)
        
        
run_game()
