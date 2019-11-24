from tkinter import *
import numpy as np
import sys
import math

# stereo or quad
mode = 4;


if sys.argv[1] == "mode=stereo":
  print("appliying stereo mode")
  mode = 2
#global variables
canvas_width = 512
canvas_height = 512
counter = 0
max_points = 512
last_point = np.array([0,0])

master = Tk()
traj = np.zeros((max_points, 3))
# print(traj)

# variable string for remaining points label
v = StringVar()

master.title( "Dibujar Trayectoria" )
w = Canvas(master, 
           width=canvas_width, 
           height=canvas_height)
w.pack(expand = NO, fill = BOTH)
w.create_line(0, canvas_height/2, canvas_width, canvas_height/2, fill="#aaaaaa")
w.create_line(canvas_width/2, 0, canvas_width/2, canvas_height, fill="#aaaaaa")

def paint( event ):
  global counter
  global max_points
  global v
  if(counter < max_points):
    
    color = math.trunc(np.interp(counter, [0, max_points], [0, 255]))
    
    point_color = '#{:02x}{:02x}{:02x}'.format( color, color , color )
    x1, y1 = ( event.x - 2 ), ( event.y - 2 )
    x2, y2 = ( event.x + 2 ), ( event.y + 2 )
    w.create_oval( x1, y1, x2, y2, fill = point_color)
    y = event.y - canvas_height/2
    x = event.x - canvas_width/2

    r,a = cart2pol(x, y);
    
    #stereo distance
    if mode == 2:
      r = y

    traj[counter] = np.degrees(a)+ 180,abs(y),0
    # print(traj[counter])
    # print("{} | angulo {} - distancia {}".format(traj[counter], a, abs(r)))
    counter = counter + 1
    v.set("{} / {}".format(counter, max_points));
    # print(counter)
  #else:
    #print(traj)

def save_trajectory():
  """saves the trajectory data in a file"""
  # convert
  #traj[::,1::] = np.abs(traj[::,1::])
  #np.abs(traj[::,0:1:], out=traj[::,0:1:])
  # save trajectory file
  print("saving file "+traj_name.get())
  print(traj)
  np.savetxt("traj/"+traj_name.get(), traj[:counter], fmt='%i')

def clean_traj():
  """clear the window"""
  # delete after -1 the traj values

# convert coordinates from cartesian to polar
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

w.bind( "<B1-Motion>", paint )

# traj name imput
Label(master, text="nombre de la trayectoria").pack()
traj_name = Entry(master)
traj_name.pack()
#save button
b = Button(master, text ="Guardar", command = save_trajectory)
b.pack()


message_remain = Label( master, textvariable=v )
message_remain.pack( side = TOP )

#message = Label( master, text = "Press and Drag the mouse to draw" )
#message.pack( side = BOTTOM )


mainloop()