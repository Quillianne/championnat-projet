from tkinter import Tk, Canvas, Button, PhotoImage
import main as champ
import scrollableframe
from pathlib import Path


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)





class BoxBox(Canvas):
    def __init__(self, parent, x, y, button_images, button_commands):
        super().__init__(parent, bg="#3485FF", height=300, width=220, bd=0, highlightthickness=0, relief="ridge")
        self.place(x=x, y=y)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("box.png"))
        self.image_1 = self.create_image(
            110,
            100,
            image=self.image_image_1
        )

        self.bouton_images = []
        self.bouton = []
        for i in range(len(button_images)):

            self.bouton_images.append(PhotoImage(file=relative_to_assets(button_images[i])))
            self.bouton.append(Button(self, image=self.bouton_images[i], borderwidth=0, highlightthickness=0, command=button_commands[i], relief="flat"))
            self.bouton[i].place(x=32, y=140-38*i,width=158.0,height=34.0)


class MatchBox(BoxBox):
    def __init__(self, parent, match, x, y):
        super().__init__(parent, x,y, ["modifier.png"], [lambda: print("modifier clicked")])
        self.match = match
        self.place(x=x, y=y)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("box.png"))
        self.image_1 = self.create_image(
            110,
            100,
            image=self.image_image_1
        )

        self.create_text(30, 30, anchor="nw", text=f"{match.equipe_domicile.nom} VS {match.equipe_exterieur.nom}", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))
        self.create_text(30, 70, anchor="nw", text="Date: 16/04/2024", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))
        self.create_text(30, 100, anchor="nw", text="Time: 20H", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))


class ClubBox(BoxBox):
    def __init__(self, parent, club, x, y):
        super().__init__(parent, x,y, ["supprimer.png","modifier.png"], [lambda: print("supprimer clicked"),lambda: print("modifier clicked")])
        self.club = club
        self.place(x=x, y=y)

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("box.png"))
        self.image_1 = self.create_image(
            110,
            100,
            image=self.image_image_1
        )

        self.create_text(30, 30, anchor="nw", text=f"{club.nom}", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))




