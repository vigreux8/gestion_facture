import os
import PyPDF2
import re
from Setting.CONSTANTE import FOLDER_LOCAL
import importlib
from datetime import datetime
from fonction_commun import facture_fonction_commun

#comment savoir que j'ai tester tout les models ? 

class ModelFacture():
    def __init__(self,path_facture_amazon_prime) -> None:
        self.provenance = "amazon_prime"
        print(f"instance : {self.provenance} active")
        self.separateur = "_"
        self.facture = {}
        self.contenue_pdf = ""
        self.facture["path"] = path_facture_amazon_prime
        self.facture["nom_fichier"] = os.path.basename(path_facture_amazon_prime) 
        self.PATTERN_ID = r"(\D\d{2}-\d{7}-\d{7}\D)"
        self.PATTERN_COUT_TTC = r"TTC\s(.*?)(?=\s\|)"
        self.PATTERN_DATE =  r"\d{1,2}\s\w+\s\d{4}"
        self.PATTERN_DATE_ALTERNATIVE = r"Date de la commande (\d{1,2}\s\w+\.\s\d{4})"
        self.PATTERN_PRIX_TTC = r"Total à payer\s+EUR\s+(\d+\.\d{2})"
        self.pattern_provenance = "487773327 • RCS Nanterre"
        print(re.search(self.pattern_provenance,self.contenue_pdf))
        self.get_contenue_pdf()
        self.cree_fichier_texte_contenue_document(self.contenue_pdf)
        if  self.pattern_provenance in self.contenue_pdf:
            self.get_all_content_to_pdf()
            self.print_contenue_info_facture()
            
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        # print(self.infos_factures[0][1:len(self.infos_factures[0])])
        
    def get_contenue_pdf(self):
        with open(self.facture["path"],"rb") as binarie_file:
            pdf_reader = PyPDF2.PdfReader(binarie_file)
            first_page = pdf_reader.pages[0]
            self.contenue_pdf = first_page.extract_text()
            
    def get_all_content_to_pdf(self): 
            self.facture["date"] = self.get_date_achat(self.contenue_pdf)
            self.facture["id"] = self.get_ID(self.contenue_pdf)
            self.facture["nom_produit"] = self.provenance
            self.facture["ttc"] = self.get_prix_ttc(self.contenue_pdf)

    def cree_fichier_texte_contenue_document(self,page,nom_fichier = ""):
        chemin_dossier = FOLDER_LOCAL.DOSSIER_CONTENUE_PDF
        extension = ".txt"
        if nom_fichier == "":
            nom_fichier = self.facture["nom_fichier"].replace(".pdf","")
            nom_fichier = f"{nom_fichier}{extension}"
        else:
            nom_fichier = f"{nom_fichier}{extension}"
        
        chemins_fichier = os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier)
        
        if  os.path.exists(chemins_fichier):
            print("fichier déjat existant")
            return
        with open(os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier),"wb") as fichier:
                fichier.write(page.encode("utf-8"))
    
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
                # print("Aucune date trouvée.")

    def get_prix_ttc(self,contenue):
        prix_total_TTC = re.search(self.PATTERN_PRIX_TTC,contenue)
        if prix_total_TTC:
            return prix_total_TTC.group(1)
            # print("Prix :", prix_total_TTC)
        else:
            return "None"
            # print("Aucun prix trouvé.")
        
    def set_name_fichier(self):
        for facture in self.infos_factures: 
                path_old = facture[1]
                print("facture[5]zeezrzerrze",path_old)

                nom_fichier = self.separateur.join([self.provenance,date,id,nom_produit,prix_ttc])
                # print(prix_total_TTC)
                print(nom_fichier)
                patch_new = os.path.join(FOLDER_LOCAL.AMAZON,f"{nom_fichier}.pdf")
                os.rename(path_old,patch_new)

#comment faire pour avoir un template de model


# def main_test():
#     chem_facture =  os.path.join("facture","pas traiter","Prime_demo.pdf")
#     facture = ModelFacture(chem_facture)
    
#     #recupere tout les cles de facture et lis les valeur des clés
#     for key in list(facture.facture):
#         print(key,":",facture.facture[key])
    
        
# main_test()
        