#!/usr/bin/python3.12

import dearpygui.dearpygui as dpg
import time
import os
import sqlite3
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT 

dpg.create_context()

conn = sqlite3.connect('websites_db.db', check_same_thread=False)
cur = conn.cursor()
# cur.execute("CREATE TABLE webst(websites, date_last_save, duration_last_save, folder_size)")   # uncomment for creating the database for the 1st time if no database exist

path_to_save = ""
url_website = ""
#"http://blog.electronique-radioamateur.fr/", "https://vitrine-mam.fr/", "https://jivaro-models.org/", "https://onepage.io/fr/blog"
#"https://wikilibriste.fr/", "https://interstices.info/", "https://korben.info/", "https://www.it-connect.fr", "https://www.geeksforgeeks.org/"
url_lst = []
date_last_save_lst = []
duration_last_save_lst = []
file_size_lst = []
selected_url = ""
prep = ""
current_path_to_save = ""
tag="table"
scloc = os.popen("pwd")
scloc_format = scloc.read()
script_location = scloc_format[0:(len(scloc_format)-1)] + "/"

###########################################################################################################################################################

def delete_old_path_save_folder():
    cur.execute("""DELETE FROM webst WHERE date_last_save LIKE 1900""")
    conn.commit()

def callback_path():
    path_saving = dpg.get_value(path_to_save) + "/"
    print(path_saving)
    #print(dpg.get_value(path_to_save))
    global conn
    delete_old_path_save_folder()
    command = """INSERT INTO webst VALUES (""" + "\"" + path_saving + "\"" + """, 1900, 0, 0)"""
    cur.execute(command)
    conn.commit()
    dpg.set_value(new_path_display, f"New path saved : {path_saving}")
    dpg.set_value(current_path, f"Saving current path : {path_saving}")

def read_path_save_folder():
    global current_path_to_save     # do not delete !
    cur.execute("""SELECT websites FROM webst WHERE date_last_save LIKE 1900""")
    tempo = cur.fetchall()
    for el in tempo:
        (tempoone,) = el    # conversion de : el (tuple) vers tempoone (str)
        current_path_to_save = tempoone

def sorted_array_display():
    cur.execute("""SELECT * FROM webst WHERE date_last_save NOT LIKE 1900 ORDER BY websites ASC""")
    tempo = cur.fetchall()
    print("valeur :", tempo)

    for el in tempo:
        (tempoone, tempotwo, tempothree, tempofour) = el    # conversion de : el (tuple) vers tempoone (str)
        url_lst.append(tempoone)
        tempotwo = str(tempotwo)    # str conversion for next comparison
        date_last_save_lst.append(tempotwo)
        duration_last_save_lst.append(tempothree)
        file_size_lst.append(tempofour)

def callback_sort_array_display():
    os.system("./delete_and_restart.sh")

def read_all_websites_from_db():
    global url_lst
    cur.execute("""SELECT * FROM webst WHERE date_last_save NOT LIKE 1900""")
    tempo = cur.fetchall()
    print("valeur :", tempo)

    for el in tempo:
        (tempoone, tempotwo, tempothree, tempofour) = el    # conversion de : el (tuple) vers tempoone (str)
        url_lst.append(tempoone)
        tempotwo = str(tempotwo)    # str conversion for next comparison
        date_last_save_lst.append(tempotwo)
        duration_last_save_lst.append(tempothree)
        file_size_lst.append(tempofour)

