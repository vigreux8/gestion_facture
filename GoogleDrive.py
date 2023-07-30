from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Setting.CONSTANTE import GOOGLE_AUTH
from os import path
from Setting.CONSTANTE import *


class MrDrive:
    def __init__(self) -> None:
        self.key_connexion = None
        self.drive = None
        self.init_connexion_api()

    def init_connexion_api(self):
        key_connecte_google_drive = GoogleAuth()
        key_connecte_google_drive.settings['client_config_file'] = (GOOGLE_AUTH.KEY_AUTH_OAUTH)
        key_connecte_google_drive.LoadCredentialsFile(GOOGLE_AUTH.TOKEN_REFRESH)

        # Si les informations d'identification ne sont pas valides, lancez le processus d'authentification
        if key_connecte_google_drive.credentials is None:
            # Il s'agit de la première exécution, ou les informations d'identification ont expiré
            key_connecte_google_drive.LocalWebserverAuth()
        elif key_connecte_google_drive.access_token_expired:
            # Les informations d'identification ont expiré, mais le refresh token permet de les renouveler automatiquement
            key_connecte_google_drive.Refresh()
        else:
            # Les informations d'identification sont valides
            key_connecte_google_drive.Authorize()

        # Enregistrez les informations d'identification dans le fichier de token
        key_connecte_google_drive.SaveCredentialsFile(GOOGLE_AUTH.TOKEN_REFRESH)
        self.key_connexion = key_connecte_google_drive
        self.drive = GoogleDrive(key_connecte_google_drive)








#formater le nom selon l'information

# recuperer et decomposer le nom du fichier
def get_all_file_folder_formater(patch_dossier = FOLDER.FACTURE_TRAITER):
    all_facture_id_name_chem = []
    for nom_fichier in os.listdir(patch_dossier):
        if os.path.isfile(os.path.join(patch_dossier, nom_fichier)):
            id_facture = nom_fichier.split("_")[1].split(".")[0]
            all_facture_id_name_chem.append({"id":id_facture,
                                          "name":nom_fichier,
                                          "path" : os.path.join(patch_dossier,nom_fichier)})
    return all_facture_id_name_chem

list_factures_non_traiter = get_all_file_folder_formater(FOLDER.FACTURE_PAS_TRAITER)
        
#upload la facture sur googledrive
google_drive = MrDrive().drive
for facture in list_factures_non_traiter : 
    facture_traiter = google_drive.CreateFile(
    {
    'parents': [{'id': GOOGLEDRIVE.ID_DOSSIER_FACTURE_TRAITER}],
    "title" : facture["id"]
    })
    facture_traiter.SetContentFile(facture["path"])
    facture_traiter.Upload()