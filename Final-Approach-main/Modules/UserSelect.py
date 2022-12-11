from tkinter import *
import os, pickle, sys
sys.path.append('../Final-Approach')
import Modules.Navigator as Navigator

# Stores Directories for User Selection
selected_directories = set()

def main():

    Launch = Navigator.LaunchModule()

    window = Tk()
    window.title("Final Approach")
    window.geometry("900x600")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 600,
        width = 900,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
    canvas.place(x = 0, y = 0)

    tklogo = PhotoImage(file = r"Modules\GUI\icons.png")
    window.iconphoto(False, tklogo)

    background_img = PhotoImage(file = r"Modules\GUI\background.png")
    background = canvas.create_image(
        450.0, 300.0,
        image=background_img)

    img0 = PhotoImage(file = r"Modules\GUI\split.png")
    b0 = Button(
        image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = Launch.mod_breakCSV,
        relief = "flat",
        )
    b0.place(
        x = 178, y = 258,
        width = 200,
        height = 90)

    img1 = PhotoImage(file = r"Modules\GUI\load.png")
    b1 = Button(
        image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = load_file,
        relief = "flat")
    b1.place(
        x = 540, y = 211,
        width = 200,
        height = 90)

    img2 = PhotoImage(file = r"Modules\GUI\graph.png")
    b2 = Button(
        image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = window.destroy,
        relief = "flat")
    b2.place(
        x = 540, y = 320,
        width = 200,
        height = 90)

    window.resizable(False, False)
    window.mainloop()

    # Serialize and Store User Selection from GUI
    with open('Modules/Caches/directories.pkl', 'wb') as file:
        # A new file will be created
        pickle.dump(selected_directories, file)

def load_file():
    global selected_directories
    
    plotFolder = os.listdir('Plot_Folder')
    root = os.getcwd()

    #  Gets Absolute path of selected file 
    for i in plotFolder:
        filepath = f'{root}\Plot_Folder\{i}'
        
        if os.path.isfile(filepath):
            selected_directories.add(filepath)

if __name__ == '__main__':
    main()