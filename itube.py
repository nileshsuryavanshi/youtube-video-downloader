from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from pytube import YouTube
import os
import re
from subprocess import call
import sys

root = Tk()

# getting current working directory
current_dir = os.getcwd()

# size of the windows and title
root.geometry('870x578')
root.resizable(width=False, height=False)
root.title('I-Tube -(YouTube video and audio downloader)')

# variable to show details of song
var_dict = {1080:'', 720:'', 360:'', 480:'', 'ado':''}
detail_dict = {'1080p':{'tag':0, 'type':'', 'size':0},
                '720p':{'tag':0, 'type':'', 'size':0},
                '480p':{'tag':0, 'type':'', 'size':0},
                '360p':{'tag':0, 'type':'', 'size':0},
              'ado':{'tag':0, 'type':'', 'size':0}}
video_downloaded = False

# to show available files
def runn():
    Label(right_frame, text=var_dict[1080], bg='grey').grid(row=5, column=1, pady=5, padx=2, sticky='nw')
    Label(right_frame, text=var_dict[720], bg='grey').grid(row=6, column=1, pady=5, padx=2, sticky='nw')
    Label(right_frame, text=var_dict[480], bg='grey').grid(row=7, column=1, pady=5, padx=2, sticky='nw')       
    Label(right_frame, text=var_dict[360], bg='grey').grid(row=8, column=1, pady=5, padx=2, sticky='nw')
    Label(right_frame, text=var_dict['ado'], bg='grey').grid(row=10, column=1, pady=5, padx=2, sticky='nw')

    add_size = detail_dict['ado']['size']
    if "1080p" in res_list:
        Label(right_frame, text=str(round(detail_dict['1080p']['size']+add_size, 2))+' MB', bg='grey').grid(row=5, column=2, pady=5, padx=2, sticky='nw')
    if "720p" in res_list:
        Label(right_frame, text=str(round(detail_dict['720p']['size']+add_size, 2))+' MB', bg='grey').grid(row=6, column=2, pady=5, padx=2, sticky='nw')
    if "480p" in res_list:
        Label(right_frame, text=str(round(detail_dict['480p']['size']+add_size, 2))+' MB', bg='grey').grid(row=7, column=2, pady=5, padx=2, sticky='nw')
    if "360p" in res_list:
        Label(right_frame, text=str(round(detail_dict['360p']['size']+add_size, 2))+' MB', bg='grey').grid(row=8, column=2, pady=5, padx=2, sticky='nw')
    Label(right_frame, text=str(round(detail_dict['ado']['size'], 2))+' MB', bg='grey').grid(row=10, column=2, pady=5, padx=2, sticky='nw')

# to get progress bar when downloading
def progress_Check(stream, chunk,bytes_remaining):
    file_size = down_file.filesize
    percent = round((100*(file_size-bytes_remaining))/file_size, 2)   
    bar['value'] = percent
    root.update_idletasks()

# checking availabel files
def avalilable_files():
    global valid_url 
    valid_url = False
    global video
    try:
        video = YouTube(url_value.get(), on_progress_callback=progress_Check)
        stream = video.streams.filter(only_video=True)
        valid_url = True
        global res_list
        res_list = []
        size_list = []
        type_list = []
        tag_list= []
        for val in stream:
            # taking video with fps <= 60
            if val.fps <= 60:
                res_list.append(val.resolution)
                size_list.append(val.filesize/(1024*1024))
                type_list.append(val.mime_type.split('/')[1])
                tag_list.append(val.itag)
        
        # check if the particular resolution available or not
        if "1080p" in res_list:
            var_dict[1080] = 'Available'
            index_1080 = res_list.index("1080p")
            detail_dict['1080p'].update({'tag':tag_list[index_1080], 'type':type_list[index_1080], 'size':size_list[index_1080]})
        if "720p" in res_list:
            var_dict[720] = 'Available'
            index_720 = res_list.index("720p")
            detail_dict['720p'].update({'tag':tag_list[index_720], 'type':type_list[index_720], 'size':size_list[index_720]})
        if "480p" in res_list:
            var_dict[480] = 'Available'
            index_480 = res_list.index("480p")    
            detail_dict['480p'].update({'tag':tag_list[index_480], 'type':type_list[index_480], 'size':size_list[index_480]})
        if "360p" in res_list:
            var_dict[360] = 'Available'
            index_360 = res_list.index("360p")
            detail_dict['360p'].update({'tag':tag_list[index_360], 'type':type_list[index_360], 'size':size_list[index_360]})
             
        ado_size = []
        ado_type = []
        ado_tag = []
        ado_qlt = []
        for val_ado in video.streams.filter(only_audio=True):
            # inserting audio information into lists
            ado_size.append(val_ado.filesize/(1024*1024))
            ado_type.append(val_ado.mime_type.split('/')[1])
            ado_tag.append(val_ado.itag)
            ado_qlt.append(int(val_ado.abr.split('k')[0]))
        ado_index = ado_qlt.index(max(ado_qlt))    
        
        if ado_index:
            # check if audio is available
            var_dict['ado'] = 'Available'
            detail_dict['ado'].update({'tag':ado_tag[ado_index], 'type':ado_type[ado_index], 'size':ado_size[ado_index]}) 
 
        runn()  ## calling runn() function to show result
    except Exception:
        wrong_url = 'Wrong URL or not downloadable.'
        messagebox.showerror('I-tube - (Error)', wrong_url)


