"""
Modes:
    the more notes the player hits, the more points they get
    practice - a slider for slowdown of the music & percent of notes player hits
Music volume slider
Sound effects
Animation
Images
Cross platform compatibility
"""

import pygame
from sys import exit as end

songs = {1: 'Music/Hot Cross Buns.mp3', 2: 'Music/TwinkleTwinkleLittleStar.mp3', 3: 'Music/HappyBirthday.mp3',
         4: 'Music/JingleBells.wav', 5: 'Music/FurElise.mp3'}
# Pygame start up
pygame.init()
screen = pygame.display.set_mode([799, 500], pygame.RESIZABLE)
screen.fill('dark gray')
clock = pygame.time.Clock()
volume = 0.2


class Button(pygame.sprite.Sprite):
    # the center of the button, text, color of sprite, color of text, image path, dimensions (if there is an image path)
    def __init__(self, pos: tuple[int | float] | list[int | float],
                 mode_c: str,
                 text=None,
                 text_size=None, *,
                 color=(150, 150, 150),
                 tcolor='black', path='',
                 dim=(), alpha=255) -> None:
        """
        :param pos: The position of the center of the button
        :param mode_c: When clicked, the button will return this parameter
        :param text: The text the button will display (text is the size of the button)
        :param text_size: The size of the text the button displays (controls the size of the button)
        :param color: The color of the background of the button
        :param tcolor: The color of the text the button displays
        :param path: The image path
        :param dim: The size of the image
        :param alpha: The alpha value of alpha
        """
        super().__init__()
        self.pos, self.text, self.tcolor, self.mode_c, self.ts = pos, text, tcolor, mode_c, text_size
        if path:  # needs to have 'path' and 'dim'
            self.image = pygame.transform.scale(pygame.image.load(path), dim)  # resizes the image to 'dim'
        else:  # needs to have 'text' and 'text_size'
            self.rect = pygame.font.Font("Fonts/Roboto-Light.ttf", self.ts).render(
                str(self.text), True, self.tcolor).get_rect()
            dim = self.rect.bottomright[0] - self.rect.topleft[0] + 20, self.rect.bottomright[1] - self.rect.topleft[
                1] + 20
            self.image = pygame.Surface(dim).convert_alpha()
            self.image.fill((color[0], color[1], color[2], alpha))
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

    def update(self) -> None:
        text = pygame.font.Font("Fonts/Roboto-Light.ttf", self.ts).render(str(self.text), True, self.tcolor)
        screen.blit(text, text.get_rect(center=self.rect.center))


class ScrollBar(pygame.sprite.Sprite):
    def __init__(self, start_p, end_p, dim, color_front, color_back, orientation='vertical') -> None:
        """
        Scroll bar is currently composed of a background rect and a slider which can be moved by scrolling

        :param start_p: The starting position of the background rect is (the minimum horizontal/vertical position of the
        scroll bar)
        :param end_p: Similar to start_p but the end position instead
        :param dim: Dimension of the slider
        :param color_front: Color of the slider
        :param color_back: Color of the background rect
        :param orientation: The axis the scroll bar moves when scrolling
        """
        super().__init__()
        self.start_pos, self.end_pos, self.dim, self.orientation = start_p, end_p, dim, orientation
        self.back_color = color_back
        self.image = pygame.Surface(dim)
        self.image.fill(color_front)
        self.rect = self.image.get_rect()
        self.rect.topleft = start_p
        self.back_rect = pygame.Rect(self.start_pos, [self.end_pos[0] - self.start_pos[0],
                                                      self.end_pos[1] - self.start_pos[1]])
        self.step_size = None

    def update(self, move=None, screen_change=False) -> None | float | int:
        if move is not None:
            original = self.rect.topleft
            if self.orientation == 'vertical':
                self.rect.topleft = self.rect.topleft[0], self.rect.topleft[1] + move  # these are tuples
            else:
                self.rect.topleft = self.rect.topleft[0] + move, self.rect.topleft[1]
            self.check_slider_pos()
            index = 1 if self.orientation == 'vertical' else 0
            return abs(self.rect.topleft[index] - original[index])
        if screen_change:
            self.back_rect = pygame.Rect(self.start_pos, self.end_pos)
        pygame.draw.rect(screen, self.back_color, self.back_rect)

    def check_slider_pos(self):
        if self.orientation == 'vertical':
            if self.rect.bottomright[1] > self.end_pos[1]:
                self.rect.bottomright = self.rect.bottomright[0], self.end_pos[1]
            elif self.rect.topleft[1] < self.start_pos[1]:
                self.rect.topleft = self.rect.topleft[0], self.start_pos[1]
        else:
            if self.rect.bottomright[0] > self.end_pos[0]:
                self.rect.bottomright = self.end_pos[0], self.rect.bottomright[1]
            elif self.rect.topleft[0] < self.start_pos[0]:
                self.rect.topleft = self.start_pos[0], self.rect.topleft[1]

    def click_drag(self, clicked_pos) -> float | int | None:
        """
        :param clicked_pos: where the mouse clicked
        :return: What the variable 'up' will be in level selection
        """
        index = 0 if self.orientation == 'horizontal' else 1
        if index == 0:
            self.rect.center = clicked_pos[0], self.rect.center[1]
        else:
            self.rect.center = self.rect.center[0], clicked_pos[1]
        self.check_slider_pos()
        if self.step_size:
            return (self.rect.topleft[index] - self.start_pos[index]) / self.step_size
        else:
            return None


