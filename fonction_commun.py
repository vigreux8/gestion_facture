import os 
from Setting.CONSTANTE import FOLDER_LOCAL

class facture_fonction_commun():
    def __init__(self) -> None:
        self.message_erreur_info_incomplete = "InfoManquante"
    
    def if_info_incomplete(self):
        key_none = []
        for key in list(self.facture):
            if self.facture[key] == None:
                key_none.append(key)
        if key_none:        
            self.message_erreur_info_incomplete ="_".join((self.message_erreur_info_incomplete,f"{key}")) 
            self.facture["id"] = self.message_erreur_info_incomplete
    
    def print_all_info(self):
        # for key in list(self.facture):
        #     print(key,":",self.facture[key])
        #     print(self.facture[key] == None)
        pass
    
    def formater_name_facture(self):
        path_original = self.facture["path"]
        extension = os.path.splitext(path_original)[-1]
        repertoir_parent = os.path.dirname(path_original)
        separateur = "_"
        new_nom_fichier = separateur.join([self.provenance,f"{self.facture['id']}{extension}"])
        #si message erreur donner manquante
        if self.facture["id"] == self.message_erreur_info_incomplete:
            patch_new = os.path.join(FOLDER_LOCAL.FACTURE_INFO_MANQUANTE,new_nom_fichier)
        else:
            patch_new = os.path.join(repertoir_parent,new_nom_fichier)
        
        os.rename(path_original,patch_new)
    
    def cree_fichier_texte_contenue_document(self,page,nom_fichier = ""):
        chemin_dossier = FOLDER_LOCAL.DOSSIER_CONTENUE_PDF
        extension = ".txt"
        if nom_fichier == "":
            nom_fichier = self.facture["name"].replace(".pdf","")
            nom_fichier = f"{nom_fichier}{extension}"
        else:
            nom_fichier = f"{nom_fichier}{extension}"
        
        chemins_fichier = os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier)
        
        if  os.path.exists(chemins_fichier):
            print("fichier déjat existant")
            return
        with open(os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier),"wb") as fichier:
                fichier.write(page.encode("utf-8"))
