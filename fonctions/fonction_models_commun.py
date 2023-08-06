import os 
from Setting.CONSTANTE import FOLDER_LOCAL,MOIS_TRADUCTION,OPTION_LOCAL
from datetime import datetime
from dateutil.parser import parse
import PyPDF2


class facture_fonction_commun():
    def __init__(self,path=None) -> None:
        self.message_erreur_info_incomplete = "InfoManquante"
        self.facture = {
            "path" : path
        }
        self.donner_manquante = False
        self.trouver = False
        self.contenue_pdf_byte = None
        self.contenue_pdf_str = None
        
        
        self.separateur_rename = OPTION_LOCAL.SEPARATEUR
      
    def get_contenue_pdf(self ):
        with open(self.facture["path"],"rb") as binarie_file:
            pdf_reader = PyPDF2.PdfReader(binarie_file)
            first_page = pdf_reader.pages[0]
            self.contenue_pdf_byte = first_page.extract_text()
            
    def f_date(self):
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
        for key in list(self.facture):
            print(key,":",self.facture[key])
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
           
    def cree_fichier_texte_prompt_document(self):
        self.get_contenue_pdf()
        chemin_dossier = FOLDER_LOCAL.DOSSIER_CONTENUE_PDF
        extension = ".txt"
        nom_fichier = os.path.basename(self.facture["path"]).replace(".pdf","")
        nom_fichier = f"{nom_fichier}{extension}"
        contenue = self.contenue_pdf_byte
        
        chemins_fichier = os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier)
        if  os.path.exists(chemins_fichier):
            print("fichier déjat existant")
            return
        if not self.trouver or self.donner_manquante:
            with open(os.path.join(FOLDER_LOCAL.PROMPT_GPT,nom_fichier),"w",encoding="utf-8") as fichier:
                    fichier.write(f"""voici une facture garde la en memoire et repond uniquement "OK je suis pret a prendre les consigne" n écrire rien d autre
    facture :"{contenue}"


    voici tes consignes a partir du pdf fournie et tu dois parfaitement les respecter :
    tu peux créer le regex
    installe-le ensuite dans un fichier que je peux copier (n indique pas de commentaires en # mais les variables à la suite et n explique rien)
    CONSIGNE IMPORTANT:
    -le prix doit être uniquement composer de valeur numerique separer par une virgule
    -la date doit se composer uniquement de la date et rien d'autre 
    self.PATTERN_ID = r"ici patern regex pour trouver le numéro de facture l id doit être unique à chaque facture"
    self.PATTERN_DATE = r"ici paterne date"
    self.PATTERN_PRIX_TTC = r"ici paterne regex du prix TTC"
    identifiant_unique = "ressort le numéro de TVA ou le SIREN ou SIRET ou l adresse de l entreprise surtout pas un numero commande ou idenfiant semblable a l'id"

    afficher les resultat attendu dans ton encadre chatgpt :

    1. Identifiant de la facture : []
    2. Date de la facture : []
    3. Prix total TTC : []
    4. Identifiant unique : [] """

    )
        else:
            with open(os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier),"w",encoding="utf-8") as fichier:
                    fichier.write(contenue)
    def get_all_content_to_pdf(self): 
            self.facture["date"] = self.get_date_achat(self.contenue_pdf_byte)
            self.facture["id"] = self.get_ID(self.contenue_pdf_byte)
            self.facture["provenance"] = self.provenance
            self.facture["ttc"] = self.get_prix_ttc(self.contenue_pdf_byte)
            if self.facture["ttc"]:
                self.facture["ttc"] = self.facture["ttc"].replace(".",",")
    
    def run_programme_model(self):
        self.trouver = True
        self.get_all_content_to_pdf()
        self.f_date()
        self.if_info_incomplete()
        if os.path.dirname(self.facture["path"]) == FOLDER_LOCAL.FACTURE_TEST:
            self.print_all_info()
        self.formater_name_facture()
        self.cree_fichier_texte_prompt_document()
            