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
from Utilities import *

#Runs the chaos game on the provided polygon and draw the result
class ChaosGame:
	def __init__(self, image, listVertices):
		self.image = image
		self.draw = ImageDraw.Draw(self.image)
		
		self.outline(listVertices)
		self.generate(listVertices)
	#draw the outline of the polygon
	def outline(self, listVertices):
		pass
		
x = Point(3,4)