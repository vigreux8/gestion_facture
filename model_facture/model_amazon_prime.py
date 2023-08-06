import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun


class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture_amazon_prime) -> None:
        super().__init__()
        
        self.provenance = "AmazonPrime"
        print(f"instance : {self.provenance} active")
        self.facture["path"] = path_facture_amazon_prime
        self.facture["name"] = os.path.basename(path_facture_amazon_prime) 
        self.PATTERN_ID = r"(\D\d{2}-\d{7}-\d{7}\D)"
        self.PATTERN_DATE =  r"\d{1,2}\s\w+\s\d{4}"
        self.PATTERN_DATE_ALTERNATIVE = r"Date de la commande (\d{1,2}\s\w+\.\s\d{4})"
        self.PATTERN_PRIX_TTC = r"Total à payer\s+EUR\s+(\d+\.\d{2})"
        self.pattern_provenance_siren = "487773327 • RCS Nanterre"
        self.get_contenue_pdf()
        if  self.pattern_provenance_siren in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
          

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
        else:
            return None

    def get_prix_ttc(self,contenue):
        prix_total_TTC = re.search(self.PATTERN_PRIX_TTC,contenue)
        if prix_total_TTC:
            return str(prix_total_TTC.group(1))
            # print("Prix :", prix_total_TTC)
        else:
            return None
            # print("Aucun prix trouvé.")

    @classmethod
    def Test_facture(self) -> object: 
        """retourne la facture present dnas le dossier test"""
        if len(os.listdir(FOLDER_LOCAL.FACTURE_TEST)) == 1:
            nom_fichier =  os.listdir(FOLDER_LOCAL.FACTURE_TEST)[0]
            path_fichier = os.path.join(FOLDER_LOCAL.FACTURE_TEST,nom_fichier)
            return ModelFacture(path_fichier)
        elif len(os.listdir(FOLDER_LOCAL.FACTURE_TEST)) >= 1:
            print("le dossier test doit contenir 1 seul fichier ")
        else:
            print("fichier vide")
            
# ModelFacture.Test_facture()