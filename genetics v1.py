import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *


waterPoints = []
generation = 0

font = pg.font.SysFont(fontName, 24)

maxAgeAverage = 0
waterRangeAverage = 0
breedChanceAverage = 0

def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	g.Draw()

	maxAgeAverage = 0
	waterRangeAverage = 0
	breedChanceAverage = 0
	count = 0
	for row in g.grid:
		for cell in row:
			if cell.alive:
				count += 1
				maxAgeAverage += cell.gene.get("maxAge")
				waterRangeAverage += cell.gene.get("waterRange")
				breedChanceAverage += cell.gene.get("unsuccessfulBreedChance")

	maxAgeAverage /= count
	waterRangeAverage /= count
	breedChanceAverage /= count

	screen.blit(font.render(str(generation), True, darkWhite), (width // 2 - 300, 20, 50, 50))
	screen.blit(font.render("Gene Average", True, darkWhite), (width - 600, 20, 200, 50))
	screen.blit(font.render(f"Max age: {maxAgeAverage}", True, darkWhite), (width - 600, 70, 200, 50))
	screen.blit(font.render(f"Water Range: {waterRangeAverage}", True, darkWhite), (width - 600, 100, 200, 50))
	screen.blit(font.render(f"Unsuccessful breed chance: {breedChanceAverage}", True, darkWhite), (width - 600, 130, 200, 50))

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

		self.gene = {
			"maxAge": randint(20, 30),
			"waterRange": randint(30, 40),
			"unsuccessfulBreedChance": randint(0, 100)
		}

		self.ChangeColor()

	def ChangeState(self, alive=None, gene=None):
		if gene != None:
			self.gene = gene

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
		aliveChance = randint(0, 8)
		return aliveChance

	def IsCellWater(self, x, y):
		waterChance = randint(-1, 79)
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

					cell.age += 1

					if cell.alive:
						if neighbours < 2 or neighbours > 3:
							cell.ChangeState(False)
						if cell.age > cell.gene.get("maxAge"):
							cell.ChangeState(False)
						if cell.GetTaxicabDistance(waterPoints)[0] > cell.gene.get("waterRange"):
							cell.ChangeState(False)
					else:
						if neighbours == 3:
							if randint(-50, 50) != cell.gene.get("unsuccessfulBreedChance"):
								cell.ChangeState(True, cell.gene)
								cell.age = 0
								cell.gene["maxAge"] += 1
								cell.gene["unsuccessfulBreedChance"] -= randint(-1, 4)

					if cell.gene.get("waterRange") % 100 == 0:
						cell.gene["waterRange"] += randint(-2, 2)



g = Grid((width // 2 - 600, height // 2 - 300, 600, 600), white, (6, 6))


fps = 30
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
