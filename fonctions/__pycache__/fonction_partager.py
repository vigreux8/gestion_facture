import os 
from Setting.CONSTANTE import FOLDER_LOCAL

class facture_fonction_commun():
    def __init__(self) -> None:
        pass
    
    def print_contenue_info_facture(self):
        for key in list(self.facture):
            print(key,":",self.facture[key])
            
    def set_name_fichier(self):
        for facture in self.infos_factures: 
                path_old = facture[1]
                print("facture[5]zeezrzerrze",path_old)

                nom_fichier = self.separateur.join([self.provenance,date,id,nom_produit,prix_ttc])
                # print(prix_total_TTC)
                print(nom_fichier)
                patch_new = os.path.join(FOLDER_LOCAL.AMAZON,f"{nom_fichier}.pdf")
                os.rename(path_old,patch_new)
    
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