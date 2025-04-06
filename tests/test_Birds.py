# test_bird.py

"""
here I create a dummy in each function to make sure there will be no problems,
I understand that this leads to a dry violation,
but I am so sure that nothing will break for sure
"""

from Birds import Bird
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))


def test_bird_initialization(dummy_sprite_sheet):
    bird = Bird(
        value=10, x=100, y=200, speed=2, hp=3,
        DirectionTimeChange=1.0,
        right=True, left=False, up=True, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )

    assert bird.x == 100
    assert bird.y == 200
    assert bird.hp == 3
    assert bird.alive is True
    assert bird.sprite_sheet == dummy_sprite_sheet


def test_bird_kill(dummy_sprite_sheet):
    bird = Bird(
        value=10, x=100, y=200, speed=2, hp=3,
        DirectionTimeChange=1.0,
        right=False, left=False, up=False, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )
    bird.kill()
    assert bird.alive is False


def test_check_collision(dummy_sprite_sheet):
    bird = Bird(
        value=10, x=50, y=50, speed=2, hp=3,
        DirectionTimeChange=1.0,
        right=False, left=False, up=False, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )
    inside_point = (55, 55)
    outside_point = (10, 10)
    assert bird.check_collision(inside_point) is True
    assert bird.check_collision(outside_point) is None


def test_update_position_changes(dummy_sprite_sheet):
    bird = Bird(
        value=10, x=100, y=100, speed=1, hp=3,
        DirectionTimeChange=0,
        right=True, left=False, up=False, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )
    bird.update()
    assert bird.x < 100
