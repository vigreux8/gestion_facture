from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Setting.CONSTANTE import GOOGLE_AUTH
from os import path
from Setting.CONSTANTE import *
import shutil
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class MrDrive:
    def __init__(self) -> None:
        self.key_connexion = None
        self.drive = None
        self.facture_info = ({
            "name" : "D01-3598561-0389456",
            "id" : "D01-3598561-0389456",
            "date" : "29/05/2021",
            "ttc" : 12.27,
            "provenance" : "amazon"
        })
        self.init_connexion_api()
        self.local_list_factures_non_traiter = self.local_get_all_file_folder_formater(FOLDER_LOCAL.FACTURE_PAS_TRAITER)
        self.local_list_factures_archiver = self.local_get_all_file_folder_formater(FOLDER_LOCAL.FACTURE_ARCHIVER)
        self.drive_liste_archiver = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_ARCHIVER)
        self.drive_list_factures_INCONNUE = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_INCONNUE)
        self.drive_list_factures_EN_COURS = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_EN_COURS)
        
        
        
    @staticmethod
    def local_move_file_pas_traiter(facture,destination = FOLDER_LOCAL.FACTURE_ARCHIVER):
        facture_path_destination = os.path.join(destination,facture["name"]) 
        if os.path.isfile(facture["path"]):
            shutil.move(facture["path"],facture_path_destination)
        else : 
            print("fichier inexistant")
        pass
    
    def get_all_file_drive_folder(self,id_folder = FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_ARCHIVER ):
        #recuperais tout les dossier present dans le fichier google drive
        drive_liste = []
        file_liste = self.drive.ListFile({'q': f"'{id_folder}' in parents and trashed=false"}).GetList()
        if file_liste:
            for file in file_liste:
                drive_liste.append({
                    "name":file['title'],
                    "id":file['id'],
                    "id_folder": id_folder,
                    "url" : file['alternateLink']
                })
            return drive_liste

    def drive_move_file_to_folder(self,file_id, folder_id):
        """Move specified file to the specified folder.
        Args:
            file_id: Id of the file to move.
            folder_id: Id of the folder
        Print: An object containing the new parent folder and other meta data
        Returns : Parent Ids for the file

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        
        try:
            # call drive api client
            service = build('drive', 'v3', credentials=self.key_connexion.credentials)

            # pylint: disable=maybe-no-member
            # Retrieve the existing parents to remove
            file = service.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            # Move the file to the new folder
            file = service.files().update(fileId=file_id, addParents=folder_id,
                                        removeParents=previous_parents,
                                        fields='id, parents').execute()
            return file.get('parents')

        except HttpError as error:
            print(F'An error occurred: {error}')
            return None
       
    def main_constructeur(self):
        # recuperer tout les id du fichier 
        # verifier si l'id facture du fichier et present dans le google sheets 
        #   si oui ne rien faire et déplacer le fichier dans archiver local
        #   si non rajouter les information du fichier
        
        
        # regrouper les information fichier id_drive_fichier, url et "date", "ttc"  (si id pas present dans google sheets)
        
                
        
        pass
    
    def grouper_infos(self,facture_info,list_dossier_drive ):
        for fichier in self.drive_list_factures_EN_COURS:
            if self.facture_info["name"] == fichier["name"]:
                self.facture_info.update(fichier)
                print(self.facture_info)
                print("hello2")
      
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

    @staticmethod
    def local_get_all_file_folder_formater(patch_dossier = FOLDER_LOCAL.FACTURE_ARCHIVER):
        all_facture_id_name_chem = []
        for nom_fichier in os.listdir(patch_dossier):
            if os.path.isfile(os.path.join(patch_dossier, nom_fichier)):
                id_facture = nom_fichier.split("_")[1].split(".")[0]
                all_facture_id_name_chem.append({"id":id_facture,
                                            "name":nom_fichier,
                                            "path" : os.path.join(patch_dossier,nom_fichier)})
        return all_facture_id_name_chem

    def upload_local_to_drive(self,id_dossier_destionation = FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_ARCHIVER ):
        for facture in self.local_list_factures_non_traiter : 
            drive_facture_traiter = self.drive.CreateFile(
            {
            'parents': [{'id': id_dossier_destionation}],
            "title" : facture["id"]
            })
            drive_facture_traiter.SetContentFile(facture["path"])
            drive_facture_traiter.Upload()
    
    



drive = MrDrive()
drive.main_constructeur()

