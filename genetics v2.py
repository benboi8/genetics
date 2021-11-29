import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GUI import *

generation = 0
counter = 0

font = pg.font.SysFont(fontName, 24)

maxAgeAverage = 0
waterRangeAverage = 0
breedChanceAverage = 0

def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	g.Draw()

	screen.blit(font.render(str(generation), True, darkWhite), (width // 2 - 300, 20, 50, 50))
	screen.blit(font.render(f"Population: {len(g.grid)}", True, darkWhite), (width // 2 + 30, 50, 50, 50))

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)


class Cell:
	def __init__(self, pos, size, gene=None):
		self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
		self.age = 0

		if gene == None:
			self.gene = {
				"moveDirection": (randint(-2, 3), randint(-2, 3))
			}
		else:
			self.gene = gene

		self.color = white

	def Draw(self):
		pg.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

	def Move(self, pos, boundary):
		rect = pg.Rect(self.rect.x + pos[0], self.rect.y + pos[1], self.rect.w, self.rect.h)
		if rect.x >= boundary.x and rect.y >= boundary.y and rect.x + rect.w <= boundary.x + boundary.w and rect.y + rect.h <= boundary.y + boundary.h:
			self.rect = rect

	def Reproduce(self, pos):
		return Cell(pos, (self.rect.w, self.rect.h), self.gene)


class Grid(NumGrid):
	def __init__(self, rect, color, gridSize, generationSize, genMax, gridFunc=None, surface=screen):
		self.surface = surface
		self.rect = pg.Rect(rect)
		self.borderColor = color
		self.generationSize = generationSize
		self.genMax = genMax
		super().__init__(gridSize, gridFunc, [])

	def CreateGrid(self):
		self.grid = [Cell((randint(self.rect.x, self.rect.w), randint(self.rect.y, self.rect.h)), (self.gridSize[0], self.gridSize[1])) for x in range(self.generationSize)]

	def Draw(self):
		pg.draw.rect(self.surface, self.borderColor, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
		for cell in self.grid:
			cell.Draw()

		self.CheckCells()

	def CheckCells(self):
		global generation, counter
		counter += 1
		pg.draw.line(screen, red, (self.rect.x + self.rect.w // 1.5, self.rect.y), (self.rect.x + self.rect.w // 1.5, self.rect.y + self.rect.h))

		for cell in self.grid:
			cell.Move([self.gridSize[0] * cell.gene.get("moveDirection", [0, 0])[0], self.gridSize[1] * cell.gene.get("moveDirection", [0, 0])[1]], self.rect)

		if counter >= self.genMax:
			counter = 0
			grid = []
			generation += 1
			for cell in self.grid:
				if cell.rect.x > self.rect.x + self.rect.w // 1.5:
					cell = cell.Reproduce((randint(self.rect.x, self.rect.x + self.rect.w), randint(self.rect.y, self.rect.y + self.rect.h)))
					grid.append(cell)
					if randint(0, 100) == 0:
						for i in range(5):
							if cell.rect.x - cell.rect.w > self.rect.x + self.rect.w // 1.5 and cell.rect.y - cell.rect.h > self.rect.y + self.rect.h // 1.5:
								cell.rect = pg.Rect(cell.rect.x - cell.rect.w, cell.rect.y - cell.rect.h, cell.rect.w, cell.rect.h)
							else:
								cell.rect = pg.Rect(cell.rect.x + cell.rect.w, cell.rect.y + cell.rect.h, cell.rect.w, cell.rect.h)
							grid.append(cell)

			self.grid = grid


g = Grid((width // 2 - 600, height // 2 - 300, 600, 600), lightBlack, (6, 6), 1000, 50)

fps = 60
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
