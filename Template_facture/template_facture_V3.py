import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun
#date : {{date}}

class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture) -> None:
        super().__init__(path_facture)
        self.provenance = "nom_provenance"
        print(f"instance : {self.provenance} active")
        self.path = path_facture
        self.nom = os.path.basename(path_facture)
        self.id_provenance = "numero unique"
        self.url_facture = None
        
        #1

        
        self.get_contenue_pdf()
        if  self.id_provenance in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        


 