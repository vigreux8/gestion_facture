import os 
from Setting.CONSTANTE import FOLDER_LOCAL

class facture_fonction_commun():
    def __init__(self) -> None:
        pass
    
    def if_info_incomplete(self):
        for key in list(self.facture):
            if not self.facture[key]:
                self.facture_id = "InformationIncompletes"
    
    def infor_incomplete(self):
        for key in list(self.facture):
            print(key,":",self.facture[key])
            
    def formater_name_file(self):
        path_original = self.facture["path"]
        extension = os.path.splitext(path_original)[-1]
        repertoir_parent = os.path.dirname(path_original)
        separateur = "_"
        new_nom_fichier = separateur.join([self.provenance,f"{self.facture['id']}{extension}"])
        patch_new = os.path.join(repertoir_parent,new_nom_fichier)
        if not patch_new == path_original:
            os.rename(path_original,patch_new)
    
    def cree_fichier_texte_contenue_document(self,page,nom_fichier = ""):
        chemin_dossier = FOLDER_LOCAL.DOSSIER_CONTENUE_PDF
        extension = ".txt"
        if nom_fichier == "":
            nom_fichier = self.facture["nom_fichier"].replace(".pdf","")
            nom_fichier = f"{nom_fichier}{extension}"
        else:
            nom_fichier = f"{nom_fichier}{extension}"
        
        chemins_fichier = os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier)
        
        if  os.path.exists(chemins_fichier):
            print("fichier déjat existant")
            return
        with open(os.path.join(FOLDER_LOCAL.DOSSIER_CONTENUE_PDF,nom_fichier),"wb") as fichier:
                fichier.write(page.encode("utf-8"))
