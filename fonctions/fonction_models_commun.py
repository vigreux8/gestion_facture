import os 
from Setting.CONSTANTE import FOLDER_LOCAL,MOIS_TRADUCTION,OPTION_LOCAL
from datetime import datetime
from dateutil.parser import parse
import PyPDF2


class facture_fonction_commun():
    def __init__(self) -> None:
        self.message_erreur_info_incomplete = "InfoManquante"
        self.facture = {}
        self.donner_manquante = False
        self.trouver = False
        self.contenue_pdf = ""
        self.separateur_rename = OPTION_LOCAL.SEPARATEUR
      
    def get_contenue_pdf(self):
        with open(self.facture["path"],"rb") as binarie_file:
            pdf_reader = PyPDF2.PdfReader(binarie_file)
            first_page = pdf_reader.pages[0]
            self.contenue_pdf = first_page.extract_text()
            
    def f_date(self):
        #F pour format date 
        #si le format de la date n'ai pas JJ/MM/YYYY
        facture_date = self.facture['date']
        try:
            date_obj = parse(facture_date)
            date_obj = date_obj.strftime('%d/%m/%Y')
            self.facture["date"] = date_obj
        except:
            try:
                for mois in list(MOIS_TRADUCTION.MOIS_TRADUCTION_FR_TO_ANGLAIS):
                    if mois in facture_date:
                        facture_date = facture_date.replace(mois,MOIS_TRADUCTION.MOIS_TRADUCTION_FR_TO_ANGLAIS[mois])
                        break
                date_obj = parse(facture_date)
                date_obj = date_obj.strftime('%d/%m/%Y')
                self.facture["date"] = date_obj
            except ValueError as error:
                print("An error occurred:", str(error))
    
    
    def if_info_incomplete(self):
        key_none = []
        for key in list(self.facture):
            if self.facture[key] == None:
                key_none.append(key)
        if key_none:        
            self.message_erreur_info_incomplete ="_".join((self.message_erreur_info_incomplete,f"{key}")) 
            self.facture["id"] = self.message_erreur_info_incomplete
            self.donner_manquante = True
    
    def print_all_info(self):
        # for key in list(self.facture):
        #     print(key,":",self.facture[key])
        #     print(self.facture[key] == None)
        pass
    
    def formater_name_facture(self):
        path_original = self.facture["path"]
        extension = os.path.splitext(path_original)[-1]
        repertoir_parent = os.path.dirname(path_original)
        new_nom_fichier = self.separateur_rename.join([self.provenance,f"{self.facture['id']}{extension}"])
        #si message erreur donner manquante
        if self.facture["id"] == self.message_erreur_info_incomplete:
            self.facture["path"] = os.path.join(FOLDER_LOCAL.FACTURE_INFO_MANQUANTE,new_nom_fichier)
            self.facture["name"] = os.path.basename(self.facture["path"])
        else:
            self.facture["path"] = os.path.join(repertoir_parent,new_nom_fichier)
            self.facture["name"] = os.path.basename(self.facture["path"])
        os.rename(path_original,self.facture["path"])
           
    def cree_fichier_texte_contenue_document(self,page,nom_fichier = ""):
        chemin_dossier = FOLDER_LOCAL.DOSSIER_CONTENUE_PDF
        extension = ".txt"
        if nom_fichier == "":
            nom_fichier = self.facture["name"].replace(".pdf","")
            nom_fichier = f"{nom_fichier}{extension}"
        else:
            nom_fichier = f"{nom_fichier}{extension}"
        
        chemins_fichier = os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier)
        
        if  os.path.exists(chemins_fichier):
            print("fichier déjat existant")
            return
        with open(os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier),"wb") as fichier:
                fichier.write(page.encode("utf-8"))
