import casioplot
from math import sqrt
from math import pi
from math import cos
from math import sin
from math import atan2

turtleshapes={"classic":[[-9,5],[-9,4],[-8,4],[-8,3],[-8,2],[-8,-2],[-8,-3],[-8,-4],[-9,-4],[-9,-5],[-7,4],[-7,1],[-7,0],[-7,-1],[-7,-4],[-6,3],[-6,-3],[-5,3],[-5,-3],[-4,2],[-4,-2],[-3,2],[-3,-2],[-2,1],[-2,-1],[-1,1],[-1,-1],[0,0]],"turtle": [[-3,3],[2,3],[-2,2],[-1,2],[0,2],[1,2],[-2,1],[-1,1],[1,1],[0,1],[2,1],[3,1],[-2,0],[-1,0],[0,0],[1,0],[-1,-1],[-2,-1],[0,-1],[1,-1],[2,0],[3,0],[-3,-2],[2,-2]]}
turtle_name="classic"
turtle_data=turtleshapes[turtle_name]
turtle_pos=[0,0]
turtle_angle=0
turtle_color=(0,0,0)
writing=True
pen_size=1
turtle_buffer=[[]]
turtle_speed=5
frame_count=0
turtle_visible=True

def draw_turtle(x,y,a,c):
  global turtle_buffer
  def inbuffer(x,y):
    inlist=False
    for i in range(1,len(turtle_buffer)):
      if x==turtle_buffer[i][0] and y==turtle_buffer[i][1]:
        inlist=True
    return inlist
  if turtle_visible==True:
    u=cos(a*pi/180)
    v=sin(a*pi/180)
    for point in turtle_data:
      xx=x+(point[0]*u-point[1]*v)
      yy=y+(point[1]*u+point[0]*v)
      xpixel=int(round(xx+192))
      ypixel=int(round(-yy+96))
      if (0<=xpixel<=383 and 0<=ypixel<=191):
        if not inbuffer(xpixel,ypixel):
          turtle_buffer+=[[xpixel,ypixel,casioplot.get_pixel(xpixel,ypixel)]]
        casioplot.set_pixel(xpixel,ypixel,c)

def erase_turtle():
  global turtle_buffer
  for i in range(1,len(turtle_buffer)):
    xpixel=turtle_buffer[i][0]
    ypixel=turtle_buffer[i][1]
    if turtle_buffer[i][2]!=None :
      lastcolor=turtle_buffer[i][2]
    else:
      lastcolor=(255,255,255)
    casioplot.set_pixel(xpixel,ypixel,lastcolor)
  turtle_buffer=[[]]

def pen_brush(x,y,turtle_color):
  global frame_count
  erase_turtle()
  xpixel=int(round(x+192))
  ypixel=int(round(-y+96))
  if writing==True and (0<=xpixel<=383 and 0<=ypixel<=191) :
    colorpixel=(int(turtle_color[0]*255), int(turtle_color[1]*255),int(turtle_color[2]*255))
    casioplot.set_pixel(xpixel,ypixel,colorpixel)
    frame_count+=1
    if turtle_speed!=0:
      if frame_count%(turtle_speed*4)==0:
        draw_turtle(x,y,turtle_angle,colorpixel)
        casioplot.show_screen()
    else :
      if frame_count%500==0:
        draw_turtle(x,y,turtle_angle,colorpixel)
        casioplot.show_screen()

def refresh_turtle():
  c=(int(turtle_color[0]*255), int(turtle_color[1]*255),int(turtle_color[2]*255))
  erase_turtle()
  draw_turtle(turtle_pos[0],turtle_pos[1],turtle_angle,c)
  casioplot.show_screen()

def back(n):
  forward(-n)

def backward(n):
  back(n)

def bk(n):
  back(n)

def circle(radius,extent=360):
  global  turtle_angle, turtle_pos
  x1=turtle_pos[0]
  y1=turtle_pos[1]
  if round(radius)==0:
    pen_brush(x1,y1,turtle_color)
    turtle_angle+=extent
  elif round(extent,8)==0:
    pen_brush(x1,y1,turtle_color)
  else:
    e=radius/abs(radius)
    theta=extent*pi/180*e
    Rx=cos(theta)
    Ry=sin(theta)
    Dx=radius*sin(turtle_angle*pi/180)
    Dy=-radius*cos(turtle_angle*pi/180)
    xcenter=x1-Dx
    ycenter=y1-Dy
    nbpixelarc=int(round(abs(radius*theta*1.05)))
    angle=turtle_angle
    if nbpixelarc!=0:
      alpha=theta/nbpixelarc
      for k in range(nbpixelarc+1):
        x=xcenter+Dx*cos(alpha*k)-Dy*sin(alpha*k)
        y=ycenter+Dx*sin(alpha*k)+Dy*cos(alpha*k)
        turtle_angle+=alpha*180/pi
        pen_brush(x,y,turtle_color)
    turtle_pos[0]=xcenter+Dx*Rx-Dy*Ry
    turtle_pos[1]=ycenter+Dx*Ry+Dy*Rx
    turtle_angle=angle+extent*e
  refresh_turtle()

def clear():
  erase_turtle()
  casioplot.clear_screen()
  casioplot.show_screen()
  refresh_turtle()

def distance(x,y):
  return sqrt((x-turtle_pos[0])**2+(y-turtle_pos[1])**2)

def down():
  global writing
  writing=True

def fd(d):
  forward(d)

