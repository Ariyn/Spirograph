#!python3
from PIL import Image, ImageDraw
from math import radians, sin, cos, floor

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

	def initImage(self, imageSize):
		self.image = Image.new("RGB", (imageSize, imageSize))
		self.draw = ImageDraw.Draw(self.image)

	def drawSampleLine(self, mid, size):
		halfSize = size/2

		self.draw.point(mid[0])
		self.draw.line((mid[0][0] + halfSize, mid[0][1], 512, mid[0][1]))
		self.draw.line((mid[0][0] - halfSize, mid[0][1], 0, mid[0][1]))
		self.draw.line((mid[0][0], mid[0][1] + halfSize, mid[0][0], 512))
		self.draw.line((mid[0][0], mid[0][1] - halfSize, mid[0][0], 0))

	def drawSirograph(self, mid, size, deltaAngle, repeatSize = None, start=0, deltaSize=100, colorLambda=lambda x:hsv2rgb(x, 1, 1), width=0, deltaAngleDelta=0):
		delta360Angle = deltaAngle/360
		deltaX, deltaY = 0, 0

		halfSize = size/2

		if not repeatSize:
			repeatSize = 360 // deltaAngle
			# this fomula is not correct in these angles
			# 50 - 36 times
			# 70 - 36 times
			# 80 -  9 times
			# 100 - 18 times
			# 110 - 36 times
			# 130 - 36 times
			# 140 - 18 times
			# 150 - 12 times
			# 160 - 9 times
			# 170 - 36 times
			# 180
			
			# 330 - 12
			# 340 - 36
			# 350 - 36

		x,y = sin(radians(0))*halfSize, cos(radians(0))*halfSize
		deltaRunningAngle = 0
		
		# range(0, repeatSize)
		repeatList = [i*3 for i in range(0,repeatSize)]
		for repeat in repeatList:
			# draw.point((deltaX+mid[0][0], deltaY+mid[0][1]))
			# deltaX, deltaY = cos(radians(repeat*deltaAngle))*deltaSize, sin(radians(repeat*deltaAngle))*deltaSize
			# print(deltaAngle*repeat)
			
			for angIndex in range(0, 360):
				# print(cos(radians(ang))*halfSize)
				ang = angIndex % 360
				newX, newY = sin(radians(ang))*halfSize, cos(radians(ang))*halfSize
				pointLoc = (mid[0][0]+x+deltaX, mid[0][1]+y+deltaY, mid[1][0]+newX+deltaX, mid[1][1]+newY+deltaY)
				rgb = colorLambda(deltaAngle*(repeat+ang/360))
				# print(repeat*10+deltaAngle/3608*ang, rgb)
				self.draw.line(pointLoc, fill=rgb, width=width)
				# draw.point((deltaX, deltaY))

				# print(pointLoc[0]+x, pointLoc[1]+y)
				x, y = newX, newY

				# deltaWidth, deltaHeight = cos(radians(repeat*deltaAngle/360))*deltaSize, sin(radians(repeat*deltaAngle/360))*deltaSize
				deltaX, deltaY = cos(radians(repeat*deltaAngle+delta360Angle*ang))*deltaSize, sin(radians(repeat*deltaAngle+delta360Angle*ang))*deltaSize
				# deltaRunningAngle = (deltaRunningAngle+deltaAngleDelta)%360
				# print(repeat, deltaX, deltaY)
				# deltaLastWidth, deltaLastHeight = deltaWidth, deltaHeight

	def save(self, fileName):
		self.image.save(fileName)

if __name__ == "__main__":
	mid = ((300, 300), (300, 300))
	siro = Sirograph()

	siro.initImage(600)
	# siro.drawSampleLine(mid, 120)
	siro.drawSirograph(mid, 120, 160, repeatSize = 36, deltaSize = 160, start=8, colorLambda=lambda x:(255, 255, 255), width=3, deltaAngleDelta=0.1)
	siro.drawSirograph(mid, 80, 160, repeatSize = 36, deltaSize = 80, start=8, colorLambda=lambda x:(255, 0, 0), width=3, deltaAngleDelta=0.1)
	# siro.drawSirograph(mid, 150, 160, repeatSize = 9, deltaSize = 140, start=8, colorLambda=lambda x:(0, 255, 255), width=3)
	# siro.drawSirograph(mid, 199, 160, repeatSize = 9, deltaSize = 199, start=8, colorLambda=lambda x:(255, 255, 0), width=3)
	# siro.drawSirograph(mid, 50, 160, repeatSize = 9, deltaSize = 40, start=8, colorLambda=lambda x:(255, 0, 255), width=3)
	
	# , repeatSize=36
	siro.save("sample1.png")
	exit(3)
	for i in range(10, 370, 10):
		siro.initImage(512)
		siro.drawSirograph(mid, 100, i)
		# , repeatSize=36
		siro.save("samples/sample %d.png"%i)
