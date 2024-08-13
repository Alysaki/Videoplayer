import tkinter as tk
import video_library as lib
import font_manager as fonts


def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class CreateVideosList():
    def __init__(self, window2):
        self.window2 = window2
        window2.geometry("850x400")  #window size
        window2.title("Create Video")  #window title

        #BUTTON
        add_videos_btn = tk.Button(window2, text="Add Video", command=self.add_videos_clicked)
        add_videos_btn.grid(row=0, column=0, padx=10, pady=10)

        play_video_btn = tk.Button(window2, text="Play Video", command=self.play_count)
        play_video_btn.grid(row=0, column=3, padx=10, pady=10)

        reset_btn = tk.Button(window2, text="Reset", command=self.reset_clicked)
        reset_btn.grid(row=0, column=4, padx=10, pady=10)

        back_btn = tk.Button(window2, text="Back To Main", background="red", command=self.back_to_main_clicked)
        back_btn.grid(row=2, column=4, padx=10, pady=10)

        # place to enter number videos
        enter_lbl = tk.Label(window2, text="Enter Video Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)
        self.input_txt = tk.Entry(window2, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        #display video name
        self.list_txt = tk.Text(window2, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        #display video information
        self.video_txt = tk.Text(window2, width=24, height=4, wrap="none")
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        #font, size notification under left
        self.status_lbl = tk.Label(window2, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        self.playliststore = []  # place to store the playlist
        self.playliststore_key = []  # place to store the key of videos in the playlist
        self.current_video_key = None  # Variable to store the current selected video key
        self.filtered_list = ""  # String to store the filtered video list

    def add_videos_clicked(self):
        key = self.input_txt.get()
        if key.startswith(
                '-'):  #startswith: kiểm tra giá trị so với một chuỗi đã cho và trả về True nếu chuỗi bắt đầu bằng giá trị đó
            self.status_lbl.configure(text="enter a valid number")
        elif not key.isdigit():  #isdigit: true với mọi số, ko phải số = false
            self.status_lbl.configure(text="enter a valid number")
            return
        name = lib.get_name(str(key).zfill(2))
        if name is None:
            self.status_lbl.configure(text="Video not found")
            return

        director = lib.get_director(str(key).zfill(2))
        rating = lib.get_rating(str(key).zfill(2))
        play_count = lib.get_play_count(str(key).zfill(2))

        self.name = name
        self.director = director
        self.rating = rating

        # Update filtered_list with the new video details
        self.filtered_list += f"{key} {self.name} - {self.director} {self.stars()}\n"

        # Update list_txt with the filtered video details
        set_text(self.list_txt, self.filtered_list)

        # Add video to playlist and update the display
        self.playliststore.append(f"{name}\n{director}\nrating: {rating}\nplays: {play_count}")
        self.playliststore_key.append(str(key).zfill(2))
        self.current_video_key = str(key).zfill(2)

        self.display_playlist()  # Display updated playlist
        self.update_status_label()  # Update status label
        self.input_txt.delete(0, tk.END)  # Clear input field

    def reset_clicked(self):
        for key in self.playliststore_key:
            lib.reset_play_count(self)  # Reset the play count of each video in the playlist
        self.playliststore = []  # Clear the playlist
        self.playliststore_key = []  # Clear the keys of the playlist
        self.display_playlist()  # Clear the text area
        self.filtered_list = ""  # Clear the filtered list
        set_text(self.list_txt, "")  # Clear the list_txt text area
        self.status_lbl.configure(text="Playlist reset.")  # Update the status label

    # Generate a string of stars based on the rating.
    def stars(self):
        stars = ""
        if self.rating is not None:
            for i in range(self.rating):
                stars += "*"
        return stars

    def display_current_video(self):
        """Display the currently selected video in the text area."""
        if self.current_video_key:
            name = lib.get_name(self.current_video_key)
            director = lib.get_director(self.current_video_key)
            rating = lib.get_rating(self.current_video_key)
            play_count = lib.get_play_count(self.current_video_key)
            video_details = (f"Video {self.current_video_key}:\nName: {name}\nDirector: {director}\n"
                             f"Rating: {rating}\nPlay Count: {play_count}\n")
            set_text(self.video_txt, video_details)

    def update_status_label(self):
        """Update the status label with the current playlist."""
        playlist_summary = " | ".join(self.playliststore_key)
        self.status_lbl.configure(text=f"Current Playlist: {playlist_summary}")

    def display_playlist(self):
        """Display the playlist in the text area."""
        playlist_content = "\n".join(self.playliststore)  # Join playlist items into a single string
        set_text(self.video_txt, playlist_content)  # Display the playlist in the text area

    def update_playlist(self):
        updated_playlist = []
        for key in self.playliststore_key:
            name = lib.get_name(key)
            director = lib.get_director(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            updated_playlist.append(f"{name}\n{director}\nrating: {rating}\nplays: {play_count}")
        self.playliststore = updated_playlist
        self.display_playlist()

    def update_status_label(self):  #Update the status label with the current playlist.
        playlist_summary = " | ".join(self.playliststore_key)
        self.status_lbl.configure(text=f"Current Playlist: {playlist_summary}")

    def play_count(self):
        if self.current_video_key is not None:
            lib.increment_play_count(self.current_video_key)  # Increment the play count of the current video
            self.update_playlist()  # Update the playlist with new play counts
            self.status_lbl.configure(
                text="Play clicked, please click reset button to add and play another video")  # Update the status label
        else:
            self.status_lbl.configure(text="select a video to play")

    def back_to_main_clicked(self):
        self.window2.destroy()


if __name__ == "__main__":  # only runs when this file is run as a standalone
    window2 = tk.Tk()  # create a TK object
    fonts.configure()  # configure the fonts
    CreateVideosList(window2)  # open the CheckVideo GUI
    window2.mainloop()  # run the window2 main loop, reacting to button presses, etc
