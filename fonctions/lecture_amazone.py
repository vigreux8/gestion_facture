import os
import PyPDF2
import re
from Setting.CONSTANTE import FOLDER
# from Setting.CONSTANTE import FOLDER


class facture():
    def __init__(self) -> None:
        self.factures_folder = []
        self.folder = ""
        self.provenance = "amazon"
        self.separateur = "_"
        self.infos_factures = []
        self.IDs = ""
        self.nom_produit = ""
        self.DATE_ACHAT  = ""
        self.prix_ttc = ""
        self.PATTERN_ID
        self.PATTERN_PRIX_TTC
        self.PATTERN_COUT_TTC 
        self.PATTERN_DATE
    
    def init_all_content(self):
        """
        récupere tout les contenue de tout les PDF
        self.content = [contenu,chemins_fichier,nom_fichier,date,id,nom_produit,prix_ttc,]
        """
        for PATCH_FICHIER,ORGINAL_NAME_FICHIER in self.factures_folder:
            binarie_file = open(PATCH_FICHIER,"rb")
            pdf_reader = PyPDF2.PdfReader(binarie_file)
            first_page = pdf_reader.pages[0]
            first_page = first_page.extract_text()
            date = self.get_date_achat(first_page)
            id = self.get_ID(first_page)
            nom = self.get_nom_produit(first_page)
            prix = self.get_prix_ttc(first_page)
            self.infos_factures.append([first_page,PATCH_FICHIER,ORGINAL_NAME_FICHIER,date,id,nom,prix])
            binarie_file.close()
             
    def get_all_info(self):
        for contenus,chemins,original_name in self.contents:
            self.get_ID(contenus)
    
    def init_contenus_folder(self):
        for fichier in os.listdir(self.folder):
            if os.path.isfile(os.path.join(self.folder, fichier)):
                self.factures_folder.append([os.path.join(self.folder,fichier),fichier])

    def set_name_fichier(self):
        for facture in self.infos_factures: 
                path_old = facture[1]
                nom_original = facture[2]
                date = facture[3]
                id = facture[4]
                nom_produit = facture[5]
                prix_ttc = facture[6]
                print("date :", date)
                print("id :", id)
                print("nom_produit :", nom_produit)
                print("prix_ttc :", prix_ttc)
                nom_fichier = self.separateur.join([self.provenance,date,id,nom_produit,prix_ttc])
                # print(prix_total_TTC)
                print(nom_fichier)
                patch_new = os.path.join(FOLDER.AMAZON,f"{nom_fichier}.pdf")
                print("liens_1",path_old)
                print("liens_2",patch_new)
                os.rename(path_old,patch_new)

class facture_amazon_produit():
    def __init__(self) -> None:
        self.factures_folder = []
        self.folder = FOLDER.AMAZON
        self.provenance = "amazon"
        self.separateur = "_"
        self.infos_factures = []
        self.IDs = ""
        self.nom_produit = ""
        self.DATE_ACHAT  = ""
        self.prix_ttc = ""
        self.PATTERN_ID = r"(\d{3}-\d{7}-\d{7})"
        self.PATTERN_COUT_TTC = r"TTC\s(.*?)(?=\s\|)"
        self.PATTERN_DATE =  r"Date de la commande (\d{2}\.\d{2}\.\d{4})"
        self.PATTERN_PRIX_TTC = r"([\d,]+) €"
        self.init_contenus_folder()
        self.init_all_content()
        # print(self.infos_factures[0][1:len(self.infos_factures[0])])
        
    def init_all_content(self):
        """
        récupere tout les contenue de tout les PDF
        self.content = [contenu,chemins_fichier,nom_fichier,date,id,nom_produit,prix_ttc,]
        """
        for PATCH_FICHIER,ORGINAL_NAME_FICHIER in self.factures_folder:
            binarie_file = open(PATCH_FICHIER,"rb")
            pdf_reader = PyPDF2.PdfReader(binarie_file)
            first_page = pdf_reader.pages[0]
            first_page = first_page.extract_text()
            date = self.get_date_achat(first_page)
            id = self.get_ID(first_page)
            nom = self.get_nom_produit(first_page)
            prix = self.get_prix_ttc(first_page)
            self.infos_factures.append([first_page,PATCH_FICHIER,ORGINAL_NAME_FICHIER,date,id,nom,prix])
            binarie_file.close()
             
    def get_all_info(self):
        for contenus,chemins,original_name in self.contents:
            self.get_ID(contenus)
    
    def init_contenus_folder(self):
        for fichier in os.listdir(self.folder):
            if os.path.isfile(os.path.join(self.folder, fichier)):
                self.factures_folder.append([os.path.join(self.folder,fichier),fichier])

    def get_ID(self,contenue):
        numero_commande = re.search(self.PATTERN_ID,contenue)
        if numero_commande:
           return str(numero_commande.group(0))
            # print("Numéro de commande:", numero_commande)
        else:
            return None
            print("Aucun numéro de commande trouvé.")

    def get_nom_produit(self,contenue):
        nom_produit = re.search(self.PATTERN_COUT_TTC,contenue, re.DOTALL)
        if nom_produit:
            resultat = nom_produit.group(1)
            resultat = re.sub(r'\W+', '', resultat)
            return resultat.replace("Total", "").replace("TTC", "").strip()
        else:
            return "None"
            # print("Aucun résultat trouvé.")
    
    def get_date_achat(self,contenue):
        date_commande = re.search(self.PATTERN_DATE,contenue)

        if date_commande:
            return str(date_commande.group(1))
            # print("Date :", self.DATE_ACHAT)
        else:
            return "None"
            # print("Aucune date trouvée.")

    def get_prix_ttc(self,contenue):
        prix_total_TTC = re.search(self.PATTERN_PRIX_TTC,contenue)
        if prix_total_TTC:
            prix_total_TTC = prix_total_TTC.group(0)
            return str(prix_total_TTC.replace(" ","").replace("€",""))
            # print("Prix :", prix_total_TTC)
        else:
            return "None"
            # print("Aucun prix trouvé.")
        
    def set_name_fichier(self):
        for facture in self.infos_factures: 
                path_old = facture[1]
                print("facture[5]zeezrzerrze",path_old)
                nom_original = facture[2]
                date = facture[3]
                id = facture[4]
                nom_produit = facture[5]
                prix_ttc = facture[6]
                print("date :", date)
                print("id :", id)
                print("nom_produit :", nom_produit)
                print("prix_ttc :", prix_ttc)
                nom_fichier = self.separateur.join([self.provenance,date,id,nom_produit,prix_ttc])
                # print(prix_total_TTC)
                print(nom_fichier)
                patch_new = os.path.join(FOLDER.AMAZON,f"{nom_fichier}.pdf")
                print("liens_1",path_old)
                print("liens_2",patch_new)
                os.rename(path_old,patch_new)

