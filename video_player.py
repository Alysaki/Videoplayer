import tkinter as tk
import font_manager as fonts
from Update_video import UpdateVideo
from check_videos import CheckVideos
from Create_Videos_List import CreateVideosList


def check_videos_clicked():
    CheckVideos(tk.Toplevel(window_main))
def update_video_clicked():
    UpdateVideo(tk.Toplevel(window_main))
def create_video_list_clicked():
    CreateVideosList(tk.Toplevel(window_main))


window_main = tk.Tk()
window_main.geometry("600x150")
window_main.title("Video Player")

#font label
status_lbl = tk.Label(window_main, text="", font=("Helvetica", 10))
status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
fonts.configure()

header_lbl = tk.Label(window_main, text="Select an option by clicking one of the buttons below")
header_lbl.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

#BUTTON

check_videos_btn = tk.Button(window_main, text="Check Videos", command=check_videos_clicked)
check_videos_btn.grid(row=1, column=0, padx=10, pady=10)

create_video_list_btn = tk.Button(window_main, text="Create Video List", command=create_video_list_clicked)
create_video_list_btn.grid(row=1, column=1, padx=10, pady=10)

update_videos_btn = tk.Button(window_main, text="Update Videos", command=update_video_clicked)
update_videos_btn.grid(row=1, column=2, padx=10, pady=10)
def Close():
    quit()
exit_button_btn = tk.Button(window_main, text="EXIT", command=Close, bg="red", activebackground="#8B0000")
exit_button_btn.grid(row=1, column=3, padx=10, pady=10)





window_main.mainloop()
