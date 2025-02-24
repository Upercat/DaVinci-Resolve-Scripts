import sys
import os
import time


# Manually add the Resolve script path
resolve_path = "C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules"
sys.path.append(resolve_path)

import DaVinciResolveScript as dvr # Connect to DaVinci Resolve

resolve = dvr.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()
media_pool = project.GetMediaPool()
current_folder = media_pool.GetCurrentFolder()
subfolders = current_folder.GetSubFolderList()
clips = current_folder.GetClipList()


# Un programa para sincronizar clips de video con clips de audio en DaVinci Resolve.
#

# El programa escanea una carpeta de archivos de video y una carpeta de archivos de audio.


# Find the audio folder
audio_folder = None
for folder in subfolders:
    if folder.GetName().lower() == "audio":  # Match folder name (case-insensitive)
        audio_folder = folder
        print("Carpeta de archivos de audio: " ,audio_folder.GetName())
        break
    else:
        print("No se ha encontrado la carpeta de archivos de audio")


video_files = (current_folder.GetClipList()) # Convertir la lista de archivos de vídeo.
audio_files = (audio_folder.GetClipList()) # Convertir la lista de archivos de audio.

# 🔹 Function to remove file extensions from Clip Name
def remove_extension(clip_name):
    return ".".join(clip_name.split(".")[:-1])  # Removes only the last extension

lista_timelines_creados = [] # Crear una lista vacía para almacenar los nombres de los timelines creados.

# Los archivos de video y audio que coinciden se sincronizan en un nuevo timeline.
for video_clip in video_files:
    for audio_clip in audio_files:
        print("Buscando...")
        time.sleep(0.2)
        if remove_extension(video_clip.GetClipProperty("Clip Name")) == remove_extension(audio_clip.GetClipProperty("Clip Name")):
            print(f"Archivo de video {video_clip.GetName()} tiene un archivo de audio correspondiente.")

            time.sleep(1)
            # Crear un nuevo timeline con los clips de video y audio.
            # no sirve new_timeline = media_pool.CreateTimelineFromClips(f"{video.GetClipProperty("Clip Name")}_sync", [video, audio]) # para crear el timeline usaremos CreateTimelineFromClips(name, [clips])
            # timeline_name = f"{video_clip.GetName()}_sync"
            # new_timeline = media_pool.CreateEmptyTimeline(timeline_name) # para crear el timeline usaremos CreateTimeline(name)


            # así vamos a sincronizar los AutoSyncAudio([MediaPoolItems], {audioSyncSettings})
            # opciones: resolve.AUDIO_SYNC_MODE con resolve.AUDIO_SYNC_WAVEFORM
            
            print("Sincronizando clips de video y audio, por favor espere..." )
            time.sleep(1)
            try:
               
                opciones_de_sync = {
                        resolve.AUDIO_SYNC_MODE: resolve.AUDIO_SYNC_WAVEFORM,
                        resolve.AUDIO_SYNC_CHANNEL_NUMBER: -1,
                        resolve.AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO : False,
                        resolve.AUDIO_SYNC_RETAIN_VIDEO_METADATA : True
                    }
                sync_list = [video_clip, audio_clip]

                media_pool.AutoSyncAudio(sync_list, opciones_de_sync)

                print("Clips de video y audio sincronizados con éxito")

            except Exception as e:
                print(f"Error al sincronizar clips de video {e}")



            try:
                # new_timeline.AppendToTimeline(video_clip)
                time.sleep(1)
                newtimeline = media_pool.CreateTimelineFromClips(f"{video_clip.GetName()}_sync", video_clip)
                time.sleep(1)
                print(f"Timeline {newtimeline.GetName()} creado")
                time.sleep(1)
                print("Clips de video añadidos al timeline")
                lista_timelines_creados.append(newtimeline.GetName())
            except Exception as e:
                print(f"Error al añadir clips de video al timeline {e}")	
                
            
            break

           
            

print(f"Se han creado {len(lista_timelines_creados)} timelines con los clips de video y audio sincronizados.")
time.sleep(1)
pprint.pp(lista_timelines_creados)
time.sleep(1)         
print("Fin del programa")