class facture_amazon_prime():
    def __init__(self) -> None:
        self.factures_folder = []
        self.folder = FOLDER.AMAZON_PRIME
        self.provenance = "amazon"
        self.separateur = "_"
        self.infos_factures = []
        self.IDs = ""
        self.nom_produit = ""
        self.DATE_ACHAT  = ""
        self.prix_ttc = ""
        self.PATTERN_ID = r"(\D\d{2}-\d{7}-\d{7}\D)"
        self.PATTERN_COUT_TTC = r"TTC\s(.*?)(?=\s\|)"
        self.PATTERN_DATE =  r"\d{1,2}\s\w+\s\d{4}"
        self.PATTERN_DATE_ALTERNATIVE = r"Date de la commande (\d{1,2}\s\w+\.\s\d{4})"
        self.PATTERN_PRIX_TTC = r"Total à payer\s+EUR\s+(\d+\.\d{2})"
        self.init_contenus_folder()
        self.init_all_content()
        # print(self.infos_factures[0][1:len(self.infos_factures[0])])
        
    def init_all_content(self):
        """
        récupere tout les contenue de tout les PDF
        self.content = [contenu,chemins_fichier,nom_fichier,date,id,nom_produit,prix_ttc,]
        """
        for PATCH_FICHIER,ORGINAL_NAME_FICHIER in self.factures_folder:
            binarie_file = open(PATCH_FICHIER,"rb")
            pdf_reader = PyPDF2.PdfReader(binarie_file)
            first_page = pdf_reader.pages[0]
            first_page = first_page.extract_text()
            date = self.get_date_achat(first_page)
            id = self.get_ID(first_page)
            nom = self.get_nom_produit(first_page)
            prix = self.get_prix_ttc(first_page)
            self.infos_factures.append([first_page,PATCH_FICHIER,ORGINAL_NAME_FICHIER,date,id,nom,prix])
            binarie_file.close()
             
    def get_all_info(self):
        for contenus,chemins,original_name in self.contents:
            self.get_ID(contenus)
    
    def init_contenus_folder(self):
        for fichier in os.listdir(self.folder):
            if os.path.isfile(os.path.join(self.folder, fichier)):
                self.factures_folder.append([os.path.join(self.folder,fichier),fichier])

    def get_ID(self,contenue):
        numero_commande = re.search(self.PATTERN_ID,contenue)
        if numero_commande:
           return str(numero_commande.group(0))
            # print("Numéro de commande:", numero_commande)
        else:
            return None
            print("Aucun numéro de commande trouvé.")

    def get_nom_produit(self,contenue):
        return "amazon_prime"
    
    def get_date_achat(self,contenue):
        date_commande = re.search(self.PATTERN_DATE,contenue)

        if date_commande:
            return str(date_commande.group(0))
            # print("Date :", self.DATE_ACHAT)
        else:
            date_commande = re.search(self.PATTERN_DATE_ALTERNATIVE,contenue)
            if date_commande:
                return str(date_commande.group(0))
            else:
                return "None"
                # print("Aucune date trouvée.")

    def get_prix_ttc(self,contenue):
        prix_total_TTC = re.search(self.PATTERN_PRIX_TTC,contenue)
        if prix_total_TTC:
            prix_total_TTC = prix_total_TTC.group(0)
            return str(prix_total_TTC.replace(" ","").replace("€","").replace("TotalàpayerEUR",""))
            # print("Prix :", prix_total_TTC)
        else:
            return "None"
            # print("Aucun prix trouvé.")
        
    def set_name_fichier(self):
        for facture in self.infos_factures: 
                path_old = facture[1]
                print("facture[5]zeezrzerrze",path_old)
                nom_original = facture[2]
                date = facture[3]
                id = facture[4]
                nom_produit = facture[5]
                prix_ttc = facture[6]
                print("date :", date)
                print("id :", id)
                print("nom_produit :", nom_produit)
                print("prix_ttc :", prix_ttc)
                nom_fichier = self.separateur.join([self.provenance,date,id,nom_produit,prix_ttc])
                # print(prix_total_TTC)
                print(nom_fichier)
                patch_new = os.path.join(FOLDER.AMAZON,f"{nom_fichier}.pdf")
                print("liens_1",path_old)
                print("liens_2",patch_new)
                os.rename(path_old,patch_new)
 
# Affichez les noms des fichiers

    # Utiliser une expression régulière pour extraire le numéro de commande
    
        
  
        
  
        

   
