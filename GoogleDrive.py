from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Setting.CONSTANTE import GOOGLE_AUTH,FOLDER_GOOGLESHEET
import gspread
from os import path
from Setting.CONSTANTE import *
import shutil
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sqlite3

class MrLocal:
    def __init__(self) -> None:
        self.list_factures_non_traiter = self.extract_site_id_path_from_files(FOLDER_LOCAL.FACTURE_PAS_TRAITER)
        self.list_factures_archiver = self.extract_site_id_path_from_files(FOLDER_LOCAL.FACTURE_ARCHIVER)
        self.list_factures_inconnue = self.extract_site_id_path_from_files(FOLDER_LOCAL.FACTURE_INCONNUE)
        self.list_all_list_facture = []
        self.rassembler_toute_les_facture()
        self.facture_info_test = ({
            "name" : "prime_D01-3598561-0389456.pdf",
            "id" : "D01-3598561-0389456",
            "date" : "29/05/2021",
            "ttc" : 12.27,
            "provenance" : "amazon"
        })
    def refresh(self):
        self.list_factures_non_traiter = self.extract_site_id_path_from_files(FOLDER_LOCAL.FACTURE_PAS_TRAITER)
        self.list_factures_archiver = self.extract_site_id_path_from_files(FOLDER_LOCAL.FACTURE_ARCHIVER)
        self.list_factures_inconnue = self.extract_site_id_path_from_files(FOLDER_LOCAL.FACTURE_INCONNUE)
        self.rassembler_toute_les_facture()
        
        
    def rassembler_toute_les_facture(self):
        self.list_all_list_facture.extend(self.list_factures_non_traiter)
        self.list_all_list_facture.extend(self.list_factures_archiver)
        self.list_all_list_facture.extend(self.list_factures_inconnue)
        
    @staticmethod
    def local_move_file_formater(nom_facture,origine_path_facture,destination = FOLDER_LOCAL.FACTURE_ARCHIVER):
        #bouge les fichier locals dans un dossier a un autre
        facture_path_destination = os.path.join(destination,nom_facture) 
        if os.path.isfile(origine_path_facture):
            shutil.move(origine_path_facture,facture_path_destination)
        else : 
            print("fichier inexistant")


    @staticmethod
    def extract_site_id_path_from_files(patch_dossier = FOLDER_LOCAL.FACTURE_PAS_TRAITER):
        #recupere tout les fichiers formater en separant le site d'origine et l'id du fichier
        all_facture_id_name_chem = []
        for nom_fichier in os.listdir(patch_dossier):
            if os.path.isfile(os.path.join(patch_dossier, nom_fichier)):
                id_facture = nom_fichier.split("_")[1].split(".")[0]
                all_facture_id_name_chem.append({
                    "id":id_facture,
                    "name":nom_fichier,
                    "path" : os.path.join(patch_dossier,nom_fichier)})
                
        return all_facture_id_name_chem

class MrDrive:
    def __init__(self) -> None:
        self.key_connexion = None
        self.drive = None
        self.facture_info = ({
            "name" : "D01-3598561-0389456",
            "id_drive" : "D01-3598561-0389456",
            "id" : "D01-3598561-0389456",
            "date" : "29/05/2021",
            "ttc" : 12.27,
            "provenance" : "amazon"
        })
        self.init_connexion_api()
        self.list_archiver = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_ARCHIVER)
        self.list_factures_inconnue = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_INCONNUE)
        self.list_factures_en_cours = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_EN_COURS)
        self.list_all_facture = []
        self.rassembler_toute_les_facture()
    def refresh(self):
        self.list_archiver = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_ARCHIVER)
        self.list_factures_inconnue = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_INCONNUE)
        self.list_factures_en_cours = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_EN_COURS)
            
    
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

    def rassembler_toute_les_facture(self):
        self.tchek_liste_vide(self.list_archiver)
        self.tchek_liste_vide(self.list_factures_inconnue)
        self.tchek_liste_vide(self.list_factures_en_cours)
        
    def tchek_liste_vide(self,liste):
        if liste:
            self.list_all_facture.extend(liste)
        
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
        except HttpError as error:
            print(F'An error occurred: {error}')
            return None
       
    def main_constructeur(self):
        # verifier si l'id facture du fichier et present dans le google sheets 
        #   si oui ne rien faire et déplacer le fichier dans archiver local
        #   si non rajouter les information du fichier
        
        
        # regrouper les information fichier id_drive_fichier, url et "date", "ttc"  (si id pas present dans google sheets)
        
                
        
        pass
      
    def init_connexion_api(self):
        key_connecte_google_drive = GoogleAuth()
        key_connecte_google_drive.settings['client_config_file'] = (GOOGLE_AUTH.KEY_AUTH_OAUTH)
        key_connecte_google_drive.LoadCredentialsFile(GOOGLE_AUTH.KEY_TOKEN_REFRESH)

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
        key_connecte_google_drive.SaveCredentialsFile(GOOGLE_AUTH.KEY_TOKEN_REFRESH)
        self.key_connexion = key_connecte_google_drive
        self.drive = GoogleDrive(key_connecte_google_drive)

    def upload_local_to_drive(self,id_dossier_destionation = FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_ARCHIVER ):
        for facture in self.local_list_factures_non_traiter : 
            drive_facture_traiter = self.drive.CreateFile(
            {
            'parents': [{'id': id_dossier_destionation}],
            "title" : facture["id"]
            })
            drive_facture_traiter.SetContentFile(facture["path"])
            drive_facture_traiter.Upload()
    

