import sqlite3
import random
import json
from datetime import datetime


def transform_list(lst):
    if len(lst) < 2:
        return lst
    
    # Trouver le point de division de la liste
    mid = len(lst) // 2
    
    # Diviser la liste en deux moitiés
    first_half = lst[:mid]
    second_half = lst[mid:]
    
    # Inverser la deuxième moitié
    second_half.reverse()
    
    # Créer une nouvelle liste pour le résultat
    result = []
    
    # Insérer les éléments de la deuxième moitié entre les éléments de la première moitié
    for i in range(mid):
        result.append(first_half[i])
        if i < len(second_half):
            result.append(second_half[i])
    
    return result




def generate_real_club_data():
    # Liste de clubs avec des noms de clubs et villes réelles
    clubs = [
        {"nom": "Paris Saint-Germain", "ville": "Paris", "entraineur": "Christophe Galtier", "logo": "logo_psg.png", "abbreviation": "PSG"},
        {"nom": "Olympique de Marseille", "ville": "Marseille", "entraineur": "Igor Tudor", "logo": "logo_om.png", "abbreviation": "OM"},
        {"nom": "AS Monaco", "ville": "Monaco", "entraineur": "Philippe Clement", "logo": "logo_asm.png", "abbreviation": "ASM"},
        {"nom": "Stade Brestois", "ville": "Brest", "entraineur": "Michel Der Zakarian", "logo": "logo_sb29.png", "abbreviation": "SB29"},
        {"nom": "Lille OSC", "ville": "Lille", "entraineur": "Paulo Fonseca", "logo": "logo_losc.png", "abbreviation": "LOSC"},
        {"nom": "Olympique Lyonnais", "ville": "Lyon", "entraineur": "Laurent Blanc", "logo": "logo_ol.png", "abbreviation": "OL"},
        {"nom": "Stade Rennais FC", "ville": "Rennes", "entraineur": "Bruno Génésio", "logo": "logo_srf.png", "abbreviation": "SRFC"},
        {"nom": "RC Lens", "ville": "Lens", "entraineur": "Franck Haise", "logo": "logo_rcl.png", "abbreviation": "RCL"},
        {"nom": "Stade de Reims", "ville": "Reims", "entraineur": "Oscar Garcia", "logo": "logo_sdr.png", "abbreviation": "SDR"},
        {"nom": "OGC Nice", "ville": "Nice", "entraineur": "Lucien Favre", "logo": "logo_ogcn.png", "abbreviation": "OGCN"},
        {"nom": "Montpellier HSC", "ville": "Montpellier", "entraineur": "Olivier Dall'Oglio", "logo": "logo_mhsc.png", "abbreviation": "MHSC"},
        {"nom": "Angers SCO", "ville": "Angers", "entraineur": "Gérald Baticle", "logo": "logo_sco.png", "abbreviation": "SCO"},
        {"nom": "FC Metz", "ville": "Metz", "entraineur": "Laszlo Bölöni", "logo": "logo_fcm.png", "abbreviation": "FCM"},
        {"nom": "RC Strasbourg Alsace", "ville": "Strasbourg", "entraineur": "Julien Stéphan", "logo": "logo_rcsa.png", "abbreviation": "RCSA"},
        {"nom": "FC Nantes", "ville": "Nantes", "entraineur": "Antoine Kombouaré", "logo": "logo_fcn.png", "abbreviation": "FCN"},
        {"nom": "Dijon FCO", "ville": "Dijon", "entraineur": "David Linarès", "logo": "logo_dfco.png", "abbreviation": "DFCO"},
        # Ajoutez plus de clubs de Ligue 1, Ligue 2, La Liga, etc.
    ]
    return clubs

def generate_fake_championships(num_championships, num_teams_per_championship):
    all_clubs = generate_real_club_data()
    
    for i in range(num_championships):
        championnat_name = f"Championnat_{i+1}"
        championnat = Championnat(championnat_name)

        selected_clubs = random.sample(all_clubs, num_teams_per_championship)
        
        clubs = [
            Club(club_data["nom"], club_data["ville"], club_data["entraineur"], club_data["logo"], club_data["abbreviation"])
            for club_data in selected_clubs
        ]

        for club in clubs:
            championnat.ajouter_participant(club)

        championnat.generer_calendrier()

        for tour in championnat.tours:
            resultats = [(random.randint(0, 5), random.randint(0, 5)) for _ in tour.matchs]
            championnat.jouer_tour(resultats, tour)

        # Exporter le championnat au format JSON
        file_name = f"{championnat_name}.json"
        ImportExport().exporter_championnat_json(championnat, file_name)

if __name__ == "__main__":
    from main import *
    generate_fake_championships(10, 4)