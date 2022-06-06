import pygame

class Button():
    def __init__(self, ai_class, msg, x = 0, y = 0):
        self.screen = ai_class.screen
        self.screen_rect = ai_class.screen.get_rect()

        self.width, self.height = (200, 50)

        self.button_color = (25, 101, 224)
        self.text_color = (0, 0, 0)
        
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.rect.center = self.screen_rect.center
        
        if not x == 0:
            self.rect.x = x
        if not y == 0:
            self.rect.y = y

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Text():
    def __init__(self, ai_class, text, color = (0, 0, 0), font = None, font_size = 48, x = 0, y = 0):
        self.screen = ai_class.screen
        self.screen_rect = ai_class.screen_rect

        self.font = pygame.font.SysFont(font, font_size)
        self.text_color = color

        self.update_text(text)
        self._set_text(x ,y)
    
    def update_text(self, text):
        self.text_image = self.font.render(text, True, self.text_color)

    def _set_text(self, x ,y):
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.screen_rect.center

        if not x == 0:
            self.text_image_rect.x = x
        if not y == 0:
            self.text_image_rect.y = y

    def draw_text(self):
        self.screen.blit(self.text_image, self.text_image_rect)