import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun


class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture) -> None:
        super().__init__()
        self.provenance = "AmazonProduit"
        print(f"instance : {self.provenance} active")
        self.facture["path"] = path_facture
        self.facture["name"] = os.path.basename(path_facture) 
        self.PATTERN_ID = r"Numéro de la commande ([\d-]+)"
        self.PATTERN_DATE =  r"(\d{2}\.\d{2}\.\d{3})"
        self.PATTERN_PRIX_TTC = r"\d{1,2},\d{2} €"
        self.pattern_provenance_siren = "R.C.S. Luxembourg: B 93815"
        self.get_contenue_pdf()
        if  self.pattern_provenance_siren in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
    
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
            return str(prix_total_TTC.group(0))
            # print("Prix :", prix_total_TTC)
        else:
            return None
            # print("Aucun prix trouvé.")

#comment faire pour avoir un template de model
def main_test():
    chem_facture =  os.path.join("facture","pas traiter","adobe.pdf")
    facture = ModelFacture(chem_facture)
      
# main_test()
        