import os
import PyPDF2
import re
from Setting.CONSTANTE import FOLDER_LOCAL
import importlib
from fonctions.fonction_commun import facture_fonction_commun


class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture) -> None:
        super().__init__()
        self.provenance = "AmazonProduit"
        print(f"instance : {self.provenance} active")
        self.separateur = "_"  
        self.facture = {}
        self.contenue_pdf = ""
        self.facture["path"] = path_facture
        self.facture["name"] = os.path.basename(path_facture) 
        self.PATTERN_ID = r"Numéro de la commande ([\d-]+)"
        self.PATTERN_DATE =  r"(\d{2}\.\d{2}\.\d{4})"
        self.PATTERN_PRIX_TTC = r"Total à payer (\d+\,\d{2}) €"
        self.pattern_provenance_siren = "R.C.S. Luxembourg: B 93815"
        self.trouver = False
        print(re.search(self.pattern_provenance_siren,self.contenue_pdf))
        self.get_contenue_pdf()
        self.cree_fichier_texte_contenue_document(self.contenue_pdf)
        if  self.pattern_provenance_siren in self.contenue_pdf:
            self.get_all_content_to_pdf()
            self.f_date()
            self.if_info_incomplete()
            self.print_all_info()
            self.formater_name_facture()
            self.trouver = True
            
            
            
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
            self.facture["provenance"] = self.provenance
            self.facture["ttc"] = self.get_prix_ttc(self.contenue_pdf)

    def get_ID(self,contenue):
        numero_commande = re.search(self.PATTERN_ID,contenue)
        if numero_commande:
           return str(numero_commande.group(1))
            # print("Numéro de commande:", numero_commande)
        else:
            return None
            print("Aucun numéro de commande trouvé.")

    def get_nom_produit(self,contenue):
        return "amazon_prime"
    
    def get_date_achat(self,contenue):
        date_commande = re.search(self.PATTERN_DATE,contenue)

        if date_commande:
            return  str(date_commande.group(0))
            # print("Date :", self.DATE_ACHAT)
        else:
            return None
                # print("Aucune date trouvée.")

    def get_prix_ttc(self,contenue):
        prix_total_TTC = re.search(self.PATTERN_PRIX_TTC,contenue)
        if prix_total_TTC:
            return prix_total_TTC.group(1)
            # print("Prix :", prix_total_TTC)
        else:
            return None
            # print("Aucun prix trouvé.")

#comment faire pour avoir un template de model


def main_test():
    chem_facture =  os.path.join("facture","pas traiter","adobe.pdf")
    facture = ModelFacture(chem_facture)
      
# main_test()
        