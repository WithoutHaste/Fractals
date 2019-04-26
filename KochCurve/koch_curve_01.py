#Koch Curve - attempt 01

import math as Math
from PIL import Image, ImageDraw

#represents an (x,y) coordinate
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		return Point(self.x - other.x, self.y - other.y)
	#returns absolute distance between two points
	def distance(self, other):
		return Math.sqrt( (self.x-other.x)**2 + (self.y-other.y)**2 )
	#returns slope between two points
	def slope(self, other):
		return ((other.y - self.y) / (other.x - self.x))
	#returns tuple (x,y)
	def toTuple(self):
		return (self.x, self.y)
	#returns string (x, y)
	def __str__(self):
		return "(%f, %f)" % (self.x, self.y)

#static geometry operations
class Geometry:
	@staticmethod
	def degreesToRadians(degrees):
		return degrees * Math.pi / 180
	@staticmethod
	#returns a point that is "distance" away from "start", moving towards "end"
	def getPointBetweenPoints(pointStart, pointEnd, distanceFromStart):
		#equation of line: y' = slope(x' - x) + y
		slope = pointStart.slope(pointEnd)
		xPrime = pointStart.x + (distanceFromStart / Math.sqrt( 1 + slope**2 ))
		if (xPrime < pointStart.x and xPrime < pointEnd.x) or (xPrime > pointStart.x and xPrime > pointEnd.x):
			#travel in correct direction from start
			xPrime = pointStart.x - (distanceFromStart / Math.sqrt( 1 + slope**2 ))
		yPrime = slope * (xPrime - pointStart.x) + pointStart.y
		return Point(xPrime, yPrime)
	@staticmethod
	#rotates "A" around "center" and returns the result; "degrees" are positive in counter-clockwise direction
	def rotatePointAroundPoint(pointA, pointCenter, degrees):
		pointARelativeToOrigin = pointA - pointCenter
		radians = Geometry.degreesToRadians(degrees)
		xPrime = (pointARelativeToOrigin.x * Math.cos(radians)) - (pointARelativeToOrigin.y * Math.sin(radians))
		yPrime = (pointARelativeToOrigin.y * Math.cos(radians)) + (pointARelativeToOrigin.x * Math.sin(radians))
		return Point(xPrime, yPrime) + pointCenter

class KochCurve:
	def __init__(self, image):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		self.generate(Point(0,0+2), Point(image.width, 0+2))
	def generate(self, pointStart, pointEnd):
		#generate entire Koch Curve to default depth
		unit = KochCurveUnit(pointStart, pointEnd)
		self.drawUnit(unit);
	def drawUnit(self, unit):
		#image will be inverted on y-axis since images have origin in upper-left instead of bottom-left
		self.draw.line([unit.pointA.toTuple(), unit.pointB.toTuple(), unit.pointC.toTuple(), unit.pointD.toTuple(), unit.pointE.toTuple()], fill='gray', width=2)
		
class KochCurveUnit:
	def __init__(self, pointA, pointE):
		fullDistance = pointA.distance(pointE)
		print(fullDistance)
		self.pointA = pointA
		print(self.pointA)
		self.pointB = Geometry.getPointBetweenPoints(pointA, pointE, fullDistance / 3)
		print(self.pointB)
		self.pointD = Geometry.getPointBetweenPoints(pointA, pointE, 2 * fullDistance / 3)
		self.pointC = Geometry.rotatePointAroundPoint(self.pointD, pointCenter = self.pointB, degrees = 60)
		print(self.pointC)
		print(self.pointD)
		self.pointE = pointE
		print(self.pointE)
		
#################################

dimensions = (800, 600)
outputFileName = '../output/test.png'
 
image = Image.new('RGB', dimensions, 'white')
kochCurve = KochCurve(image);
image.save(outputFileName)