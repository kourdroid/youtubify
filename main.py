import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import time
from pytube import YouTube, Playlist
from moviepy.editor import *
import subprocess

#=======================================================================================
#                                        Variables
#=======================================================================================

custom_font = ('Montserrat', 24,'bold')
red_color = '#FF2525'
bg_color = '#2E2E2E'

menu_fonts = 'Montserrat', 10,'bold'

#=======================================================================================

main_window = None
radio_var = None

#=======================================================================================
#                                     Other Windows
#=======================================================================================

resolution_options = ['1080p', '720p', '480p']

def open_download_window(window_type):

    global main_window
    global radio_var

    if main_window:
        main_window.withdraw()  # Hide the main window if it exists

    download_window = tk.Toplevel()
    download_window.title('Youtube Downloader')
    download_window.geometry('750x450')
    download_window.configure(bg=bg_color)


    def on_close():
        download_window.destroy()
        if main_window:
            main_window.deiconify()  # Show the main window again when the popup is closed



    download_window.protocol("WM_DELETE_WINDOW", on_close)

    if window_type == 'playlist':
        label_text = 'Playlist URL:'
        label = ttk.Label(download_window, text='PLAYLIST DOWNLOADER',font=(custom_font),background=bg_color,foreground=red_color)
        button_text = 'DOWNLOAD PLAYLIST'
        
    elif window_type == 'video':
        label_text = 'Video URL:'
        label = ttk.Label(download_window, text='VIDEO DOWNLOADER',font=(custom_font),background=bg_color,foreground=red_color)
        button_text = 'DOWNLOAD VIDEO'
        
    else:
        download_window.destroy()  # Close the window if an invalid type is provided
        return

    

    label.pack(pady=30)

    url_label_frame = tk.Frame(download_window, bg=bg_color)  # Create a frame to hold the label and entry widgets
    url_label_frame.pack(pady=5)

    url_label = ttk.Label(url_label_frame, text=label_text, font=(menu_fonts), background=bg_color, foreground='#E9E9E9')
    url_label.pack(side=tk.LEFT,pady=5,padx=5)

    entry_style = ttk.Style()
    entry_style.configure('Custom.TEntry',fieldbackground='#121212',forground='#E9E9E9')


    entry = tk.Entry(url_label_frame,width=55)
    entry.configure(bg='#121212',fg='#E9E9E9',highlightthickness=0,bd=0)
    entry.pack(side=tk.LEFT,pady=10,padx=5)
   

    #----------------------------------------------

# iwould add three inline buttons here 1st : 1080p  2nd: 720p  3rd: 480p

    resolution_frame = tk.Frame(download_window,background='#2E2E2E')
    resolution_frame.pack()

    radio_var = tk.StringVar()
    radio_var.set('default_value')  # Set the default selection to the first resolution option

    for resolution_option, new_value in zip(resolution_options, ['1080p','720p','480p']):
        resolution_button = ttk.Radiobutton(
            resolution_frame,
            text=resolution_option,
            variable=radio_var,
            value=new_value,
            style='Custom.TRadiobutton'
        )
        resolution_button.pack(side=tk.LEFT, padx=5,pady=10)

    button_style_resolution = ttk.Style()
    button_style_resolution.configure('Custom.TRadiobutton', background='#2E2E2E', foreground='#FFF', font=('Montserrat', 14, 'bold'), highlightbackground=red_color,takefocus=False)
    button_style_resolution.map('Custom.TRadiobutton', background=[('active', '#121212')],indicatorcolor = [('selected', red_color)],focuscolor=download_window.cget("background"))
    #button_style_resolution.state(['!alternate'])

    #----------------------------------------------
    
    # Create the resolution menu for the download window
    

    def choose_destination():
        # Function to open file explorer popup and get the selected folder
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            destination_entry.delete(0, tk.END)
            destination_entry.insert(0, folder_selected)


    des_label_frame = tk.Frame(download_window, bg=bg_color)  # Create a frame to hold the label and entry widgets
    des_label_frame.pack(pady=5)

    destination_label = ttk.Label(des_label_frame, text='Destination: ', font=(menu_fonts), background=bg_color, foreground='#E9E9E9')
    destination_label.pack(side=tk.LEFT,pady=5)

    #------------------- File Choosing Entry ---------------------
    destination_entry = tk.Entry(des_label_frame, width=55)
    destination_entry.configure(bg='#121212',fg='#E9E9E9', highlightthickness=0, bd=0)
    destination_entry.pack(side=tk.LEFT,pady=10)

    #---------------------- Button Styling ------------------------
    button_style = ttk.Style()
    button_style.configure('Custom.TButton', font=('Montserrat', 10,'bold'), background=red_color, foreground='#E9E9E9', padding=5)
    button_style.map('Custom.TButton', background=[('active', '#333')])  # Set active background color


    #------------------- File Choosing Button ---------------------
    choose_button = ttk.Button(download_window, text='CHOOSE FOLDER', command=choose_destination,style='Custom.TButton')
    choose_button.pack(pady=10)


    #------------------------ Progress bar ------------------------
    progress = ttk.Progressbar(download_window, orient='horizontal', length=550 , mode='determinate')
    progress.pack(pady=20)

    def download_process():
        resolution_selected = radio_var.get()
        url = entry.get()  # Get the URL from the entry widget
        if not url:
            # Display an error message if the URL is empty
            tk.messagebox.showerror("Error", "Please enter a valid URL.")
            return

        if not resolution_selected:
            # Display an error message if no resolution is selected
            tk.messagebox.showerror("Error", "Please select a video resolution.")
            return

        if window_type == 'video':
            download_video(url, resolution_selected, progress)
        elif window_type == 'playlist':
            download_playlist(url, resolution_selected ,progress)

        on_close()


