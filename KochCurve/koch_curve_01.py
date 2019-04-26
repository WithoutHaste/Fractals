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
	#returns copy of object
	def copy(self):
		return Point(self.x, self.y)
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
	@staticmethod
	#given the number of sides an equilateral shapes has, what angle is each internal corner at?
	#example: 3 (equilateral triangle) => 60 degrees
	def getInternalDegreesBySides(sides):
		if (sides < 3):
			raise Exception('Requires at least 3 sides.')
		totalDegrees = (sides - 2) * 180 #triangle has 180*, square has 360*, pentagon has 540*, etc
		return totalDegrees / sides

#generates entire curve and draw it on the image
#a shape defined clockwise will grow outward, a shape defined counter-clockwise will grow inward
class KochCurve:
	#generate and draw entire Koch curve, starting with the initial points
	#if there are more than 2 points, it is assumed the first and last are joined as well
	#"sides" means how many sides does the recursive shape have? the default Koch Curve is made of triangles, so it has 3 sides
	def __init__(self, image, listInitialPoints, sides=3):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		self.sides = sides
		
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
		unit = KochCurveUnit(pointStart, pointEnd, self.sides)
		self.drawUnit(unit)
		if unit.getLength() < 10: #stop recursion
			return
		for i in range(0,len(unit.points) - 1):
			self.generate(unit.points[i], unit.points[i+1])
	#image will be inverted on y-axis since images have origin in upper-left instead of bottom-left
	def drawUnit(self, unit):
		self.draw.line([unit.getStartPoint().toTuple(), unit.getEndPoint().toTuple()], fill='white', width=1)
		self.draw.line(unit.getPointsToTuples(), fill='gray', width=1)
		
#represents one unit of a Koch Curve
class KochCurveUnit:
	#"sides" means how many sides does the recursive shape have? the default Koch Curve is made of triangles, so it would have 3 sides
	def __init__(self, pointStart, pointEnd, sides):
		fullDistance = pointStart.distance(pointEnd)
		internalDegrees = Geometry.getInternalDegreesBySides(sides)
		
		self.points = [pointStart]
		pointStartPrime = Geometry.getPointBetweenPoints(pointStart, pointEnd, fullDistance / 3) #straight in from "start" to edge of recursive shape
		self.points.append(pointStartPrime)

		pointEndPrime = Geometry.getPointBetweenPoints(pointStart, pointEnd, 2 * fullDistance / 3) #straight in from "end" to edge of recursive shape
		pointRotate = pointEndPrime.copy()
		pointCenter = pointStartPrime.copy()
		for i in range(1, sides - 1):
			pointNext = Geometry.rotatePointAroundPoint(pointRotate, pointCenter, internalDegrees)
			self.points.append(pointNext)
			pointRotate = pointCenter
			pointCenter = pointNext

		self.points.append(pointEndPrime)
		self.points.append(pointEnd)
	#returns distance from "start" to "end"
	def getLength(self):
		return self.points[0].distance(self.points[-1])
	#returns first point
	def getStartPoint(self):
		return self.points[0]
	#returns last point
	def getEndPoint(self):
		return self.points[-1]
	#returns list of tuples instead of list of Points
	def getPointsToTuples(self):
		return [point.toTuple() for point in self.points]
		
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

#one line across entire image - pentagon
image = Image.new('RGB', (800, 400), 'white')
kochCurve = KochCurve(image, [Point(0, 2), Point(image.width, 2)], sides=5);
image.save('../output/koch_curve_line_pentagon.png')

#equilateral pentagon centered in image
image = Image.new('RGB', (800, 800), 'white')
center = Point(400, 400)
distance = 250
points = [Point(center.x, center.y - distance)] #top of pentagon
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -72)) #top-right of pentagon
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -144)) #bottom-right of pentagon
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -216)) #bottom-left of pentagon
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -288)) #top-left of pentagon
kochCurve = KochCurve(image, points, sides=5);
image.save('../output/koch_curve_pentagon_outward.png')

