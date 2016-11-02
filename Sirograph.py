from PIL import Image, ImageDraw
from math import radians, sin, cos, floor

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


class Sirograph:
    def __init__(self, imageSize=512):
        self.initImage(imageSize)

    def initImage(self, imageSize):
        self.image = Image.new("RGB", (imageSize, imageSize))
        self.draw = ImageDraw.Draw(self.image)

    def drawSampleLine(self, mid, size):
        halfSize = size/2

        self.drawdraw.point(mid[0])
        self.drawdraw.line((mid[0][0] + halfSize, mid[0][1], 512, mid[0][1]))
        self.drawdraw.line((mid[0][0] - halfSize, mid[0][1], 0, mid[0][1]))
        self.drawdraw.line((mid[0][0], mid[0][1] + halfSize, mid[0][0], 512))
        self.drawdraw.line((mid[0][0], mid[0][1] - halfSize, mid[0][0], 0))

    def drawSirograph(self, mid, size, deltaAngle, repeatSize = None, deltaSize=100, colorLambda=lambda x:hsv2rgb(x, 1, 1)):
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

        x,y = sin(radians(0))*halfSize, cos(radians(0))*halfSize

        for repeat in range(0, repeatSize):
            # draw.point((deltaX+mid[0][0], deltaY+mid[0][1]))
            # deltaX, deltaY = cos(radians(repeat*deltaAngle))*deltaSize, sin(radians(repeat*deltaAngle))*deltaSize
            # print(deltaAngle*repeat)
            for ang in range(0, 360):
                # print(cos(radians(ang))*halfSize)
                newX, newY = sin(radians(ang))*halfSize, cos(radians(ang))*halfSize
                pointLoc = (mid[0][0]+x+deltaX, mid[0][1]+y+deltaY, mid[1][0]+newX+deltaX, mid[1][1]+newY+deltaY)
                rgb = colorLambda(deltaAngle*(repeat+ang/360))
                # print(repeat*10+deltaAngle/3608*ang, rgb)
                self.draw.line(pointLoc, fill=rgb)
                # draw.point((deltaX, deltaY))

                # print(pointLoc[0]+x, pointLoc[1]+y)
                x, y = newX, newY

                # deltaWidth, deltaHeight = cos(radians(repeat*deltaAngle/360))*deltaSize, sin(radians(repeat*deltaAngle/360))*deltaSize
                deltaX, deltaY = cos(radians(repeat*deltaAngle+delta360Angle*ang))*deltaSize, sin(radians(repeat*deltaAngle+delta360Angle*ang))*deltaSize
                # print(repeat, deltaX, deltaY)
                # deltaLastWidth, deltaLastHeight = deltaWidth, deltaHeight

    def save(self, fileName):
        self.image.save(fileName)

mid = ((256, 256), (256, 256))
siro = Sirograph()
angle = 340

siro.initImage(512)
siro.drawSirograph(mid, 100, angle, repeatSize = 36)
# , repeatSize=36
siro.save("samples/sample %d.png"%angle)
exit()
for i in range(10, 370, 10):
    siro.initImage(512)
    siro.drawSirograph(mid, 100, i)
    # , repeatSize=36
    siro.save("samples/sample %d.png"%i)
