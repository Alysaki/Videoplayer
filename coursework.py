import tkinter as tk
import font_manager as fonts
import video_library as lib


def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)


class Coursework():
    def __init__(self, window):
        self.window = window
        window.geometry("1150x450")  # window size
        window.title("Course Work")  # window title

        enter_lbl = tk.Label(window, text="Enter Video Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        enter1_lbl = tk.Label(window, text="Enter New Rating")
        enter1_lbl.grid(row=0, column=4, padx=10, pady=10)

        # button
        list_videos_btn = tk.Button(window, text="List All Videos", command=self.list_videos_clicked)
        list_videos_btn.grid(row=0, column=0, padx=10, pady=10)

        check_video_btn = tk.Button(window, text="Check Video", command=self.check_video_clicked)
        check_video_btn.grid(row=0, column=3, padx=10, pady=10)

        add_videos_btn = tk.Button(window, text="Add Video", command=self.add_videos_clicked)
        add_videos_btn.grid(row=2, column=0, padx=10, pady=10)

        play_video_btn = tk.Button(window, text="Play Video", command=self.play_count)
        play_video_btn.grid(row=1, column=3, padx=10, pady=10)

        reset_btn = tk.Button(window, text="Reset", command=self.reset_clicked)
        reset_btn.grid(row=2, column=3, padx=10, pady=0)

        update_rate_video_btn = tk.Button(window, text="Update New Rating", command=self.update_rate_video_clicked)
        update_rate_video_btn.grid(row=0, column=6, padx=10, pady=10)

        exit_btn = tk.Button(window, text="EXIT", bg="red", command=self.exit_button_clicked)
        exit_btn.grid(row=2, column=6, padx=10, pady=10)

        # text
        self.input_txt = tk.Entry(window, width=3)  # place to enter video number
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        self.list_txt = tk.Text(window, width=38, height=12, wrap="none")  # place show information video
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.video_txt = tk.Text(window, width=24, height=4,
                                 wrap="none")  # place show information after click check video
        self.video_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        self.update_rate_txt = tk.Text(window, width=3, height=1)  # place to enter rating number
        self.update_rate_txt.grid(row=0, column=5, padx=10, pady=10)

        self.new_rate_txt = tk.Text(window, width=24, height=4,
                                    wrap="none")  # place to show info after click update rate
        self.new_rate_txt.grid(row=1, column=6, sticky="NW", padx=10, pady=10)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 14))  # place to show notifications
        self.status_lbl.grid(row=100, column=1, columnspan=4, sticky="W", padx=10, pady=10)

        self.list_videos_clicked()

    def check_video_clicked(self):
        key = self.input_txt.get()
        name = lib.get_name(key)
        if name is not None:
            director = lib.get_director(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            video_details = f"{name}\n{director}\nrating: {rating}\nplays: {play_count}"
            set_text(self.video_txt, video_details)
        else:
            set_text(self.video_txt, f"Video {key} not found")
        self.status_lbl.configure(text="Check Video button was clicked!")

    def list_videos_clicked(self):
        video_list = lib.list_all()
        set_text(self.list_txt, video_list)
        self.status_lbl.configure(text="")

        self.playliststore = []  # place to store the playlist
        self.playliststore_key = []  # place to store the key of videos in the playlist
        self.current_video_key = None  # Variable to store the current selected video key
        self.filtered_list = ""  # String to store the filtered video list
        self.status_lbl.configure(text="List Videos button was clicked!")


    def add_videos_clicked(self):
        key = self.input_txt.get()
        if key.startswith(
                '-'):  # startswith: Checks a value against a selected string and returns True if the string starts with that value.
            self.status_lbl.configure(text="enter a valid number")
        elif not key.isdigit():  # isdigit: true for all numbers, non-numbers = false
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

    def reset_clicked(self):
        for key in self.playliststore_key:
            lib.reset_play_count(self)  # Reset the play count of each video in the playlist
        self.playliststore = []  # Clear the playlist
        self.playliststore_key = []  # Clear the keys of the playlist
        self.display_playlist()  # Clear the text area
        self.filtered_list = ""  # Clear the filtered list
        set_text(self.list_txt, "")  # Clear the list_txt text area
        self.status_lbl.configure(text="Playlist reset.")  # Update the status label
        self.input_txt.delete(0, tk.END)

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

    def update_status_label(self):  # Update the status label with the current playlist.
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
            director = lib.get_director(key)
            updated_rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            video_details = f"{video_name}\n{director}\nNew Rating: {updated_rating}\nplays: {play_count}"
            set_text(self.new_rate_txt, video_details)
            self.status_lbl.configure(text="Rating updated successfully!")
        else:
            set_text(self.new_rate_txt, f"Failed to update rating for video {key}")
            self.status_lbl.configure(text="Failed to update rating.")

    def exit_button_clicked(self):
        self.window.destroy() # destroy GUI


if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()  # create a TK object
    fonts.configure()  # configure the fonts
    Coursework(window)  # open the CheckVideo GUI
    window.mainloop()  # run the window main loop, reacting to button presses, etc