def main():
    global full_screen
    mode = "intro"
    while True:  # Playing >> End screen
        print(mode)
        if mode == "intro":
            mode = intro()
        elif mode == 'level selection':
            mode = level_select()
        elif mode == 'options':
            mode = options()
        elif type(mode) is int:
            mode = level(mode)
        elif isinstance(mode, tuple):
            mode = outro(mode)


def intro():
    while True:
        intro_g = pygame.sprite.Group()
        intro_l = [
            Button([screen.get_width() // 2, screen.get_height() // 2 - 50], '', 'A Random Piano Game', 50),
            Button([screen.get_width() // 2, screen.get_height() // 2 + 50], 'level selection', 'Play', 30),
            Button([screen.get_width() // 2, screen.get_height() // 2 + 100], 'options', 'Options', 30)
        ]
        intro_g.add(intro_l)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(len(intro_g.sprites())):
                        s = intro_g.sprites()[i]
                        pos = pygame.mouse.get_pos()
                        if s.rect.collidepoint(pos[0], pos[1]) and intro_l[i].mode_c:
                            return intro_l[i].mode_c
        screen.fill('light gray')
        intro_g.draw(screen)
        intro_g.update()
        pygame.display.update()


def options():
    global volume
    sound_slider = ScrollBar([50, 160], [screen.get_width()-50, 180], [20, 20], 'black', 'dark gray')
    sliders = pygame.sprite.Group(sound_slider)
    UIs=[Button([screen.get_width() / 2, 50], '', 'Options', 50),
        Button([screen.get_width() / 2, 125], '', 'Volume', 30)]
    others=pygame.sprite.Group(UIs)
    mouse_down = False
    while True:
        screen.fill('light gray')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                end()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_pos = pygame.mouse.get_pos()
                    if sound_slider.back_rect.collidepoint(clicked_pos):
                        sound_slider.click_drag(clicked_pos)
                    if sound_slider.rect.collidepoint(clicked_pos):
                        sound_slider.click_drag(clicked_pos)
                        mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "intro"
        if mouse_down:
            sound_slider.click_drag(pygame.mouse.get_pos())
        sliders.update()
        sliders.draw(screen)
        others.draw(screen)
        others.update()
        pygame.display.update()


def level_select():
    up = 0
    slider = ScrollBar([0, 100], [10, screen.get_height()], [10, 50], 'black', 'dark gray')
    slider_g = pygame.sprite.GroupSingle(slider)
    velocity = 0
    last_time = pygame.time.get_ticks()
    framerate = 30
    others_g = pygame.sprite.Group()
    others_l = [
        Button([screen.get_width() / 2, 50], '', 'Click On a Level', 50),
    ]
    level_select_g = pygame.sprite.Group()
    level_select_l = []
    for _i in range(50):
        _i += 1
        try:
            directory = songs[_i]
            name = directory[directory.find("/") + 1:directory.find(".")]
        except KeyError:
            name = 0
        level_select_l.append(
            Button([screen.get_width() / 2, _i * 60 + 65 - up], _i, name, 30)
        )
    total_len = level_select_l[-1].rect.bottom - level_select_l[0].rect.top - screen.get_height() + 100
    index = 1 if slider.orientation == 'vertical' else 0
    slider_step_size = (slider.end_pos[index] - slider.start_pos[index] - slider.dim[index]) / total_len
    slider.step_size = slider_step_size
    others_g.add(others_l)
    level_select_g.add(level_select_l)
    mouse_down = False
    while True:
        dt = (pygame.time.get_ticks() - last_time) / 1000
        dt *= 60
        last_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                end()
            elif event.type == pygame.VIDEORESIZE:
                slider.end_pos = [10, screen.get_height()]
                slider.update(screen_change=True)
                total_len = level_select_l[-1].rect.bottom - level_select_l[0].rect.top - screen.get_height() + 100
                index = 1 if slider.orientation == 'vertical' else 0
                slider_step_size = (slider.end_pos[index] - slider.start_pos[index] - slider.dim[index]) / total_len
                slider.step_size = slider_step_size
                others_l[0].rect.center = [screen.get_width() / 2, 50]
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'intro'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_pos = pygame.mouse.get_pos()
                    for i in range(len(level_select_g.sprites())):
                        s = level_select_g.sprites()[i]
                        if s.rect.collidepoint(clicked_pos) and level_select_l[i].mode_c:
                            return level_select_l[i].mode_c
                    if slider.back_rect.collidepoint(clicked_pos):
                        mouse_down = True
                        up = slider.click_drag(clicked_pos)
                        # slider.rect.center = slider.rect.center[0], clicked_pos[1]
                        # up = (slider.rect.topleft[1]-slider.start_pos[1])/slider_step_size
                elif event.button == 4:
                    velocity -= dt * 4
                elif event.button == 5:
                    velocity += dt * 4
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
        if mouse_down:
            up = slider.click_drag(pygame.mouse.get_pos())
        if total_len > 0:
            velocity *= .9
            if abs(velocity) < 1:
                velocity = 0
            up += velocity
            if up < 0:
                up = 0
                velocity = 0
            elif up > total_len:
                up = total_len
                velocity = 0
            slider.rect.topleft = slider.rect.topleft[0], up * slider_step_size + slider.start_pos[1]
        else:
            up = 0
        for i, sprite in enumerate(level_select_l):
            sprite.rect.center = screen.get_width() / 2, (i + 1) * 60 + 65 - up
        screen.fill('light gray')
        level_select_g.draw(screen)
        level_select_g.update()
        pygame.draw.rect(screen, 'light gray', (0, 0, screen.get_width(), 95))
        others_g.draw(screen)
        others_g.update()
        if total_len > 0:
            slider_g.update()
            slider_g.draw(screen)
        pygame.display.update()
        clock.tick(framerate)


def level(which: int) -> tuple[int, float] | str:
    global full_screen
    colors = [(255, 0, 0, 100), (255, 165, 0, 100), (255, 255, 0, 100), (0, 255, 0, 100), (0, 255, 255, 100),
              (0, 0, 255, 100),
              (255, 0, 255, 100)]
    note_numbers = {'q': 0, 'w': 1, 'e': 2, 'r': 3, 't': 4, 'y': 5, 'u': 6, 'i': 7, 'o': 8, 'p': 9}
    keys = {'q': 113, 'w': 119, 'e': 101, 'r': 114, 't': 116, 'y': 121, 'u': 117, 'i': 105, 'o': 111,
            'p': 112}
    holds: dict[str, None | float] = {'q': None, 'w': None, 'e': None, 'r': None, 't': None, 'y': None,
                                      'u': None, 'i': None, 'o': None, 'p': None}
    dt = 0
    notes = note_extractor(which)
    correct_hits = 0
    total_hits = 0
    last_time = pygame.time.get_ticks()
    framerate = 30
    first = True
    pygame.mixer.music.set_volume(volume)

    def all_note_cycle():  # note GFX
        nonlocal notes
        current_color = 0
        notes_copy = notes[:]
        notes_copy.reverse()
        for note in notes_copy:  # check list representing note
            if note[2] <= 0 <= note[2] + note[1]:
                color = (0, 255, 0, 255)  # green-clickable
            else:
                color = colors[current_color]
                current_color += 1
                if current_color == len(colors):
                    current_color = 0
            if holds[note[0]] == 0 and note[2] <= 0 <= note[2] + note[1] and note[3]:
                color = (255, 0, 0, 255)
            draw_rect_alpha(screen, color, (
                note_numbers[note[0]] * screen.get_width() / 10, screen.get_height() * .8 - note[2] - note[1],
                screen.get_width() / 10, note[1]))
            note[2] -= dt  # decrease time>>note fall down.

    while True:
        line_level = int(screen.get_height() * .8)
        screen.fill('dark gray')
        pygame.draw.line(screen, 'black', (0, line_level), (screen.get_width(), line_level))
        dt = (pygame.time.get_ticks() - last_time) / 1000
        dt *= 60
        if first: dt = 0
        last_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return 'level selection'
                if first:
                    pygame.mixer.music.load(songs[which])
                    pygame.mixer.music.play()
                    first = False
                clicked = False
                for i in notes:  # i = note
                    if i[2] <= 0 <= i[2] + i[1]:  # if key in range
                        if event.key == keys[i[0]]:  # the target note is held
                            clicked = True
                            if i[3]:
                                holds[i[0]] = i[1] * .5
                            else:
                                notes.remove(i)
                                total_hits += 1
                                correct_hits += 1
                    else:  # it is a note that is not the lowest so don't check the rest
                        break
                if not clicked:
                    print('failure')
                    total_hits += 1
            elif event.type == pygame.KEYUP:
                for i in notes:
                    if i[2] <= 0 <= i[2] + i[1] and i[3]:  # if in colliding range
                        try:  #
                            if event.key == keys[i[0]] and holds[i[0]] <= 0 and i[3]:
                                total_hits += 1
                                correct_hits += 1
                                holds[i[0]] = None
                                notes.remove(i)
                        except Exception as e:
                            if isinstance(e, TypeError):
                                print(e, i, holds)
        if len(notes) == 0:  # check if finished song
            pygame.mixer.music.stop()
            return which, correct_hits / total_hits * 100
        if 0 > notes[0][2] + notes[0][1]:
            # note is going to go off-screen this event can be triggered after removal of a note
            print('fail')
            total_hits += 1
            notes.pop(0)
        for a in holds.keys():
            if type(holds[a]) is float:  # is being held
                if holds[a] > 0:
                    holds[a] -= dt
                else:
                    holds[a] = 0
        all_note_cycle()
        for i in ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']:
            make_text((note_numbers[i] + .5) * screen.get_width() / 10, screen.get_height() * .9, i.upper())
        try:
            make_text(screen.get_width() / 2, 20, int(correct_hits / total_hits * 100))
        except ZeroDivisionError:
            make_text(screen.get_width() / 2, 20, 0)
        pygame.display.update()
        clock.tick(framerate)


def outro(variables):  # variable = [level number, score]
    outro_g = pygame.sprite.Group()
    directory = songs[variables[0]]
    outro_l = [Button([screen.get_width() / 2, screen.get_height() // 2 + 50], variables[0], 'Play again', 30),
               Button([screen.get_width() / 2, screen.get_height() // 2 - 50], '',
                      f'You scored {variables[1]:.2f}% on {directory[directory.find("/") + 1:directory.find(".")]}',
                      30),
               Button([screen.get_width() / 2, screen.get_height() // 2 + 110], 'level selection',
                      'Return to level selection', 30)]
    outro_g.add(outro_l)
    print(outro_l)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                end()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'level selection'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(len(outro_g.sprites())):
                        s = outro_g.sprites()[i]
                        pos = pygame.mouse.get_pos()
                        if s.rect.collidepoint(pos[0], pos[1]) and outro_l[i].mode_c:
                            return outro_l[i].mode_c
        screen.fill('light gray')
        outro_g.draw(screen)
        outro_g.update()
        pygame.display.update()


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def note_extractor(which_level) -> list[list[str, float, float, bool]]:
    """
    :return: list[list[note, length of note, dist. from bottom, if needs to be held], ...]
    """
    with open(f'MachineNotes/{which_level}.txt') as f:
        machine_notes: list[str] = f.read().strip('][').replace("'", '').split(', ')
    multi = 1
    notes = []
    hold_threshold = 1
    dist_from_bottom = 0
    for line in machine_notes:  # a#-#
        if line[0] == 'm':
            multi = eval(line[1:line.find('-')])
        elif line[0] in ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']:
            leng = float(line[1:line.find("-")]) * multi
            notes.append([line[0], leng * 60, dist_from_bottom, leng > hold_threshold])
            leng = float(line[line.find("-") + 1:]) * multi
            dist_from_bottom += leng * 60
        else:  # line[0] is space
            leng = float(line[1:line.find("-")]) * multi
            dist_from_bottom += leng * 60
    return notes


def make_text(x, y, what):
    text = pygame.font.Font('Fonts/Roboto-Light.ttf', 30).render(str(what), True, 'blue')
    screen.blit(text, text.get_rect(center=(x, y)))


if __name__ == "__main__":
    main()
