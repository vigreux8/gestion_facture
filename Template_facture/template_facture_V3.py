import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun
#date : {{date}}

class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture_amazon_prime) -> None:
        super().__init__(path_facture_amazon_prime)
        self.provenance = "nom_provenance"
        print(f"instance : {self.provenance} active")
        self.facture["path"] = path_facture_amazon_prime
        self.facture["name"] = os.path.basename(path_facture_amazon_prime)
        self.provenance = "numero unique"
        
        #1

        
        self.get_contenue_pdf()
        if  self.pattern_provenance in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        


# permet de construire la facture plus facilements
ModelFacture(ModelFacture.get_instance_Test_facture())
 