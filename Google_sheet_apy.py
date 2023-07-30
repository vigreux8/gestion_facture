import gspread
from  Setting.CONSTANTE import GOOGLE_AUTH,FOLDER_GOOGLESHEET


compte = gspread.service_account(GOOGLE_AUTH.KEY_MAILS_AUTH)
document_spreeshit =  compte.open(FOLDER_GOOGLESHEET.SHEET_OPEN)
feuille1 = document_spreeshit.worksheet("Feuille1")
correspondance_index_to_letter = {
    1:"a",
    2:"b",
    3:"c",
    4:"d",
    5:"e",
    6:"f",
    7:"h"
        
}

def get_last_value_col(colonne:str = "a"):
    index_ligne = len(feuille1.col_values(1)) 
    dernier_valeur = int(feuille1.acell(f"{colonne}{index_ligne}").value)
    return index_ligne,dernier_valeur

def set_lettre_associer_au_nom_colonne(ligne: int=1):
    all_name_colonnes = feuille1.row_values(1)
    # all_colonnes_and_lettres = []
    all_colonnes_and_lettres = {}
    
    
    index = 1
    for name_colonne in all_name_colonnes:
        # all_colonnes_and_lettres.append((correspondance_index_to_letter[index],name_colonne))
        all_colonnes_and_lettres[correspondance_index_to_letter[index]] = name_colonne
        index +=1
    return all_colonnes_and_lettres
    
def set_last_value_incrementale(colonne:str = "a"):
    index_ligne,dernier_valeur = get_last_value_col(colonne)
    feuille1.update(f"{colonne}{index_ligne+1}",dernier_valeur+1)


