import os

class FOLDER():
    DOSSIER_FACTURE = "facture"
    AMAZON = os.path.join(".",DOSSIER_FACTURE,"amazon")
    AMAZON_PRIME = os.path.join(".",DOSSIER_FACTURE,"amazon_prime")
    FACTURE_PAS_TRAITER = os.path.join(".",DOSSIER_FACTURE,"pas traiter")
    FACTURE_TRAITER = os.path.join(".",DOSSIER_FACTURE,"traiter")
    

class GOOGLE_AUTH():
    DOSSIER ="google-api-identifiant"
    KEY_MAILS_AUTH = os.path.join(DOSSIER,"service_account.json")
    KEY_AUTH_OAUTH = os.path.join(DOSSIER,"client_secrets.json")
    TOKEN_REFRESH = os.path.join(DOSSIER,"token_refresh.json")
    
class GOOGLESHEET():
    SHEET_OPEN = "test script python"
    FACTURE = "facture_obh_test" 
    
    
class GOOGLEDRIVE():
    ID_DOSSIER_FACTURE_TRAITER = "1y27_FsNR0PRaxNz564CI27L_jK1sZnFp"
    ID_DOSSIER_FACTURE_INCONNUE = "1xrYm-Wo_8jpvbfo3srmdMdsds1mptfXL"