import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun
#date : {{date}}

class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture_amazon_prime) -> None:
        super().__init__(path_facture_amazon_prime)
        self.provenance = "adobe"
        print(f"instance : {self.provenance} active")
        self.path = path_facture_amazon_prime
        self.nom = os.path.basename(path_facture_amazon_prime)
        self.id_provenance = "IE6364992H"
        self.url_facture = None
        
        #1
        self.add_pattern("ttc",r"TOTAL\(EUR\)\s+(\d+\.\d{2})",1,"int","C")
        self.add_pattern("date",r"\b(\d{1,2}-[A-Z]{3}-\d{4})\b",0,"date","B")
        self.add_pattern("id",r"Numéro de commande\s+(\d+)",1,"str","D")
        self.get_contenue_pdf()
        if self.id_provenance in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        


 