import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun


class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture_amazon_prime) -> None:
        super().__init__(path_facture_amazon_prime)
        self.pattern_provenance_siren = "IE6364992H"
        self.provenance = "Adobe"
        print(f"instance : {self.provenance} active")
        self.facture["path"] = path_facture_amazon_prime
        self.facture["name"] = os.path.basename(path_facture_amazon_prime)
        self.list_pattern = {
                "id" : (r"Numéro de commande\s+(\d+)","1","str","colonne_sheets"),
                "date" : (r"\b(\d{1,2}-[A-Z]{3}-\d{4})\b","0","str","colonne_sheets"),
                "ttc" : (r"TOTAL\(EUR\)\s+(\d+\.\d{2})","1","int","colonne_sheets"),
            }
        self.get_contenue_pdf()
        if  self.pattern_provenance_siren in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        


# permet de construire la facture plus facilements
ModelFacture(ModelFacture.get_path_Test_facture())
 