import os


class KEY_FACTURE():
    NOM_FICHIER = "name"
    LOCAL_PATH = 'path'
    DATE = 'date'
    PROVENANCE = 'provenance'
    TTC = "ttc"
    ID = 'id'
    ID_GOOGLE = 'google_id'
    URL_GOOGLE = 'google_url'
    ID_FOLDER = 'google_folder_id'
    
class SHEET_OPTION:
    POSITION_NOM_COLONNE = 1
    
    
class OPTION_LOCAL:
    SEPARATEUR = "_"

class FOLDER_LOCAL():
    DOSSIER_FACTURE = "facture"
    DOSSIER_CONTENUE_PDF = "ContenuePdf"
    DOSSIER_MODEL_FACTURE = "model_facture"
    DOSSIER_TEMPLATE_FACTURE = "Template_facture"
    AMAZON = os.path.join(".",DOSSIER_FACTURE,"amazon")
    AMAZON_PRIME = os.path.join(".",DOSSIER_FACTURE,"amazon_prime")
    FACTURE_PAS_TRAITER = os.path.join(".",DOSSIER_FACTURE,"pas traiter")
    FACTURE_ARCHIVER = os.path.join(".",DOSSIER_FACTURE,"archiver")
    FACTURE_INFO_MANQUANTE= os.path.join(".",DOSSIER_FACTURE,"info_manquante")
    FACTURE_INCONNUE= os.path.join(".",DOSSIER_FACTURE,"inconnue")
    MODEL_FACTURE = os.path.join(".",DOSSIER_MODEL_FACTURE)
    PROMPT_GPT = os.path.join(".",DOSSIER_CONTENUE_PDF,"prompt_gpt")
    FACTURE_TEST= os.path.join(".",DOSSIER_FACTURE,"test_facture_uniquement_1_fichier")
    TEMPLATE_MODEL = os.path.join(".",DOSSIER_TEMPLATE_FACTURE,"template_facture_V3.py")
    
    
    

class GOOGLE_AUTH():
    DOSSIER ="google-api-identifiant"
    KEY_MAILS_AUTH = os.path.join(DOSSIER,"service_account.json")
    KEY_AUTH_OAUTH = os.path.join(DOSSIER,"client_secrets.json")
    KEY_TOKEN_REFRESH = os.path.join(DOSSIER,"token_refresh.json")
    
class FOLDER_GOOGLESHEET():
    SHEET_OPEN = "test script python"
    DOCUMENT_SHEET = "OBH_factures" 
    NAME_FEUILLE = "Facture"
    
    
class FOLDER_GOOGLEDRIVE():
    ID_DOSSIER_FACTURE_ARCHIVER = "11vkmYk2sBCt0qNXafgJ_RyLKU5UdpTGF"
    ID_DOSSIER_FACTURE_INCONNUE = "1Mk2nAL9eWWpvyZ55FnjpHhUTjoArRUls"
    ID_DOSSIER_FACTURE_TAMPON = "1srPR_m-nRSEnHQPIzfBvc1BVYsGjeQie"
    ID_DOSSIER_FACTURE_DONNER_MANQUANTE = "1hx2MK-hxmnvlaoguJIPq6EN-Ptwqbzby"
    
class KEY_INFOMRATION():
    CONTROLLER = "controller"
    DATE ="date"
    TTC = "ttc"
    URL = "url"
    RAISON = "raison"
    PROVENANCE = "provenance"
    PERSONNE = "personne"
    REMBOURSER = "rembourser"
    
class ALPHABET:
    #flemme j'ai utiliser gpt pour faire la liste au lieux d'utiliser ord Forgive my
    COLONNE_GOOGLE_SHEETS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
)
class MOIS_TRADUCTION():
    MOIS_TRADUCTION_FR_TO_ANGLAIS = {
    "janvier": "january",
    "février": "february",
    "mars": "march",
    "avril": "april",
    "mai": "may",
    "juin": "june",
    "juillet": "july",
    "juil." : "jul",
    "août": "august",
    "aou" : "AUG",
    "septembre": "september",
    "octobre": "october",
    "novembre": "november",
    "décembre": "december"
}