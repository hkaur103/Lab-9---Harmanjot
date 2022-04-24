import imghdr
from tkinter import *
from tkinter import ttk
from pokkeemon import get_pokemon_list, get_pokemon_img_url
from pokkeemon import get_pokemon_Infos
import os
import sys
import ctypes
import requests

def main():

#it gives full path to directory where our script exists
    script_dir = sys.path[0]
    #os.path checks that the directory exist
    images_dir = os.path.join(script_dir, 'Images')
   # makes a directory named image whether or not the image is downloaded.
    if not os.path.isdir(images_dir):
        os.makedirs(images_dir)

    root = Tk()
    root.title('Pokemon Image Viewer')

    #access function that will set a pokeicon on taskbar
    app_id = 'COMP593.PokemonImageViwer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

# getting icon that we downloaded  
    root.iconbitmap(os.path.join(script_dir, "Poke-Ball.ico"))
    
#Getting a resizable window
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
# makes a frame with resizable window
    frm = ttk.Frame(root)
    frm.grid(stick=(N,S,E,W))
    frm.columnconfigure(0, weight=1)
    frm.rowconfigure(0, weight=1)

#  getting pokeball icon using photoimage as it displays image on GUI
    img_pokemon = PhotoImage(file=os.path.join(script_dir, 'poke-ball.png'))
    lbl_image = Label(frm, image=img_pokemon)
    lbl_image.grid(row=0, column=0, padx=10, pady=10)

# getting a list of pokemons with a 1000 limit and sorting the 
    pokemon_list = get_pokemon_list(limit=1000)
    pokemon_list.sort()

# setting a combobox to get a list of options from which we can select name of pokemons and set the combobox default name
    cbo_pokemon_sel = ttk.Combobox(frm, values= pokemon_list, state= 'readonly', )
    cbo_pokemon_sel.set('Select a Pokemon')
    cbo_pokemon_sel.grid(row=1, column=0)

# here this function handles events of combobox, which means when we select any option
# from combobox it will show a pokemon image.
    def handle_cbo_pokmon_sel(event):
        pokemon_name = cbo_pokemon_sel.get()
        # getting a pokemon image from list of all pokemons
        image_url = get_pokemon_img_url(pokemon_name)
        pass
        image_path = os.path.join(images_dir, pokemon_name + '.png')

        # downloadind and saving the pokemon image
        if dwnld_img_from_url(image_url, image_path):
            img_pokemon['file'] = image_path
            #disbaling the desktop button after selecting pokemon, so that we can set image to desktop
            btn_set_desktop.state(['!disabled'])

# generate event when we select a option from combobox
    cbo_pokemon_sel.bind('<<ComboboxSelected>>', handle_cbo_pokmon_sel)

# this function set a desktop image of pokemon that we selected or the image that is in image directory. 
    def btn_set_dsktop_click():
        pokemon_name = cbo_pokemon_sel.get()
        image_path = os.path.join(images_dir, pokemon_name + '.png')
        set_desktop_bckgrnd_img(image_path)

# it creates a desktop button under comboboc which is set to disabled before selecting image.
    btn_set_desktop = ttk.Button(frm, text='Set as Desktop Image', command=btn_set_dsktop_click)
    btn_set_desktop.state(['disabled'])
    btn_set_desktop.grid(row=2, column=0, padx=10, pady=10)

    

# download and save image of pokemon and check file akes the path of
# a file as a parameter as well as checks whether the given path contains a valid file 
    def dwnld_img_from_url(url, path):

        if os.path.isfile(path):
            return path

        resp_msg = requests.get(url)
        if resp_msg.status_code == 200:
            try:
                img_data = resp_msg.content
                with open(path, 'wb') as fp:
                    fp.write(img_data)
                return path
            except:
                return
        else:
            print('Failed to download image.')
            print('Response code:', resp_msg.status_code)
            print(resp_msg.text)

   # function to show a desktop image error if image not set   
    def set_desktop_bckgrnd_img(path):
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        except:
            print("Eroor setting dsktp bckgrnd img ")

        
    root.mainloop()

main()
    

    

  