import math as Math
import imageio

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
	def getPointHalfwayBetweenPoints(pointA, pointB):
		return Point((pointA.x + pointB.x) / 2, (pointA.y + pointB.y) / 2)
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
	@staticmethod
	#http://mathworld.wolfram.com/TrianglePointPicking.html
	#returns a random point within a triangle with uniform distribution
	def getRandomPointInTriangle(pointA, pointB, pointC):
		originPoint = Geometry.getLeftmostLowestPoint([pointA, pointB, pointC])
		v1 = None
		v2 = None
		if (originPoint == pointA):
			v1 = pointB
			v2 = pointC
		elif (originPoint == pointB):
			v1 = pointA
			v2 = pointC
		else:
			v1 = pointA
			v2 = pointB
		
	@staticmethod
	#return point that is (first) leftmost, then (second) lowest
	def getLeftmostLowestPoint(listPoints):
		minX = listPoints[0].x
		for point in listPoints:
			minX = min(minX, point.x)
		minPoint = None
		for point in listPoints:
			if (minX != point.x):
				continue
			if (minPoint == None or minPoint.y > point.y):
				minPoint = point
		return minPoint

#static graphical operations		
class Graphics:
	@staticmethod
	def saveAnimatedGif(filename, imageFilenames, framesPerSecond):
		images = []
		for imageFilename in imageFilenames:
			images.append(imageio.imread(imageFilename))
		imageio.mimsave(filename, images, fps=framesPerSecond)
		