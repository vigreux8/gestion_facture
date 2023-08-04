from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from Setting.CONSTANTE import GOOGLE_AUTH,FOLDER_GOOGLESHEET
import gspread
import os
from Setting.CONSTANTE import *
import shutil
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import PyPDF2
import re
import importlib
import inspect

class MrLocal:
    def __init__(self) -> None:
        self.list_template_factures = []   
        self.pattern_class = "ModelFacture"
        self.init_model_class()
        
    def refresh(self):
        self.list_factures_non_traiter = self.set_data_file(FOLDER_LOCAL.FACTURE_PAS_TRAITER)
        
    @staticmethod
    def move_file(origine_path,dossier_destination = FOLDER_LOCAL.FACTURE_ARCHIVER):
        #bouge les fichier locals dans un dossier a un autre a besoins uniquement du path d'origine
        path_destination = os.path.join(dossier_destination,os.path.basename(origine_path)) 
        if os.path.isfile(origine_path):
            shutil.move(origine_path,path_destination)
        else : 
            print("fichier inexistant")
                
    @staticmethod
    def listdir_sans_pycache(folder):
        list_fichier = os.listdir(folder)
        list_fichier_nettoyer = []
        for fichier in list_fichier:
            if not "__pycache__" in fichier:
               list_fichier_nettoyer.append(fichier)
        return list_fichier_nettoyer
          
    def listdir_path_complet_sans_pycache(self,folder):
        list_fichier = os.listdir(folder)
        list_fichier_nettoyer = []
        for fichier in list_fichier:
            if not "__pycache__" in fichier:
               list_fichier_nettoyer.append(os.path.join(folder,fichier))
        return list_fichier_nettoyer
                      
    def init_model_class(self):
        for titre_module in (self.listdir_sans_pycache(FOLDER_LOCAL.DOSSIER_MODEL_FACTURE)):
            modules_factures = {}
            titre_module = titre_module.replace(".py","")
            modules_factures["module"] =  f"{FOLDER_LOCAL.DOSSIER_MODEL_FACTURE}.{titre_module}"
            print(modules_factures["module"])
            module = importlib.import_module(modules_factures["module"])
            ma_classe = getattr(module, self.pattern_class)
            modules_factures["class"] = ma_classe
            self.list_template_factures.append(modules_factures["class"])
                    
    def formater_name_inconnue(self):
        path_original = self.facture["path"]
        extension = os.path.splitext(path_original)[-1]
        repertoir_parent = os.path.dirname(path_original)
        separateur = "_"
        new_nom_fichier = separateur.join([self.provenance,f"{self.facture['id']}{extension}"])
        patch_new = os.path.join(repertoir_parent,new_nom_fichier)
        if not patch_new == path_original:
            os.rename(path_original,patch_new)
    # @staticmethod
    # def set_data_formater_file(patch_dossier = FOLDER_LOCAL.FACTURE_PAS_TRAITER):
    #     #recupere tout les fichiers formater en separant le site d'origine et l'id du fichier
    #     all_facture_id_name_chem = []
    #     for nom_fichier in os.listdir(patch_dossier):
    #         if os.path.isfile(os.path.join(patch_dossier, nom_fichier)):
    #             #lie le pdf
    #             id_facture = nom_fichier.split("_")[1].split(".")[0]
    #             all_facture_id_name_chem.append({
    #                 "id":id_facture,
    #                 "name":nom_fichier,
    #                 "path" : os.path.join(patch_dossier,nom_fichier)}),         
        # return all_facture_id_name_chem

class MrDrive:
    def __init__(self) -> None:
        self.key_connexion = None
        self.drive = None
        self.init_connexion_api()
        self.list_factures_en_cours = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_EN_COURS)
        self.list_all_facture = []
    
    def refresh(self):
        self.list_archiver = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_ARCHIVER)
        self.list_factures_inconnue = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_INCONNUE)
        self.list_factures_en_cours = self.get_all_file_drive_folder(FOLDER_GOOGLEDRIVE.ID_DOSSIER_FACTURE_EN_COURS)
            
    
    def get_all_file_drive_folder(self,id_folder ):
        #recuperais tout les dossier present dans le fichier google drive
        drive_liste = []
        file_liste = self.drive.ListFile({'q': f"'{id_folder}' in parents and trashed=false"}).GetList()
        if file_liste:
            for file in file_liste:
                id_facture = file["title"].split("_")[1].split(".")[0]
                drive_liste.append({
                    "name":file['title'],
                    "id_facture": id_facture,
                    "google_file_id":file['id'],
                    "google_folder_id": id_folder,
                    "url" : file['alternateLink']
                })
            return drive_liste

    def tchek_liste_vide(self,liste):
        if liste:
            self.list_all_facture.extend(liste)
        
    def drive_move_file_to_folder(self,file_id_original, folder_id):
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
            file = service.files().get(fileId=file_id_original, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            # Move the file to the new folder
            file = service.files().update(fileId=file_id_original, addParents=folder_id,
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

    def upload_local_to_drive(self,id_dossier_destionation,facture_local ):
            drive_facture_traiter = self.drive.CreateFile(
            {
            'parents': [{'id': id_dossier_destionation}],
            "title" : facture_local["id"]
            })
            drive_facture_traiter.SetContentFile(facture_local["path"])
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
        list_facture_pas_traiter =  self.local.listdir_path_complet_sans_pycache(FOLDER_LOCAL.FACTURE_PAS_TRAITER)
        list_element_inconnue = list_facture_pas_traiter.copy()
        for path_facture in list_facture_pas_traiter:
            for template_facture in self.local.list_template_factures:
                instance =  template_facture(path_facture)
                if instance.trouver:
                    list_element_inconnue.remove(path_facture)
                    break
                
        if list_element_inconnue:
            for path_facture in list_element_inconnue:
                index = str(len(os.listdir(FOLDER_LOCAL.FACTURE_INCONNUE)))
                path_facture = self.formater_name_file(path_facture,index)
                self.local.move_file(path_facture,FOLDER_LOCAL.FACTURE_INCONNUE)
            
        # for facture in list_facture_pas_traiter:
        #     if facture in new_list_facture_pas_traiter:
        #         list_element_inconnue
        #[OK]gerer les facture inconnue
        #[]]upload facture inconnue dans drive
        #[]upload donner manquante dans drive
        
        
        #[]recuperais id present dans le sheets
        #[]comparer les fichier 
        #[]transferer les fichier non present dans sheets
        #[]recuperais les fichier present dans le drive 
        #[]comparer l'id pour recuperer l'id Fichier et pathalternative
        #[]crée l'url 
        #[]mettre les valeurs à la suite de la dernier valeurs
        #[]deplacer les ficier drive dans archiver
            
    def formater_name_file(self,path_file : str,index :str, message = ["facture","inconnue"]):
        path_original = path_file
        extension = os.path.splitext(path_file)[-1]
        message.append(index)
        message[-1] +=extension
        repertoir_parent = os.path.dirname(path_file)
        separateur = "_"
        new_nom_fichier = separateur.join(message)
        #si message erreur donner manquante
        patch_new = os.path.join(repertoir_parent,new_nom_fichier)
        os.rename(path_original,patch_new)
        return patch_new

main = MrOrchestre()
main.main_constructor()