class MrSheets():
    def __init__(self,compte_mail_json=GOOGLE_AUTH.KEY_MAILS_AUTH,file_sheets=FOLDER_GOOGLESHEET.FACTURE,feuille="Feuille1") -> None:
        #self.file = gspread.oauth(credentials_filename=GOOGLE_AUTH.KEY_AUTH_OAUTH,authorized_user_filename=GOOGLE_AUTH.KEY_TOKEN_REFRESH)
        self.file = gspread.service_account(filename=compte_mail_json)
        self.sheets = self.file.open(file_sheets)
        self.feuille1 = self.sheets.worksheet(f"{feuille}")
        self.index_association = self.init_lettre_associer_au_nom_colonne
        self.list_all_value_colonne_id = self.get_colonne_id_index_dict()
    
    
    def get_colonne_id_index_dict(self):
        list_google_sheet = []
        for index,value in list(enumerate(self.feuille1.col_values(4)))[1:]:
            list_google_sheet.append({
                "id" : value,
                "index_sheet" : index
            })
        return list_google_sheet
            
    def refresh(self):
        # recuperer tout les id du fichier google sheet
        self.list_all_value_colonne_id = list(enumerate(self.feuille1.col_values(4)))
      
    def get_last_value_col(self,colonne:str = "C"):
        index_ligne = len(self.feuille1.col_values(3)) 
        dernier_valeur = self.feuille1.acell(f"{colonne}{index_ligne}").value 
        return index_ligne,dernier_valeur

    def init_lettre_associer_au_nom_colonne(self,ligne: int=1):
        all_name_colonnes = self.feuille1.row_values(1)
        self.correspondance_index_to_letter = {
            1:"a",
            2:"b",
            3:"c",
            4:"d",
            5:"e",
            6:"f",
            7:"h"
                
        }
        all_colonnes_and_lettres = {}
        index = 1
        for name_colonne in all_name_colonnes:
            # all_colonnes_and_lettres.append((correspondance_index_to_letter[index],name_colonne))
            all_colonnes_and_lettres[self.correspondance_index_to_letter[index]] = name_colonne
            index +=1
        return all_colonnes_and_lettres

    def set_last_value_incrementale(self,colonne:str = "a"):
        index_ligne,dernier_valeur = self.get_last_value_col(colonne)
        self.feuille1.update(f"{colonne}{index_ligne+1}",dernier_valeur+1)

    def main_constructeur(self):
        pass
        
    #recuperer tout les id du fichier google sheet
    
class MrOrchestre():
    def __init__(self) -> None:
        self.sheet = MrSheets()
        self.drive = MrDrive()
        self.local = MrLocal()
        self.Super_liste_facture = []
    
    def refresh(self):
        self.sheet.refresh()
        self.drive.refresh()
        
    def main_constructor(self):
        # print(self.local.local_all_list_facture)
        # print(self.sheet.list_all_value_colonne_id)
        self.grouper_info(self.local.list_all_list_facture,self.drive.list_all_facture)
        print(self.Super_liste_facture)
        pass
    
    
    
    def grouper_info(self,list_facture_local,list_dossier_drive: list):
        # rassembler tout les donner local et drive pour tout avoir au même endroit
        #vérifier le bon fonctionnement
        liste_fichier_drive = list_dossier_drive 
        index__drive = 0
        for fichier_local in list_facture_local:
            # print("fichier locale",fichier_local)       
            for fichier_drive in liste_fichier_drive:
                # print("fichier drive",fichier_drive)       
                
                if fichier_local["name"] == fichier_drive["name"]:
                    # fichier_local.add(fichier_drive)
                    fichier_local =  set(fichier_drive+fichier_local)
                    if list_facture_local is list:
                        liste_fichier_drive.remove(index__drive)
                self.Super_liste_facture.append(fichier_local)
                index__drive +=1
            
    def tchek_id_in_sheet(self, list_sheets):
        for facture in self.Super_liste_facture:
            # je comparer si il se trouve dans pas_traiter ou en_cours_drive compare
            for facture_present in list_sheets:
                if facture["id"] == facture_present["id"]:
                        print("oker")

main = MrOrchestre()
main.main_constructor()

