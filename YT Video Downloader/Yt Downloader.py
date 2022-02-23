
# ***************************************** Importing Modules ***********************************

from pytube import YouTube
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror,showinfo,askyesno
from tkinter import filedialog
from PIL import ImageTk,Image
import io 
import urllib
import threading

# ***************************************** Main Window Class *************************************

class Window:
    
    def __init__(self,root):
        
        # =================================== Setting Screen ===================================
        
        self.root = root
        self.root.title("Youtube Downloader")
        self.root.geometry("610x610+370+50")
        self.root.maxsize("610","610")
        self.root.minsize("610","610")
        
        # =================================       =================================================
        
        self.background = Image.open("background.jpg")
        self.background = self.background.resize((610, 610), Image.ANTIALIAS)     
        self.background = ImageTk.PhotoImage(self.background)
        self.background_image = Label(self.root,image=self.background).pack()
        
        # =================================   =======================================================
        
        self.logo = Image.open("logo.png")
        self.logo = self.logo.resize((40, 40), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.logo)
        self.header = Label(self.root,image=self.logo,text="Youtube Downloader",font=("Times New Roman",20,"bold"),fg="white",bg="black",compound=LEFT).place(x = 150,y=50)

        # =================================   ==================================================
        
        self.url = StringVar()
        
        self.f1 = Frame(self.root,bg="#EE384E")
        
        self.l1 = Label(self.f1,text="Enter Video URL:",font=("Times New Roman",15,"bold"),bg="#EE384E").grid(row=0,column=0,padx=10)
        self.e1 = Entry(self.f1,textvar=self.url,font='lucida 12 bold',relief="solid",width=30).grid(row=0,column=1,padx=10)       
        
        self.f1.place(x=70, y=150)
        
        self.b1 = Button(self.root,text="Search",font=("Times New Roman",13,"bold"),command=self.search_vid,bg = "#EE384E",activebackground="#EE384E",relief=SOLID,width=12).place(x=235,y=190)
  
    # =======================================   =========================================================
    
    def search_vid(self):
        
        # try:
            
        self.vid = self.url.get() 
        
        self.yt = Video(self.vid)
        
        #Video Title
        self.vid_name = Label(self.root,text=f"Video Title: {self.yt.vid_title()}",font=("Times New Roman",15,"bold"),bg="black",fg="white",wraplength=545,justify=CENTER).place(x=40,y=240)
        
        #Creating Canvas for the image
        self.f2 = Frame(self.root)
        self.canva = Canvas(self.f2,width=370,height=200)
        self.canva.pack()
        self.canva.create_rectangle(0,0,370,200)
        self.f2.place(x=120,y=305)
        
        # Resizing Pic
        self.image = self.yt.vid_thumbnail().resize((370, 200), Image.ANTIALIAS) 
        self.image = ImageTk.PhotoImage(self.image)
        
        #Placing image into Canvas
        self.l3 = Label(self.canva,image=self.image).pack()
        
        self.res_opt = StringVar()
        self.res_options = ttk.Combobox(self.root,textvariable=self.res_opt,values=tuple(self.yt.res),font=("Times New Roman",14,"bold"),width=20,justify=CENTER,state="readonly").place(x=120,y=530)
        self.res_opt.set("Choose Resolution")
    
        # create Progressbar
        self.pbar = ttk.Progressbar(self.root,length=450,mode="determinate")
        self.pbar.place(x=80,y=575)
        
        # Percentage Label
        
        self.percent = StringVar()
        self.percent.set("0 %")
        self.per = Label(self.root,textvar=self.percent,font=("Times New Roman",11,"bold"),bg="black",fg="white")
        self.per.place(x=530,y=575)
        
        # Download Button
        self.b2 = Button(self.root,text="Download",font=("Times New Roman",13,"bold"),relief=SOLID,width=12,bg="#EE384E",command=self.download_vid).place(x=400,y=530)
            
        # except:
            
        #     showerror("Error","Please enter the correct URL")
        
    def download_vid(self):
        
        self.vid_resolution = self.res_opt.get()
        
        if self.vid_resolution != "Choose Resolution":
        
            self.directory = filedialog.askdirectory()
            
            if len(self.directory) != 0:
                
                self.maxfile_size = self.yt.url.streams.filter(progressive="True",resolution=self.vid_resolution).first().filesize
                print(self.maxfile_size)
                self.pbar.start()
                
                threading.Thread(target=self.yt.url.register_on_progress_callback(self.download_callback)).start()

                # call Download file func
                threading.Thread(target=self.downloading_vid).start()
       
        else:
            
            showerror("Resolution Error","Please select the desired resolution first",parent=self.root)
            
    def downloading_vid(self):
        
        self.yt.url.streams.filter(progressive="True",resolution=self.vid_resolution).first().download(f"{self.directory}")
        
    def download_callback(self,stream=None, chunk=None, file_handle=None, bytes_remaining=None):
        
        self.percent.set(f"{int(100-(100*(bytes_remaining/self.maxfile_size)))}")
        
        
                    
# ************************************* Video Class for Requesting YT Video **********************************

class Video:
    
    def __init__(self,url):
        
        self.url = YouTube(url)
        
        self.resol = ["144p","240p","360p","480p","720p","1080p"]
        self.res = []
        
        self.count = 0
        for i in self.resol:
            a = self.url.streams.filter(progressive="True",res=i)
            if len(list(a))!=0:
                self.res.append(i)
        
    # =================================== Getting Video Title ===========================================
    
    def vid_title(self):
        
        return self.url.title
    
    # =================================== Getting Video Thumbnail =======================================
    
    def vid_thumbnail(self):
        
        self.thumbnail =  self.url.thumbnail_url
        # Requesting image from url
        self.raw_data = urllib.request.urlopen(f"{self.thumbnail}").read()
        self.image = Image.open(io.BytesIO(self.raw_data))
    
        return self.image
        

# ******************************************* Main Code ***************************************

if __name__ == '__main__':
    
    root = Tk()
    main_window = Window(root)
    root.mainloop()