# to download desired video or audio
def download():
    if url_value.get() and valid_url:
        global to_download
        global video_downloaded
        to_download = vdo.get()
        if to_download in ('1080p', '720p', '480p', '360p'):
            global directory
            global video_address
            global audio_address
            global down_file
            global file_name
            global audio_file_name

            # asking for directory to download video
            directory = filedialog.askdirectory(initialdir='Choose path')
            title_name = re.sub(r'[^a-zA-Z0-9 ]','',video.title)
            title_name = title_name.replace(' ','_')
            file_name = 'video_'+title_name

            # download video file
            down_file = video.streams.get_by_itag(detail_dict[to_download]['tag'])
            down_file.download(directory, filename=file_name)          
            video_address = f"{directory}/{file_name}.{detail_dict[to_download]['type']}"
            audio_file_name = f'audio_{title_name}'

            # download audio file
            down_file = video.streams.get_by_itag(detail_dict['ado']['tag'])
            down_file.download(directory, filename=audio_file_name)
            audio_address = f"{directory}/{audio_file_name}.{detail_dict['ado']['type']}"
            vid_notify='Downloaded successfully.\nWait, press convert button to enable audio.'    
            messagebox.showinfo('I-Tube', vid_notify)
            video_downloaded = True 

        elif to_download == 'ado':
            global directory_ado
            global ado_address

            # asking for directory to download audio
            directory_ado = filedialog.askdirectory(initialdir='Choose path')
            title_name = re.sub(r'[^a-zA-Z0-9 ]','',video.title)
            title_name = title_name.replace(' ','_')
            audio_file_name = f"audio_{title_name}"

            # downloading audio
            down_file = video.streams.get_by_itag(detail_dict['ado']['tag'])
            down_file.download(directory_ado, filename=audio_file_name)
            ado_address = directory_ado + '/' + audio_file_name + '.' + detail_dict['ado']['type']
            ado_notify='Downloaded successfully.\nWait, press convert button to get your audio.'    
            messagebox.showinfo('I-Tube', ado_notify)
            video_downloaded = True 

        else:
            download_alert = 'Please choose valid option!'
            messagebox.showerror('I-Tube -(Error)', download_alert)    
    else:  
        no_url_alert = 'Please provide a valid URL'
        messagebox.showerror('I-Tube -(Error)', no_url_alert)      

    
# function to convert the downloaded file
def convert():
    try:
        if video_downloaded:
            if to_download in ('1080p', '720p', '480p', '360p'):
                os.chdir(directory)
                final_name = f"{file_name}_c.{detail_dict[to_download]['type']}"
                v_name = f"{file_name}.{detail_dict[to_download]['type']}"
                a_name = f"{audio_file_name}.{detail_dict['ado']['type']}"

                # merging audio and video files
                cmd = f'ffmpeg -i {v_name} -i {a_name} -c:v copy -c:a  copy {final_name}'
                call(cmd, shell=True)

                # deleting audio and video files
                os.remove(v_name)
                os.remove(a_name)

                # updating converting status
                conv_vid_notify='All done. Thank you'    
                messagebox.showinfo('I-Tube', conv_vid_notify)
                os.chdir(current_dir) 

            elif to_download == 'ado':
                os.chdir(directory_ado)
                final_name = f"{audio_file_name}.mp3"
                a_name = f"{audio_file_name}.{detail_dict['ado']['type']}"

                # changing audio file formate to mp3
                cmd_ado = f'ffmpeg -i {a_name} {final_name}'
                call(cmd_ado, shell=True)

                # removing previous audio file
                os.remove(a_name)
                conv_ado_notify='All done. Thank you'    
                messagebox.showinfo('I-Tube', conv_ado_notify) 
                os.chdir(current_dir)
        else:
            not_downloaded = 'First download the video'
            messagebox.showerror('I-Tube -(Error)', not_downloaded)
            os.chdir(current_dir)

    except Exception:
        # show message when error occured during converting
        converting_error = 'An erro occured while converting'
        messagebox.showerror('I-tube - (Error)', converting_error)        

