import os
import re
from fonctions.fonction_models_commun import facture_fonction_commun
#date : {{date}}

class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture) -> None:
        super().__init__(path_facture)
        self.provenance = "brevo"
        print(f"instance : {self.provenance} active")
        self.path = path_facture
        self.nom = os.path.basename(path_facture)
        self.id_provenance = "FR80498019298"
        self.url_facture = None
        
        #1
        self.add_pattern(r"ttc","Total(\d+,\d{2} )",1,"montant","C")
        self.add_pattern(r"date","payé le (\d{2} [a-zA-Z]+, \d{4})",1,"date","B")
        self.add_pattern(r"id","Facture #—([A-Z0-9-]+)",1,"normale","A")


        
        self.get_contenue_pdf()
        if  self.id_provenance in self.contenue_pdf_byte:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        


 