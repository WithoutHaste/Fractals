#Toothpick Sequence

from PIL import Image, ImageDraw
import sys

#generate entire diagram and draw it on the image
#starts in the center and works outward
class ToothpickDiagram:
	def __init__(self, image):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		self.generateMap()
		self.drawMap()
	def generateMap(self):
		self.unit = 20
		imageWidth, imageHeight = self.image.size
		mapWidth = int(imageWidth/self.unit)
		mapHeight = int(imageHeight/self.unit)
		self.map = Map(mapWidth, mapHeight)
	def drawMap(self):
		self.thickness = 2
		for col in range(self.map.width):
			for row in range(self.map.height):
				square = self.map.map[col][row]
				if square.north:
					self.draw.line([((col-1)*self.unit, row*self.unit), (col*self.unit, row*self.unit)], fill='black', width=self.thickness)
				if square.south:
					self.draw.line([((col-1)*self.unit, (row+1)*self.unit), (col*self.unit, (row+1)*self.unit)], fill='black', width=self.thickness)
				if square.west:
					self.draw.line([(col*self.unit, row*self.unit), (col*self.unit, (row+1)*self.unit)], fill='black', width=self.thickness)
				if square.east:
					self.draw.line([((col+1)*self.unit, row*self.unit), ((col+1)*self.unit, (row+1)*self.unit)], fill='black', width=self.thickness)

class Map:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.map = []
		for i in range(self.width):
			col = []
			self.map.append(col)
			for i in range(self.height):
				col.append(Square())
		self.applyVerticalToothpick(int(self.width/2), int(self.height/2 - 1))
		#self.applyHorizontalToothpick(int(self.width/2), int(self.height/2 - 1))
		self.fill()
	def fill(self):
		#apply new toothpicks
		for col in range(self.map.width):
			for row in range(self.map.height):
				pass
		#after each, resolve room numbers
		pass
	#toothpick extends south from point 2 units
	def applyVerticalToothpick(self, x, y):
		self.map[x-1][y].east = True
		self.map[x-1][y+1].east = True
		self.map[x][y].west = True
		self.map[x][y+1].west = True
	#toothpick extends east from point 2 units
	def applyHorizontalToothpick(self, x, y):
		self.map[x+1][y].north = True
		self.map[x+2][y].north = True
		self.map[x+1][y-1].south = True
		self.map[x+2][y-1].south = True
		
class Square:
	def __init__(self):
		self.north = False
		self.south = False
		self.west = False
		self.east = False
		self.complete = False
	
#################################

if(len(sys.argv) != 3 or sys.argv[1] == 'help' or sys.argv[1] == '-help'):
	print("Usage : python Toothpick.py width height : fills image of this size with diagram")
	sys.exit()
else:
	width = int(sys.argv[1])
	height = int(sys.argv[2])
	image = Image.new('RGB', (width, height), 'white')
	toothpick = ToothpickDiagram(image)
	image.save('output/toothpick_'+str(width)+'x'+str(height)+'.png')
