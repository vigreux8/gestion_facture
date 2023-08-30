import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun
#date : {{date}}

class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture) -> None:
        super().__init__(path_facture)
        self.provenance = "adobe"
        print(f"instance : {self.provenance} active")
        self.path = path_facture
        self.nom = os.path.basename(path_facture)
        self.id_provenance = "IE6364992H"
        self.url_facture = None
        
        #1
        self.add_pattern(r"ttc","MONTANT NET\(EUR\) (\d+\.\d{2})",1,"int","C")

        self.add_pattern(r"date","(\d{2}-[A-Z]{3}-\d{4})\s+Date de facturation",1,"date","B")

        self.add_pattern(r"id","(\d{13})\s+Numéro de facture",1,"str","D")


        
        self.get_contenue_pdf()
        if  self.id_provenance in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        


 