#                      vidoeDownloader        
#==========================================================
    def download_video(url, resolution_selected, progress):
        try:
            yt = YouTube(url)

            # Filter the streams for video-only and audio-only
            video_stream = yt.streams.filter(file_extension='mp4', res=resolution_selected, only_video=True).first()
            audio_stream = yt.streams.filter(only_audio=True).first()

            # If the selected resolution or audio is not available, show an error message
            if video_stream is None or audio_stream is None:
                tk.messagebox.showerror('Error', f"Video or audio with {resolution_selected} quality not available for this video.")
                return

            tk.messagebox.showinfo("showinfo", f"Downloading '{yt.title}' in {resolution_selected} quality...")
            destination_folder = destination_entry.get()
            if destination_folder:
                video_filename = f"{yt.title}_video.mp4"
                audio_filename = f"{yt.title}_audio.mp3"

                video_stream.download(output_path=destination_folder, filename=video_filename)
                audio_stream.download(output_path=destination_folder, filename=audio_filename)

                # Do not remove the files before merging
                video_path = os.path.join(destination_folder, video_filename)
                audio_path = os.path.join(destination_folder, audio_filename)

                # Use ffmpeg to merge video and audio
                final_filename = f"{yt.title}_{resolution_selected}.mp4"
                cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{os.path.join(destination_folder, final_filename)}"'
                subprocess.run(cmd, shell=True)

                # Remove the intermediate downloaded files after merging
                os.remove(video_path)
                os.remove(audio_path)

                for i in range(101):
                    progress['value'] = i
                    download_window.update_idletasks()  # Update the progress bar
                    time.sleep(0.05)

                tk.messagebox.showinfo('showinfo', "Download completed successfully.")
        except Exception as e:
            print(f"Error downloading video: {e}")


    def download_playlist(url, progress, resolution_selected):
        if resolution_selected in ('720p', '1080p'):
            try:
                yt = YouTube(url)

                # Filter the streams for video-only and audio-only
                video_stream = yt.streams.filter(file_extension='mp4', res=resolution_selected, only_video=True).first()
                audio_stream = yt.streams.filter(only_audio=True).first()

                # If the selected resolution or audio is not available, show an error message
                if video_stream is None or audio_stream is None:
                    tk.messagebox.showerror('Error', f"Video or audio with {resolution_selected} quality not available for this video.")
                    return

                tk.messagebox.showinfo("showinfo", f"Downloading '{yt.title}' in {resolution_selected} quality...")
                destination_folder = destination_entry.get()
                if destination_folder:
                    video_filename = f"{yt.title}_video.mp4"
                    audio_filename = f"{yt.title}_audio.mp3"

                    video_stream.download(output_path=destination_folder, filename=video_filename)
                    audio_stream.download(output_path=destination_folder, filename=audio_filename)

                    # Do not remove the files before merging
                    video_path = os.path.join(destination_folder, video_filename)
                    audio_path = os.path.join(destination_folder, audio_filename)

                    # Use ffmpeg to merge video and audio
                    final_filename = f"{yt.title}_{resolution_selected}.mp4"
                    cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac "{os.path.join(destination_folder, final_filename)}"'
                    subprocess.run(cmd, shell=True)

                    # Remove the intermediate downloaded files after merging
                    os.remove(video_path)
                    os.remove(audio_path)

                    for i in range(101):
                        progress['value'] = i
                        download_window.update_idletasks()  # Update the progress bar
                        time.sleep(0.05)

                    tk.messagebox.showinfo('showinfo', "Download completed successfully.")
            except Exception as e:
                print(f"Error downloading video: {e}")
        else:
            try:
                yt_p = Playlist(url)
                destination_folder = destination_entry.get()
                if destination_folder:
                    for idx, video_url in enumerate(yt_p.video_urls, start=1):
                        try:
                            yt = YouTube(video_url)
                            video_stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution_selected).first()
                            if not video_stream:
                                tk.messagebox.showerror("Error", "Selected resolution is not available for this video.")
                                return

                            video_stream.download(output_path=destination_folder)
                            progress['value'] = (idx / len(yt_p.video_urls)) * 100
                            download_window.update_idletasks()  # Update the progress bar
                            time.sleep(0.05)
                        except Exception as e:
                            print(f"Error downloading video: {e}")
                            continue

                tk.messagebox.showinfo('showinfo', "Download completed successfully.")
            except Exception as e:
                print(f"Error downloading playlist: {e}")

