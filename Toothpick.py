#Toothpick Sequence

from PIL import Image, ImageDraw
from Utilities import *
import sys

#generate entire diagram and draw it on the image
#starts in the center and works outward
class ToothpickDiagram:
	def __init__(self, image):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		self.generate()
	#starts with a vertical toothpick in the center of the image and works outward until is hits the edges
	def generate(self):
		imageWidth, imageHeight = self.image.size
		toothpicks = []
		openToothpicks = []
		#initialize
		firstToothpick = Toothpick(Point(imageWidth/2 - Toothpick.thickness/2, imageHeight/2 - Toothpick.length/2), Point(imageWidth/2 - Toothpick.thickness/2, imageHeight/2 + Toothpick.length/2), 'red')
		toothpicks.append(firstToothpick)
		openToothpicks.append(firstToothpick)
		#loop
		while(True):
			newToothpicks = []
			for toothpick in toothpicks:
				if toothpick.pointAOpen:
					newToothpick = toothpick.getExtensionA('black')
					newToothpicks.append(newToothpick)
					openToothpicks.append(newToothpick)
				if toothpick.pointBOpen:
					newToothpick = toothpick.getExtensionB('black')
					newToothpicks.append(newToothpick)
					openToothpicks.append(newToothpick)
			outOfBounds = False
			for toothpick in newToothpicks:
				if toothpick.isOutOfBounds(imageWidth, imageHeight):
					outOfBounds = True
			toothpicks.extend(newToothpicks)
			for toothpick in openToothpicks:
				for otherToothpick in toothpicks:
					toothpick.updateOpen(otherToothpick)
			openToothpicks = list(filter(lambda x: x.isOpen(), openToothpicks))
			if outOfBounds:
				break
		#draw
		for toothpick in toothpicks:
			toothpick.draw(self.draw)
		
class Toothpick:
	thickness = 2
	length = 20
	#points are the center of each end of toothpick
	def __init__(self, pointA, pointB, color):
		self.pointA = pointA
		self.pointB = pointB
		self.pointAOpen = True
		self.pointBOpen = True
		self.color = color
	def isOpen(self):
		return (self.pointAOpen or self.pointBOpen)
	def isHorizontal(self):
		return self.pointA.y == self.pointB.y
	def isVertical(self):
		return self.pointA.x == self.pointB.x
	def updateOpen(self, other):
		if not self.pointAOpen and not self.pointBOpen:
			return
		if self.equals(other):
			return
		if other.containsPoint(self.pointA):
			self.pointAOpen = False
		if other.containsPoint(self.pointB):
			self.pointBOpen = False
	def containsPoint(self, point):
		if self.isHorizontal():
			return self.pointA.y == point.y and min(self.pointA.x, self.pointB.x) <= point.x and max(self.pointA.x, self.pointB.x) >= point.x
		else:
			return self.pointA.x == point.x and min(self.pointA.y, self.pointB.y) <= point.y and max(self.pointA.y, self.pointB.y) >= point.y
	def equals(self, other):
		return self.pointA.equals(other.pointA) and self.pointB.equals(other.pointB)
	#returns the toothpick that is perpendicular to and centered on End A
	def getExtensionA(self, color):
		if(self.isHorizontal()):
			return Toothpick(Point(self.pointA.x, self.pointA.y - Toothpick.length/2), Point(self.pointA.x, self.pointA.y + Toothpick.length/2), color);
		else:
			return Toothpick(Point(self.pointA.x - Toothpick.length/2, self.pointA.y), Point(self.pointA.x + Toothpick.length/2, self.pointA.y), color);
	#returns the toothpick that is perpendicular to and centered on End B
	def getExtensionB(self, color):
		if(self.isHorizontal()):
			return Toothpick(Point(self.pointB.x, self.pointB.y - Toothpick.length/2), Point(self.pointB.x, self.pointB.y + Toothpick.length/2), color);
		else:
			return Toothpick(Point(self.pointB.x - Toothpick.length/2, self.pointB.y), Point(self.pointB.x + Toothpick.length/2, self.pointB.y), color);
	def isOutOfBounds(self, width, height):
		return (self.pointA.isOutOfBounds(width, height) or self.pointB.isOutOfBounds(width, height))
	def draw(self, drawObject):
		drawObject.line([self.pointA.toTuple(), self.pointB.toTuple()], fill=self.color, width=Toothpick.thickness)
		
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def toTuple(self):
		return (self.x, self.y)
	def isOutOfBounds(self, width, height):
		return (self.x < 0 or self.x > width or self.y < 0 or self.y > height)
	def equals(self, other):
		return self.x == other.x and self.y == other.y

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