# function to restart the program
def restart():
    os.execl(sys.executable, 'python', __file__, *sys.argv[1:])

# making left frame
left_frame = Frame(root, width=400,height=400, bg='black')
left_frame.grid(row=0, column=0, padx=2, pady=2)

# making right frame
right_frame = Frame(root, width=300, height=400, bg='grey')
right_frame.grid(row=0, column=1, pady=2)

# adding logo in left frame
img = PhotoImage(file='image/i-tube image.png')
Label(left_frame, image=img, bg='black').pack()

# some documentation in left frame
menual = '''This program will help you to download any video or audio you want from youtube, 
only you need to copy the url and past in the box, and your are done!'''
Label(left_frame, text=menual, bg='black', fg='white', padx=5, pady=20).pack()

# print "Welcome" in right frame
Label(right_frame, text='Welcome!', font='ubuntu 20 bold', bg='grey').grid(row=0, column=0, pady=8,sticky='nw')
Label(right_frame, text='Okay, copy and paste url below -', font='ubuntu 12', bg='grey').grid(row=1, column=0,
      pady=10, padx=2, columnspan=2, sticky='nw')

# url entry and its label
Label(right_frame, text='Youtube link', font='ubuntu 12', bg='grey').grid(row=2, column=0, pady=5, sticky='nw')
url_value = StringVar()
url_entry = Entry(right_frame, textvariable=url_value, font='ubuntu', width=23)
url_entry.grid(row=2, column=1, pady=5, padx=2, sticky='nw', columnspan=2)

# button to show available files
Button(right_frame, text='See available files', command=avalilable_files, foreground='white', background='black',
       borderwidth=0).grid(row=3, column=1, pady=10, sticky='nw')

# title to show available video files
Label(right_frame, text='Video files -', font='ubuntu 12', bg='grey').grid(row=4, column=0, pady=5, padx=2, sticky='nw')

# radio buttons for video resolution
Label(right_frame, text=var_dict[1080], bg='grey').grid(row=5, column=1, pady=5, padx=2, sticky='nw')
Label(right_frame, text=var_dict[720], bg='grey').grid(row=6, column=1, pady=5, padx=2, sticky='nw') 
Label(right_frame, text=var_dict[480], bg='grey').grid(row=7, column=1, pady=5, padx=2, sticky='nw')      
Label(right_frame, text=var_dict[360], bg='grey').grid(row=8, column=1, pady=5, padx=2, sticky='nw')

vdo = StringVar()
vdo.set('Radio')
Radiobutton(right_frame, text='1080P', variable=vdo, value='1080p').grid(row=5, column=0, pady=5, padx=20, sticky='nw')
Radiobutton(right_frame, text='720P  ', variable=vdo, value='720p').grid(row=6, column=0, pady=5, padx=20, sticky='nw')
Radiobutton(right_frame, text='480P  ', variable=vdo, value='480p').grid(row=7, column=0, pady=5, padx=20, sticky='nw')
Radiobutton(right_frame, text='360P  ', variable=vdo, value='360p').grid(row=8, column=0, pady=5, padx=20, sticky='nw')


# audio files available label and radio button
Label(right_frame, text='Audio files -', font='ubuntu 12', bg='grey').grid(row=9, column=0, pady=5, padx=2, sticky='nw')
Radiobutton(right_frame, text='Best    ', variable=vdo, value='ado').grid(row=10, column=0, pady=5, padx=20, sticky='nw')

# documentation for downloading and converting
Label(right_frame, text='Note: Once, download gets complete then it is\nnecessary to press convert to get things done.', 
      bg='grey').grid(row=11, column=0, columnspan=3, pady=10, padx=2, sticky='nw')

# download button
Button(right_frame, text='1. Download', command=download, foreground='white', background='black', font='ubuntu 10 bold',
       borderwidth=0).grid(row=12, column=0, pady=5, padx=2, sticky='nw')

# converting button
Button(right_frame, text='2. Convert    ', command=convert, foreground='white', background='black', font='ubuntu 10 bold',
       borderwidth=0).grid(row=13, column=0, pady=5, padx=2, sticky='nw')       

# restart button
Button(right_frame, text='Restart', command=restart, foreground='white', background='black', font='ubuntu 12 bold',
       borderwidth=0).grid(row=14, column=1, pady=8, padx=2, sticky='nw')     

# creating and editing progress bar 
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
bar = ttk.Progressbar(right_frame, length=200, orient=HORIZONTAL, mode='determinate', style="red.Horizontal.TProgressbar")
bar.grid(row=12, column=1, columnspan=2, pady=5, sticky='nw', ipady=5)

# the end
root.mainloop()