def forward(d):
  global turtle_pos
  dx=d*cos(turtle_angle*pi/180)
  dy=d*sin(turtle_angle*pi/180)
  x1=turtle_pos[0]
  y1=turtle_pos[1]
  if round(abs(d))==0:
    pen_brush(x1+dx,y1+dy,turtle_color)
  elif abs(dx)>=abs(dy):
    e=int(dx/abs(dx))
    m=dy/dx
    p=y1-m*x1
    for x in range(int(round(x1)),int(round(x1+dx)),e):
      pen_brush(x,m*x+p,turtle_color)
  else:
    e=int(dy/abs(dy))
    m=dx/dy
    p=x1-m*y1
    for y in range(int(round(y1)),int(round(y1+dy)),e):
      pen_brush(m*y+p,y,turtle_color)
  turtle_pos[0]+=dx
  turtle_pos[1]+=dy
  refresh_turtle()

def goto(x,y):
  a=turtle_angle
  setheading(towards(x,y))
  forward(distance(x,y))
  setheading(a)
  refresh_turtle()

def heading():
  return turtle_angle

def hideturtle():
  global turtle_visible
  turtle_visible=False
  refresh_turtle()

def home():
  global turtle_pos,turtle_angle
  turtle_pos[0]=turtle_pos[1]=0
  turtle_angle=0
  refresh_turtle()

def ht():
  hideturtle()

def isdown():
  return writing

def isvisible():
  return turtle_visible

def left(a):
  right(-a)

def lt(a):
  right(-a)

def pd():
  down()

def pencolor(*c):
  global turtle_color
  colornames={"black":(0,0,0),"blue":(0,0,1),"green":(0,1,0),"red":(1,0,0),"cyan":(0,1,1),"yellow":(1,1,0),"magenta":(1,0,1),"white":(1,1,1),"orange":(1,0.65,0),"purple":(0.66,0,0.66),"brown":(0.75,0.25,0.25),"pink":(1,0.75,0.8),"grey":(0.66,0.66,0.66)}
  if c==():
    return turtle_color
  elif c[0] in colornames:
    turtle_color=colornames[c[0]]
  elif isinstance(c[0],(list,tuple)) and len(c[0])==3 and isinstance(c[0][0],(int,float)) and isinstance(c[0][1],(int,float)) and isinstance(c[0][2],(int,float)) and 0<=c[0][0]<=1 and 0<=c[0][1]<=1 and 0<=c[0][2]<=1:
    turtle_color=list(c[0])
  else:
    raise ValueError('error using pencolor : enter a color text or 3 floats between 0 and 1')
  refresh_turtle()

def pendown():
  down()

def pensize(n):
  global pen_size
  pen_size=n
  refresh_turtle()

def penup():
  global writing
  writing=False

def pos():
  return (xcor(),ycor())

def position():
  return (xcor(),ycor())

def pu():
  penup()

def reset():
  global turtle_color,writing,pen_size,speed,turtle_visible
  clear()
  turtle_color=(0,0,0)
  home()
  writing=True
  pen_size=1
  speed=5
  turtle_visible=True
  shape("classic")
  refresh_turtle()

def right(a):
  global turtle_angle
  turtle_angle-=a
  refresh_turtle()

def rt(a):
  right(a)

def seth(a):
  setheading(a)

def setheading(a):
  global turtle_angle
  turtle_angle=a
  refresh_turtle()

def setpos(x,y):
  goto(x,y)
  refresh_turtle()

def setposition(x,y):
  setpos(x,y)

def setx(x):
  global turtle_pos
  turtle_pos[0]=x
  refresh_turtle()

def sety(y):
  global turtle_pos
  turtle_pos[1]=y
  refresh_turtle()

def shape(text=None):
  global turtle_name,turtle_data
  if text==None:
    return turtle_name
  elif text in turtleshapes:
    turtle_name=text
    turtle_data=turtleshapes[text]
  else:
    raise ValueError('available shapes: "classic" or "turtle"')
  refresh_turtle()

def showturtle():
  global turtle_visible
  turtle_visible=True
  refresh_turtle()

def speed(v=None):
  global turtle_speed
  speedwords = {'fastest':0, 'fast':10, 'normal':6, 'slow':3, 'slowest':1 }
  if v==None:
    pass
  elif isinstance(v,(int,float)) and (v<=0.5 or v>=10.5):
    turtle_speed=0
  elif isinstance(v,(int,float)) and (0.5<v<10.5):
    turtle_speed=int(round(v))
  elif isinstance(v,str) and v in speedwords:
    turtle_speed=speedwords[v]
  else:
    raise ValueError("Error using function speed: enter a real between 0 & 10")

def st():
  showturtle()

def towards(x,y):
  if round(x-turtle_pos[0],8)==0 and round(y-turtle_pos[1],8)==0:
    return 0
  else:
    return (atan2(y-turtle_pos[1],x-turtle_pos[0])*180/pi)

def up():
  penup()

def width(n):
  pensize(n)

def write(text):
  xpixel=int(round(turtle_pos[0]+192))
  ypixel=int(round(-turtle_pos[1]+96))
  c=(int(turtle_color[0]*255), int(turtle_color[1]*255),int(turtle_color[2]*255))
  casioplot.draw_string(xpixel,ypixel,str(text),c,"small")
  casioplot.show_screen()

def xcor():
  return round(turtle_pos[0],6)
def ycor():
  return round(turtle_pos[1],6)