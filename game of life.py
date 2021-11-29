import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *


waterPoints = []
generation = 0

def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	g.Draw()

	screen.blit(pg.font.SysFont(fontName, 24).render(str(generation), True, darkWhite), (width // 2, 20, 50, 50))

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)


class Cell:
	def __init__(self, pos, size, alive=False, isWater=False):
		self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
		self.alive = alive
		self.age = 0
		self.isWater = isWater
		if self.isWater:
			waterPoints.append(pos)

		self.ChangeColor()

	def ChangeState(self, alive=None):
		if self.isWater:
			return

		if alive == None:
			if self.alive == True:
				self.alive = False
			else:
				self.alive = True

		else:
			self.alive = alive

		self.age = 0

		self.ChangeColor()

	def ChangeColor(self):
		if self.alive:
			self.color = white
		else:
			self.color = black

		if self.isWater:
			self.color = lightBlue

	def Draw(self):
		pg.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

		for i in range(waterPoints.count((self.rect.x, self.rect.y)) - 1):
			waterPoints.remove((self.rect.x, self.rect.y))

	def GetTaxicabDistance(self, poses):
		minDist = 99999
		maxDist = 0
		for pos in poses:
			dist = abs(self.rect.x - pos[0]) + abs(self.rect.y - pos[1])
			minDist = min(dist, minDist)
			maxDist = max(dist, maxDist)

		return (minDist, maxDist)

class Grid(NumGrid):
	def __init__(self, rect, color, gridSize, gridFunc=None, surface=screen):
		self.surface = surface
		self.rect = pg.Rect(rect)
		self.borderColor = color
		self.waterRange = 30
		super().__init__(gridSize, gridFunc, [])

	def CreateGrid(self):
		self.grid = [[Cell((self.rect.x + (x * self.gridSize[0]), self.rect.y + (y * self.gridSize[1])), (self.gridSize[0], self.gridSize[1]), True if self.CreateCell(x, y) == 0 else False, True if self.IsCellWater(x, y) == -1 else False) for x in range(self.rect.w // self.gridSize[0])] for y in range(self.rect.h // self.gridSize[1])]

	def Draw(self):
		pg.draw.rect(self.surface, self.borderColor, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
		for row in self.grid:
			for cell in row:
				cell.Draw()

		self.CheckCells()

	def CreateCell(self, x, y):
		aliveChance = randint(0, 10)
		return aliveChance

	def IsCellWater(self, x, y):
		waterChance = randint(-1, 99)
		return waterChance

	def CheckCells(self):
		global generation
		generation += 1
		for j, row in enumerate(self.grid):
			for i, cell in enumerate(row):
				if not cell.isWater:
					neighbours = 0
					for x in range(-1, 2):
						for y in range(-1, 2):
							if x != 0 or y != 0:
								if j - x != len(self.grid) and i - y != len(row):
									if self.grid[j - x][i - y].alive:
										neighbours += 1

					# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
					# Any live cell with two or three live neighbours lives on to the next generation.
					# Any live cell with more than three live neighbours dies, as if by overpopulation.
					# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

					cell.age += 1

					if cell.alive:
						if neighbours < 2 or neighbours > 3:
							cell.ChangeState(False)
						if cell.age > 30:
							cell.ChangeState(False)
						if cell.GetTaxicabDistance(waterPoints)[0] > self.waterRange:
							cell.ChangeState(False)

					else:
						if neighbours == 3:
							cell.ChangeState(True)
							cell.age = 0

					if generation % 500 == 0:
						self.waterRange += 20


g = Grid((width // 2 - 300, height // 2 - 300, 600, 600), white, (6, 6))


fps=60
while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	DrawLoop()
