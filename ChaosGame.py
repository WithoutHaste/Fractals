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
import sys

#Runs the chaos game on the provided polygon and draw the result
class ChaosGame:
	def __init__(self, image, listVertices, saveAnimatedGif=False, gifFilename=None):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		self.gifFilename = gifFilename
		self.listVertices = listVertices

		self.outline()

		 #TODO: get random point in triangle instead of this static one
		if(saveAnimatedGif):
			self.generateAnimated(Point(300, 310), iterationCount=25000)
		else:
			self.generateStatic(Point(300, 310), iterationCount=90000)

	#draw the outline of the polygon
	def outline(self):
		self.draw.line([point.toTuple() for point in self.listVertices], fill='gray', width=1)
		self.draw.line([self.listVertices[0].toTuple(), self.listVertices[-1].toTuple()], fill='gray', width=1)
	#generate and draw all the points - store static image
	def generateStatic(self, pointReference, iterationCount):
		points = self.generatePoints(pointReference, iterationCount)
		for point in points:
			self.draw.point([point.toTuple()], fill='gray')
	#generate and draw all the points - save animated gif
	def generateAnimated(self, pointReference, iterationCount):
		points = self.generatePoints(pointReference, iterationCount)
		imageFilenames = []
		imageIndex = 0
		for point in points:
			self.draw.point([point.toTuple()], fill='gray')
			if(imageIndex % 250 == 0):
				imageFilename = 'output/temp/animation' + str(imageIndex) + '.png'
				self.image.save(imageFilename)
				imageFilenames.append(imageFilename)
			imageIndex += 1
		Graphics.saveAnimatedGif(self.gifFilename, imageFilenames, framesPerSecond=10)
	#generate and return a list of points
	def generatePoints(self, pointReference, iterationCount):
		points = []
		for i in range(iterationCount):
			nextVertex = self.getRandomVertex(self.listVertices)
			nextPoint = Geometry.getPointHalfwayBetweenPoints(pointReference, nextVertex)
			points.append(nextPoint)
			pointReference = nextPoint
		return points[10:] #it takes a few iterations to settle into the pattern, so skip the first points
	@staticmethod
	#returns a random vertex
	# NOTE: if I limit the vertex to be different from the current vertex, the triangle does not form
	def getRandomVertex(listVertices):
		if (len(listVertices) < 2):
			raise Exception("Requires at least 2 vertices.")
		return random.choice(listVertices)
		
#################################

saveAnimatedGif = False
if(len(sys.argv) > 1):
	if(sys.argv[1] == '-help' or sys.argv[1] == 'help'):
		print("Usage : python ChaosGame.py : will generate static image")
		print("Usage : python ChaosGame.py -gif : will generate animated gif")
		sys.exit()
	elif(sys.argv[1] == '-gif' or sys.argv[1] == 'gif'):
		saveAnimatedGif = True

#equilateral triangle centered in image
image = Image.new('RGB', (800, 800), 'white')
center = Point(400, 475)
distance = 400
points = [Point(center.x, center.y - distance)] #top of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = 120)) #bottom-left of triangle
points.append(Geometry.rotatePointAroundPoint(points[0], center, degrees = -120)) #bottom-right of triangle
if(saveAnimatedGif):
	ChaosGame(image, points, saveAnimatedGif, 'output/chaos_game_sierpinski_triangle_animation.gif');
else:
	ChaosGame(image, points);
	image.save('output/chaos_game_sierpinski_triangle.png')
