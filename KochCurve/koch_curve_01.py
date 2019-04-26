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

#generates entire curve and draw it on the image
#a shape defined clockwise will grow outward, a shape defined counter-clockwise will grow inward
class KochCurve:
	#generate and draw entire Koch curve, starting with the initial points
	#if there are more than 2 points, it is assumed the first and last are joined as well
	def __init__(self, image, listInitialPoints):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		
		count = len(listInitialPoints)
		if count == 1:
			return
		elif count == 2:
			self.generate(listInitialPoints[0], listInitialPoints[1])
		else:
			for i in range(-1, count-1):
				self.generate(listInitialPoints[i], listInitialPoints[i+1])
	#generate and draw entire Koch Curve to default depth
	def generate(self, pointStart, pointEnd):
		unit = KochCurveUnit(pointStart, pointEnd)
		self.drawUnit(unit)
		if unit.getLength() < 10: #stop recursion
			return
		self.generate(unit.pointA, unit.pointB)
		self.generate(unit.pointB, unit.pointC)
		self.generate(unit.pointC, unit.pointD)
		self.generate(unit.pointD, unit.pointE)
	#image will be inverted on y-axis since images have origin in upper-left instead of bottom-left
	def drawUnit(self, unit):
		self.draw.line([unit.pointA.toTuple(), unit.pointE.toTuple()], fill='white', width=1)
		self.draw.line([unit.pointA.toTuple(), unit.pointB.toTuple(), unit.pointC.toTuple(), unit.pointD.toTuple(), unit.pointE.toTuple()], fill='gray', width=1)
		
#hard-coded to equilateral triangle, 1/3 of length
class KochCurveUnit:
	def __init__(self, pointA, pointE):
		fullDistance = pointA.distance(pointE)
		self.pointA = pointA
		self.pointB = Geometry.getPointBetweenPoints(pointA, pointE, fullDistance / 3)
		self.pointD = Geometry.getPointBetweenPoints(pointA, pointE, 2 * fullDistance / 3)
		self.pointC = Geometry.rotatePointAroundPoint(self.pointD, pointCenter = self.pointB, degrees = 60)
		self.pointE = pointE
	#returns distance from A to E
	def getLength(self):
		return self.pointA.distance(self.pointE)
		
#################################

#one line across entire image
image = Image.new('RGB', (800, 400), 'white')
kochCurve = KochCurve(image, [Point(0, 2), Point(image.width, 2)]);
image.save('../output/koch_curve_line.png')

#equilateral triangle centered in image
image = Image.new('RGB', (800, 800), 'white')
center = Point(400, 400)
distance = 300
points = [Point(center.x, center.y - distance)] #top of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = 120)) #bottom-left of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -120)) #bottom-right of triangle
kochCurve = KochCurve(image, points);
image.save('../output/koch_curve_triangle_inward.png')

#equilateral triangle centered in image
image = Image.new('RGB', (800, 800), 'white')
reversedPoints = points[:]
reversedPoints.reverse()
kochCurve = KochCurve(image, reversedPoints);
image.save('../output/koch_curve_triangle_outward.png')
