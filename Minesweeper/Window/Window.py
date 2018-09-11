import pygame
from pygame.locals import *
import math

class Window:
	def __init__(self, x_dim, y_dim):
		self.x_dim = x_dim
		self.y_dim = y_dim
		self.SPACE_PIXELS = 32
		self.MARGIN = 8
		self.HEADER_BAR = self.SPACE_PIXELS * 3
		self.WIDTH = self.SPACE_PIXELS*x_dim + 2 * self.MARGIN
		self.HEIGHT = self.SPACE_PIXELS*y_dim + 2 * self.MARGIN + self.HEADER_BAR
		pygame.init()
		pygame.font.init()

		self._screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		self._gameScreen = self._screen.subsurface(Rect(self.MARGIN, self.HEADER_BAR + self.MARGIN, self.SPACE_PIXELS*x_dim, self.SPACE_PIXELS*y_dim))
		self._reset = self._screen.subsurface(Rect(self.MARGIN, self.MARGIN, self.SPACE_PIXELS*6, self.HEADER_BAR-self.MARGIN))
		self._screen.fill(Color('light grey'))
		self._gameScreen.fill(Color('black'))

		pygame.display.flip()

		pygame.display.set_caption("BitSweeper")
		self.clock = pygame.time.Clock()

	@property
	def gameScreen(self):
		return self._gameScreen

	@gameScreen.setter
	def setGameScreen(self, appSurface):
		""" Adds appSurface as a subsurface to screen """
		self._screen.subsurface(appSurface)

	def onClick(self, event):
		x,y = event.pos
		print((x,y))
		x_game, y_game = (math.floor((x-self.MARGIN)/self.SPACE_PIXELS), math.floor((y-self.MARGIN-self.HEADER_BAR)/self.SPACE_PIXELS))
		if not (0 <= x_game <= self.x_dim-1 and 0 <= y_game <= self.y_dim-1): 
			x_min,y_min = self._reset.get_abs_offset()
			x_reset_size, y_reset_size = self._reset.get_size()
			(x_max, y_max) = (x_min + x_reset_size, y_min + y_reset_size) 
			print([(x_min, y_min), (x, y), (x_max, y_max)])
			if (x_min <= x <= x_max) and (y_min <= y <= y_max):
				print ('RESETTING')
				return 'RESET'
			return 
		return pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (x_game, y_game), 'button': event.button})
	
import time

def main():
	win = Window(20,20)
	time.sleep(5)
	pygame.quit()

if __name__ == '__main__': main()