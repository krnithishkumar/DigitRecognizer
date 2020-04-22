from tkinter import *
import tkinter.font as tkFont
import win32gui
from PIL import ImageGrab, Image
import numpy as np

from keras.models import load_model

'''
Let us deploy the model in the python application using tkinter
'''
class application(Frame):
    def __init__(self,master):
        super().__init__(master)
        self.fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        self.master=master
        self.pack()
        self.createWidget()

    def createWidget(self):
        self.canvas = Canvas(self,width=224,height=224,bg='black')
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind('<B1-Motion>',self.activate_paint)

    def activate_paint(self, event):
        global lastx, lasty
        self.canvas.bind('<B1-Motion>', self.paint)
        lastx, lasty = event.x, event.y

    def paint(self,event):
        global lastx, lasty
        x, y = event.x, event.y
        self.canvas.create_line((lastx, lasty, x, y), width=12, fill='white')

        lastx, lasty = x, y

    def clearCanvas(self):
        self.canvas.delete("all")
        answer.configure(text='Answer Goes Here', font=self.fontStyle)
        self.canvas.bind('<B1-Motion>',self.activate_paint)

    def predicted_result(self, data):
        ans = data.argsort()[-8:][::-1]  #sorting in descending
        return ans


    def predictDigit(self):
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        im = ImageGrab.grab(rect) # get image of the current location
        im.save('file.png')

        img = Image.open('file.png').convert('L')
        img = img.resize((28,28), Image.ANTIALIAS)
        img.save('resized.png')

        #after resizing the image data
        #convert to np array

        data = np.array(img)
        data = data/255.0 # for range b/w 0-1
        data = data.reshape(1, 28, 28, 1).astype('float32')

        #import the model
        model = load_model('./digitrecognition.h5')
        result = model.predict(data)
        ans = self.predicted_result(result)
        
        answer.configure(text='Predicted Digit: '+str(ans[0][-1]), font=self.fontStyle)

        
if __name__ == '__main__':
    root = Tk()
    root.geometry('300x400')
    
    
    app=application(root)
    # let us create button to clear the drawn items and predict the value

    clear = Button(root, text='Clear', command=app.clearCanvas)
    clear.pack()

    predict = Button(root, text='Predict', command=app.predictDigit)
    predict.pack()

    answer = Label(root, text="Answer Goes Here", font=app.fontStyle)
    answer.pack()

    root.title('Draw a Digit')
    root.mainloop()


    #let us run and see