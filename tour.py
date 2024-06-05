from tkinter import Tk, Canvas, Button, PhotoImage, Entry
import main as champ
import scrollableframe
from pathlib import Path
import choose_date


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets")


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
        super().__init__(parent, x,y, ["modifier.png"], [lambda: self.modifier_horaire()])
        self.match = match
        self.place(x=x, y=y)


        self.VS = self.create_text(60, 30, anchor="nw", text=f"{match.equipe_domicile.surnom} VS {match.equipe_exterieur.surnom}", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))
        self.date = self.create_text(50, 70, anchor="nw", text=f"{match.date.strftime('%d/%m/%Y')}", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))
        #self.hour = self.create_text(50, 100, anchor="nw", text=f"{match.date.strftime('%HH%M')}", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))

    def modifier_horaire(self):
        new_date = choose_date.DateDialog(window, 'Choisir horaire', self.match.date).selected_date
        self.match.date = new_date
        self.itemconfig(self.date, text=f"{self.match.date.strftime('%d/%m/%Y')}")
        #self.itemconfig(self.hour, text=f"{self.match.date.strftime('%HH%M')}")

    


class ClubBox(BoxBox):
    def __init__(self, parent, club, x, y, clubgui):
        super().__init__(parent, x,y, ["supprimer.png","modifier.png"], [lambda: self.delete(),lambda: club_gui.modifier_equipe(club)])
        self.club = club
        self.place(x=x, y=y)
        self.clubgui = clubgui


        self.create_text(30, 30, anchor="nw", text=f"{club.surnom}", fill="#000000", font=("DelaGothicOne Regular", 12 * -1))



    def delete(self):
        self.clubgui.championnat.supprimer_club(self.club)
        self.clubgui.update()
    





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
            #TextEntryBox(self, x, y)
            #ClubBox(self, match.equipe_domicile, x, y)
            x += 220
            if x + 220 > self.winfo_width():  # Nouvelle ligne si la largeur est dépassée
                x = 10
                y += 220
                
        self.configure(height=y)




