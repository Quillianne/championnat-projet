import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
from main import Club, Match, Tour, Championnat, Statistiques

class ClubInfoGUI:
    def __init__(self, club, matches_played):
        self.root = tk.Toplevel()
        self.root.title(f"Informations sur {club.nom}")

        # Créer une étiquette pour afficher les informations du club
        club_info_text = (f"Informations sur {club.nom}\n"
                          f"Entraîneur : {club.entraineur}\n"
                          f"Emplacement : {club.emplacement}\n"
                          f"Matchs joués : {club.statistique.matchs_joues}\n"
                          f"Victoires à domicile : {club.statistique.victoires_domicile}\n"
                          f"Victoires à l'extérieur : {club.statistique.victoires_exterieur}\n"
                          f"Matchs nuls : {club.statistique.matchs_nuls}\n"
                          f"Défaites : {club.statistique.defaites}\n"
                          f"Score : {club.statistique.score}\n"
                          f"Goal Average : {club.statistique.goal_average}\n\n"
                          f"Rencontres passées :\n")
        for match in matches_played:
            club_info_text += f"{match.equipe_domicile.nom} {match.resultat[0]} - {match.resultat[1]} {match.equipe_exterieur.nom}\n"

        self.label = tk.Label(self.root, text=club_info_text)
        self.label.pack()

class ClassementGUI:
    def __init__(self, classement, calendrier):
        self.root = tk.Tk()
        self.root.title("Classement du Championnat")

        self.classement = classement
        self.calendrier = calendrier

        # Créer un style pour personnaliser l'apparence des en-têtes de colonnes
        self.style = ttk.Style()
        self.style.configure("Custom.Treeview.Heading", foreground="black")

        self.tableau = ttk.Treeview(self.root, style="Custom.Treeview")
        self.tableau["columns"] = ("Position", "Logo", "Nom", "Victoires", "Nuls", "Défaites", "Score", "Goal Average")

        self.tableau.heading("Position", text="Position")
        self.tableau.heading("Logo", text="Logo")
        self.tableau.heading("Nom", text="Nom")
        self.tableau.heading("Victoires", text="Victoires")
        self.tableau.heading("Nuls", text="Nuls")
        self.tableau.heading("Défaites", text="Défaites")
        self.tableau.heading("Score", text="Score")
        self.tableau.heading("Goal Average", text="Goal Average")

        self.logo_images = {}  # Dictionnaire pour stocker les images des logos

        for i, (club, _) in enumerate(self.classement, 1):
            # Charger l'image du logo
            logo = Image.open(club.logo)
            logo = logo.resize((50, 50), Image.LANCZOS)  # Utiliser LANCZOS pour le redimensionnement
            logo_tk = ImageTk.PhotoImage(logo)

            # Ajouter l'image du logo au dictionnaire
            self.logo_images[club.nom] = logo_tk

            # Ajouter une ligne au tableau avec le nom du club et son logo
            self.tableau.insert("", "end", values=(i, "", club.nom, club.statistique.victoires_domicile + club.statistique.victoires_exterieur,
                                                   club.statistique.matchs_nuls, club.statistique.defaites, club.statistique.score,
                                                   club.statistique.goal_average))

        # Lier la méthode 'show_club_info' à l'événement de double clic sur une ligne du tableau
        self.tableau.bind("<Double-1>", self.show_club_info)

        self.tableau.pack(expand=True, fill="both")

    def show_club_info(self, event):
        # Récupérer l'élément sélectionné dans le tableau
        selection = self.tableau.selection()

        # Vérifier si une sélection a été faite et qu'il y a un élément sélectionné
        if selection:
            # Récupérer l'indice de l'élément sélectionné dans le tableau
            item = selection[0]
            index = self.tableau.index(item)

            # Récupérer le nom du club sélectionné
            club_name = self.tableau.item(item, "values")[2]

            # Récupérer l'objet Club correspondant
            club = [club for club, _ in self.classement if club.nom == club_name][0]

            # Récupérer les matchs joués par le club depuis le calendrier
            matches_played = []
            for tour in self.calendrier:
                for match in tour.matchs:
                    if match.equipe_domicile.nom == club.nom or match.equipe_exterieur.nom == club.nom:
                        matches_played.append(match)

            # Afficher les informations du club et les rencontres passées dans une nouvelle fenêtre
            club_info_window = ClubInfoGUI(club, matches_played)

    def afficher(self):
        self.root.mainloop()


if __name__ == "__main__":
    # Supposons que 'championnat' contienne l'instance de Championnat après son exécution
    championnat = Championnat("Ligue 1")

    clubs = [
        Club("Paris Saint-Germain", "Paris", "Mauricio Pochettino","logo_psg.png"),
        Club("Olympique de Marseille", "Marseille", "Jorge Sampaoli","logo_psg.png"),
        Club("AS Monaco", "Monaco", "Niko Kovač","logo_psg.png"),
        Club("FC EnstApagnan", "Brest", "Quentin Dutailly","logo_psg.png"),
        Club("Lille OSC", "Lille", "Christophe Galtier","logo_psg.png"),
        Club("Olympique Lyonnais", "Lyon", "Rudi Garcia","logo_psg.png"),
        Club("Stade Rennais FC", "Rennes", "Kilian Barantal","logo_psg.png"),
        Club("RC Lens", "Lens", "Franck Haise","logo_psg.png"),
        Club("Stade de Reims", "Reims", "David Guion","logo_psg.png"),
        Club("OGC Nice", "Nice", "Adrian Ursea","logo_psg.png"),
        Club("Montpellier HSC", "Montpellier", "Michel Der Zakarian","logo_psg.png"),
        Club("Angers SCO", "Angers", "Gérald Baticle","logo_psg.png"),
        Club("FC Metz", "Metz", "Frédéric Antonetti","logo_psg.png"),
        Club("RC Strasbourg Alsace", "Strasbourg", "Thierry Laurey","logo_psg.png"),
        Club("FC Nantes", "Nantes", "Antoine Kombouaré","logo_psg.png"),
        Club("Dijon FCO", "Dijon", "David Linarès","logo_psg.png")
    ]

    for club in clubs:
        championnat.ajouter_participant(club)

    # Générer le calendrier et jouer les matchs
    championnat.generer_calendrier()
    for tour in championnat.tours:
        for match in tour.matchs:
            # Simuler les scores aléatoires
            score_equipe_domicile = random.randint(0, 5)
            score_equipe_exterieur = random.randint(0, 5)

            # Jouer le match
            match.jouer_match((score_equipe_domicile, score_equipe_exterieur))

    # Obtenir le classement des clubs
    classement_championnat = championnat.classement()

    # Créer une instance de la classe ClassementGUI en lui passant le classement et le calendrier
    interface = ClassementGUI(classement_championnat, championnat.tours)

    # Afficher l'interface
    interface.afficher()

