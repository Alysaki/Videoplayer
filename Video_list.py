import tkinter as main
import font_manager as fonts



window = main.Tk()
window.geometry("720x350")
window.title("Update Videos")

fonts.configure()

                      #title
header_lbl1 = main.Label(window, text="Write a number to add video")
header_lbl1.grid(row=0, column=9, padx=10, pady=10)


                       #button
send_btn = main.Button(window, text="")
send_btn.grid(row=10, column=6, padx=10, pady=10)

cancel_btn = main.Button(window, text="")
cancel_btn.grid(row=10, column=3, padx=10, pady=10)




status_lbl = main.Label(window, text="", font=("Helvetica", 10))
status_lbl.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

window.mainloop()