#============================================================

    button_style_download = ttk.Style()
    button_style_download.configure('Custom_download.TButton', font=('Montserrat', 15,'bold'), background=red_color, foreground='#E9E9E9', padding=5)
    button_style_download.map('Custom_download.TButton', background=[('active', '#333')])  # Set active background color

    button = ttk.Button(download_window, text=button_text, command=download_process, style='Custom_download.TButton')
    button.pack(pady=10)

#========================================================================================
#                                    The Start of the UI
#========================================================================================


def main():
    #main_window = tk.Tk()
    main_window = ThemedTk(theme='plastic')
    main_window.title('Youtube Downloader')
    main_window.geometry('750x450')
    main_window.configure(bg="#2E2E2E")

    frame = ttk.Frame(main_window, padding=20)
    frame.pack(expand=True)

    # Create widgets
    label = ttk.Label(master=main_window,text='YOUTUBIFY',font=('Opensans', 36,'bold'),foreground=red_color,background=bg_color,padding=(0,30))
    label.pack()

    # Import Images
    base_path = os.path.dirname(os.path.abspath(__file__))
    playlist_image = Image.open(os.path.join(base_path, 'video download.png'))
    video_image = Image.open(os.path.join(base_path, 'video download (1).png'))

    # tkImages:
    playlist_tk = ImageTk.PhotoImage(playlist_image)
    video_tk = ImageTk.PhotoImage(video_image)

    # Custom style for the frame
    style = ttk.Style()
    style.configure('Custom.TFrame', background=bg_color)  # Set the background color for the custom frame style

    # Frame for padding (margin) effect
    frame = ttk.Frame(main_window, padding=(0, 50), style='Custom.TFrame')
    frame.pack()

    # Button with image (inside the frame)
    button_playlist = ttk.Button(frame, image=playlist_tk, style='Custom.TButton', command=lambda: open_download_window('playlist'))
    button_playlist.pack(side=tk.LEFT, padx=5)  # Adjust the margin by changing the padx value

    button_video = ttk.Button(frame, image=video_tk, style='Custom.TButton', command=lambda: open_download_window('video'))
    button_video.pack(side=tk.RIGHT, padx=5)  # Adjust the margin by changing the padx value

    # Use a built-in theme from ttkthemes
    style.theme_use('default')
    # Use the default built-in theme

    #=================================================================================================
    #                                         EXECUTE THE CODE
    #=================================================================================================

    main_window.mainloop()

if __name__ == "__main__":
    main()
