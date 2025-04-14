# test_bird.py

"""
here I create a dummy in each function to make sure there will be no problems,
I understand that this leads to a dry violation,
but I am so sure that nothing will break for sure
"""
import sys
import os
import pytest
from unittest import mock

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))
from Birds import Bird


@pytest.mark.unit
@pytest.mark.parametrize("x, y, hp", [
    (100, 200, 3),
    (50, 75, 1),
    (0, 0, 0)
])
def test_bird_initialization(dummy_sprite_sheet, x, y, hp):
    bird = Bird(
        value=10, x=x, y=y, speed=2, hp=hp,
        DirectionTimeChange=1.0,
        right=True, left=False, up=True, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )

    assert bird.x == x
    assert bird.y == y
    assert bird.hp == hp
    assert bird.alive is True
    assert bird.sprite_sheet == dummy_sprite_sheet


@pytest.mark.unit
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


@pytest.mark.unit
@pytest.mark.parametrize("point, expected", [
    ((55, 55), True),
    ((10, 10), None),
])
def test_check_collision(dummy_sprite_sheet, point, expected):
    bird = Bird(
        value=10, x=50, y=50, speed=2, hp=3,
        DirectionTimeChange=1.0,
        right=False, left=False, up=False, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )
    result = bird.check_collision(point)
    assert result is expected


@pytest.mark.unit
@mock.patch('Birds.time.time', return_value=1000.0)
@mock.patch('Birds.random.choice', return_value=1)
def test_update_position_changes(mock_choice, mock_time, dummy_sprite_sheet):
    bird = Bird(
        value=10, x=100, y=100, speed=1, hp=3,
        DirectionTimeChange=0,  # to force change
        right=True, left=False, up=False, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )
    bird.update()
    assert bird.x < 100
    assert bird.DirChoice == 1


@pytest.mark.slow
@mock.patch('Birds.time.time', return_value=1000.0)
def test_dead_bird_falls_faster(mock_time, dummy_sprite_sheet):
    bird = Bird(
        value=10, x=100, y=100, speed=1, hp=3,
        DirectionTimeChange=1.0,
        right=False, left=False, up=False, down=False,
        sprite_sheet=dummy_sprite_sheet,
        SpritePerRow=4, SpriteWidth=32, SpriteHeight=32
    )
    bird.kill()
    initial_y = bird.y
    bird.update()
    assert bird.y > initial_y  # Bird falls down
