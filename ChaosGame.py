#Chaos Game

#Given a polygon
#Given a fraction between 0 and 1
#Select a random point in the polygon - the reference
# Select a random vertex (corner or point) of the polygon
#	Place a point halfway between the reference and the vertex
#   This point becomes the next reference, and the cycle continues

#Suggestion is to throw out the first few points, until the patterns settles in

#Suggestion is to never use the same Vertex twice in a row

from PIL import Image, ImageDraw
import random
from Utilities import *

#Runs the chaos game on the provided polygon and draw the result
class ChaosGame:
	def __init__(self, image, listVertices):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		
		self.outline(listVertices)
		 #TODO: get random point in triangle
		self.generate(listVertices, Point(300, 310), previousVertex=None)
	#draw the outline of the polygon
	def outline(self, listVertices):
		self.draw.line([point.toTuple() for point in listVertices], fill='gray', width=1)
		self.draw.line([listVertices[0].toTuple(), listVertices[-1].toTuple()], fill='gray', width=1)
	#generate and draw the next point
	def generate(self, listVertices, pointReference, previousVertex):
		pointIndex = 0 #it takes a few iterations to settle into the proper pattern
		imageFilenames = []
		imageIndex = 0
		for i in range(25000):
			nextVertex = self.getRandomVertex(listVertices, previousVertex);
			nextPoint = Geometry.getPointHalfwayBetweenPoints(pointReference, nextVertex)
			if(pointIndex > 10):
				self.draw.point([nextPoint.toTuple()], fill='gray')
			pointReference = nextPoint
			previousVertex = nextVertex
			pointIndex += 1
			###########################
			if(imageIndex % 250 == 0):
				imageFilename = 'output/temp/animation' + str(imageIndex) + '.png'
				self.image.save(imageFilename)
				imageFilenames.append(imageFilename)
			imageIndex += 1
		Graphics.saveAnimatedGif('output/chaos_game_sierpinski_triangle_animation.gif', imageFilenames);
	@staticmethod
	#returns a random vertex
	# NOTE: if I limit the vertex to be different from the current vertex, the triangle does not form
	def getRandomVertex(listVertices, previousVertex):
		if (len(listVertices) < 2):
			raise Exception("Requires at least 2 vertices.")
		return random.choice(listVertices)
		
#################################

#equilateral triangle centered in image
image = Image.new('RGB', (800, 800), 'white')
center = Point(400, 475)
distance = 400
points = [Point(center.x, center.y - distance)] #top of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = 120)) #bottom-left of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -120)) #bottom-right of triangle
chaosGame = ChaosGame(image, points);
image.save('output/chaos_game_sierpinski_triangle.png')

