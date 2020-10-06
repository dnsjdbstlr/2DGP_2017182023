from pico2d import *
from Map import Map

PATH = '../res/'
map = Map()

# 모션별 딜레이
MOTION_DELAY = {
    'idle': 15,
    'run': 10,
    'jump': 4,
    'attack1': 15,
    'attack2': 10,
    'attack3': 10,
    'air_attack1' : 5,
    'air_attack2' : 10
}

# 모션별 프레임 수
MOTION_FRAME = {
    'idle': 4,
    'run': 6,
    'jump': 10,
    'attack1': 3,
    'attack2': 8,
    'attack3': 6,
    'air_attack1': 4,
    'air_attack2': 4
}

# 모션별 히트박스
MOTION_HITBOX = {
    'idle': (6, 37 / 2 - 7, -5, -37 / 2),
    'run': (0, 37 / 2 - 7, -11, -37 / 2),
    'jump': (5, 5, -7, -9),
    'jump2': (5, 5, -7, -9),
    'attack1': (5, 37 / 2 - 15, -5, -37 / 2),
    'attack2': (5, 37 / 2 - 13, -5, -37 / 2),
    'attack3': (5, 37 / 2 - 13, -5, -37 / 2),
    'air_attack1': (8, 37 / 2 - 15, -2, -37 / 2),
    'air_attack2': (5, 37 / 2 - 13, -5, -37 / 2)
}

# 달리기 입력 무시
RUN_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2'
)

# 점프 입력 무시
JUMP_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2'
)

# 공격 입력 무시
ATTACK1_EXCEPTION = (
    'attack1', 'attack2', 'attack3',
    'air_attack1', 'air_attack2'
)

