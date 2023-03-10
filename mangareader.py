# importing libraries
import os, shutil, atexit 
from pathlib import Path
from tkinter import CENTER, Canvas , filedialog , Tk, Menu 
from PIL import Image , ImageTk
from zipfile import ZipFile

global canvas
global tempdir
tempdir = Path("C:/Users/ADMIN/Desktop/MangaHaven/temp")

def SelectDir():
   try:
      directory = filedialog.askdirectory() 
      return directory
   except:
      pass

# Create File explorer:
def browseFiles():
   try:
     filename = filedialog.askopenfilename(
        initialdir = "Library", 
        title = "Select a Manga", 
        filetypes = (("All files","*.*"),("Comic Book Zip","*.cbz*"),("Zip Files","*.zip*"))
      )
     return filename

   except FileNotFoundError:
        pass

# Create a function to extract pages:
def extractPage(filename, page):
   global tempdir
   try:
      deleteAll()
      with ZipFile(filename, "r") as zipobj:
         listOfDirectories = zipobj.namelist()
         if listOfDirectories[1].endswith((".jpg",".png",".JPG")):
            zipobj.extract(listOfDirectories[page],tempdir)
         else:
            with ZipFile(listOfDirectories):
               zipobj.extract(listOfDirectories[1],tempdir)
         zipobj.close()
   except:
      pass

# create an instance of tkinter window
mangareader = Tk()

# Title of window
mangareader.title("Manga Reader") 

# define the geometry of the window
mangareader.attributes("-fullscreen", False)
mangareader.geometry("600x900")
mangareader.config(background = "grey")
mangareader.resizable(True, True)

# create canvas
canvas = Canvas(mangareader, width = 600 , height = 900 )
canvas.place(relx = 0.5, rely = 0.5 , anchor = CENTER)

# Load bookmark function:
def loadBookmark():
   global file
   global pageNum
   bmark = open("bookmark.txt","r")
   str = bmark.read()
   file, pageNumStr = str.split(" at page ")
   pageNum = int(pageNumStr)
   extractPage(file, pageNum)
   display()

def Denest(path):
   global new_path
   global new_path2
   dirs = os.listdir(path)
   new_path = Path(path, dirs[0])
   if dirs[0].endswith((".jpg",".png",".JPG")):
      try:
         nested_path = os.listdir(new_path)
         new_path = Path(path, dirs[0], nested_path[0])
      except NotADirectoryError:
         pass
      return new_path

   else:
      new_path2 = Denest(new_path)
      return new_path2

# function to display images: 
def display():
   try:
      global displayed_image
      global tempdir
      global canvas
      canvas.delete("all")
      image_path = Denest(tempdir)
      image = Image.open(image_path)
      panel_height = canvas.winfo_height()
      image_width, image_height = image.size
      aspect_ratio =  image_width/ image_height
      panel_width = int(aspect_ratio*(panel_height))
      panel_pos_x = int(panel_width/2)
      panel_pos_y = int(panel_height/2)
      resized_im = image.resize((panel_width,panel_height))
      displayed_image = ImageTk.PhotoImage(resized_im)
      canvas.create_image(panel_pos_x , panel_pos_y , image = displayed_image)
      canvas.place(relx = 0.5, rely = 0.5 , anchor = CENTER)
   except IndexError:
      extractPage(file, pageNum + 1 )
      display()
   except FileNotFoundError:
      pass 

#Deletes all files in temp directory
def deleteAll():
   global tempdir
   if os.path.isdir(tempdir):
      for files in os.listdir(tempdir):
         shutil.rmtree(tempdir)
   else:
      pass

#extracts the first page (usually the cover)
def getManga():
   global pageNum
   global tempdir
   global file
   pageNum = 1
   file = browseFiles()
   extractPage(file, pageNum)
   display()

def nextPage():
   global pageNum
   global file
   pageNum = pageNum + 1
   deleteAll()
   extractPage(file, pageNum)
   display()

def previousPage():
   global pageNum
   global file
   pageNum = pageNum - 1
   deleteAll()
   extractPage(file, pageNum)
   display()

def bookmark():
   global pageNum
   global file
   bmark = open("bookmark.txt","w")
   pageNumStr = str(pageNum)
   sep = " at page "
   string = (file , sep , pageNumStr)
   bmark.writelines(string)
   bmark.close()

def ConfigWindow():
   configwin = Tk()
   configwin.title("Configure Manga Reader")
   configwin.attributes("-fullscreen", False)
   configwin.geometry("600x300")
   configwin.config(background = "grey")
   configwin.resizable(True, True)
   
atexit.register(deleteAll)

#Add menu bar

menubar = Menu(mangareader)
menubar.add_command(label = "Browse", command= getManga)
menubar.add_command(label = "Load Bookmark", command = loadBookmark)
menubar.add_command(label = "Previous", command = previousPage)
menubar.add_command(label = "Next", command = nextPage)
menubar.add_command(label = "Bookmark", command = bookmark)
menubar.add_command(label = "Exit", command= mangareader.quit)
menubar.add_command(label = "Config", command= ConfigWindow )

mangareader.config(menu= menubar)
mangareader.mainloop()