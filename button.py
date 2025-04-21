import pygame

class Button:

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.button_pressed = False

    def checkPressed(self):

        mouse_pos =  pygame.mouse.get_pos()
        left_clicked = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos) and not self.button_pressed:
            if left_clicked:
                self.button_pressed = True
                return True

        if not left_clicked:
            self.button_pressed = False

    def draw(self, surface):

        surface.blit(self.image, (self.rect.x, self.rect.y))

class Switch(Button):

    def __init__(self, x, y, image, image2, state):
        super().__init__(x, y, image)
        self.image2 = image2
        self.state = state

    def draw(self, surface):
        if self.state:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        else:
            surface.blit(self.image2, (self.rect.x, self.rect.y))

    def checkPressed(self, surface):

        mouse_pos =  pygame.mouse.get_pos()
        left_clicked = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos) and not self.button_pressed:
            if left_clicked:
                self.button_pressed = True
                self.state = not self.state
                self.draw(surface)
                return True

        if not left_clicked:
            self.button_pressed = False

class TextInput(Button):

    def __init__(self, x, y, image, selected_image):
        super().__init__(x, y, image)
        self.box_selected = False
        self.selected_image = selected_image

    def checkSelected(self):

        mouse_pos =  pygame.mouse.get_pos()
        left_clicked = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos) and not self.button_pressed:
            if left_clicked:
                self.box_selected = True
                self.button_pressed = True

        elif left_clicked:
            self.box_selected = False

        if not left_clicked:
            self.button_pressed = False

        return self.box_selected

    def draw(self, screen):
        if self.box_selected:
            screen.blit(self.selected_image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))
