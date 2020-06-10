#对于配置文件读取和保存
import json

class Config():
    """建立配置文件类"""

    def __init__(self,ai_settings):
        """初始化"""
        self.config = {}
        self.config_screen = {}
        self.config_ship = {}
        self.config_bullet = {}
        self.config_alien = {}
        self.high_score = {}

        self.config['screen'] = self.config_screen
        self.config['ship'] = self.config_ship
        self.config['bullet'] = self.config_bullet
        self.config['alien'] = self.config_alien
        self.config['highscore'] = self.high_score

        self.updatedic(ai_settings)

        #读取配置文件
        self.read_config()
        self.updatepara(ai_settings)

    def updatedic(self,ai_settings):
        # 初始化config 字典
        self.updatedic_screen(ai_settings)
        self.updatedic_ship(ai_settings)
        self.updatedic_bullet(ai_settings)
        self.updatedic_alien(ai_settings)

    def updatedic_screen(self,ai_setting):
        """屏幕字典"""
        # 屏幕的设置
        self.config_screen['screen_width'] = ai_setting.screen_width
        self.config_screen['screen_height'] = ai_setting.screen_height
        self.config_screen['bg_color'] = ai_setting.bg_color

    def updatedic_ship(self,ai_setting):
        """飞船字典"""
        # 飞船的设置
        self.config_ship['ship_speed_factor'] = ai_setting.ship_speed_factor
        self.config_ship['ship_limit'] = ai_setting.ship_limit

    def updatedic_bullet(self,ai_setting):
        """子弹字典"""
        # 子弹设置
        self.config_bullet['bullet_speed_factor'] = ai_setting.bullet_speed_factor
        self.config_bullet['bullet_width'] = ai_setting.bullet_width
        self.config_bullet['bullet_height'] = ai_setting.bullet_height
        self.config_bullet['bullet_color'] = ai_setting.bullet_color
        self.config_bullet['bullet_allowed'] = ai_setting.bullet_allowed

    def updatedic_alien(self,ai_setting):
        """外星人字典"""
        # 外星人设置
        # 转到屏幕后外星人下降的速度
        self.config_alien['fleet_drop_speed'] = ai_setting.fleet_drop_speed

        # 以什么样的速度加快游戏节奏
        self.config_alien['speedup_scale'] = ai_setting.speedup_scale
        # 外星人点数提高速度
        self.config_alien['score_scale'] = ai_setting.score_scale

        # 计分
        self.config_alien['alien_points'] = ai_setting.alien_points

        self.config_alien['ship_speed_factor'] = ai_setting.ship_speed_factor
        self.config_alien['bullet_speed_factor'] = ai_setting.bullet_speed_factor
        self.config_alien['alien_speed_factor'] = ai_setting.alien_speed_factor

        # 外星人移动方向：1向右移动，-1向左移动
        self.config_alien['fleet_direction'] = ai_setting.fleet_direction

    def updatepara(self,ai_settings):
        self.updatepara_screen(ai_settings)
        self.updatepara_ship(ai_settings)
        self.updatepara_bullet(ai_settings)
        self.updatepara_alien(ai_settings)

    def updatepara_screen(self,ai_setting):
        """屏幕字典"""
        # 屏幕的设置
        ai_setting.screen_width = self.config['screen']['screen_width']
        ai_setting.screen_height = self.config['screen']['screen_height']
        ai_setting.bg_color = self.config['screen']['bg_color']

    def updatepara_ship(self,ai_setting):
        """飞船字典"""
        # 飞船的设置
        ai_setting.ship_speed_factor = self.config['ship']['ship_speed_factor']
        ai_setting.ship_limit = self.config['ship']['ship_limit']

    def updatepara_bullet(self,ai_setting):
        """子弹字典"""
        # 子弹设置
        ai_setting.bullet_speed_factor = self.config['bullet']['bullet_speed_factor']
        ai_setting.bullet_width = self.config['bullet']['bullet_width']
        ai_setting.bullet_height = self.config['bullet']['bullet_height']
        ai_setting.bullet_color = self.config['bullet']['bullet_color']
        ai_setting.bullet_allowed = self.config['bullet']['bullet_allowed']

    def updatepara_alien(self,ai_setting):
        """外星人字典"""
        # 外星人设置
        # 转到屏幕后外星人下降的速度
        ai_setting.fleet_drop_speed = self.config['alien']['fleet_drop_speed']

        # 以什么样的速度加快游戏节奏
        ai_setting.speedup_scale = self.config['alien']['speedup_scale']
        # 外星人点数提高速度
        ai_setting.score_scale = self.config['alien']['score_scale']

        # 计分
        ai_setting.alien_points = self.config['alien']['alien_points']

        ai_setting.ship_speed_factor = self.config['alien']['ship_speed_factor']
        ai_setting.bullet_speed_factor = self.config['alien']['bullet_speed_factor']
        ai_setting.alien_speed_factor = self.config['alien']['alien_speed_factor']

        # 外星人移动方向：1向右移动，-1向左移动
        ai_setting.fleet_direction = self.config['alien']['fleet_direction']

    def read_config(self):
        """获得配置"""
        filename = '../config/config.json'
        try:
            with open(filename) as f_obj:
                self.config = json.load(f_obj)
        except:
            self.updata_config()
            # update_high_score()
        else:
            print(self.config)


    def updata_config(self):
        """创建配置文件，加载初始化信息"""

        filename = 'config.json'
        with open(filename,'w') as f_obj:
            json.dump(self.config,f_obj)







