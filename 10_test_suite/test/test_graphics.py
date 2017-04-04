from maze_run.draw_maze import draw_grid
from maze_run.__main__ import pygame, Rect, handle_key
from maze_run.__main__ import tile_img, tiles, maze
from unittest import mock


def draw(surface):
    # prepare the maze and draw the graphics
    img = draw_grid(maze, tile_img, tiles)
    surface.blit(img, Rect((0, 0, 384, 224)), Rect((0, 0, 384, 224)))
    pygame.display.update()


@mock.patch('pygame.display.update')
def test_mocking(mock_update):
    handle_key(275)
    assert mock_update.called is True
    assert mock_update.call_count == 1


@mock.patch('pygame.display.update')
def test_bad_mocks(mock_update):
    assert mock_update.twenty_blue_dolphins()
    assert mock_update.caled    # !!! passes


def test_blit():
    mock_surf = mock.MagicMock(name='surface')
    draw(mock_surf)
    assert mock_surf.blit.called is True
