# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_a


def a_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


class Auto_run:

    @staticmethod
    def enter(boy):
        boy.frame = 0
        if boy.action == 3:
            boy.action = 1
        elif boy.action == 2:
            boy.action = 0
        boy.start_time = get_time()
        print('autorun Enter')
        pass

    @staticmethod
    def exit(boy):
        print('autorun Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if boy.action == 1:
            boy.x = boy.x + 1
        elif boy.action == 0:
            boy.x = boy.x - 1
        if boy.x > 800:
            boy.action = 0
        elif boy.x < 0:
            boy.action = 1

        if get_time() - boy.start_time > 5 :
            boy.state_machine.handle_event(('TIME_OUT' , 0))
        print('autorun Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class Idle:

    @staticmethod
    def enter(boy):
        Boy.frame = 0
        boy.action = 3
        print('Idle Enter')
        pass

    @staticmethod
    def exit(boy):
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
            Idle: {a_key_down: Auto_run},
            Auto_run: {time_out: Idle}
        }

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.boy)

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