class TextEntryBox(Canvas):
    def __init__(self, parent, x, y, text, default_text=""):
        super().__init__(parent, bg="#3485FF", height=80, width=365, bd=0, highlightthickness=0, relief="ridge")
        self.place(x=x, y=y)

        self.text_box_bg = PhotoImage(file=relative_to_assets("TextBox_Bg.png"))
        self.create_image(180, 40, image=self.text_box_bg)
        
        self.token_entry = Entry(self, bd=0, bg="#F6F7F9", fg="#000716", highlightthickness=0)
        self.token_entry.place(x=20, y=30, width=321.0, height=35)
        self.token_entry.insert(0, default_text)  # Insérer le texte prérempli ici

        self.create_text(
            20, 20.0, text=text, fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")
        
        self.token_entry.focus()

    def get(self):
        return self.token_entry.get()



class NewClubGui(Canvas):
    def __init__(self, window, championnat):
        super().__init__(window, bg="#3485FF", height=650, width=900, bd=0, highlightthickness=0, relief="ridge")

        self.window = window
        self.championnat = championnat

        self.pack()

        self.create_rectangle(0, 0, 900, 650, fill="#3485FF", outline="")

        self.create_text(20, 10, anchor="nw", text=self.championnat.nom, fill="#FFFFFF", font=("DelaGothicOne Regular", 21 * -1))

        #On place aussi la ligne en dessous du titre
        self.line = self.create_rectangle(
            20.0,
            40.0,
            147.0,
            44.0,
            fill="#FFFFFF",
            outline="")
    
        
        self.club_surname = TextEntryBox(self,270,180,"SURNOM")
        self.club_city = TextEntryBox(self,270,260,"VILLE")
        self.club_entraineur = TextEntryBox(self,270,340,"ENTRAINEUR")
        self.club_logo = TextEntryBox(self,270,420,"LOGO")
        self.club_name = TextEntryBox(self,270,100,"NOM DU CLUB")

                # Store reference to the image
        self.button_ok_image = PhotoImage(file=relative_to_assets("ok.png"))
        self.button_ok = Button(self,
            image=self.button_ok_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.create_club(),
            relief="flat"
        )
        self.button_ok.place(
            x=320.0,
            y=565.0,
            width=250.0,
            height=35.0
        )

        self.button_cancel_image = PhotoImage(file=relative_to_assets("cancel.png"))
        self.button_cancel = Button(self,
            image=self.button_cancel_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.cancel_creation(),
            relief="flat"
        )
        self.button_cancel.place(
            x=320.0,
            y=605.0,
            width=250.0,
            height=35.0
        )

    def create_club(self):
        self.club = champ.Club(self.club_name.get(), self.club_city.get(), self.club_entraineur.get(), self.club_logo.get(), self.club_surname.get())
        self.championnat.ajouter_participant(self.club)
        print(len(self.championnat.participants))
        self.pack_forget()
        club_gui.update()
        #self.destroy()

    def cancel_creation(self):
        self.pack_forget()
        #self.destroy()

class ModifyClubGui(NewClubGui):
    def __init__(self, window, championnat, club):
        super().__init__(window, championnat)
        self.club = club

        self.club_surname = TextEntryBox(self,270,180,"SURNOM",self.club.surnom)
        self.club_city = TextEntryBox(self,270,260,"VILLE",self.club.emplacement)
        self.club_entraineur = TextEntryBox(self,270,340,"ENTRAINEUR",self.club.entraineur)
        self.club_logo = TextEntryBox(self,270,420,"LOGO",self.club.logo)
        self.club_name = TextEntryBox(self,270,100,"NOM DU CLUB",self.club.nom)
        self.button_ok.configure(command=lambda: self.modify_club())

    def modify_club(self):
        self.club.surnom = self.club_surname.get()
        self.club.emplacement = self.club_city.get()
        self.club.entraineur = self.club_entraineur.get()
        self.club.logo = self.club_logo.get()
        self.club.nom = self.club_name.get()
        self.pack_forget()
        club_gui.update()


class ClubGui(Canvas):
    def __init__(self, window, championnat):
        super().__init__(window, bg="#3485FF", height=650, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.window = window
        self.championnat = championnat

        self.place(x=0,y=0)

        self.create_rectangle(0, 0, 900, 650, fill="#3485FF", outline="")

        self.create_text(20, 10, anchor="nw", text=self.championnat.nom, fill="#FFFFFF", font=("DelaGothicOne Regular", 21 * -1))

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
        self.button_export = PhotoImage(file=relative_to_assets("exporter.png"))
        button_export = Button(self,
            image=self.button_export,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("exporter clicked"),
            relief="flat"
        )
        button_export.place(
            x=600.0,
            y=15.0,
            width=250.0,
            height=35.0
        )


        self.button_image_10 = PhotoImage(file=relative_to_assets("lancer.png"))
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



        self.button_club_image = PhotoImage(file=relative_to_assets("club_activated.png"))
        button_club = Button(self,
            image=self.button_club_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.update(),
            relief="flat"
        )
        button_club.place(
            x=525.0,
            y=590.0,
            width=55.0,
            height=35.0
        )

        self.button_match_image = PhotoImage(file=relative_to_assets("match.png"))
        button_match = Button(self,
            image=self.button_match_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (tour_gui.update(),tour_gui.place(x=0,y=0), club_gui.place_forget()),
            relief="flat"
        )
        button_match.place(
            x=450.0,
            y=590.0,
            width=75.0,
            height=33.0
        )

        self.button_add_image = PhotoImage(file=relative_to_assets("ajouter_equipe.png"))
        button_add = Button(self,
            image=self.button_add_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.ajouter_equipe(),
            relief="flat"
        )
        button_add.place(
            x=600.0,
            y=590.0,
            width=250.0,
            height=35.0
        )

        self.club_canvas = Canvas(self.club_frame.scrollable_frame, bg="#3485FF", height=500, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.club_canvas.pack(pady=0)
        self.club_canvas.update_idletasks()  # Forcer la mise à jour de la géométrie

        x, y = 10, 40

        self.boxes = []

        for club in self.championnat.participants:
            #MatchBox(self, match, x, y)
            self.boxes.append(ClubBox(self.club_canvas, club, x, y, self))
            x += 220
            if x + 220 > self.club_canvas.winfo_width():  # Nouvelle ligne si la largeur est dépassée
                x = 10
                y += 220
                
        self.club_canvas.configure(height=y)

    def ajouter_equipe(self):
        #self.pack_forget()
        self.new_club_gui = NewClubGui(self.window, self.championnat)


    def modifier_equipe(self, club):
        #self.pack_forget()
        self.new_club_gui = ModifyClubGui(self.window, self.championnat, club)

    def update(self):
        for box in self.boxes:
            box.pack_forget()
            box.destroy()
        self.boxes.clear()
        print(len(self.championnat.participants))

        x, y = 10, 40

        for club in self.championnat.participants:
            #MatchBox(self, match, x, y)
            self.boxes.append(ClubBox(self.club_canvas, club, x, y, self))
            x += 220
            if x + 220 > self.club_canvas.winfo_width():  # Nouvelle ligne si la largeur est dépassée
                x = 10
                y += 220
                
        self.club_canvas.configure(height=y+450)



class TourGui(Canvas):
    def __init__(self, window, championnat):
        super().__init__(window, bg="#3485FF", height=650, width=900, bd=0, highlightthickness=0, relief="ridge")
        self.window = window
        self.championnat = championnat
        self.boxes = []

        self.place(x=0,y=0)

        self.create_rectangle(0, 0, 900, 650, fill="#3485FF", outline="")

        self.create_text(20, 10, anchor="nw", text=self.championnat.nom, fill="#FFFFFF", font=("DelaGothicOne Regular", 21 * -1))

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

        self.tour_frame = scrollableframe.ScrollableFrame(self.scroll_canvas, bg="#3485FF")
        self.tour_frame.place(x=0, y=0, relwidth=1, relheight=1)


        # Store reference to the image
        self.button_export = PhotoImage(file=relative_to_assets("exporter.png"))
        button_export = Button(self,
            image=self.button_export,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("exporter clicked"),
            relief="flat"
        )
        button_export.place(
            x=600.0,
            y=15.0,
            width=250.0,
            height=35.0
        )


        self.button_image_10 = PhotoImage(file=relative_to_assets("lancer.png"))
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

        self.button_reset_image = PhotoImage(file=relative_to_assets("reset.png"))
        button_reset = Button(self,
            image=self.button_reset_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (self.championnat.reset_calendrier(),self.update()),
            relief="flat"
        )
        button_reset.place(
            x=320.0,
            y=590.0,
            width=110.0,
            height=35.0
        )

        self.button_club_image = PhotoImage(file=relative_to_assets("club.png"))
        button_club = Button(self,
            image=self.button_club_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: (club_gui.update(), tour_gui.place_forget(), club_gui.place(x=0,y=0)),
            relief="flat"
        )
        button_club.place(
            x=525.0,
            y=590.0,
            width=55.0,
            height=35.0
        )

        self.button_match_image = PhotoImage(file=relative_to_assets("match_activated.png"))
        button_match = Button(self,
            image=self.button_match_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.update(),
            relief="flat"
        )
        button_match.place(
            x=450.0,
            y=590.0,
            width=75.0,
            height=33.0
        )

        self.button_generate_image = PhotoImage(file=relative_to_assets("generer.png"))
        button_generate = Button(self,
            image=self.button_generate_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.generer_calendrier_et_update(),
            relief="flat"
        )
        button_generate.place(
            x=600.0,
            y=590.0,
            width=250.0,
            height=35.0
        )


    def update(self):
        for box in self.boxes:
            box.pack_forget()
            box.destroy()
        self.boxes.clear()

        # Ajouter les nouveaux éléments
        for tour in self.championnat.tours:
            self.boxes.append(TourBox(self.tour_frame.scrollable_frame, tour))


    def generer_calendrier_et_update(self):
        self.championnat.generer_calendrier()
        self.update()





if __name__ == "__main__":
    window = Tk()
    window.geometry("900x650")
    window.configure(bg="#FFFFFF")
    window.resizable(False, False)

    championnat = champ.Championnat("Ligue 1")

    clubs = [
        champ.Club("Paris Saint-Germain", "Paris", "Mauricio Pochettino", "logo_club1.png", "PSG"),
        champ.Club("Olympique de Marseille", "Marseille", "Jorge Sampaoli", "logo_club2.png", "OM"),
        champ.Club("AS Monaco", "Monaco", "Niko Kovač", "logo_club3.png", "ASM"),
        champ.Club("Stade Brestois", "Brest", "Quentin Dutailly", "logo_club4.png", "SB29"),
        champ.Club("Lille OSC", "Lille", "Christophe Galtier", "logo_club5.png", "LOSC"),
        champ.Club("Olympique Lyonnais", "Lyon", "Rudi Garcia", "logo_club6.png", "OL"),
        champ.Club("Stade Rennais FC", "Rennes", "Kilian Barantal", "logo_club7.png", "SRFC"),
        champ.Club("RC Lens", "Lens", "Franck Haise", "logo_club8.png", "RCL"),
        champ.Club("Stade de Reims", "Reims", "David Guion", "logo_club9.png", "SDR"),
        champ.Club("OGC Nice", "Nice", "Adrian Ursea", "logo_club10.png", "OGCN"),
        champ.Club("Montpellier HSC", "Montpellier", "Michel Der Zakarian", "logo_club11.png", "MHSC"),
        champ.Club("Angers SCO", "Angers", "Gérald Baticle", "logo_club12.png", "SCO"),
        champ.Club("FC Metz", "Metz", "Frédéric Antonetti", "logo_club13.png", "FCM"),
        champ.Club("RC Strasbourg Alsace", "Strasbourg", "Thierry Laurey", "logo_club14.png", "RCSA"),
        champ.Club("FC Nantes", "Nantes", "Antoine Kombouaré", "logo_club15.png", "FCN"),
        champ.Club("Dijon FCO", "Dijon", "David Linarès", "logo_club16.png", "DFCO")
    ]

    for club in clubs:
        championnat.ajouter_participant(club)

    
    club_gui = ClubGui(window, championnat)
    tour_gui = TourGui(window, championnat)
    
    tour_gui.place_forget()
    
    #TextEntryBox(window, 100, 200)

    window.mainloop()
