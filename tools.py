import sqlite3

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


import sqlite3


def creer_tables(db_filename):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS championnat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        date_debut TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS club (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        emplacement TEXT,
        entraineur TEXT,
        logo TEXT,
        surnom TEXT,
        championnat_id INTEGER,
        FOREIGN KEY (championnat_id) REFERENCES championnat (id)
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
        championnat_id INTEGER,
        FOREIGN KEY (championnat_id) REFERENCES championnat (id)
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


# Appel de la fonction pour créer les tables


if __name__ == "__main__":
    creer_tables("championnat.db")