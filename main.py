from itertools import combinations
import random
from tools import transform_list

from tkinter import Tk
from datetime import datetime, timedelta
import sqlite3
import json

class Club:
    def __init__(self, nom, emplacement, entraineur, logo, surnom = None):
        self._nom = nom
        self._emplacement = emplacement
        self._entraineur = entraineur
        self.logo = logo
        self.surnom = surnom
        self.statistique = Statistiques()

    def __str__(self):
        return self.nom

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        self._nom = value

    @property
    def emplacement(self):
        return self._emplacement

    @emplacement.setter
    def emplacement(self, value):
        self._emplacement = value

    @property
    def entraineur(self):
        return self._entraineur

    @entraineur.setter
    def entraineur(self, value):
        self._entraineur = value

    def afficher_statistiques_club(self):
        print(f"Statistiques pour le club {self.nom}:")
        print(f"Nombre de matchs joués: {self.statistique.matchs_joues}")
        print(f"Matchs score: {self.statistique.score}")
        print(f"Victoires à domicile: {self.statistique.victoires_domicile}")
        print(f"Victoires à l'extérieur: {self.statistique.victoires_exterieur}")
        print(f"Matchs nuls: {self.statistique.matchs_nuls}")
        print(f"Goal Average: {self.statistique.goal_average}")

class Match:
    def __init__(self, equipe_domicile, equipe_exterieur):
        self._equipe_domicile = equipe_domicile
        self._equipe_exterieur = equipe_exterieur
        self._resultat = None
        self.date = None

    def __str__(self):
        date_str = self.date.strftime("%d/%m/%Y") if self.date else "Date non définie"
        return f"Match: {self._equipe_domicile} VS {self._equipe_exterieur}, résultat: {self._resultat}, date: {date_str}"

    @property
    def equipe_domicile(self):
        return self._equipe_domicile

    @property
    def equipe_exterieur(self):
        return self._equipe_exterieur

    @property
    def resultat(self):
        return self._resultat

    def jouer_match(self, resultat):
        self._resultat = resultat
        difference_goals = resultat[0] - resultat[1]
        if resultat[0] > resultat[1]:
            self.equipe_domicile.statistique.incrementer_victoires_domicile()
            self.equipe_exterieur.statistique.incrementer_defaites()

        elif resultat[0] < resultat[1]:
            self.equipe_exterieur.statistique.incrementer_victoires_exterieur()
            self.equipe_domicile.statistique.incrementer_defaites()

        else:
            self.equipe_exterieur.statistique.incrementer_matchs_nuls()
            self.equipe_domicile.statistique.incrementer_matchs_nuls()
        self.equipe_domicile.statistique.mettre_a_jour_goal_average(difference_goals)
        self.equipe_exterieur.statistique.mettre_a_jour_goal_average(-difference_goals)
        # Incrementer le nombre de matchs joués pour les deux équipes
        self.equipe_domicile.statistique.incrementer_matchs_joues()
        self.equipe_exterieur.statistique.incrementer_matchs_joues()


class Tour:
    def __init__(self, numero):
        self._numero = numero
        self._matchs = []

    def __str__(self):
        return f"Tour numéro {self._numero}, matchs: {' | '.join(map(str, self._matchs))}"

    @property
    def numero(self):
        return self._numero
    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def matchs(self):
        return self._matchs

    def ajouter_match(self, match):
        self._matchs.append(match)