class Character:
    # 50x37
    def __init__(self):
        # 디버그
        map.load_map('100')

        self.leftKeyDown = False
        self.rightKeyDown = False

        self.state = 'idle'             # 상태
        self.subState = 'jump'          # 중복 가능 상태
        self.frame = 0                  # 프레임
        self.timer = 0                  # 점프 최신화 주기
        self.dir = 'RIGHT'              # 좌우
        self.hitBox = ()                # 히트박스
        self.x, self.y = 400, 200       # 좌표
        self.dx, self. dy = 0, 0        # 움직이는 속도
        self.image = load_image(PATH + 'adventurer-v1.5-Sheet.png')

    def draw(self):
        # 점프
        if self.subState == 'jump' or self.subState == 'jump2':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['jump'] % 7 * 50, 37 * 13 - (self.frame // MOTION_DELAY['jump'] // 7 * 37), 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['jump'] % 7 * 50, 37 * 13 - (self.frame // MOTION_DELAY['jump'] // 7 * 37), 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 대기
        elif self.state == 'idle':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['idle'] * 50, 555, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['idle'] * 50, 37 * 15, 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 달리기
        elif self.state == 'run':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['run'] * 50 + 50, 37 * 14, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['run'] * 50 + 50, 37 * 14, 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 일반공격1
        elif self.state == 'attack1':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['attack1'] * 50, 37 * 9, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['attack1'] * 50, 37 * 9, 50, 37,
                                               0, 'h', self.x, self.y, 50, 37)
        # 일반공격2
        elif self.state == 'attack2':
            if self.dir == 'RIGHT':
                if self.frame // MOTION_DELAY['attack2'] < 4:
                    self.image.clip_draw(self.frame // MOTION_DELAY['attack2'] * 50 + 50 * 3, 37 * 9, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // MOTION_DELAY['attack2'] - 4) * 50, 37 * 8, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                if self.frame // MOTION_DELAY['attack2'] < 4:
                    self.image.clip_composite_draw(self.frame // MOTION_DELAY['attack2'] * 50 + 50 * 3, 37 * 9, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // MOTION_DELAY['attack2'] - 4) * 50, 37 * 8, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)
        # 일반공격3
        elif self.state == 'attack3':
            if self.dir == 'RIGHT':
                if self.frame // MOTION_DELAY['attack3'] < 3:
                    self.image.clip_draw(self.frame // MOTION_DELAY['attack3'] * 50 + 50 * 4, 37 * 8, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // MOTION_DELAY['attack3'] - 3) * 50, 37 * 7, 50, 37, self.x, self.y)
            elif self.dir == 'LEFT':
                if self.frame // MOTION_DELAY['attack3'] < 3:
                    self.image.clip_composite_draw(self.frame // MOTION_DELAY['attack3'] * 50 + 50 * 4, 37 * 8, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // MOTION_DELAY['attack3'] - 3) * 50, 37 * 7, 50, 37,
                                                   0, 'h', self.x, self.y, 50, 37)

        # 공중공격
        elif self.state == 'air_attack1':
            if self.dir == 'RIGHT':
                if self.frame // MOTION_DELAY['air_attack1'] < 3:
                    self.image.clip_draw(self.frame // MOTION_DELAY['air_attack1'] * 50 + 50 * 4, 37, 50, 37, self.x, self.y)
                else:
                    self.image.clip_draw((self.frame // MOTION_DELAY['air_attack1'] - 3) * 50, 0, 50, 37, self.x, self.y)
            else:
                if self.frame // MOTION_DELAY['air_attack1'] < 3:
                    self.image.clip_composite_draw(self.frame // MOTION_DELAY['air_attack1'] * 50 + 50 * 4, 37, 50, 37, 0, 'h', self.x, self.y, 50, 37)
                else:
                    self.image.clip_composite_draw((self.frame // MOTION_DELAY['air_attack1'] - 3) * 50, 0, 50, 37, 0, 'h', self.x, self.y, 50, 37)

        # 공중공격 마무리
        elif self.state == 'air_attack2':
            if self.dir == 'RIGHT':
                self.image.clip_draw(self.frame // MOTION_DELAY['air_attack2'] * 50, 0, 50, 37, self.x, self.y)
            else:
                self.image.clip_composite_draw(self.frame // MOTION_DELAY['air_attack2'] * 50, 0, 50, 37, 0, 'h', self.x, self.y, 50, 37)

    def update(self, delta_time):
        # 히트박스 업데이트
        self.updateHitBox()
        #draw_rectangle(*self.hitBox)

        # 대기
        if self.state == 'idle':
            if self.rightKeyDown:
                self.state = 'run'
                self.dir = 'RIGHT'
                if not map.isCrashed(self.hitBox, self.dx, self.dy)[0]:
                    self.dx = 2
            elif self.leftKeyDown:
                self.state = 'run'
                self.dir = 'LEFT'
                if not map.isCrashed(self.hitBox, self.dx, self.dy)[0]:
                    self.dx = -2
            else:
                # If it doesn't exist, frame goes up twice when I jump.
                if self.subState == 'none':
                    self.frame += 1
                if self.frame >= MOTION_FRAME['idle'] * MOTION_DELAY['idle']:
                    self.frame = 0
        # 달리기
        elif self.state == 'run' and self.subState == 'none':
            self.frame += 1

            if self.frame >= MOTION_FRAME['run'] * MOTION_DELAY['run']:
                self.frame = 0

            # Fallen Check
            isLanded = map.isLanded(self.hitBox, self.dy)
            if not isLanded[0]:
                self.subState = 'jump'
                self.frame = 0

        # 공격
        elif self.state == 'attack1':
            self.frame += 1
            if self.frame >= MOTION_FRAME['attack1'] * MOTION_DELAY['attack1']:
                self.frame = 0
                self.state = 'idle'
        elif self.state == 'attack2':
            self.frame += 1
            if self.frame >= MOTION_FRAME['attack2'] * MOTION_DELAY['attack2']:
                self.frame = 0
                self.state = 'idle'
        elif self.state == 'attack3':
            self.frame += 1
            if self.frame >= MOTION_FRAME['attack3'] * MOTION_DELAY['attack3']:
                self.frame = 0
                self.state = 'idle'

        # 공중공격
        elif self.state == 'air_attack1':
            self.frame += 1
            self.dy -= 0.05

            # Frame Repeat
            if self.frame >= (MOTION_FRAME['air_attack1'] - 1) * MOTION_DELAY['air_attack1']:
                self.frame = MOTION_DELAY['air_attack1']

            # Landing Check
            isLanded = map.isLanded(self.hitBox, self.dy)
            if isLanded[0]:
                self.state = 'air_attack2'
                self.frame, self.dy = 0, 0
                self.y = isLanded[1]

        elif self.state == 'air_attack2':
            self.frame += 1
            if self.frame >= MOTION_FRAME['air_attack2'] * MOTION_DELAY['air_attack2']:
                self.state = 'idle'
                self.frame = 0

        # 점프
        if self.subState == 'jump' or self.subState == 'jump2':
            self.frame += 1

            # update Cycle
            self.timer += delta_time
            if self.timer > delta_time * 5:
                self.dy -= 2
                self.timer = 0

            # Frame Fix
            if self.frame > (MOTION_FRAME['jump'] - 1) * MOTION_DELAY['jump']:
                self.frame = (MOTION_FRAME['jump'] - 1) * MOTION_DELAY['jump']

            # Landing Check
            isLanded = map.isLanded(self.hitBox, self.dy)
            if isLanded[0]:
                self.state = 'idle'
                self.subState = 'none'
                self.frame = 0
                self.dy = 0
                self.y = isLanded[1]
            else:
                # keep going if now pressing button
                if self.leftKeyDown:
                    self.dx = -2
                elif self.rightKeyDown:
                    self.dx = 2

        # Crash Check
        isCrashed = map.isCrashed(self.hitBox, self.dx, self.dy)
        if isCrashed[0]:
            if isCrashed[1] != 0: self.x = isCrashed[1]
            if isCrashed[2] != 0: self.y = isCrashed[2]
            self.dx, self.dy = isCrashed[3], isCrashed[4]

        # Chr Pos Update
        self.x += self.dx
        self.y += self.dy

    def eventHandler(self, e):
        # 점프
        if (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.state not in JUMP_EXCEPTION and self.subState == 'none':
            self.subState = 'jump'
            self.frame, self.timer = 0, 0
            self.y, self.dy = self.y + 10, 6

        # 더블점프
        elif (e.key, e.type) == (SDLK_c, SDL_KEYDOWN) and self.subState == 'jump':
            self.subState = 'jump2'
            self.frame, self.timer = 0, 0
            self.y, self.dy = self.y + 5, 5


        # 왼쪽 달리기
        elif (e.key, e.type) == (SDLK_LEFT, SDL_KEYDOWN):
            self.leftKeyDown = True
            if self.state not in RUN_EXCEPTION:
                self.dir = 'LEFT'
                self.state = 'run'
                self.dx = -2

        elif (e.key, e.type) == (SDLK_LEFT, SDL_KEYUP):
            self.leftKeyDown = False
            if self.state not in RUN_EXCEPTION:
                self.state = 'idle'
                self.dx = 0

        # 오른쪽 달리기
        elif (e.key, e.type) == (SDLK_RIGHT, SDL_KEYDOWN):
            self.rightKeyDown = True
            if self.state not in RUN_EXCEPTION:
                self.dir = 'RIGHT'
                self.state = 'run'
                self.dx = 2

        elif (e.key, e.type) == (SDLK_RIGHT, SDL_KEYUP):
            self.rightKeyDown = False
            if self.state not in RUN_EXCEPTION:
                self.state = 'idle'
                self.dx = 0

        # 기본공격 1타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state not in ATTACK1_EXCEPTION and self.subState == 'none':
            self.state = 'attack1'
            self.frame, self.dx = 0, 0

        # 기본공격 2타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state == 'attack1' and self.frame >= (MOTION_FRAME['attack1'] - 0.8) * MOTION_DELAY['attack1']:
            self.state = 'attack2'
            self.frame = 0

        # 기본공격 3타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and self.state == 'attack2' and self.frame >= (MOTION_FRAME['attack2'] - 2) * MOTION_DELAY['attack2']:
            self.state = 'attack3'
            self.frame = 0

        # 공중공격 1타
        elif (e.key, e.type) == (SDLK_x, SDL_KEYDOWN) and (self.subState == 'jump' or self.subState == 'jump2'):
            self.state, self.subState = 'air_attack1', 'none'
            self.frame, self.dx, self.dy = 0, 0, -4

    def updateHitBox(self):
        if self.dir == 'RIGHT':
            if self.subState == 'jump' or self.subState == 'jump2':
                self.hitBox = (self.x - MOTION_HITBOX[self.subState][0], self.y + MOTION_HITBOX[self.subState][1],
                               self.x - MOTION_HITBOX[self.subState][2], self.y + MOTION_HITBOX[self.subState][3])
            else:
                self.hitBox = (self.x - MOTION_HITBOX[self.state][0], self.y + MOTION_HITBOX[self.state][1],
                               self.x - MOTION_HITBOX[self.state][2], self.y + MOTION_HITBOX[self.state][3])
        else:
            if self.subState == 'jump' or self.subState == 'jump2':
                self.hitBox = (self.x - MOTION_HITBOX[self.subState][0], self.y + MOTION_HITBOX[self.subState][1],
                               self.x - MOTION_HITBOX[self.subState][2], self.y + MOTION_HITBOX[self.subState][3])
            else:
                self.hitBox = (self.x + MOTION_HITBOX[self.state][0], self.y + MOTION_HITBOX[self.state][1],
                               self.x + MOTION_HITBOX[self.state][2], self.y + MOTION_HITBOX[self.state][3])