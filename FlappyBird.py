from tkinter import *
from time import time as tic
import random as rd

# PARAMETROS DEL PROGRAMA #

dt = 0.02
doorSpace = 100
cnvShape = (500,400)

# DEFINICIÓN DE LAS CLASES NECESARIAS

class birdClass():
	def __init__(self,canvas):
		self.rad = 20
		self.x0 = self.rad+10
		self.y0 = cnvShape[1]/2
		self.acc = 700
		self.parent = canvas
		self.birth()

	def birth(self):
		self.bbox = [[self.x0-self.rad, self.y0-self.rad],[self.x0+self.rad,self.y0+self.rad]]
		self.draw = self.parent.create_oval(self.bbox[0][0],self.bbox[0][1],self.bbox[1][0],self.bbox[1][1],fill="#F6F916")
		self.vel = 0

	def dead(self):
		self.parent.delete(self.draw)

	def move_up(self):
		self.vel -= 400

	def move_down(self):
		dx = 0
		dy = self.vel*dt+0.5*self.acc*dt**2
		self.parent.move(self.draw,dx,dy)
		self.vel = self.vel+self.acc*dt
		self.bbox[0][0] += dx
		self.bbox[0][1] += dy
		self.bbox[1][0] += dx
		self.bbox[1][1] += dy


class doorClass():
	def __init__(self,canvas):
		self.w = 50
		self.h = 100
		self.x = cnvShape[0]
		self.y = rd.randint(self.h+10, cnvShape[1]-10)
		self.parent = canvas

	def create(self):
		x0 = cnvShape[0]; y0=0
		x1 = cnvShape[0]+self.w; y1=self.y-self.h
		self.supWall = self.parent.create_rectangle(x0,y0,x1,y1,fill="#38D258")

		x0 = cnvShape[0]; y0=self.y
		x1 = cnvShape[0]+self.w; y1=cnvShape[1]
		self.infWall = self.parent.create_rectangle(x0,y0,x1,y1,fill="#38D258")

	def destroy(self):
		self.parent.delete(self.supWall)
		self.parent.delete(self.infWall)

	def move(self,dx):
		dy = 0
		self.parent.move(self.supWall,dx,dy)
		self.parent.move(self.infWall,dx,dy)
		self.x += dx
		self.y += dy


class spaceClass():
	def __init__(self,canvas):
		self.disp = 0
		self.vel = -70
		self.acc = -20
		self.blanck = 300
		self.doors = []
		self.doorsID = []
		self.parent = canvas
		self.add_door()

	def move(self):
		dx = self.vel*dt+0.5*self.acc*dt**2
		self.vel = self.vel+self.acc*dt
		self.disp +=dx
		for iDoor in self.doors:
			iDoor.move(dx)

		self.lastChange = 0
		if -self.disp > self.blanck:
			self.add_door()
			self.disp = 0
		if self.doors[0].x + self.doors[0].w < 0:
			self.destroy_door()

	def add_door(self):
		self.doors.append(doorClass(self.parent))
		self.doors[-1].create()
		if self.doorsID:
			self.doorsID.append(self.doorsID[-1]+1)
		else:
			self.doorsID.append(0)

	def destroy_door(self):
		self.doors[0].destroy()
		self.doors.pop(0)
		self.doorsID.pop(0)

	def reset(self):		
		self.vel = -80
		self.disp = 0
		for i in range(len(self.doors)):
			self.destroy_door()
		self.add_door()

# DEFINICIÓN DE FUNCIONES #

def mousse_pressed(event):
	bird.move_up()

def update_score(state,reset=False):
	if reset:
		scoreVar.set("SCORE: 0")
		return
	textList = scoreVar.get().split()
	number = int(textList[-1])
	if state == 0:
		number += 10
	elif state == 1:
		number += 20
	elif state == 2:
		number += 5
	scoreVar.set("SCORE: "+str(number))

def track_bird(bird,space,doorID):
	dist = bird.rad
	ind = space.doorsID.index(doorID)
	activeDoor = space.doors[ind]
	check1 = bird.bbox[1][1] > cnvShape[1]
	check2 = bird.bbox[0][1] < 0
	check3 = activeDoor.x < bird.bbox[1][0]
	check4 = activeDoor.y-activeDoor.h > bird.bbox[0][1]
	check5 = activeDoor.y < bird.bbox[1][1]
	if check1 | check2:
		dist = 0
	elif check3 & check4:
		center = []
		center.append(0.5*(bird.bbox[0][0]+bird.bbox[1][0]))
		center.append(0.5*(bird.bbox[0][1]+bird.bbox[1][1]))
		if center[0] > activeDoor.x+activeDoor.w:
			vertex = []
			vertex.append(activeDoor.x+activeDoor.w)
			vertex.append(activeDoor.y-activeDoor.h)
			dist = sum([(vertex[i]-center[i])**2 for i in range(2)])**0.5
		elif center[0] < activeDoor.x:
			vertex = []
			vertex.append(activeDoor.x)
			vertex.append(activeDoor.y-activeDoor.h)
			dist = sum([(vertex[i]-center[i])**2 for i in range(2)])**0.5
		else:
			dist = 0
	elif check3 & check5:
		center = []
		center.append(0.5*(bird.bbox[0][0]+bird.bbox[1][0]))
		center.append(0.5*(bird.bbox[0][1]+bird.bbox[1][1]))
		if center[0] > activeDoor.x+activeDoor.w:
			vertex = []
			vertex.append(activeDoor.x+activeDoor.w)
			vertex.append(activeDoor.y)
			dist = sum([(vertex[i]-center[i])**2 for i in range(2)])**0.5
		elif center[0] < activeDoor.x:
			vertex = []
			vertex.append(activeDoor.x)
			vertex.append(activeDoor.y)
			dist = sum([(vertex[i]-center[i])**2 for i in range(2)])**0.5
		else:
			dist = 0
	if dist < bird.rad:
		reset_game()
		doorID = 0
	elif activeDoor.x+activeDoor.w < bird.bbox[0][0]:
		update_score(0)
		doorID += 1
	return doorID

def reset_game():
	bird.dead()
	bird.birth()
	space.reset()
	update_score(0,True)



# GENERACIÓN DE LA INTERFAZ GRÁFICA #

root = Tk()
scoreVar = StringVar(root, value="SCORE: 0")
root.resizable(width=False, height=False)
scoreLabel = Label(root)
scoreLabel.config(textvariable=scoreVar, fg="#3EFF00", font=("Courier New",18,"bold"))
scoreLabel.config(height=1, bg="black", relief="groove")
scoreLabel.pack(fill=X)
cnv = Canvas(root,width=cnvShape[0],height=cnvShape[1])
cnv.config(bg='#4DF9E4')
cnv.bind("<Button-1>",mousse_pressed)
cnv.pack()

# EJECUCIÓN DEL PROGRAMA #

bird = birdClass(cnv)
space = spaceClass(cnv)
doorID = 0
t=tic()
while True:
	if tic()-t > dt:
		bird.move_down()
		space.move()
		doorID = track_bird(bird,space,doorID)
		t=tic()
	root.update_idletasks()
	root.update()