class ImportExport():
    def __init__(self):
        pass
    
    def creer_tables(self, db_filename="championnat.db"):
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS championnat (
            nom TEXT,
            date_debut TEXT,
            PRIMARY KEY (nom, date_debut)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS club (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            emplacement TEXT,
            entraineur TEXT,
            logo TEXT,
            surnom TEXT,
            championnat_nom TEXT,
            championnat_date_debut TEXT,
            FOREIGN KEY (championnat_nom, championnat_date_debut) REFERENCES championnat (nom, date_debut)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS statistiques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id INTEGER,
            victoires_domicile INTEGER,
            victoires_exterieur INTEGER,
            matchs_nuls INTEGER,
            defaites INTEGER,
            score INTEGER,
            goal_average INTEGER,
            matchs_joues INTEGER,
            FOREIGN KEY (club_id) REFERENCES club (id)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS tour (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER,
            championnat_nom TEXT,
            championnat_date_debut TEXT,
            FOREIGN KEY (championnat_nom, championnat_date_debut) REFERENCES championnat (nom, date_debut)
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS match (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipe_domicile_id INTEGER,
            equipe_exterieur_id INTEGER,
            resultat_domicile INTEGER,
            resultat_exterieur INTEGER,
            date TEXT,
            tour_id INTEGER,
            FOREIGN KEY (equipe_domicile_id) REFERENCES club (id),
            FOREIGN KEY (equipe_exterieur_id) REFERENCES club (id),
            FOREIGN KEY (tour_id) REFERENCES tour (id)
        )''')

        conn.commit()
        conn.close()

    def exporter_championnat_bd(self, championnat, db_filename="championnat.db"):
        self.championnat = championnat
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Insérer le championnat
        cursor.execute("INSERT INTO championnat (nom, date_debut) VALUES (?, ?)", (self.championnat.nom, self.championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))

        # Insérer les clubs et leurs statistiques
        club_ids = {}
        for club in self.championnat.participants:
            cursor.execute(
                "INSERT INTO club (nom, emplacement, entraineur, logo, surnom, championnat_nom, championnat_date_debut) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (club.nom, club.emplacement, club.entraineur, club.logo, club.surnom, self.championnat.nom, self.championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S"))
            )
            club_id = cursor.lastrowid
            club_ids[club.nom] = club_id
            cursor.execute(
                "INSERT INTO statistiques (club_id, victoires_domicile, victoires_exterieur, matchs_nuls, defaites, score, goal_average, matchs_joues) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    club_id,
                    club.statistique.victoires_domicile,
                    club.statistique.victoires_exterieur,
                    club.statistique.matchs_nuls,
                    club.statistique.defaites,
                    club.statistique.score,
                    club.statistique.goal_average,
                    club.statistique.matchs_joues
                )
            )

        # Insérer les tours et les matchs
        for tour in self.championnat.tours:
            cursor.execute("INSERT INTO tour (numero, championnat_nom, championnat_date_debut) VALUES (?, ?, ?)", (tour.numero, self.championnat.nom, self.championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))
            tour_id = cursor.lastrowid
            for match in tour.matchs:
                resultat_domicile, resultat_exterieur = match.resultat if match.resultat else (None, None)
                cursor.execute(
                    "INSERT INTO match (equipe_domicile_id, equipe_exterieur_id, resultat_domicile, resultat_exterieur, date, tour_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (
                        club_ids[match.equipe_domicile.nom],
                        club_ids[match.equipe_exterieur.nom],
                        resultat_domicile,
                        resultat_exterieur,
                        match.date.strftime("%Y-%m-%d") if match.date else None,
                        tour_id
                    )
                )

        conn.commit()
        conn.close()


    def exporter_championnat_json(self,championnat, filename):
        self.championnat = championnat
        championnat_data = {
            "nom": self.championnat.nom,
            "date_debut": self.championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S"),
            "participants": [
                {
                    "nom": club.nom,
                    "emplacement": club.emplacement,
                    "entraineur": club.entraineur,
                    "logo": club.logo,
                    "surnom": club.surnom,
                    "statistiques": {
                        "victoires_domicile": club.statistique.victoires_domicile,
                        "victoires_exterieur": club.statistique.victoires_exterieur,
                        "matchs_nuls": club.statistique.matchs_nuls,
                        "defaites": club.statistique.defaites,
                        "score": club.statistique.score,
                        "goal_average": club.statistique.goal_average,
                        "matchs_joues": club.statistique.matchs_joues
                    }
                }
                for club in self.championnat.participants
            ],
            "tours": [
                {
                    "numero": tour.numero,
                    "matchs": [
                        {
                            "equipe_domicile": match.equipe_domicile.nom,
                            "equipe_exterieur": match.equipe_exterieur.nom,
                            "resultat": match.resultat,
                            "date": match.date.strftime("%Y-%m-%d") if match.date else None
                        }
                        for match in tour.matchs
                    ]
                }
                for tour in self.championnat.tours
            ]
        }

        with open(filename, 'w') as file:
            json.dump(championnat_data, file, indent=4, ensure_ascii=False)

    def importer_championnat_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)

        self.championnat = Championnat(None)
        self.championnat._nom = data["nom"]
        self.championnat.date_debut = datetime.strptime(data["date_debut"], "%Y-%m-%d %H:%M:%S")

        # Réinitialiser les participants et les tours actuels
        self.championnat._participants = []
        self.championnat._tours = []

        # Importer les participants
        for club_data in data["participants"]:
            club = Club(
                nom=club_data["nom"],
                emplacement=club_data["emplacement"],
                entraineur=club_data["entraineur"],
                logo=club_data["logo"],
                surnom=club_data["surnom"]
            )
            club.statistique = Statistiques()
            club.statistique._victoires_domicile = club_data["statistiques"]["victoires_domicile"]
            club.statistique._victoires_exterieur = club_data["statistiques"]["victoires_exterieur"]
            club.statistique._matchs_nuls = club_data["statistiques"]["matchs_nuls"]
            club.statistique._defaites = club_data["statistiques"]["defaites"]
            club.statistique._score = club_data["statistiques"]["score"]
            club.statistique._goal_average = club_data["statistiques"]["goal_average"]
            club.statistique._matchs_joues = club_data["statistiques"]["matchs_joues"]
            self.championnat.ajouter_participant(club)

        # Dictionnaire pour retrouver les clubs par leur nom
        clubs_by_nom = {club.nom: club for club in self.championnat._participants}

        # Importer les tours et les matchs
        for tour_data in data["tours"]:
            tour = Tour(tour_data["numero"])
            for match_data in tour_data["matchs"]:
                equipe_domicile = clubs_by_nom[match_data["equipe_domicile"]]
                equipe_exterieur = clubs_by_nom[match_data["equipe_exterieur"]]
                match = Match(equipe_domicile, equipe_exterieur)
                match._resultat = match_data["resultat"]
                match.date = datetime.strptime(match_data["date"], "%Y-%m-%d") if match_data["date"] else None
                tour.ajouter_match(match)
            self.championnat.ajouter_tour(tour)

        return self.championnat
    


    def importer_championnat_db(self, championnat, db_filename="championnat.db"):
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Vérifier si le championnat existe déjà
        cursor.execute("SELECT * FROM championnat WHERE nom = ? AND date_debut = ?", (championnat.nom, championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))
        exists = cursor.fetchone()

        if exists:
            conn.close()
            return False

        # Insérer le championnat
        self.exporter_championnat_bd(championnat, db_filename)

        conn.close()
        return True

    def update_championnat_db(self, championnat, db_filename="championnat.db"):
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        # Vérifier si le championnat existe déjà
        cursor.execute("SELECT * FROM championnat WHERE nom = ? AND date_debut = ?", (championnat.nom, championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))
        exists = cursor.fetchone()

        if not exists:
            conn.close()
            return False

        # Supprimer le championnat existant
        cursor.execute("DELETE FROM match WHERE tour_id IN (SELECT id FROM tour WHERE championnat_nom = ? AND championnat_date_debut = ?)", (championnat.nom, championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))
        cursor.execute("DELETE FROM tour WHERE championnat_nom = ? AND championnat_date_debut = ?", (championnat.nom, championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))
        cursor.execute("DELETE FROM statistiques WHERE club_id IN (SELECT id FROM club WHERE championnat_nom = ? AND championnat_date_debut = ?)", (championnat.nom, championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))
        cursor.execute("DELETE FROM club WHERE championnat_nom = ? AND championnat_date_debut = ?", (championnat.nom, championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))
        cursor.execute("DELETE FROM championnat WHERE nom = ? AND date_debut = ?", (championnat.nom, championnat.date_debut.strftime("%Y-%m-%d %H:%M:%S")))

        # Insérer les nouvelles données du championnat
        self.exporter_championnat_bd(championnat, db_filename)

        conn.close()
        return True

class Championnat:
    def __init__(self, nom, date = datetime(2024, 9, 1, 20)):
        self._nom = nom
        self._participants = []
        self._tours = []
        self.date_debut = date

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        self._nom = value

    @property
    def participants(self):
        return self._participants

    def ajouter_participant(self, participant):
        self._participants.append(participant)

    @property
    def tours(self):
        return self._tours

    def ajouter_tour(self, tour):
        self._tours.append(tour)

    def generer_calendrier(self):
        all_teams = self._participants[:]
        num_teams = len(all_teams)
        feuille_matchs_aller = []
        current_date = self.date_debut
        for j in range(num_teams - 1):
            tour = Tour(j + 1)
            for i in range(num_teams // 2):
                match = Match(all_teams[i], all_teams[num_teams - i - 1])
                tour.ajouter_match(match)
            feuille_matchs_aller.append(tour)
            #self.ajouter_tour(tour)
            all_teams.insert(1, all_teams.pop())

        feuille_matchs_retour = []
        nb_tours = len(feuille_matchs_aller)
        for tour in feuille_matchs_aller:
            nouveau_tour = Tour(tour.numero + nb_tours)
            for match in tour.matchs:
                match_retour = Match(match.equipe_exterieur, match.equipe_domicile)
                nouveau_tour.ajouter_match(match_retour)
            feuille_matchs_retour.append(nouveau_tour)

        feuille_matchs = feuille_matchs_aller + feuille_matchs_retour
        feuille_matchs = transform_list(feuille_matchs)

        for t in range(len(feuille_matchs)):
            feuille_matchs[t].numero = t + 1
        # Ajouter les tours retour au championnat
        for tour in feuille_matchs:
            for match in tour.matchs:
                match.date=current_date
            self.ajouter_tour(tour)
            current_date += timedelta(days=7)

    def jouer_tour(self, resultats):
        print("Tour", tour.numero)
        i=0
        for match in tour.matchs:
            # Simuler les scores aléatoires
            score_equipe_domicile = resultats[i][0]
            score_equipe_exterieur = resultats[i][1]

            # Jouer le match
            match.jouer_match((score_equipe_domicile, score_equipe_exterieur))
            match.date = datetime.now() + timedelta(days=1)
            i+=1
            # Afficher le match avec les résultats simulés
            print(match.equipe_domicile.nom, score_equipe_domicile, "-", score_equipe_exterieur,
                  match.equipe_exterieur.nom)


    def classement(self):
        # Calculer le score de championnat, goal average et nombre de victoires pour chaque club
        scores_clubs = {}
        for club in self.participants:
            score = club.statistique.score
            goal_average = club.statistique.goal_average
            victoires = club.statistique.victoires_domicile + club.statistique.victoires_exterieur
            scores_clubs[club] = (score, goal_average, victoires)

        # Trier les clubs en fonction de leur score, goal average et nombre de victoires
        classement = sorted(scores_clubs.items(), key=lambda x: (x[1][0], x[1][1], x[1][2]), reverse=True)

        return classement

    def reset_calendrier(self):
        self._tours = []

    def supprimer_club(self, club):
        if club in self._participants:
            self._participants.remove(club)
            self.reset_calendrier()
        else:
            print(f"Le club {club.nom} n'est pas un participant du championnat.")

    

class Statistiques:
    def __init__(self):
        self._victoires_domicile = 0
        self._victoires_exterieur = 0
        self._matchs_nuls = 0
        self._defaites = 0
        self._score = 0
        self._goal_average = 0
        self._matchs_joues = 0
        self.historique = []
        self.classement = None

    @property
    def matchs_joues(self):
        return self._matchs_joues

    def incrementer_matchs_joues(self):
        self._matchs_joues += 1

    @property
    def victoires_domicile(self):
        return self._victoires_domicile

    def incrementer_victoires_domicile(self):
        self._victoires_domicile += 1
        self._score += 3

    @property
    def victoires_exterieur(self):
        return self._victoires_exterieur

    def incrementer_victoires_exterieur(self):
        self._victoires_exterieur += 1
        self._score += 3

    @property
    def matchs_nuls(self):
        return self._matchs_nuls

    def incrementer_matchs_nuls(self):
        self._matchs_nuls += 1
        self._score += 1

    @property
    def defaites(self):
        return self._defaites

    def incrementer_defaites(self):
        self._defaites += 1

    @property
    def score(self):
        return self._score

    @property
    def goal_average(self):
        return self._goal_average

    def mettre_a_jour_goal_average(self, difference_goals):
        self._goal_average += difference_goals

    def historique_tour_par_tour(self):
        self.historique.append((self.classement, self.score))


if __name__ == "__main__":

    # Création d'une instance de Championnat
    championnat = Championnat("Ligue 1")

    # Ajout de participants au championnat
    clubs = [
        Club("Paris Saint-Germain", "Paris", "Lucas Lefevre", "logo_club1.png", "PSG"),
        Club("Olympique de Marseille", "Marseille", "Jorge Sampaoli", "logo_club2.png", "OM"),
        Club("AS Monaco", "Monaco", "Niko Kovač", "logo_club3.png", "ASM"),
        Club("Stade Brestois", "Brest", "Quentin Dutailly", "logo_club4.png", "SB29"),
        Club("Lille OSC", "Lille", "Christophe Galtier", "logo_club5.png", "LOSC"),
        Club("Olympique Lyonnais", "Lyon", "Rudi Garcia", "logo_club6.png", "OL"),
        Club("Stade Rennais FC", "Rennes", "Kilian Barantal", "logo_club7.png", "SRFC"),
        Club("RC Lens", "Lens", "Franck Haise", "logo_club8.png", "RCL"),
        Club("Stade de Reims", "Reims", "David Guion", "logo_club9.png", "SDR"),
        Club("OGC Nice", "Nice", "Adrian Ursea", "logo_club10.png", "OGCN"),
        Club("Montpellier HSC", "Montpellier", "Michel Der Zakarian", "logo_club11.png", "MHSC"),
        Club("Angers SCO", "Angers", "Gérald Baticle", "logo_club12.png", "SCO"),
        Club("FC Metz", "Metz", "Frédéric Antonetti", "logo_club13.png", "FCM"),
        Club("RC Strasbourg Alsace", "Strasbourg", "Thierry Laurey", "logo_club14.png", "RCSA"),
        Club("FC Nantes", "Nantes", "Antoine Kombouaré", "logo_club15.png", "FCN"),
        Club("Dijon FCO", "Dijon", "David Linarès", "logo_club16.png", "DFCO")
    ]

    for club in clubs:
        championnat.ajouter_participant(club)

    # Génération du calendrier
    championnat.generer_calendrier()

    for tour in championnat.tours:
        print("\n")
        print("Tour", tour.numero)
        resultats = [(random.randint(0, 5),random.randint(0, 5)) for _ in tour.matchs]
        championnat.jouer_tour(resultats)
        print()

    # Exporter le championnat dans la base de données
    championnat.exporter_championnat_bd("championnat.db")

    # Exporter les données du championnat
    championnat.exporter_championnat_json("championnat.json")

    # Importer les données du championnat
    nouveau_championnat = Championnat("Ligue 1")
    nouveau_championnat.importer_championnat_json("championnat.json")

    # Afficher les informations importées pour vérifier
    print("\nStatistiques des clubs importés:")
    for club in nouveau_championnat.participants:
        print("\n")
        club.afficher_statistiques_club()

    print("\nClassement des clubs importés:")
    classement_nouveau_championnat = nouveau_championnat.classement()
    for i, (club, _) in enumerate(classement_nouveau_championnat, 1):
        print(
            f"{i}. {club.nom} - Victoires : {club.statistique.victoires_domicile + club.statistique.victoires_exterieur} - Nuls : {club.statistique.matchs_nuls} - Défaites : {club.statistique.defaites} - Score : {club.statistique.score} - Goalaverage : {club.statistique.goal_average}")