def callback_url_website():
    db_websites_lst = []
    control = True
    # check first if url is not already in the database, if not, we store the new url in database
    command = """SELECT websites FROM webst"""
    cur.execute(command)
    for row in cur:
        for el in row:
            db_websites_lst.append(el)

    for ee in db_websites_lst:
        print(ee)
        if(ee == dpg.get_value(url_website)):
            dpg.set_value(url_display, f"New URL saved : None because already exist in database")
            control = False
        else:
            pass

    if(control):
        print(dpg.get_value(url_website))
        command = """INSERT INTO webst(websites, date_last_save, duration_last_save, folder_size) VALUES(""" + "'" + dpg.get_value(url_website) + "'" + """ , 0, 0, 0)"""
        cur.execute(command)
        conn.commit()
        dpg.set_value(url_display, f"New URL saved : {(dpg.get_value(url_website))}")
        read_all_websites_from_db()

        with dpg.table_row(parent="table"):
            dpg.add_selectable(label=f"{url_lst[-1]}", span_columns=True, callback=clb_selectable, user_data=url_lst[-1])
            dpg.add_selectable(label=f"{date_last_save_lst[-1]}", span_columns=True, callback=clb_selectable, user_data=url_lst[-1])
            dpg.add_selectable(label=f"{duration_last_save_lst[-1]}", span_columns=True, callback=clb_selectable, user_data=url_lst[-1])
            dpg.add_selectable(label=f"{file_size_lst[-1]}", span_columns=True, callback=clb_selectable, user_data=url_lst[-1])

def deleting_display_url_row():    # marche pas encore, créé pour afficher dans le GUI une nouvelle vue lorsqu'on supprime une url
    db_websites_lst = []
    command = """SELECT websites FROM webst"""
    cur.execute(command)
    for row in cur:
        for el in row:
            db_websites_lst.append(el)
    selectable_display()

def website_selected(uurl):
    dpg.set_value(selecturl, f"Selected website : {(uurl)}")
    global selected_url
    selected_url = uurl

def callback_delete_website():
    print("Suppression du site de la BDD")
    command = """DELETE FROM webst WHERE websites=""" + "\"" + selected_url + "\""
    print(command)
    cur.execute(command)
    conn.commit()  
    #deleting_display_url_row() # marche pas encore, créé pour afficher dans le GUI une nouvelle vue lorsqu'on supprime une url
    # vu que j'arrive pas a faire disparaitre la ligne que je supprime, je vais ruser :
    # a la suite de ces explications, lancer un script bash qui fera 1 pkill sur le processus, attendra genre 300ms puis ré ouvrira tout seul
    # le programme. Ainsi la ligne a supprimer aura disparu...
    os.system("./delete_and_restart.sh")

def refresh_display_website():
    command = """DELETE FROM webst WHERE websites=""" + "\"" + selected_url + "\""
    print(command)
    cur.execute(command)
    conn.commit()

def only_url(url):
    tempone = url.replace("http://", "")
    temptwo = tempone.replace("https://", "")
    tempthree = temptwo.replace("http://www.", "")
    tempfour = tempthree.replace("https://www.", "")
    reducted_url = ""
    for el in tempfour:
        if el == '/':
            break
        else:
            reducted_url += el
    return reducted_url

def callback_whole_save_website():
    di = time.strftime('%d')        # day
    dmo = time.strftime('%m')       # month
    dy = time.strftime('%y')        # year
    dh = time.strftime('%H')        # hours
    dmi = time.strftime('%M')       # minutes
    ds = time.strftime('%S')        # secondes
    date_start_time = di + '/' + dmo + '/' + dy
    dedicated_folder_date_name = only_url(selected_url) + '-' + di + '-' + dmo + '-' + dy
    complete_start_time = datetime(int(dy), int(dmo), int(di), int(dh), int(dmi), int(ds))
    print("Complete start time  :", complete_start_time)
    read_path_save_folder()
    os.chdir(current_path_to_save)
    os.mkdir(dedicated_folder_date_name)
    os.chdir(dedicated_folder_date_name)
    # permet de lancer le script de wget avec l'url du site a enregistré
    p = Popen(prep, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)  
    for line in p.stdout:  
        line = line.rstrip()
        print(line.decode())
        dpg.set_value(textControl, f"State of downloading : {(line.decode())}")
    dei = time.strftime('%d')
    demo = time.strftime('%m')
    dey = time.strftime('%y')
    deh = time.strftime('%H')
    demi = time.strftime('%M')
    des = time.strftime('%S')
    complete_end_time = datetime(int(dey), int(demo), int(dei), int(deh), int(demi), int(des))
    print("End time :", complete_end_time)
    duration = str(complete_end_time - complete_start_time)
    print("Download duration : ", duration)
    print(type(duration))
    fil_size = os.popen("du -hs")
    fil_size_format = fil_size.read()
    right_fil_size_format = ""
    print("fil_size_format a pour resultat : ", fil_size_format)
    for ol in fil_size_format:
        if ol == '\t':
            break
        else:
            right_fil_size_format += ol

    refresh_display_website()
    os.chdir(script_location)
    command = """INSERT INTO webst VALUES(""" + "'" + selected_url + "'" + """ , """ + "'" + date_start_time + "'" + """, """ + "'" + duration + "'" + """ , """ + "'" + right_fil_size_format + "'" + """)"""
    cur.execute(command)
    conn.commit()
    os.system("./delete_and_restart.sh")

