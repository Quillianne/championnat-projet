import unittest
from main import Club, Match, Tour, Championnat, Statistiques

class TestStatistiques(unittest.TestCase):
    def test_incrementer_matchs_joues(self):
        stats = Statistiques()
        stats.incrementer_matchs_joues()
        self.assertEqual(stats.matchs_joues, 1)

    def test_incrementer_victoires_domicile(self):
        stats = Statistiques()
        stats.incrementer_victoires_domicile()
        self.assertEqual(stats.victoires_domicile, 1)
        self.assertEqual(stats.score, 3)

    def test_incrementer_victoires_exterieur(self):
        stats = Statistiques()
        stats.incrementer_victoires_exterieur()
        self.assertEqual(stats.victoires_exterieur, 1)
        self.assertEqual(stats.score, 3)

    def test_incrementer_matchs_nuls(self):
        stats = Statistiques()
        stats.incrementer_matchs_nuls()
        self.assertEqual(stats.matchs_nuls, 1)
        self.assertEqual(stats.score, 1)

    def test_mettre_a_jour_goal_average(self):
        stats = Statistiques()
        stats.mettre_a_jour_goal_average(2)
        self.assertEqual(stats.goal_average, 2)

    def test_incrementer_defaites(self):
        stats = Statistiques()
        stats.incrementer_defaites()
        self.assertEqual(stats.defaites, 1)

class TestMatch(unittest.TestCase):
    def test_jouer_match_victoire_domicile(self):
        club_domicile = Club("Club A", "Lieu A", "Entraineur A", "logo_A")
        club_exterieur = Club("Club B", "Lieu B", "Entraineur B", "logo_B")
        match = Match(club_domicile, club_exterieur)
        match.jouer_match((2, 1))
        self.assertEqual(club_domicile.statistique.victoires_domicile, 1)
        self.assertEqual(club_exterieur.statistique.defaites, 1)
        self.assertEqual(club_domicile.statistique.score, 3)

    def test_jouer_match_victoire_exterieur(self):
        club_domicile = Club("Club A", "Lieu A", "Entraineur A", "logo_A")
        club_exterieur = Club("Club B", "Lieu B", "Entraineur B", "logo_B")
        match = Match(club_domicile, club_exterieur)
        match.jouer_match((1, 2))
        self.assertEqual(club_exterieur.statistique.victoires_exterieur, 1)
        self.assertEqual(club_domicile.statistique.defaites, 1)
        self.assertEqual(club_exterieur.statistique.score, 3)

class TestTour(unittest.TestCase):
    def test_ajouter_match(self):
        tour = Tour(1)
        club_domicile = Club("Club A", "Lieu A", "Entraineur A", "logo_A")
        club_exterieur = Club("Club B", "Lieu B", "Entraineur B", "logo_B")
        match = Match(club_domicile, club_exterieur)
        tour.ajouter_match(match)
        self.assertEqual(len(tour.matchs), 1)

    def test_numero_tour(self):
        tour = Tour(5)
        self.assertEqual(tour.numero, 5)

class TestChampionnat(unittest.TestCase):
    def test_ajouter_participant(self):
        championnat = Championnat("Championnat A")
        club = Club("Club A", "Lieu A", "Entraineur A", "logo_A")
        championnat.ajouter_participant(club)
        self.assertEqual(len(championnat.participants), 1)

    def test_generer_calendrier(self):
        championnat = Championnat("Championnat A")
        club_a = Club("Club A", "Lieu A", "Entraineur A", "logo_A")
        club_b = Club("Club B", "Lieu B", "Entraineur B", "logo_B")
        championnat.ajouter_participant(club_a)
        championnat.ajouter_participant(club_b)
        championnat.generer_calendrier()
        self.assertEqual(len(championnat.tours), 2)

    def test_classement(self):
        championnat = Championnat("Championnat A")
        club_a = Club("Club A", "Lieu A", "Entraineur A", "logo_A")
        club_b = Club("Club B", "Lieu B", "Entraineur B", "logo_B")
        championnat.ajouter_participant(club_a)
        championnat.ajouter_participant(club_b)
        championnat.generer_calendrier()

        # Simulation de quelques matchs pour obtenir un classement
        match_1 = Match(club_a, club_b)
        match_1.jouer_match((2, 1))
        match_2 = Match(club_b, club_a)
        match_2.jouer_match((1, 1))
        
        classement = championnat.classement()
        self.assertEqual(classement[0][0], club_a)
        self.assertEqual(classement[1][0], club_b)

if __name__ == '__main__':
    unittest.main()
