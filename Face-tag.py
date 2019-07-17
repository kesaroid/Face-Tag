from shutil import copy2
from time import sleep
from tkinter import Tk, Button, Text, Entry, Label, Scrollbar, VERTICAL
import face_recognition
from threading import Thread
import PIL
import os, sys

def display_face(image, face_locations):
    for faces in face_locations:
        top, right, bottom, left = faces

        face_image = image[top:bottom, left:right]
        pil_image = PIL.Image.fromarray(face_image)
        pil_image.show(title='Faces')

def find_faces():
    try:
        image = face_recognition.load_image_file(e1.get())
    except Exception:
        print('No image has been input. Aborting ... ')
        quit()
    face_locations = face_recognition.face_locations(image)
    print("Found {} face(s) in this photograph.".format(len(face_locations)))
    display_face(image, face_locations)

class StdoutRedirector(object):
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

def find_similiar_faces():
    try:
        folder_path = e2.get() + '/'
        images_list = os.listdir(e2.get())
    except FileNotFoundError:
        print('No file named ', e2.get())
        return

    # Face encode known image
    known_image = face_recognition.load_image_file(e1.get())
    try:
        face_encoding = face_recognition.face_encodings(known_image)
    except IndexError:
        print("I wasn't able to locate a single person in this image. Check the image files. Aborting...")
    
    # Loop through unknown images and compartmentalize
    for face_id, known_elements in enumerate(face_encoding):
        print('############################################\nChecking for images with person ', face_id + 1, '\n') 
        known_faces = [known_elements]
        new_dir = 'person_' + str(face_id + 1)

        try:
            print('------ Creating a folder named ', new_dir, '------')
            os.mkdir(new_dir)
        except FileExistsError:
            pass
        
        for image_element in images_list:
            print('Checking image: ', image_element)
            unknown_image = face_recognition.load_image_file(folder_path + image_element)
            try:
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)
            except IndexError:
                print("No faces in the image. Checking next image ..")
                continue

            for unknown_faces in unknown_face_encoding:
                result = face_recognition.compare_faces(known_faces, unknown_faces)

                if result[0]:
                    print('Found the person ', face_id + 1, '\n')
                    copy2(folder_path + image_element, new_dir)
    
    print('\n############################################\n\nSegregation has been Completed')
                    

if __name__ == '__main__':
    
    t1 = Thread(target=find_similiar_faces, daemon=True)

    master = Tk()
    master.title('Album-nator by Kesar.')
    master.geometry('400x500')
    master.configure(background='beige')

    l1 = Label(master, text="Reference Image: ", font=("Times New Roman", 14), padx=20, bg='beige')
    l1.grid(row=0, column=0)

    l2 = Label(master, text="Image Directory: ", font=("Times New Roman", 14), padx=20, bg='beige')
    l2.grid(row=2, column=0)

    e1 = Entry(master, font=("Times New Roman", 14)) 
    e1.grid(row=0, column=1, padx=10) 

    e2 = Entry(master, font=("Times New Roman", 14)) 
    e2.grid(row=2, column=1, padx=10) 

    b1 = Button(master, text='Find faces', width=25, height=2, font=("Times New Roman", 13), command=find_faces) 
    b1.grid(row=1, column=0, columnspan=2, pady=10)

    b2 = Button(master, text='Sort People', width=25, height=2, font=("Times New Roman", 13), command=t1.start) 
    b2.grid(row=3, column=0, columnspan=2, pady=10)    

    text1 = Text(master, height=17, width=47)
    text1.grid(row=4, column=0, columnspan=2, pady=20)
    
    scroll = Scrollbar(master, command=text1.yview, orient=VERTICAL)
    scroll.grid(row=4, column=2, rowspan=1)
    
    scroll.config(command=text1.yview)
    text1.configure(yscrollcommand=scroll.set)

    sys.stdout = StdoutRedirector(text1)

    master.mainloop()