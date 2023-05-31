from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re
import os

def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)

def openFile():
    global file
    file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close()

def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt', defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                 ("Text Documents", "*.txt")])
        if file =="":
            file = None
        else:
            #Save as a new file
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()
            root.title(os.path.basename(file) + " - Notepad")
            print("File Saved")
    else:
        # Save the file
        f = open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def quitApp():
    root.destroy()
def cut():
    TextArea.event_generate(("<>"))
def copy():
    TextArea.event_generate(("<>"))
def paste():
    TextArea.event_generate(("<>"))
def about():
    showinfo("Notepad", "Notepad by Abdul,Ankit & Aryan")


def find_text():
    find_dialog = Toplevel(root)
    find_dialog.title("Find")
    find_dialog.transient(root)
    
    find_label = Label(find_dialog, text="Find:")
    find_label.pack(side=LEFT)
    find_entry = Entry(find_dialog)
    find_entry.pack(side=LEFT, padx=5)
    
    find_button = Button(find_dialog, text="Find", command=lambda: find(find_entry.get()))
    find_button.pack(side=LEFT)
    
    find_dialog.mainloop()

def find(text):
    start_pos = TextArea.search(text, "1.0", END)
    if start_pos:
        end_pos = start_pos + "+{}c".format(len(text))
        TextArea.tag_remove("found", "1.0", END)
        TextArea.tag_add("found", start_pos, end_pos)
        TextArea.tag_config("found", background="yellow")
        TextArea.mark_set("insert", start_pos)
        TextArea.see("insert")
    else:
        showinfo("Not Found", "Text not found.")

def replace_text():
    replace_dialog = Toplevel(root)
    replace_dialog.title("Replace")
    replace_dialog.transient(root)
    
    find_label = Label(replace_dialog, text="Find:")
    find_label.pack(side=LEFT)
    find_entry = Entry(replace_dialog)
    find_entry.pack(side=LEFT, padx=5)
    
    replace_label = Label(replace_dialog, text="Replace:")
    replace_label.pack(side=LEFT)
    replace_entry = Entry(replace_dialog)
    replace_entry.pack(side=LEFT, padx=5)
    
    replace_button = Button(replace_dialog, text="Replace", command=lambda: replace(find_entry.get(), replace_entry.get()))
    replace_button.pack(side=LEFT)
    
    replace_dialog.mainloop()

def replace(text, replace_text):
    content = TextArea.get("1.0", END)
    modified_content = re.sub(text, replace_text, content)
    if modified_content != content:
        TextArea.delete("1.0", END)
        TextArea.insert(END, modified_content)
        showinfo("Success", "Text replaced successfully.")
    else:
        showinfo("Not Found", "Text not found.")

if __name__ == '__main__':
    #Basic tkinter setup
    root = Tk()
    root.title("Untitled - Notepad")
    # root.wm_iconbitmap("1.ico")//for icon
    root.geometry("1100x600")

    #Add TextArea
    TextArea = Text(root, font="lucida 13")
    file = None
    TextArea.pack(expand=True, fill=BOTH)

    # Lets create a menubar
    MenuBar = Menu(root)

    #File Menu Starts
    FileMenu = Menu(MenuBar, tearoff=0)
    # To open new file
    FileMenu.add_command(label="New", command=newFile)

    #To Open already existing file
    FileMenu.add_command(label="Open", command = openFile)

    # To save the current file

    FileMenu.add_command(label = "Save", command = saveFile)
    FileMenu.add_separator()
    FileMenu.add_command(label = "Exit", command = quitApp)
    MenuBar.add_cascade(label = "File", menu=FileMenu)
    # File Menu ends

    # Edit Menu Starts
    EditMenu = Menu(MenuBar, tearoff=0)
    #To give a feature of cut, copy and paste
    EditMenu.add_command(label = "Cut", command=cut)
    EditMenu.add_command(label = "Copy", command=copy)
    EditMenu.add_command(label = "Paste", command=paste)
    EditMenu.add_command(label="Find", command=find_text)
    EditMenu.add_command(label="Replace", command=replace_text)

    MenuBar.add_cascade(label="Edit", menu = EditMenu)

    # Edit Menu Ends

    # Help Menu Starts
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label = "About Notepad", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    # Help Menu Ends

    root.config(menu=MenuBar)

    #Adding Scrollbar using rules from Tkinter lecture no 22
    Scroll = Scrollbar(TextArea)
    Scroll.pack(side=RIGHT,  fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

    root.mainloop()