def selectable_display():
    with dpg.table(tag=tag, parent="Window_main", header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp) as table_sel_rows:
        dpg.add_table_column(label="URL")
        dpg.add_table_column(label="Last mirror date")
        dpg.add_table_column(label="Time does it takes")
        dpg.add_table_column(label="Folder size")
        lenn_lst = len(url_lst)
        gg = 0
       
        while(gg < lenn_lst):
            with dpg.table_row(parent=tag):
                dpg.add_selectable(label=f"{url_lst[gg]}", user_data=url_lst[gg], callback=clb_selectable, span_columns=True)
                dpg.add_selectable(label=f"{date_last_save_lst[gg]}", user_data=url_lst[gg], callback=clb_selectable, span_columns=True)
                dpg.add_selectable(label=f"{duration_last_save_lst[gg]}", user_data=url_lst[gg], callback=clb_selectable, span_columns=True)
                dpg.add_selectable(label=f"{file_size_lst[gg]}", span_columns=True, callback=clb_selectable, user_data=url_lst[-1])
            gg += 1
    dpg.bind_item_theme(table_sel_rows, table_theme)

###########################################################################################################################################################

with dpg.window(label="Window_main", no_resize=True, width=1200, height=800, no_title_bar=True, no_move=True) as window:
    read_path_save_folder()
    current_path = 0
    current_path = dpg.add_text("Saving current path :", color=[100, 160, 100, 255], label="Current path save", show_label=False)
    dpg.set_value(current_path, f"Saving current path : {(current_path_to_save)}")

    change_path_area = dpg.add_text("Change path to new path", color=[200, 100, 200, 255], label="Change path area", show_label=False)
    path_to_save = dpg.add_input_text(label="Path to save")
    path_btn = dpg.add_button(label="Save new path", callback=callback_path)
    new_path_display = dpg.add_text("New path saved :", color=[255, 165, 0, 255], label="Save new path", show_label=False)

    add_url_website_area = dpg.add_text("Add new website (url)", color=[200, 100, 200, 255], label="Add url website area", show_label=False)
    url_website = dpg.add_input_text(label="Website URL")
    input_url_btn = dpg.add_button(label="Save URL", callback=callback_url_website, user_data="url_display")
    sorted_array_display()
    url_display = dpg.add_text("New URL saved :", color=[255, 165, 0, 255], label="Save URL", show_label=False)
    
    dpg.add_button(label="Sort the array", callback=callback_sort_array_display)

    with dpg.theme() as table_theme:
        with dpg.theme_component(dpg.mvTable):
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

    def clb_selectable(sender, app_data, user_data):
        global prep
        prep = "wget --mirror --convert-links --adjust-extension --page-requisites --no-parent -e robots=off " + user_data
        website_selected(user_data)

    selectable_display()

    selecturl = 0
    selecturl = dpg.add_text("Selected website :",  color=[0, 0, 255, 255], label="selected", show_label=False)
    textControl = 0
    dpg.add_button(label="Save whole website picked", callback=callback_whole_save_website, user_data=textControl)
    textControl = dpg.add_text("State of downloading :", color=[0, 255, 0, 255], label="Mouse Move Handler", show_label=False)
    delete_selected_btn = dpg.add_button(label="Delete selected website now", callback=callback_delete_website)

conn.commit()

dpg.set_global_font_scale(1.15)
dpg.create_viewport(title='Wget_gui_db', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
conn.close()
