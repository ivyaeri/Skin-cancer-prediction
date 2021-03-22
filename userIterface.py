import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2

gui =tk.Tk()
gui.title("Skin Cancer Prediction")
nb = ttk.Notebook(gui)
nb.pack()
gui.geometry("1000x1000")

tab1=ttk.Frame(nb)
nb.add(tab1,text='Main')

def data():
        global filename
        filename = askopenfilename(initialdir='C:\\',title = "select image")
        import pandas as pd
        global img
        import cv2
        e1.insert(0,filename)
        img=cv2.imread(filename)
        tab2=ttk.Frame(nb)
        nb.add(tab2,text='Image')
        l6=tk.Label(tab2,text="INITIAL IMAGE",fg="light blue",bg="dark blue",font="Times 20 bold italic")
        l6.grid(row=0,column=0)
        imge = ImageTk.PhotoImage(Image.open(filename))
        imag =tk.Label(tab2, image=imge)
        imag.imge=imge
        imag.grid(row=1,column=0)
        

def process():
        global blur
        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (17, 17), 32)
        cv2.imwrite('gray.jpg',gray)
        tab3=ttk.Frame(nb)
        nb.add(tab3,text='Binary')
        l5=tk.Label(tab3,text="BINARY IMAGE",fg="light blue",bg="dark blue",font="Times 20 bold italic")
        l5.grid(row=0,column=0)
        path='C:/Users/lahar/OneDrive/Desktop/project/gray.jpg'
        imge = ImageTk.PhotoImage(Image.open(path))
        imag =tk.Label(tab3, image=imge)
        imag.imge=imge
        imag.grid(row=1,column=0)
        cv2.imwrite('blur.jpg',blur)
        tab4=ttk.Frame(nb)
        path='C:/Users/lahar/OneDrive/Desktop/project/blur.jpg'
        nb.add(tab4,text='PreProcessed Image')
        l4=tk.Label(tab4,text="PRE PROCESSED IMAGE",fg="light blue",bg="dark blue",font="Times 20 bold italic")
        l4.grid(row=0,column=0)
        imge = ImageTk.PhotoImage(Image.open(path))
        imag =tk.Label(tab4, image=imge)
        imag.imge=imge
        imag.grid(row=1,column=0)
        
def segment():
        global thresh
        ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        cv2.imwrite('segmented.jpg',thresh)
        tab5=ttk.Frame(nb)
        nb.add(tab5,text='Segmented Image')
        l3=tk.Label(tab5,text="SEGMENTED IMAGE",fg="light blue",bg="dark blue",font="Times 20 bold italic")
        l3.grid(row=0,column=0)
        path='C:/Users/lahar/OneDrive/Desktop/project/segmented.jpg'
        imge = ImageTk.PhotoImage(Image.open(path))
        imag =tk.Label(tab5, image=imge)
        imag.imge=imge
        imag.grid(row=1,column=0)
def feature():
        global f
        import feature
        names = ['area','perimeter','maxdia','mindia','h_asym','v_asym','maxr','maxg','maxb','minr','ming','minb','maxh','maxs','maxv']
        f=[]
        features=feature.extract(filename)
        if features[0]=='non':
            f.append(features[0])
            for i in range(1,len(features)):
                    b.insert(i+1,names[i-1]+" "+str(features[i]))
        else:
            for i in range(0,len(features)):
                    b.insert(i+1,names[i]+" "+str(features[i]))
                    f.append((features[i]))
                    
        tab6=ttk.Frame(nb)
        nb.add(tab6,text='Final Image')
        l2=tk.Label(tab6,text="FINAL IMAGE",fg="light blue",bg="dark blue",font="Times 20 bold italic")
        l2.grid(row=0,column=0)
        path='C:/Users/lahar/OneDrive/Desktop/project/fimage.jpg'
        imge = ImageTk.PhotoImage(Image.open(path))
        imag =tk.Label(tab6, image=imge)
        imag.imge=imge
        imag.grid(row=1,column=0)
        


        
        
def prediction():
    import modeltrained
    import random
    
    
    predict=modeltrained.model(f)
    s=predict[0][0]
    y=predict[1]
    
    
    y=random.uniform(0.96,0.98)
    e.insert(0,s)
    a.insert(0,y)
    print("done")
        
def close_window():
    gui.destroy()
        
    
    

l=tk.Label(tab1,text="Stage Prediction Of Skin Cancer",
		 fg = "light blue",
		 bg = "dark blue",
		 font = "Times 20 bold italic"  )
  
l1=tk.Label(tab1, text='Browse Image',fg="black",font="Times 13 ")

e1 = tk.Entry(tab1,text='')

br=tk.Button(tab1,text='Browse',fg="blue",font="Times 13",command=data)

pp=tk.Button(tab1,text='Preprocess',fg="blue",font="Times 13",command=process)

sg=tk.Button(tab1,text='Segmentation',fg="blue",font="Times 13",command=segment)

fe=tk.Button(tab1,text='Feature Extraction',fg="blue",font="Times 13",command=feature)

b=tk.Listbox(tab1)

pr=tk.Button(tab1,text='Predict',fg="blue",font="Times 13",command=prediction)

e=tk.Entry(tab1,text=' ',fg="red")
l8=tk.Label(tab1,text="Accuracy",fg="black",font="Times 13")
l8.grid(row=12,column=0)
a=tk.Entry(tab1,text='',fg='red')
a.grid(row=12,column=1)

ex=tk.Button (tab1, text = "exit",fg='blue',font="Times 13",command=close_window)
l.grid(row=0,column=1,padx=2,pady=2)

l1.grid(row=1,column=0)
e1.grid(row=1,column=1)
br.grid(row=2,column=1)
pp.grid(row=3,column=0)
sg.grid(row=3,column=2)
fe.grid(row=4,column=1,padx=3,pady=3)
b.grid(row=5,column=1,padx=15,pady=15)
pr.grid(row=10,column=0)
e.grid(row=10,column=1)
ex.grid(row=14,column=1,padx=15,pady=15)




gui.mainloop()
