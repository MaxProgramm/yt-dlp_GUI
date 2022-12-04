import PySimpleGUIQt as psg
import os
import yt_dlp



global values
global real_values

clear = lambda: os.system("clear")

#PySimpleGUIQt.Window("Test", [[]], margins = (100, 50), ).read()

#layout = [[PySimpleGUIQt.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

layout = [
        [psg.Text('Enter your Video/Audio information')],
        [psg.Radio(text="Video", group_id="FORMAT", default=True, key="Video_select"), psg.Radio(text="Audio", group_id="FORMAT", default=False, key="Audio_select")],
        [psg.Text('URL', size=(15, 1)), psg.InputText(key="URL")],
        [psg.Text('File format', size=(15, 1)), psg.InputText(key="FILE_FORMAT")],
        [psg.Text("*for audio mp3")],
        [psg.Text("*for Video mp4")],
#       [sg.Text('Phone', size=(15, 1)), sg.InputText()],
        [psg.Submit(), psg.Cancel()]
]


window = psg.Window("Test", layout) #size=(200, 200))

def check_event(get_ev):
    global values
    event, values = window.read()
    if event == get_ev:
        return True


def download_video_format(url, format):
    URLS = [f"{url}"]

    ydl_opts = {
        'format': f'{format}/bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)

def extract_audio_format(url, audio_format, audio_quality = "bestaudio/best"):
    URLS = [f"{url}"]
    ydl_opts = {
        'format': f"{audio_quality}",
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': f'{audio_format}',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)



while True:
    global real_values
    global values
    if check_event("Cancel") or check_event(psg.WIN_CLOSED):
        break

    if check_event("Submit"):
        real_values = values
        #download_video_format(values[0], real_values[1])
        if real_values["Video_select"]:
            download_video_format(real_values["URL"], real_values["FILE_FORMAT"])
        if real_values["Audio_select"]:
            extract_audio_format(real_values["URL"], real_values["FILE_FORMAT"])
        break


window.close()

print(real_values)