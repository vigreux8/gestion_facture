import os 
from Setting.CONSTANTE import FOLDER_LOCAL,MOIS_TRADUCTION,OPTION_LOCAL
from datetime import datetime
from dateutil.parser import parse
import PyPDF2
import re


class pattern_info():
    def __init__(self) -> None:
        self.nom :str = None
        self.pattern :str = None
        self.groupe : int = None
        self.out :str or int = None
        self.type : str = "str"
        # col+numero  exemple : "A1"
        self.emplacement_sheets :str = None


class facture_fonction_commun():
    def __init__(self,path=None) -> None:
        self.message_erreur_info_incomplete = "InfoManquante"
        self.facture = {
            "path" : path
        }
        self.donner_manquante = False
        self.trouver = False
        self.test = self.detect_test()
        self.contenue_pdf_byte = None
        self.contenue_pdf_str = None
        self.dict_pattern_centralle : dict(str,pattern_info) = {}
        self.default_ordre_sheets = 0
        
        self.separateur_rename = OPTION_LOCAL.SEPARATEUR
    def detect_test(self):
        if os.path.dirname(self.facture["path"]) == FOLDER_LOCAL.FACTURE_TEST:
            return True
    
    def get_contenue_pdf(self):
        with open(self.facture["path"],"rb") as binarie_file:
            pdf_reader = PyPDF2.PdfReader(binarie_file)
            first_page = pdf_reader.pages[0]
            self.contenue_pdf_byte = first_page.extract_text()
            
    def f_date(self):
        for keys in self.dict_pattern_centralle.keys():
            pattern_info = self.dict_pattern_centralle[keys]
            if pattern_info.type == "date":
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
                        pattern_info.out = date_obj
                        self.dict_pattern_centralle[keys] = pattern_info
                    except ValueError as error:
                        print("An error occurred:", str(error))
            else:
                return
    
    def if_info_incomplete(self):
        key_none = []
        for key in list(self.facture):
            if self.facture[key] == None:
                key_none.append(key)
        if key_none:        
            self.message_erreur_info_incomplete ="_".join((self.message_erreur_info_incomplete,f"{key}")) 
            self.facture["erreur"] = self.message_erreur_info_incomplete
            self.donner_manquante = True
    
    def print_all_info(self):
        for key in list(self.facture):
            print(key,":",self.facture[key])
        pass
    
    def formater_name_facture(self):
        path_original = self.facture["path"]
        extension = os.path.splitext(path_original)[-1]
        repertoir_parent = os.path.dirname(path_original)
        if self.donner_manquante:
            new_nom_fichier = self.separateur_rename.join([self.provenance,f"{self.facture['erreur']}{extension}"])
        else:
            new_nom_fichier = self.separateur_rename.join([self.provenance,f"{self.facture['id']}{extension}"])
            
        #si message erreur donner manquante
        if self.if_info_incomplete and not self.test:
            self.facture["path"] = os.path.join(FOLDER_LOCAL.FACTURE_INFO_MANQUANTE,new_nom_fichier)
            self.facture["name"] = os.path.basename(self.facture["path"])
        else:
            self.facture["path"] = os.path.join(repertoir_parent,new_nom_fichier)
            self.facture["name"] = os.path.basename(self.facture["path"])
        os.rename(path_original,self.facture["path"])
        if self.test:
            print("new_path :",self.facture["path"])
    
    def get_nombre_groupe_pattern_found(self,pattern):
        return len(re.search(pattern,self.contenue_pdf_byte))
    
    def get_len_groupe(self,pattern):
        # match = re.search(pattern,self.contenue_pdf_byte)
        match = re.search(pattern,self.contenue_pdf_byte)
        if match and not pattern == ''  :
            # len_match =sum(1 for _ in match)
            liste_element_match = list(range(0,match.lastindex+1))
            return liste_element_match
        else:
            return [0]
     
    def get_to_contenu(self,pattern,group,type):
        pattern_found = re.search(pattern,self.contenue_pdf_byte)
        if pattern_found and not pattern == '':
            if group == "None":
                return pattern_found
            elif type == "str":
                return str(pattern_found.group(int(group)))
            elif type == "int":
                return pattern_found.group(int(group)).replace(".",",")
        return "None"
    
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
        if not self.trouver or self.donner_manquante or self.test:
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
    
    def add_pattern(self,nom,pattern,groupe,type,emplacement_sheets = "None"):
        pattern_instance = pattern_info()
        pattern_instance.nom = nom
        pattern_instance.pattern = pattern
        pattern_instance.groupe = groupe
        pattern_instance.type = type
        
        if emplacement_sheets == "None":
            pattern_instance.emplacement_sheets = self.default_ordre_sheets
            self.default_ordre_sheets +=1
        self.dict_pattern_centralle[nom] = pattern_instance
        
    def set_all_content_to_pdf(self):  
        for key in list(self.dict_pattern_centralle.keys()):
            instance_pattern = self.dict_pattern_centralle[key]
            self.facture[key] = self.get_to_contenu(instance_pattern.pattern,instance_pattern.groupe,type)
            
    def run_programme_model(self):
        self.trouver = True
        self.set_all_content_to_pdf()
        if not self.test:
            self.f_date()
        self.if_info_incomplete()
        self.print_all_info()
        self.formater_name_facture()
        self.cree_fichier_texte_prompt_document()
        
    def get_instance_Test_facture(self) -> str: 
        '''
        mode : 
            -path : return path
            -instance : retourne la fonction commmun avec le path
        '''
        """retourne la facture present dnas le dossier test"""
        if len(os.listdir(FOLDER_LOCAL.FACTURE_TEST)) == 1:
            nom_fichier =  os.listdir(FOLDER_LOCAL.FACTURE_TEST)[0]
            path_fichier = os.path.join(FOLDER_LOCAL.FACTURE_TEST,nom_fichier)
            return path_fichier
        elif len(os.listdir(FOLDER_LOCAL.FACTURE_TEST)) >= 1:
            print("le dossier test doit contenir 1 seul fichier ")
        else:
            print("fichier vide")