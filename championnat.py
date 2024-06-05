
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("900x650")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 650,
    width = 900,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    900.0,
    650.0,
    fill="#3485FF",
    outline="")

canvas.create_text(
    20.0,
    10.0,
    anchor="nw",
    text="CHAMPIONNAT",
    fill="#FFFFFF",
    font=("DelaGothicOne Regular", 21 * -1)
)

canvas.create_rectangle(
    16.0,
    46.0,
    147.0,
    50.0,
    fill="#FFFFFF",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    129.0,
    215.0,
    image=image_image_1
)

canvas.create_text(
    56.0,
    170.0,
    anchor="nw",
    text="CHAMPIONNAT 1",
    fill="#000000",
    font=("DelaGothicOne Regular", 12 * -1)
)

canvas.create_text(
    56.0,
    215.0,
    anchor="nw",
    text="FOOT",
    fill="#000000",
    font=("DelaGothicOne Regular", 12 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    354.0,
    215.0,
    image=image_image_2
)

canvas.create_text(
    277.0,
    170.0,
    anchor="nw",
    text="CHAMPIONNAT 2",
    fill="#000000",
    font=("DelaGothicOne Regular", 12 * -1)
)

canvas.create_text(
    277.0,
    215.0,
    anchor="nw",
    text="FOOT",
    fill="#000000",
    font=("DelaGothicOne Regular", 12 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=276.0,
    y=260.0,
    width=158.0,
    height=34.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=51.0,
    y=260.0,
    width=158.0,
    height=34.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=47.0,
    y=590.0,
    width=250.0,
    height=35.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=600.0,
    y=590.0,
    width=250.0,
    height=35.0
)
window.resizable(False, False)
window.mainloop()