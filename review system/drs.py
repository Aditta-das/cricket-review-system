import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time


stream = cv2.VideoCapture("Virat Kohli's brilliant fielding.mp4")
flag = True
def play(speed):
	global flag
	print(f"You clicked on Play {speed}")
		# play reverse
	frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
	stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
	grabbed, frame = stream.read()
	if not grabbed:
		exit()
	grabbed, frame = stream.read()
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
	if flag:
		canvas.create_text(120, 25, fill="red", font="Arial 20", text="Decision Pending")
	flag = not flag


def pending(decision):
	# Display Decision pending
	frame = cv2.cvtColor(cv2.imread("decision-pending.jpg"), cv2.COLOR_BGR2RGB)
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
	# wait 1 second
	time.sleep(1)
	# Display sponsor
	frame = cv2.cvtColor(cv2.imread("sponsor.png"), cv2.COLOR_BGR2RGB)
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
	# wait 1.5 second
	time.sleep(1.5)
	# display out/notout
	if decision == "out":
		decisionImg = "out.png"
	else:
		decisionImg = "notout.jpg"

	frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
	frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
	frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)


def out():
	thread = threading.Thread(target=pending, args=("out",))
	thread.daemon = 1
	thread.start()
	print(f"Player is OUT")

def notout():
	thread = threading.Thread(target=pending, args=("not out",))
	thread.daemon = 1
	thread.start()
	print("Player is NOTOUT")

# width and height of main screen
SET_WIDTH = 850
SET_HEIGHT = 500

# tkinter starts from here
window = tkinter.Tk()
window.title("Third Umpier Decision Review")

cv_img = cv2.cvtColor(cv2.imread("welcome.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()


# Button to control
btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25))
btn.pack()

btn = tkinter.Button(window, text="Give OUT", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give NOT OUT", width=50, command=notout)
btn.pack()
window.mainloop()