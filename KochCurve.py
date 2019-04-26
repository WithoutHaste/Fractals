#Koch Curve - attempt 01

from PIL import Image, ImageDraw
from Utilities import *

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
image.save('output/koch_curve_line.png')

#equilateral triangle centered in image
image = Image.new('RGB', (800, 800), 'white')
center = Point(400, 400)
distance = 300
points = [Point(center.x, center.y - distance)] #top of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = 120)) #bottom-left of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -120)) #bottom-right of triangle
kochCurve = KochCurve(image, points);
image.save('output/koch_curve_triangle_inward.png')

#equilateral triangle centered in image
image = Image.new('RGB', (800, 800), 'white')
reversedPoints = points[:]
reversedPoints.reverse()
kochCurve = KochCurve(image, reversedPoints);
image.save('output/koch_curve_triangle_outward.png')

#one line across entire image - pentagon
image = Image.new('RGB', (800, 400), 'white')
kochCurve = KochCurve(image, [Point(0, 2), Point(image.width, 2)], sides=5);
image.save('output/koch_curve_line_pentagon.png')

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
image.save('output/koch_curve_pentagon_outward.png')

