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