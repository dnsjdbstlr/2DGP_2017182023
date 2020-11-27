from pico2d import *
from FRAMEWORK import Base
from INGAME.Mob import Mob
from INGAME.Map import Map
from INGAME.Character import Character
import UI

# 선언
mob = []
map = Map()
chr = Character()

def eventHandler(e):
    if e.type == SDL_QUIT or (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        Base.running = False

    # 캐릭터 이벤트처리
    chr.eventHandler(e)

    # UI 이벤트처리
    UI.eventHandler(e)

def update():
    chr.update(Base.delta_time)
    for i in mob:
        if chr.state == 'idle':
            i.hitBy = 'none'
        i.update(Base.delta_time)

def draw():
    map.draw()
    for i in mob: i.draw()
    chr.draw()
    UI.draw()

def enter():
    chr.load()
    map.load()
    UI.load()
    loadMob()

def loadMob():
    file = open('../res/Map/' + str(map.id) + '.txt', 'r')
    mobInfo = file.readlines()
    file.close()

    for i in mobInfo:
        temp = i.split()
        if temp[0] == 'm':
            type = (int(temp[1]), int(temp[2]))
            pos = (int(temp[3]), int(temp[4]))
            if type == (0, 0):
                mob.append(Mob(100, *pos))
            elif type == (1, 0):
                mob.append(Mob(101, *pos))
            elif type == (2, 0):
                mob.append(Mob(102, *pos))
    for i in mob: i.load()

def chr_collide_check():
    for tile in map.tileRect:
        # x, y, dx, dy
        dx, dy = chr.dx, chr.dy
        RESULT = [False, 0, 0, dx, dy]

        # 머리 부딪히는 조건
        # 1. 히트박스의 좌,우 중에 하나라도 해당 지형의 폭 사이에 있어야한다.
        # 2. 히트박스의 상단 + 탐색 범위가 지형의 높이 사이에 있어야한다.
        # 3. 지형의 모양이 사각형이여야한다.
        # 4. 캐릭터가 위로 점프 중이여야한다.
        if (tile[0] < chr.hitBox[0] < tile[2] or tile[0] < chr.hitBox[2] < tile[2]) and \
            tile[3] <= chr.hitBox[1] + dy <= tile[1] != tile[3] and dy > 0:
            RESULT = [True, RESULT[1], RESULT[2] + tile[3] - (abs(chr.hitBox[1] - chr.hitBox[3]) / 2), RESULT[3], 0]

        # 좌측 부딪히는 조건
        # 1. 히트박스의 상, 하 중에 하나라도 해당 지형의 높이 사이에 있어야한다.
        # 2. 히트박스의 좌측 + 탐색 범위가 지형의 오른쪽끝보다 왼쪽에 있고,
        #    히트박스의 좌측이 지형의 오른쪽 끝보단 오른쪽에 있어야한다.
        # 3. 또는 히트박스의 우측이 지형의 폭 사이에 있어야한다.
        # 4. 캐릭터가 좌측으로 이동 중이여야한다.
        if (tile[3] < chr.hitBox[1] < tile[1] or tile[3] < chr.hitBox[3] < tile[1]) and \
            (min(chr.hitBox[0], chr.hitBox[2]) + dx <= tile[2] <= min(chr.hitBox[0], chr.hitBox[2]) or tile[0] < min(chr.hitBox[0], chr.hitBox[2]) + dx < tile[2]) and dx < 0:
            if (chr.state == 'run' or chr.state == 'slide') and chr.subState == 'none':
                RESULT = [True, RESULT[1] + tile[2] + abs(chr.hitBox[0] - chr.hitBox[2]) - dx, RESULT[2], RESULT[3], RESULT[4]]
            else:
                RESULT = [True, RESULT[1] + tile[2] + abs(chr.hitBox[0] - chr.hitBox[2]) + dx, RESULT[2], RESULT[3], RESULT[4]]

        # 우측 부딪히는 조건 :: 좌측과 같음
        if (tile[3] < chr.hitBox[1] < tile[1] or tile[3] < chr.hitBox[3] < tile[1]) and \
            (max(chr.hitBox[0], chr.hitBox[2]) <= tile[0] <= max(chr.hitBox[0], chr.hitBox[2]) + dx or tile[0] < max(chr.hitBox[0], chr.hitBox[2]) + dx < tile[2]) and dx > 0:
            if (chr.state == 'run' or chr.state == 'slide') and chr.subState == 'none':
                RESULT = [True, RESULT[1] + tile[0] - abs(chr.hitBox[0] - chr.hitBox[2]) - dx, RESULT[2], RESULT[3], RESULT[4]]
            else:
                RESULT = [True, RESULT[1] + tile[0] - abs(chr.hitBox[0] - chr.hitBox[2]) + dx, RESULT[2], RESULT[3], RESULT[4]]

        # 맵 밖으로 못나가게
        if min(chr.hitBox[0], chr.hitBox[2]) + dx < 0 and chr.dir == 'LEFT':
            if (chr.state == 'run' or chr.state == 'slide') and chr.subState == 'none':
                RESULT = [True, abs(chr.hitBox[0] - chr.hitBox[2]) - dx, RESULT[2], 0, RESULT[4]]
            else:
                RESULT = [True, RESULT[1] + chr.MOTION_HITBOX[chr.subState][0], RESULT[2], 0, RESULT[4]]

        elif map.size[0] < max(chr.hitBox[0], chr.hitBox[2]) + dx:
            if (chr.state == 'run' or chr.state == 'slide') and chr.subState == 'none':
                RESULT = [True, map.size[0] - abs(chr.hitBox[0] - chr.hitBox[2]) - dx, RESULT[2], 0, RESULT[4]]
            else:
                RESULT = [True, map.size[0] - chr.MOTION_HITBOX[chr.subState][0], RESULT[2], 0, RESULT[4]]
        if RESULT[0]: return RESULT
    return [False]

def chr_landing_check():
    for tile in map.tileRect:
        # 바닥 도착 조건
        # 1. 히트박스의 좌, 우 중에 하나라도 해당 지형의 폭 사이에 있어야한다.
        # 2. 히트박스의 하단 + dy <= 지형의 상단 <= 히트박스의 하단이여야한다.
        if (tile[0] < chr.hitBox[0] < tile[2] or tile[0] < chr.hitBox[2] < tile[2]) and \
            chr.hitBox[3] + chr.dy <= tile[1] <= chr.hitBox[3]:
            return True, tile[1] + abs(chr.MOTION_HITBOX[chr.state][3])
    return [False]

def chr_portal_check():
    for portal in map.portalRect:
        PASS = False
        if chr.hitBox[2] < portal[0]: PASS = True
        if chr.hitBox[3] > portal[1]: PASS = True
        if chr.hitBox[0] > portal[2]: PASS = True
        if chr.hitBox[1] < portal[3]: PASS = True
        if not PASS:
            # if chr is in destination
            if map.id == portal[4]:
                chr.subState = 'jump2'
                chr.x, chr.y = portal[5], portal[6]
            else:
                # 유물 :: 조개화석
                for r in chr.relic:
                    if r.id == 108:
                        r.stack = 1
                        r.isActive = True

                map.id = portal[4]
                map.tileRect.clear()
                map.portalRect.clear()
                map.load()

                mob.clear()
                loadMob()

                chr.subState = 'jump2'
                chr.x, chr.y = portal[5], portal[6]
                chr.dx, chr.dy = 0, 0
            return

def chr_interaction_check():
    for obj in map.objectRect:
        if obj[0] <= chr.x <= obj[2] and obj[3] <= chr.y - 10 <= obj[1]:
            return obj[4], obj[5], (obj[0] + obj[2]) / 2, (obj[1] + obj[3]) / 2
    return -1

def mob_hit_check(hitBox):
    HIT = False
    if chr.attack_range == (0, 0, 0, 0):
        return [False]
    
    # 몬스터의 피격 범위의 한 점이 캐릭터의 공격 범위 안에 있을 경우
    left = min(chr.attack_range[0], chr.attack_range[2])
    right = max(chr.attack_range[0], chr.attack_range[2])
    top = max(chr.attack_range[1], chr.attack_range[3])
    bottom = min(chr.attack_range[1], chr.attack_range[3])
    if left < hitBox[0] < right and bottom < hitBox[1] < top: HIT = True
    if left < hitBox[2] < right and bottom < hitBox[1] < top: HIT = True
    if left < hitBox[0] < right and bottom < hitBox[3] < top: HIT = True
    if left < hitBox[2] < right and bottom < hitBox[3] < top: HIT = True

    # 몬스터의 피격 범위 안에 캐릭터의 공격 범위가 있을 경우
    mLeft = min(hitBox[0], hitBox[2])
    mRight = max(hitBox[0], hitBox[2])
    mTop = max(hitBox[1], hitBox[3])
    mBot = min(hitBox[1], hitBox[3])
    if mLeft < left < mRight and mLeft < right < mRight and \
        mBot < top < mTop and mBot < bottom < mTop:
        HIT = True

    if HIT:
        return [True, chr.state, chr.ad]
    return [False]

def mob_landing_check(hitBox, x, dy):
    for tile in map.tileRect:
        if (tile[0] < hitBox[0] < tile[2] or tile[0] < hitBox[2] < tile[2] or tile[0] < x < tile[2]) and \
            hitBox[3] + dy * 2 <= tile[1] <= hitBox[3]:
            return True, tile[1] + abs(hitBox[1] - hitBox[3])
    return [False]

def mob_collide_check(mob):
    hitBox = mob.hitBox
    dx, dy = mob.dx, mob.dy

    for tile in map.tileRect:
        RESULT = [False, 0, 0, dx, dy]

        # 머리
        if (tile[0] < hitBox[0] < tile[2] or tile[0] < hitBox[2] < tile[2]) and \
            tile[3] <= hitBox[1] + dy <= tile[1] != tile[3] and dy > 0:
            RESULT = [True, RESULT[1], RESULT[2] + tile[3] - (abs(hitBox[1] - hitBox[3]) / 2), RESULT[3], 0]

        # 좌측
        elif (tile[3] < hitBox[1] < tile[1] or tile[3] < hitBox[3] < tile[1]) and \
             (min(hitBox[0], hitBox[2]) + dx < tile[2] < min(hitBox[0], hitBox[2]) or
              tile[0] < min(hitBox[0], hitBox[2]) + dx < tile[2]) and dx < 0:
            RESULT = [True, RESULT[1] + tile[2] + (abs(hitBox[0] - hitBox[2]) / 2), RESULT[2], RESULT[3], RESULT[4]]

        # 우측
        elif (tile[3] < hitBox[1] < tile[1] or tile[3] < hitBox[3] < tile[1]) and \
             (max(hitBox[0], hitBox[2]) < tile[0] < max(hitBox[0], hitBox[2]) + dx or
              tile[0] < max(hitBox[0], hitBox[2]) + dx < tile[2]) and dx > 0:
            RESULT = [True, RESULT[1] + tile[0] - (abs(hitBox[0] - hitBox[2]) / 2), RESULT[2], RESULT[3], RESULT[4]]

        # 맵밖으로 나가는 것 체크
        if max(hitBox[0], hitBox[2]) + dx >= map.size[0] and mob.dir == 'RIGHT':
            RESULT = [True, map.size[0] - (abs(hitBox[0] - hitBox[2]) / 2), RESULT[2], RESULT[3], RESULT[4]]
        elif min(hitBox[0], hitBox[2]) - dx <= 0 and mob.dir == 'LEFT':
            RESULT = [True, abs(hitBox[0] - hitBox[2]) / 2, RESULT[2], RESULT[3], RESULT[4]]

        if RESULT[0]: return RESULT
    return [False]