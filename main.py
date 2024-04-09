from itertools import combinations
import random

class Club:
    def __init__(self, nom, emplacement, entraineur):
        self._nom = nom
        self._emplacement = emplacement
        self._entraineur = entraineur
        self.statistique = Statistiques()

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
            self.equipe_domicile.statistique.mettre_a_jour_goal_average(difference_goals)
        elif resultat[0] < resultat[1]:
            self.equipe_exterieur.statistique.incrementer_victoires_exterieur()
            self.equipe_exterieur.statistique.mettre_a_jour_goal_average(-difference_goals)
        else:
            self.equipe_exterieur.statistique.incrementer_matchs_nuls()
            self.equipe_domicile.statistique.incrementer_matchs_nuls()


class Tour:
    def __init__(self, numero):
        self._numero = numero
        self._matchs = []

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


class Championnat:
    def __init__(self, nom):
        self._nom = nom
        self._participants = []
        self._tours = []

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

        for _ in range(num_teams - 1):
            tour = Tour(len(self._tours) + 1)
            for i in range(num_teams // 2):
                match = Match(all_teams[i], all_teams[num_teams - i - 1])
                tour.ajouter_match(match)
            self.ajouter_tour(tour)
            all_teams.insert(1, all_teams.pop())

        feuille_matchs_retour = []
        nb_tours = len(self._tours)
        for tour in self._tours:
            nouveau_tour = Tour(tour.numero + nb_tours)
            for match in tour.matchs:
                match_retour = Match(match.equipe_exterieur, match.equipe_domicile)
                nouveau_tour.ajouter_match(match_retour)
            feuille_matchs_retour.append(nouveau_tour)

        # Ajouter les tours retour au championnat
        for tour in feuille_matchs_retour:
            self.ajouter_tour(tour)



class Statistiques:
    def __init__(self):
        self._victoires_domicile = 0
        self._victoires_exterieur = 0
        self._matchs_nuls = 0
        self._score = 0
        self._goal_average = 0

    @property
    def victoires_domicile(self):
        return self._victoires_domicile

    def incrementer_victoires_domicile(self):
        self._victoires_domicile += 1
        self._score +=3

    @property
    def victoires_exterieur(self):
        return self._victoires_exterieur

    def incrementer_victoires_exterieur(self):
        self._victoires_exterieur += 1
        self._score +=3

    @property
    def matchs_nuls(self):
        return self._matchs_nuls
    
    @property
    def score(self):
        return self._score

    def incrementer_matchs_nuls(self):
        self._matchs_nuls += 1
        self._score += 1

    @property
    def goal_average(self):
        return self._goal_average

    def mettre_a_jour_goal_average(self, difference_goals):
        self._goal_average += difference_goals




if __name__ == "__main__":
    # Création d'une instance de Championnat
    championnat = Championnat("Ligue 1")

    # Ajout de participants au championnat
    clubs = [
        Club("Paris Saint-Germain", "Paris", "Mauricio Pochettino"),
        Club("Olympique de Marseille", "Marseille", "Jorge Sampaoli"),
        Club("AS Monaco", "Monaco", "Niko Kovač"),
        Club("FC EnstApagnan", "Brest", "Quentin Dutailly"),
        Club("Lille OSC", "Lille", "Christophe Galtier"),
        Club("Olympique Lyonnais", "Lyon", "Rudi Garcia"),
        Club("Stade Rennais FC", "Rennes", "Kilian Barantal"),
        Club("RC Lens", "Lens", "Franck Haise"),
        Club("Stade de Reims", "Reims", "David Guion"),
        Club("OGC Nice", "Nice", "Adrian Ursea"),
        Club("Montpellier HSC", "Montpellier", "Michel Der Zakarian"),
        Club("Angers SCO", "Angers", "Gérald Baticle"),
        Club("FC Metz", "Metz", "Frédéric Antonetti"),
        Club("RC Strasbourg Alsace", "Strasbourg", "Thierry Laurey"),
        Club("FC Nantes", "Nantes", "Antoine Kombouaré"),
        Club("Dijon FCO", "Dijon", "David Linarès")
    ]

    for club in clubs:
        championnat.ajouter_participant(club)

    # Génération du calendrier
    championnat.generer_calendrier()

    for tour in championnat.tours:
        print("\n")
        print("Tour", tour.numero)
        for match in tour.matchs:
            # Simuler les scores aléatoires
            score_equipe_domicile = random.randint(0, 5)
            score_equipe_exterieur = random.randint(0, 5)
            
            # Jouer le match
            match.jouer_match((score_equipe_domicile, score_equipe_exterieur))

            # Afficher le match avec les résultats simulés
            print(match.equipe_domicile.nom, score_equipe_domicile, "-", score_equipe_exterieur, match.equipe_exterieur.nom)

    print("\nStatistiques des clubs:")
    for club in championnat.participants:
        print("\n")
        club.afficher_statistiques_club()

    # Calculer le score de championnat de chaque club
    scores_clubs = {}
    for club in championnat.participants:
        score = club.statistique.score
        scores_clubs[club] = score

    # Trier les clubs en fonction de leur score
    classement = sorted(scores_clubs.items(), key=lambda x: x[1], reverse=True)

    # Afficher le classement de chaque équipe
    print("\nClassement des clubs:")
    for i, (club, score) in enumerate(classement, 1):
        print(f"{i}. {club.nom} - Score : {score}")
