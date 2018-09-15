
from pygame import font, display, time, image
from pygame.locals import Color
from Minesweeper.Minefield import Minefield
from Minesweeper.Graphics.Window import Window
from Minesweeper.Graphics.Drawer import Drawer
import os
import math

class Minesweeper:
	def __init__(self, x=9, y=9, mines=10):		
		"""
		Minesweeper class controls the execution of the game
		
		**Args**:
				*x*: number of x squares (default 9)
				*y*: number of y squares (default 9)
				*mines*: number of mines (default 10)
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				None.
		
		**Returns**:
				None.
		"""
		self.x_dim = x
		self.y_dim = y
		self.n_mines = mines

		self.flagCounter = self.n_mines
		self.gameTimer = 0
		self.timeOfLastTimeUpdate = 0
		self.timeOfLastReset = time.get_ticks()

		self.SPACE_WIDTH = 32
		self.SPACE_HEIGHT = 32
		self.WIDTH = self.SPACE_WIDTH*self.x_dim
		self.HEIGHT = self.SPACE_HEIGHT*self.y_dim

		self.drawer = Drawer()
		self.drawButton = self.drawer.drawButton

		self.minefield = Minefield(self.x_dim, self.y_dim, self.n_mines)
		self.grid = self.minefield.minefield

		self.window = Window(self.x_dim, self.y_dim)
		self.screen = self.window._gameScreen
		self.reset_element = self.window._reset
		self.reset_flag = False
		self.timer_element = self.window._timer
		self.flag_element = self.window._flagCounter
		#Images
		self.imageRevealed = image.load('Minesweeper/assets/gridSpace_revealed.png').convert()
		self.imageUnrevealed = image.load("Minesweeper/assets/gridSpace.png").convert()
		self.imageFlag = image.load("Minesweeper/assets/flag.png").convert_alpha()
		self.imageMine = image.load("Minesweeper/assets/mine.png").convert_alpha()

		
		
	def onClick(self, event):
		"""
		Click event handler
		
		**Args**:
				*event*: Event object, event.pos is the grid position, button is 1 for left, 3 for right mouse button
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				None.
		
		**Returns**:
				*(gameOver, win)*: tuple of booleans, as named 
		"""
		newEvent = self.window.onClick(event)
		(gameOver, win) = False, False

		if newEvent is None:
			return gameOver, newEvent

		if newEvent.button == -1:
			self.reset_flag = True
			gameOver = True
			win = None
			return gameOver, win
		
		activeSpace = self.minefield.getSpace(newEvent.pos[0],newEvent.pos[1])
		if activeSpace.isRevealed:
			pass
		elif event.button == 1:
			if activeSpace.isFlagged :
				self.flagCounter = self.flagCounter + 1
			if self.minefield.reveal(newEvent.pos[0],newEvent.pos[1]):
				self.render()
				gameOver = True
				return gameOver, win
		elif event.button == 3:
			if not activeSpace.isRevealed:
				if not activeSpace.isFlagged:
					if self.flagCounter == 0:
						return gameOver, win
					self.flagCounter = self.flagCounter - 1
					self.minefield.toggleFlag(newEvent.pos[0],newEvent.pos[1])
					if self.flagCounter == 0:
						isDone = self.minefield.checkFlags()
						if isDone == True:
							gameOver = True
							win = True
							return gameOver, win
				else:
					self.flagCounter = self.flagCounter + 1
					self.minefield.toggleFlag(newEvent.pos[0],newEvent.pos[1])
				
		return gameOver, win

	def render(self):
		"""
		Renders the minefield, reset button, flag counter, and timer
		
		**Args**:
				None.
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				None.
		
		**Returns**:
				None.
		"""
		for y in range(self.minefield.y_size):
			for space in self.grid[y]:
				self.renderSpace(space)
		
		self.renderReset()
		self.updateClock()
		self.updateFlags()
		display.flip()


	def renderSpace(self, space):
		"""
		Renders an individual space on the minefield
		
		**Args**:
				*space*: Space object to be rendered
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				Space is rendered
		
		**Returns**:
				None.
		"""
		space_x = space.x_loc*self.SPACE_WIDTH
		space_y = space.y_loc*self.SPACE_HEIGHT		

		#Draw revealed space background
		if space.isRevealed:
			self.screen.blit(self.imageRevealed, (space_x, space_y))
			#Draw either a mine, or text ontop of background
			if space.isMine:
				self.screen.blit(self.imageMine, (space_x, space_y))
			elif space.numOfSurroundingMines != 0:
				#Draw Text
				t_font = font.SysFont('lucidaconsole', 20)
				text = t_font.render(str(space.numOfSurroundingMines), True, (0,0,0))
				x_text_pos = (space_x) + (self.SPACE_WIDTH / 2) - (text.get_width() / 2)
				y_text_pos = (space_y) + (self.SPACE_HEIGHT / 2) - (text.get_height() / 2)
				self.screen.blit(text, (x_text_pos, y_text_pos))
		else:
			self.screen.blit(self.imageUnrevealed, (space_x, space_y))
			#Draw a flag if the space is flagged
			if space.isFlagged:
				self.screen.blit(self.imageFlag, (space_x, space_y))

	def getTime(self):
		"""
		Returns current clock time since start of game
		
		**Args**:
				None.
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				None.
		
		**Returns**:
				None.
		"""
		return int((time.get_ticks() - self.timeOfLastReset) / 1000)

	def reset(self):
		"""
		Sets reset_flag to True
		
		**Args**:
				None.
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				None.
		
		**Returns**:
				None.
		"""
		self.reset_flag = True
	
	def renderReset(self):
		"""
		Renders the reset button
		
		**Args**:
				None.
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				Reset button is rendered
		
		**Returns**:
				None.
		"""
		reset_text = 'Reset'
		(reset_left, reset_top) = self.reset_element.get_abs_offset()
		(reset_x, reset_y) = self.reset_element.get_size()
		reset_fontsize = 20
		t_font = font.SysFont('lucidaconsole', reset_fontsize)
		while t_font.size(reset_text)[0] > reset_y + 4:
			reset_fontsize -= 1
			t_font = font.SysFont('lucidaconsole', reset_fontsize)
		self.drawButton(self.window._screen, reset_left, reset_top, reset_x, reset_y, (128,128,128), (96,96,96), reset_text, reset_fontsize, self.reset)

	def updateClock(self):
		"""
		Updates the timer element
		
		**Args**:
				None.
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				Timer element is rerendered
		
		**Returns**:
				None.
		"""
		t_font = font.SysFont('lucidaconsole', 20)
		text = t_font.render("Time : " + str(self.getTime()), False, (0,0,0))
		self.timer_element.fill(Color('light grey'))
		self.timer_element.blit(text, (0,0))	

	def onLose(self):
		"""
		Reveals all mines after on is revealed
		
		**Args**:
				None.
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				All mines are revealed and rendered
		
		**Returns**:
				None.
		"""
		for row in self.grid:
			for space in row:
				if space.isMine:
					space.isRevealed = True
					self.renderSpace(space)
					
	def updateFlags(self):
		"""
		Updates flag counter element
		
		**Args**:
				None.
		
		**Preconditions**:
				None.
		
		**Postconditions**:
				Flag counter is rerendered
		
		**Returns**:
				None.
		"""
		t_font = font.SysFont('lucidaconsole', 20)
		text = t_font.render("Flags: " + str(self.flagCounter), False, (0,0,0))
		self.flag_element.fill(Color('light grey'))
		self.flag_element.blit(text, (0,0))	
	

		

	