from pygame import image, Rect
import pygame
from unittest import mock


pygame.init()
pygame.display.set_mode((800, 600))


def draw(surface):
    img = image.load('../images/tiles.xpm')
    surface.blit(img, Rect((0, 0, 32, 32)), Rect((0, 0, 32, 32)))
    pygame.display.update()


@mock.patch('pygame.display.update')
def test_mocking(mock_update):
    display = pygame.display.get_surface()
    draw(display)
    assert mock_update.called is True
    assert mock_update.call_count == 1


def test_bad_mocks():
    mo = mock.MagicMock()
    assert mo.twenty_blue_dolphins()
    assert mo.foo.bar('spam')['eggs']
    assert mo.was_called()  # wrong method that passes
    assert mo.caled         # typo that passes!


def test_blit():
    mock_surf = mock.MagicMock(name='surface')
    draw(mock_surf)
    assert mock_surf.blit.called is True
