import os

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
    ID_DOSSIER_FACTURE_EN_COURS = "1fbgY3MimnRgRk6MqxTt23AKIqegz7pCC"