class TourBox(Canvas):
    def __init__(self, parent, tour):
        super().__init__(parent, bg="#3485FF", height=500, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.tour = tour
        self.pack(pady=0)

        self.create_text(30, 10, anchor="nw", text=f"TOUR {tour.numero}", fill="#FFFFFF", font=("DelaGothicOne Regular", 24 * -1))

        self.update_idletasks()  # Forcer la mise à jour de la géométrie

        x, y = 10, 40
        for match in tour.matchs:
            MatchBox(self, match, x, y)
            #ClubBox(self, match.equipe_domicile, x, y)
            x += 220
            if x + 220 > self.winfo_width():  # Nouvelle ligne si la largeur est dépassée
                x = 10
                y += 220
                
        self.configure(height=y)




class ClubGui(Canvas):
    def __init__(self, window, championnat):
        super().__init__(window, bg="#3485FF", height=650, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.window = window
        self.championnat = championnat

        self.pack()

        self.create_rectangle(0, 0, 900, 650, fill="#3485FF", outline="")

        self.create_text(20, 10, anchor="nw", text="CLUBS", fill="#FFFFFF", font=("DelaGothicOne Regular", 21 * -1))

        #On place aussi la ligne en dessous du titre
        self.line = self.create_rectangle(
            20.0,
            40.0,
            147.0,
            44.0,
            fill="#FFFFFF",
            outline="")
    
        self.scroll_canvas = Canvas(self,bg="#3485FF", height=450, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.scroll_canvas.place(x=0,y=100)

        self.club_frame = scrollableframe.ScrollableFrame(self.scroll_canvas, bg="#3485FF")
        self.club_frame.place(x=0, y=0, relwidth=1, relheight=1)


        # Store reference to the image
        self.button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
        button_9 = Button(self,
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_9 clicked"),
            relief="flat"
        )
        button_9.place(
            x=600.0,
            y=15.0,
            width=250.0,
            height=35.0
        )


        self.button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
        button_10 = Button(self,
            image=self.button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_10 clicked"),
            relief="flat"
        )
        button_10.place(
            x=47.0,
            y=590.0,
            width=250.0,
            height=35.0
        )

        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        button_5 = Button(self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        button_5.place(
            x=320.0,
            y=590.0,
            width=110.0,
            height=35.0
        )

        self.button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
        button_8 = Button(self,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        button_8.place(
            x=525.0,
            y=590.0,
            width=55.0,
            height=35.0
        )

        self.button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
        button_7 = Button(self,
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        button_7.place(
            x=450.0,
            y=590.0,
            width=75.0,
            height=33.0
        )

        self.button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
        button_6 = Button(self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        button_6.place(
            x=600.0,
            y=590.0,
            width=250.0,
            height=35.0
        )


        self.update_idletasks()  # Forcer la mise à jour de la géométrie

        x, y = 10, 40
        for club in championnat.participants:

            ClubBox(self.club_frame, club, x, y)
            x += 220
            if x + 220 > self.winfo_width():  # Nouvelle ligne si la largeur est dépassée
                x = 10
                y += 220
                
        self.club_frame.configure(height=y)



class TourGui(Canvas):
    def __init__(self, window, championnat):
        super().__init__(window, bg="#3485FF", height=650, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.window = window
        self.championnat = championnat

        self.pack()

        self.create_rectangle(0, 0, 900, 650, fill="#3485FF", outline="")

        self.create_text(20, 10, anchor="nw", text="TOURS", fill="#FFFFFF", font=("DelaGothicOne Regular", 21 * -1))

        #On place aussi la ligne en dessous du titre
        self.line = self.create_rectangle(
            20.0,
            40.0,
            147.0,
            44.0,
            fill="#FFFFFF",
            outline="")
    
        self.scroll_canvas = Canvas(self,bg="#3485FF", height=450, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.scroll_canvas.place(x=0,y=100)

        tour_frame = scrollableframe.ScrollableFrame(self.scroll_canvas, bg="#3485FF")
        tour_frame.place(x=0, y=0, relwidth=1, relheight=1)


        # Store reference to the image
        self.button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
        button_9 = Button(self,
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_9 clicked"),
            relief="flat"
        )
        button_9.place(
            x=600.0,
            y=15.0,
            width=250.0,
            height=35.0
        )


        self.button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
        button_10 = Button(self,
            image=self.button_image_10,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_10 clicked"),
            relief="flat"
        )
        button_10.place(
            x=47.0,
            y=590.0,
            width=250.0,
            height=35.0
        )

        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        button_5 = Button(self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        button_5.place(
            x=320.0,
            y=590.0,
            width=110.0,
            height=35.0
        )

        self.button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
        button_8 = Button(self,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        button_8.place(
            x=525.0,
            y=590.0,
            width=55.0,
            height=35.0
        )

        self.button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
        button_7 = Button(self,
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        button_7.place(
            x=450.0,
            y=590.0,
            width=75.0,
            height=33.0
        )

        self.button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
        button_6 = Button(self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        button_6.place(
            x=600.0,
            y=590.0,
            width=250.0,
            height=35.0
        )

        for tour in championnat.tours:
            TourBox(tour_frame.scrollable_frame, tour)


if __name__ == "__main__":
    window = Tk()
    window.geometry("900x650")
    window.configure(bg="#FFFFFF")
    window.resizable(False, False)

    championnat = champ.Championnat("Ligue 1")

    clubs = [
        champ.Club("Paris Saint-Germain", "Paris", "Mauricio Pochettino", "logo_club1.png"),
        champ.Club("Olympique de Marseille", "Marseille", "Jorge Sampaoli", "logo_club2.png"),
        champ.Club("AS Monaco", "Monaco", "Niko Kovač", "logo_club3.png"),
        champ.Club("FC EnstApagnan", "Brest", "Quentin Dutailly", "logo_club4.png"),
        champ.Club("Lille OSC", "Lille", "Christophe Galtier", "logo_club5.png"),
        champ.Club("Olympique Lyonnais", "Lyon", "Rudi Garcia", "logo_club6.png"),
        champ.Club("Stade Rennais FC", "Rennes", "Kilian Barantal", "logo_club7.png"),
        champ.Club("RC Lens", "Lens", "Franck Haise", "logo_club8.png"),
        champ.Club("Stade de Reims", "Reims", "David Guion", "logo_club9.png"),
        champ.Club("OGC Nice", "Nice", "Adrian Ursea", "logo_club10.png"),
        champ.Club("Montpellier HSC", "Montpellier", "Michel Der Zakarian", "logo_club11.png"),
        champ.Club("Angers SCO", "Angers", "Gérald Baticle", "logo_club12.png"),
        champ.Club("FC Metz", "Metz", "Frédéric Antonetti", "logo_club13.png"),
        champ.Club("RC Strasbourg Alsace", "Strasbourg", "Thierry Laurey", "logo_club14.png"),
        champ.Club("FC Nantes", "Nantes", "Antoine Kombouaré", "logo_club15.png"),
        champ.Club("Dijon FCO", "Dijon", "David Linarès", "logo_club16.png")
    ]

    for club in clubs:
        championnat.ajouter_participant(club)

    championnat.generer_calendrier()

    tour_gui = TourGui(window, championnat)
    #tour_gui.pack_forget()

    window.mainloop()
