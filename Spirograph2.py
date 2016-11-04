#!python3
from PIL import Image, ImageDraw
from math import radians, sin, cos, floor, pi

def hsv2rgb(h, s, v):
	h, s, v = float(h), float(s), float(v)
	h60 = h / 60.0
	h60f = floor(h60)
	hi, f = int(h60f) % 6, h60 - h60f
	
	p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
	r, g, b = 0, 0, 0
	
	if hi == 0: r, g, b = v, t, p
	elif hi == 1: r, g, b = q, v, p
	elif hi == 2: r, g, b = p, v, t
	elif hi == 3: r, g, b = p, q, v
	elif hi == 4: r, g, b = t, p, v
	elif hi == 5: r, g, b = v, p, q
	
	return int(r * 255), int(g * 255), int(b * 255)


class Sirograph:
	def __init__(self, imageSize=512):
		self.initImage(imageSize)
		self.imageSize = imageSize

	def initImage(self, imageSize=None):
		if not imageSize:
			imageSize = self.imageSize
		else:
			self.imageSize = imageSize
			
		self.image = Image.new("RGB", (imageSize, imageSize))
		self.draw = ImageDraw.Draw(self.image)

	def drawSampleLine(self, mid, size):
		halfSize = size/2

		self.draw.point(mid[0])
		self.draw.line((mid[0][0] + halfSize, mid[0][1], self.imageSize, mid[0][1]))
		self.draw.line((mid[0][0] - halfSize, mid[0][1], 0, mid[0][1]))
		self.draw.line((mid[0][0], mid[0][1] + halfSize, mid[0][0], self.imageSize))
		self.draw.line((mid[0][0], mid[0][1] - halfSize, mid[0][0], 0))
		
	def getSmallCircleCenter(self, angle):
		# predefine halfLargeSize
		x, y = sin(radians(angle))*(self.largeSize-self.smallSize)/2, cos(radians(angle))*(self.largeSize-self.smallSize)/2
		
		return x, y
		
	def drawSirograph2(self, mid, largeSize, smallSize, start=90, colorLambda=lambda x:hsv2rgb(x, 1, 1), width=0):
		self.largeSize = largeSize
		self.smallSize = smallSize
		
		innerCircleRotate = 360
		angleRate = 0.1
		
		ang = start
		halfLargeSize, halfSmallSize = largeSize/2, smallSize/2
		
		newSmallXLambda, newSmallYLambda = lambda ang:sin(radians(ang))*halfSmallSize, lambda ang:cos(radians(ang))*halfSmallSize
		piRad = pi/180.0
		
		cAngToArcLen = lambda ang, r:(ang-start)*r*piRad
		cArcLenToAng = lambda length, r:(length/piRad/r)
		# %360
		
		angleRange = [(i+start/angleRate)*angleRate for i in range(0, int(innerCircleRotate/angleRate))]
		
		arcLen = cAngToArcLen(angleRange[0], largeSize)
		bPrimeAng = cArcLenToAng(arcLen, smallSize)
		x, y = newSmallXLambda(bPrimeAng), newSmallYLambda(bPrimeAng)
		
		for largeAngle in angleRange:
		# range(0, innerCircleRotate):
			arcLen = cAngToArcLen(largeAngle, largeSize)
			
			smallCenterXY = self.getSmallCircleCenter(largeAngle)
	
			bPrimeAng = cArcLenToAng(arcLen, smallSize)
			
			newX, newY = newSmallXLambda(bPrimeAng), newSmallYLambda(bPrimeAng)
			# print(largeAngle, arcLen, bPrimeAng)
			
			centerSmallCircle = (mid[0][0]+smallCenterXY[0]+x, mid[0][1]+smallCenterXY[1]+y, mid[1][0]+smallCenterXY[0]+newX, mid[1][1]+smallCenterXY[1]+newY)
			# centerSmallCircle = (mid[0][0]+smallXY[0], mid[0][1]+smallXY[1], mid[1][0]+lastXY[0], mid[1][1]+lastXY[1])
			self.draw.line(centerSmallCircle, width=width)
			
			x, y = newX, newY
			# lastXY = smallXY
			
		# for angIndex, newX, newY in zip(range(0, len(angleRange)), map(newXLambda, angleRange), map(newYLambda, angleRange)):
		# 	angleColor = colorLambda(angIndex)
		# 	# map(colorLambda, angleRange)
		# 	# print(cos(radians(ang))*halfSize)
		# 	
		# 	# ang = (angIndex+90) % 360
		# 	
		# 	# newX, newY = newXLambda(ang), newYLambda(ang)
		# 	pointLoc = (mid[0][0]+x, mid[0][1]+y, mid[1][0]+newX, mid[1][1]+newY)
		# 	# rgb = colorLambda(ang/360)
		# 	# print(repeat*10+deltaAngle/3608*ang, rgb)
		# 	self.draw.line(pointLoc, fill=angleColor, width=width)
		# 
		# 	x, y = newX, newY

	def save(self, fileName):
		self.image.save(fileName)

if __name__ == "__main__":
	mid = ((300, 300), (300, 300))
	siro = Sirograph()

	siro.initImage(600)
	siro.drawSampleLine(mid, 120)
	# colorLambda=lambda x:(255, 255, 255)
	siro.drawSirograph2(mid, 200, 40, width=3)
	
	# , repeatSize=36
	siro.save("sample.png")