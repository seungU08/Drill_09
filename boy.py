# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_a, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP


def a_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Run:

    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.action = 1
        elif left_down(e) or right_up(e):
            boy.action = 0

        pass

    @staticmethod
    def exit(boy,e):
        print('run Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if boy.action == 1:
            boy.x = boy.x + 1
        elif boy.action == 0:
            boy.x = boy.x - 1

        print('run Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Auto_run:

    @staticmethod
    def enter(boy,e):
        boy.frame = 0
        if boy.action == 3:
            boy.action = 1
        elif boy.action == 2:
            boy.action = 0
        boy.start_time = get_time()
        print('autorun Enter')
        pass

    @staticmethod
    def exit(boy,e):
        print('autorun Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if boy.action == 1:
            boy.x = boy.x + 10
        elif boy.action == 0:
            boy.x = boy.x - 10

        if boy.x > 800:
            boy.action = 0
        elif boy.x < 0:
            boy.action = 1

        if get_time() - boy.start_time > 5:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        print('autorun Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y+40, 200, 200)


class Idle:

    @staticmethod
    def enter(boy,e):
        Boy.frame = 0
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        print('Idle Enter')
        pass

    @staticmethod
    def exit(boy,e):
        print('Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('Idle Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.table = {
            Idle: {a_key_down: Auto_run, right_down: Run, left_down: Run, right_up: Run, left_up: Run},
            Auto_run: {time_out: Idle, right_down: Run, left_down: Run, right_up: Run, left_up: Run},
            Run: {a_key_down: Auto_run, right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle}
        }

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy,e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy,e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.boy,0)

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
