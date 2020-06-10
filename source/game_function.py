import sys
import os

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from button import  Button

def check_keydown_events(event,ai_settings,screen,stats,ship,bullets):
    """响应按下按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        stats.fire_bullet_flag = True

    elif event.key == pygame.K_q:
        sys.exit(0)


def fire_bullet(ai_settings,screen,ship,bullets):
    """"如果还没有到限制，发射一颗子弹"""
    if len(bullets) < ai_settings.bullet_allowed:
        newbullet = Bullet(ai_settings, screen, ship)
        bullets.add(newbullet)


def check_keyup_events(event,stats,ship):
    """响应松开按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE:
        stats.fire_bullet_flag = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        # print(event)
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,stats,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,stats,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """在玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and (not stats.game_active):
        #重置游戏设置
        ai_settings.initialize_dynamic_setting()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群外星人，并且飞船居中
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()


def update_screen(ai_settings,screen,stats,sb,ship,ailens,bullets,play_button):
    """更新屏幕上的图像，并切换到主屏幕"""
    #每次循环时都重绘制屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所以子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    ailens.draw(screen)
    # ailen.blitme()
    sb.show_score()

    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()


    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullents(ai_settings,screen,stats,sb,ship,aliens,bullets):

    if stats.fire_bullet_flag == True:
        # 创建一颗子弹，加入编组bullet中
        fire_bullet(ai_settings, screen, ship, bullets)

    """更新子弹的位置，并且删除消失的子弹"""
    bullets.update()

    #删除已消失的子弹 到达底部的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        # print(len(bullets))

    check_bullet_alien_collision(ai_settings, screen, stats,sb,ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹和外星人碰撞"""
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        #存在一个子弹消灭多个外星人，查询val  确定
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        # 删除现有的子弹并且新建一群外星人 加快游戏节奏 提高等级
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens(ai_settings, alien_width):
    """根据屏幕大小获得外星人的数目"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def get_numbet_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """获得单个外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度

    alien = Alien(ai_settings,screen)
    number_alien_x = get_number_aliens(ai_settings,alien.rect.width)
    number_row = get_numbet_rows(ai_settings,ship.rect.height,alien.rect.height)
    number_row -= 3

    #创建一群外星人
    for row_number in range(1,number_row):
        for alien_number in range(number_alien_x):
            #创建一个外星人并将其加入当前行
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘的时候采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_dirction(ai_settings,aliens)
            break

def change_fleet_dirction(ai_settings,aliens):
    """将整个外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        #将ship_left 减一
        stats.ships_left -=1

        #更新飞船计数排
        sb.prep_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    print(stats.game_active)

    #清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    #创建一群新的外星人和子弹列表
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()

    #暂停
    sleep(0.5)

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """检查外星人是否到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)

    #检测外星人是否到达屏幕底端
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)

def check_high_score(stats,sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


