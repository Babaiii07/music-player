import pygame.mixer as mixer
from tkinter import *
from tkinter import filedialog
import audio_metadata
from PIL import ImageTk, Image
from io import BytesIO
import os
import time

def play_song(song_name: StringVar, song_list: Listbox, status: StringVar):
    name = song_list.get(ACTIVE)
    if len(name) > 40:
        name = (name[:35] + '.mp3')
    song_name.set(name)
    mixer.music.load(song_list.get(ACTIVE))
    mixer.music.play()
    global duration, metadata
    metadata=audio_metadata.load(song_list.get(ACTIVE))
    song_len = metadata.streaminfo['duration']
    duration = time.strftime('%M:%S', time.gmtime(song_len))
    play_time()

    status.set("Song Playing..")

    if resume_btn['state'] == DISABLED:
        resume_btn['state'] = NORMAL

    
def stop_song(status: StringVar):
    mixer.music.stop()
    status.set("Song Stopped!!")

    resume_btn['state'] = DISABLED
 
def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("Song Paused!")

def resume_song(status: StringVar):
    mixer.music.unpause()
    if status.get() == "<Not Available>":
        status.set("Please Select a song!")
    else:
        status.set("Song Playing..")
 
def load(listbox):
    
    os.chdir(filedialog.askdirectory(title="Open a song Directory"))
    
    tracks = os.listdir()

    for track in tracks:
        listbox.insert(END, track)

def volume(x):
    value = volume_slider.get()
    mixer.music.set_volume(value/100)

def play_time():
    current_time = mixer.music.get_pos() / 1000

    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    
    song_duration = duration
    if song_status.get() != 'Song Stopped!!':
        duration_frame.config(text=f"Time Elapsed: {converted_current_time} / {song_duration}")
    else:
       duration_frame.config(text=f"Time Elapsed: 00:00 / {song_duration}") 

    duration_frame.after(1000, play_time)

def get_song_img():
    artwork = metadata.pictures[0].data
    stream = BytesIO(artwork)
    
    img = Image.open(stream)
    img_size = img.resize((50, 50))
    new_img = ImageTk.PhotoImage(img_size)

    image_label = Label(root, image=new_img)
    image_label.place(x=150, y=190)

mixer.init()

root = Tk()
root.geometry('700x270')
root.title('My Music Player')

root.resizable(False, False)

song_frame = LabelFrame(root, text="Current song", bg='LightBlue', width=506, height=90)
song_frame.place(x=0, y=0)

button_frame = LabelFrame(root, text="Control Buttons", bg='Turquoise', width=506, height=160)
button_frame.place(y=90)

listbox_frame = LabelFrame(root, text='Playlist', bg="RoyalBlue", height=200, width=300)
listbox_frame.place(x=505, y=0)

volume_frame = LabelFrame(root, text="Volume", bg="Turquoise")
volume_frame.place(x=400, y=100)

duration_frame = Label(root, bg='pink', text='Time Elapsed: 00:00 / 00:00', bd=2, relief=GROOVE, width=28, height=2, font=('Times', 10, 'bold'))
duration_frame.place(x=505, y=214)

current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')

playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='Gold')

scroll_bar = Scrollbar(listbox_frame, orient=VERTICAL)
scroll_bar.pack(side=RIGHT, fill=BOTH)
scroll_bar.config(command=playlist.yview)

playlist.config(yscrollcommand=scroll_bar.set)
playlist.pack(fill=BOTH, padx=5, pady=5)

Label(song_frame, text="CURRENTLY PLAYING: ", bg="LightBlue", font=('Times', 10, 'bold')).place(x=5, y=20)

song_lbl = Label(song_frame, textvariable=current_song, font=('Times', 12), bg='GoldenRod')
song_lbl.place(x=150, y=20)

pause_btn = Button(button_frame, text="Pause", bg='Aqua', font=('Georgia', 13), width=7, command=lambda: pause_song(song_status))
pause_btn.place(x=15, y=20)

stop_btn = Button(button_frame, text="Stop", bg='Aqua', font=("Georgia", 13), width=7, command=lambda: stop_song(song_status))
stop_btn.place(x=105, y=20)

play_btn = Button(button_frame, text="Play", bg='Aqua', font=("Georgia", 13), width=7, command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=195, y=20)

resume_btn = Button(button_frame, text='Resume', bg="Aqua", font=("Georgia", 13), width=7, command=lambda: resume_song(song_status))
resume_btn.place(x=285, y=20)

dir_btn = Button(button_frame, text="Load Directory", bg='Aqua', font=("Georgia", 13), width=35, command=lambda: load(playlist))
dir_btn.place(x=10, y=75)

volume_slider = Scale(volume_frame, from_=100, to=0, orient=VERTICAL, command=volume, length=110, bg='orange', cursor='hand2')
volume_slider.set(30)
volume_slider.pack()

Label(root, textvariable=song_status, bg='SteelBlue', font=('Times', 8), justify=LEFT).pack(side=BOTTOM, fill=X)

root.update()
root.mainloop()