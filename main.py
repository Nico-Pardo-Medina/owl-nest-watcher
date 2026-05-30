import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from detector import process_videos


def browse_button():
    global old_folder_path
    filename = filedialog.askdirectory()
    old_folder_path = filename
    button_videos_folder_label.config(text=filename)

def browse_button2():
    global new_folder_path
    filename = filedialog.askdirectory()
    new_folder_path = filename
    button_txt_folder_label.config(text=filename)

def run():
    def on_progress(current, total):
        displayedText.set(f"Analizando archivo {current} de {total}")
        label.update_idletasks()

    process_videos(
        source_folder=old_folder_path,
        output_folder=new_folder_path,
        file_title=file_title_grid.get(),
        min_area=float(min_area_grid.get()),
        contrast=float(contrast_grid.get()),
        brightness=int(brightness_grid.get()),
        speed=float(speed_grid.get()),
        time_that_has_to_pass=float(time_that_has_to_pass_grid.get()),
        on_progress=on_progress,
    )
    messagebox.showinfo(message="El proceso ha finalizado con éxito.")


if __name__ == "__main__":
    file_title_grid_position = (1,0)
    file_title_grid_label_position = (0,0)
    brightness_grid_position = (3,0)
    brightness_grid_label_position = (2,0)
    contrast_grid_position = (5,0)
    contrast_grid_label_position = (4,0)
    speed_grid_position = (5,1)
    speed_grid_label_position = (4,1)
    button_videos_folder_position = (0,1)
    button_videos_folder_label_position = (1,1)
    button_txt_folder_position = (2,1)
    button_txt_folder_label_position = (3,1)
    min_area_grid_position = (7,0)
    min_area_grid_label_position = (6,0)
    time_that_has_to_pass_grid_position = (7,1)
    time_that_has_to_pass_grid_label_position = (6,1)
    main_button_position = (8,0)
    label_position = (8,1)
    padx=5
    pady=5
    window = Tk()
    window.title("Detector de movimiento")
    file_title_grid = ttk.Entry()
    file_title_grid_label = ttk.Label(text="Nombre del archivo")
    file_title_grid_label.grid(row=file_title_grid_label_position[0],column=file_title_grid_label_position[1],padx=padx,pady=pady)
    file_title_grid.grid(row=file_title_grid_position[0],column=file_title_grid_position[1],padx=padx,pady=pady)
    file_title_grid.insert(END,"activity_log")
    brightness_grid = ttk.Entry()
    brightness_label = ttk.Label(text="Brillo")
    brightness_label.grid(row=brightness_grid_label_position[0],column=brightness_grid_label_position[1],padx=padx,pady=pady)
    brightness_grid.grid(row=brightness_grid_position[0],column=brightness_grid_position[1],padx=padx,pady=pady)
    brightness_grid.insert(END,50)
    old_folder_path = os.getcwd()
    button_videos_folder = ttk.Button(text="Seleccionar carpeta de los vídeos",command=browse_button)
    button_videos_folder_label = ttk.Label(text=old_folder_path)
    button_videos_folder_label.grid(row=button_videos_folder_label_position[0],column=button_videos_folder_label_position[1],padx=padx,pady=pady)
    button_videos_folder.grid(row=button_videos_folder_position[0],column=button_videos_folder_position[1],padx=padx,pady=pady)
    new_folder_path = os.getcwd()
    button_txt_folder = ttk.Button(text="Seleccionar carpeta donde guardar el txt",command=browse_button2)
    button_txt_folder_label = ttk.Label(text=new_folder_path)
    button_txt_folder_label.grid(row=button_txt_folder_label_position[0],column=button_txt_folder_label_position[1],padx=padx,pady=pady)
    button_txt_folder.grid(row=button_txt_folder_position[0], column=button_txt_folder_position[1],padx=padx,pady=pady)
    contrast_grid = ttk.Entry()
    contrast_label = ttk.Label(text="Contraste")
    contrast_label.grid(row=contrast_grid_label_position[0],column=contrast_grid_label_position[1],padx=padx,pady=pady)
    contrast_grid.grid(row=contrast_grid_position[0],column=contrast_grid_position[1],padx=padx,pady=pady)
    contrast_grid.insert(END,1.25)
    speed_grid = ttk.Entry()
    speed_label = ttk.Label(text="Velocidad")
    speed_label.grid(row=speed_grid_label_position[0],column=speed_grid_label_position[1],padx=padx,pady=pady)
    speed_grid.grid(row=speed_grid_position[0],column=speed_grid_position[1],padx=padx,pady=pady)
    speed_grid.insert(END,1)
    min_area_grid = ttk.Entry()
    min_area_label = ttk.Label(text="Área mínima")
    min_area_label.grid(row=min_area_grid_label_position[0],column=min_area_grid_label_position[1],padx=padx,pady=pady)
    min_area_grid.grid(row=min_area_grid_position[0],column=min_area_grid_position[1],padx=padx,pady=pady)
    time_that_has_to_pass_grid = ttk.Entry()
    time_that_has_to_pass_label = ttk.Label(text="Tiempo que debe pasar sin actividad para que cuente que el búho se ha ido")
    time_that_has_to_pass_label.grid(row=time_that_has_to_pass_grid_label_position[0],column=time_that_has_to_pass_grid_label_position[1],padx=padx,pady=pady)
    time_that_has_to_pass_grid.grid(row=time_that_has_to_pass_grid_position[0],column=time_that_has_to_pass_grid_position[1],padx=padx,pady=pady)
    time_that_has_to_pass_grid.insert(END,0)
    min_area_grid.insert(END,500)
    main_button = ttk.Button(text="Ejecutar", command=run)
    main_button.grid(row=main_button_position[0],column=main_button_position[1],padx=padx,pady=pady)
    displayedText = StringVar()
    label = ttk.Label(textvariable=displayedText)
    label.grid(row=label_position[0],column=label_position[1],padx=padx,pady=pady)

    window.mainloop()
