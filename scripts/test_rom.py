#!/usr/bin/env python3
"""Exercise the real ROM with PyBoy; assert visible UI state, not source code."""
from pathlib import Path
import sys
from pyboy import PyBoy

rom = Path(sys.argv[1] if len(sys.argv) > 1 else 'build/dash-duel.gbc')
raw = rom.read_bytes()
assert len(raw) == 32768, 'Unexpected ROM size'
assert raw[0x143] == 0xC0, 'Expected Game Boy Color-only ROM'
checksum = 0
for value in raw[0x134:0x14D]:
    checksum = (checksum - value - 1) & 255
assert checksum == raw[0x14D], 'Invalid header checksum'

def row(p, y):
    return ''.join(chr(p.memory[0x9800 + y * 32 + x] + 32) for x in range(20))

def start(p):
    p.button_press('start')
    p.tick(10)
    p.button_release('start')
    p.tick(180)
    assert 'GO!' in row(p, 16), row(p, 16)

def press_pair(p, buttons, frames=6):
    for b in buttons:
        p.button_press(b)
    p.tick(frames)
    for b in buttons:
        p.button_release(b)

p = PyBoy(str(rom), window='null')
p.set_emulation_speed(0)
try:
    p.tick(120)
    assert 'DASH // DUEL' in row(p, 0)
    assert 'START TO RACE' in row(p, 16)
    start(p)
    # A held input must not keep accelerating either runner.
    press_pair(p, ['left', 'a'], 180)
    assert row(p, 5)[2:5] == '000' and row(p, 5)[12:15] == '000'
    p.tick(1)
    # Equal alternating inputs finish together.
    for i in range(130):
        press_pair(p, ['right', 'b'] if i % 2 == 0 else ['left', 'a'])
    assert 'TIE!' in row(p, 16), row(p, 16)
    assert row(p, 5)[2:5] == '100' and row(p, 5)[12:15] == '100'
    start(p)
    # Faster P1 cadence must win, while allowing P2 to finish too.
    for i in range(360):
        buttons = ['left' if i % 2 == 0 else 'right']
        if i % 2 == 0:
            buttons.append('a' if (i // 2) % 2 == 0 else 'b')
        press_pair(p, buttons)
        if 'WINS!' in row(p, 16):
            break
    assert 'P1 WINS!' in row(p, 16), row(p, 16)
    p.screen.image.save(rom.parent / 'gameplay-test.png')
    start(p)
    p.stop(save=False)
    p = PyBoy(str(rom), window='null')
    p.set_emulation_speed(0)
    p.tick(120)
    for title in ('JAVELIN THROW', 'SHOT PUT'):
        press_pair(p, ['select'], 5)
        p.tick(60)
        assert title in row(p, 1), row(p, 1)
        press_pair(p, ['start'], 30)
        for player in range(2):
            for i in range(20):
                press_pair(p, ['a'] if i % 2 == 0 else ['b'], 6)
            p.tick(120)
            assert 'A:THROW' in row(p, 16), row(p, 16)
            press_pair(p, ['a'], 5)
            p.tick(90)
            if player == 0:
                assert 'NEXT PLAYER' in row(p, 16), row(p, 16)
                press_pair(p, ['start'], 30)
            else:
                assert 'TIE!' in row(p, 16) or 'WINS!' in row(p, 16), row(p, 16)
        p.screen.image.save(rom.parent / ('javelin-test.png' if title == 'JAVELIN THROW' else 'shot-put-test.png'))
    print('PASS: sprint, held inputs, tie, win, rematch, javelin and shot put')
finally:
    p.stop(save=False)
