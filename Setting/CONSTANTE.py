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
    
class OPTION_SHEET:
    POSITION_NOM_COLONNE = 1
    
class OPTION_LOCAL:
    SEPARATEUR = "_"

class FOLDER_LOCAL():
    DOSSIER_FACTURE = "facture"
    DOSSIER_CONTENUE_PDF = "ContenuePdf"
    DOSSIER_MODEL_FACTURE = "model_facture"
    AMAZON = os.path.join(".",DOSSIER_FACTURE,"amazon")
    AMAZON_PRIME = os.path.join(".",DOSSIER_FACTURE,"amazon_prime")
    FACTURE_PAS_TRAITER = os.path.join(".",DOSSIER_FACTURE,"pas traiter")
    FACTURE_ARCHIVER = os.path.join(".",DOSSIER_FACTURE,"archiver")
    FACTURE_INFO_MANQUANTE= os.path.join(".",DOSSIER_FACTURE,"info_manquante")
    FACTURE_INCONNUE= os.path.join(".",DOSSIER_FACTURE,"inconnue")
    MODEL_FACTURE = os.path.join(".",DOSSIER_MODEL_FACTURE)
    PROMPT_GPT = os.path.join(".",DOSSIER_CONTENUE_PDF,"prompt_gpt")
    
    

class GOOGLE_AUTH():
    DOSSIER ="google-api-identifiant"
    KEY_MAILS_AUTH = os.path.join(DOSSIER,"service_account.json")
    KEY_AUTH_OAUTH = os.path.join(DOSSIER,"client_secrets.json")
    KEY_TOKEN_REFRESH = os.path.join(DOSSIER,"token_refresh.json")
    
class FOLDER_GOOGLESHEET():
    SHEET_OPEN = "test script python"
    FACTURE = "facture_obh_test" 
    
    
class FOLDER_GOOGLEDRIVE():
    ID_DOSSIER_FACTURE_ARCHIVER = "1y27_FsNR0PRaxNz564CI27L_jK1sZnFp"
    ID_DOSSIER_FACTURE_INCONNUE = "1xrYm-Wo_8jpvbfo3srmdMdsds1mptfXL"
    ID_DOSSIER_FACTURE_TAMPON = "1TznVt-En12t2TEmU0NDsUxJ8k6G2tUv4"
    ID_DOSSIER_FACTURE_DONNER_MANQUANTE = "17liWRmuGIvEHtHS6cJT__MGVmJ1PYcvK"
    
class KEY_INFOMRATION():
    CONTROLLER = "controller"
    DATE ="date"
    TTC = "ttc"
    URL = "url"
    RAISON = "raison"
    PROVENANCE = "provenance"
    PERSONNE = "personne"
    REMBOURSER = "rembourser"

class MOIS_TRADUCTION():
    MOIS_TRADUCTION_FR_TO_ANGLAIS = {
    "janvier": "january",
    "février": "february",
    "mars": "march",
    "avril": "april",
    "mai": "may",
    "juin": "june",
    "juillet": "july",
    "août": "august",
    "septembre": "september",
    "octobre": "october",
    "novembre": "november",
    "décembre": "december"
}