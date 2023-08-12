import tkinter as tk
from Setting.CONSTANTE import FOLDER_LOCAL
import os


class grahpique():
    def __init__(self) -> None:
        self.contenue_py = None
        self.fenetre = self.init_fenetre()
        self.dict_variable_widget = {}
        self.init_variable_tkinter("groupeid","groupe_valeurs")
        self.init_variable_tkinter("pattern_id","saisir pattern_id")
        self.init_variable_tkinter("nom_fichier","saisir nom_fichier")
        # self.main_constructor()
        

    def init_fenetre(self):
        fenetre = tk.Tk()
        # fenetre.geometry("800x800")
        fenetre.title("Fenêtre avec Menu Déroulant")
        return fenetre
    
    def get_nom_fichier(self):
        return self.dict_variable_widget["nom_fichier"].get()
    
    def cree_fichier_model_facture(self):
        path_complet = os.path.join(FOLDER_LOCAL.MODEL_FACTURE,f"{self.get_nom_fichier()}.py") 
        if os.path.exists(path_complet):
            "le fichier existe dejat, changer de nom"
        else:
            with open(path_complet,"w") as fichier:
                fichier.write(self.contenue_py)
        
    
    def Rajouter_pattern(self,rajouts="",recherche='#1'):
        rajouts = 'self.add_pattern(self,key: str,pattern : str,group : int,type : str,position_sheet: int)'
        element_rechercher = recherche
        with open(FOLDER_LOCAL.TEMPLATE_MODEL,"r") as facture_template:
            contenue_py = facture_template.read()
        position_depart = contenue_py.find(element_rechercher)+len(recherche)
        contenu_py_modifier = contenue_py[:position_depart]+"\n"+"\t\t"+rajouts+contenue_py[position_depart:]
        print(contenu_py_modifier)
        self.contenue_py = contenu_py_modifier
            
    
    def init_variable_tkinter(self,key,text_visible):
        association = tk.StringVar()
        association.set(text_visible)  # Définir la première option comme valeur par défaut
        self.dict_variable_widget[key] =  association
    
    def cree_bouton_liste(self,variable_tkinter,liste,v_row=1,v_column=1):
        widget_menu_deroulant = tk.OptionMenu(self.fenetre,variable_tkinter,*liste )
        widget_menu_deroulant.grid(row=v_row,column= v_column)
        return widget_menu_deroulant
    
    def ActualiseVariable(self,*args):
            for key in list(self.dict_variable_widget.keys):
                self.dict_variable_widget["groupeid"].get()
                saisi = self.pattern_id.get()
                print(saisi)

    def main_constructor(self):
        widget_liste =  self.cree_bouton_liste(self.dict_variable_widget["groupeid"],["1","2","3"],1,1)
        widget_liste.pack()
        widget_saisi_texte = tk.Entry(self.fenetre,textvariable=self.dict_variable_widget["pattern_id"])
        widget_saisi_texte.pack()
        widget_saisi_texte.bind("<KeyPress-Return>", self.ActualiseVariable)
        self.fenetre.mainloop()
        
# Lancement de la boucle principale

test = grahpique()