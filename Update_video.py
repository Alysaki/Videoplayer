import tkinter as tk
import video_library as lib
import font_manager as fonts

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class UpdateVideo():
    def __init__(self, window1):
        self.window1 = window1
        window1.geometry("900x300")
        window1.title("Update Video")

        enter_lbl = tk.Label(window1, text="Enter Video Number")
        enter_lbl.grid(row=0, column=0, padx=10, pady=10)

        find_videos_btn = tk.Button(window1, text="Find Video", command=self.find_videos_clicked)
        find_videos_btn.grid(row=0, column=2, padx=10, pady=10)

        enter1_lbl = tk.Label(window1, text="Enter New Rating")
        enter1_lbl.grid(row=0, column=3, padx=10, pady=10)

        update_rate_video_btn = tk.Button(window1, text="Update New Rating", command=self.update_rate_video_clicked)
        update_rate_video_btn.grid(row=0, column=5, padx=10, pady=10)

        back_btn = tk.Button(window1, text="Back to Main", command=self.back_to_main_clicked)
        back_btn.grid(row=3, column=3, padx=10, pady=10)

        self.input_txt = tk.Entry(window1, width=3)
        self.input_txt.grid(row=0, column=1, padx=10, pady=10)

        self.find_txt = tk.Text(window1, width=24, height=4, wrap="none")
        self.find_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.update_rate_txt = tk.Text(window1, width=3, height=1)
        self.update_rate_txt.grid(row=0, column=4, padx=10, pady=10)

        self.new_rate_txt = tk.Text(window1, width=24, height=4, wrap="none")
        self.new_rate_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        self.status_lbl = tk.Label(window1, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=3, column=0, columnspan=4, sticky="W", padx=10, pady=10)

    def update_rate_video_clicked(self):
        key = self.input_txt.get()
        new_rating = self.update_rate_txt.get("1.0", tk.END)

        if not new_rating.isdigit():
            set_text(self.new_rate_txt, "Please enter a valid number")
        elif not (0 <= int(new_rating) <= 5):
            set_text(self.new_rate_txt, "Please enter a valid rating (0-5)")
            return
        success = lib.update_rating(key, int(new_rating))
        if success:
            video_name = lib.get_name(key)
            updated_rating = lib.get_rating(key)
            video_details = f"{video_name}\nNew Rating: {updated_rating}"
            set_text(self.new_rate_txt, video_details)
            self.status_lbl.configure(text="Rating updated successfully!")
        else:
            set_text(self.new_rate_txt, f"Failed to update rating for video {key}")
            self.status_lbl.configure(text="Failed to update rating.")

    def find_videos_clicked(self):
        key = self.input_txt.get()
        video_name = lib.get_name(key)

        if video_name is not None:
            director = lib.get_director(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            video_details = f"{video_name}\n{director}\nRating: {rating}\nPlays: {play_count}"
            set_text(self.find_txt, video_details)
        else:
            set_text(self.find_txt, f"Please enter a valid video number")
        self.status_lbl.configure(text="Find Video button was clicked!")

    def back_to_main_clicked(self):
        self.window1.destroy()

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window1 = tk.Tk()        # create a TK object
    fonts.configure()        # configure the fonts
    UpdateVideo(window1)     # open GUI
    window1.mainloop()       # run the window1 main loop, reacting to button presses, etc
