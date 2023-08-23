import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun
#date : {{date}}

class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture_amazon_prime) -> None:
        super().__init__(path_facture_amazon_prime)
        self.provenance = "amazon_produit"
        print(f"instance : {self.provenance} active")
        self.facture["path"] = path_facture_amazon_prime
        self.facture["name"] = os.path.basename(path_facture_amazon_prime)
        self.provenance = "LU19647148"
        
        #1
        self.add_pattern(r"ttc","Total à payer (\d+,\d+)",1,"str","C")
        self.add_pattern(r"date","Date de la commande (\d{2}\.\d{2}\.\d{4})",1,"str","B")
        self.add_pattern(r"id","Numéro de la facture ([^\s]+)
",1,"str","D")

        
        self.get_contenue_pdf()
        if  self.pattern_provenance in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        


 