import tkinter as tk
from Setting.CONSTANTE import FOLDER_LOCAL
from fonctions.fonction_models_commun import facture_fonction_commun
import os

class pattern_constructor():
    def __init__(self) -> None:
        self.pattern = None
        self.liste_groupe = [0]
        self.type = None
        self.var_tkinter_pattern = None
        self.var_tkinter_groupe = None
        self.var_tkinter_nom = None
        self.var_tkinter_sortie = None
        self.colonne_sheets = None
        self.widget_pattern = None
        self.widget_liste_groupe = None
        self.widget_label = None
        self.widget_sortie = None
    
    def get_var_widget_varchar_groupe(self):
        return self.widget_liste_groupe,self.var_tkinter_groupe
    
    
        
class grahpique(facture_fonction_commun):
    def __init__(self) -> None:
        super().__init__(self.get_instance_Test_facture())
        self.contenue_py = None
        self.dict_pattern_centralle = {}
        self.fenetre = self.init_fenetre()
        self.last_row_element = 0
        self.var_tkinter_pattern_provenance = self.init_variable_tkinter("siren ou id ou adresse")
        self.widget_tkinter_presence = {}
        
        self.get_contenue_pdf()
        
    def modifier_pattern(self,nom : str,pattern : str):
        self.dict_pattern_centralle[nom]["pattern"] = pattern
    def tkinter_menus_bas_page(self):
        #menus bas de page 
        pass
    def cree_pattern_instance(self,nom_pattern : str, type = "str",):
        pattern_build = pattern_constructor()
        pattern_build.nom = nom_pattern
        pattern_build.var_tkinter_sortie = self.init_variable_tkinter("None")
        pattern_build.var_tkinter_pattern = self.init_variable_tkinter("saisir pattern")
        pattern_build.var_tkinter_groupe = self.init_variable_tkinter(0,"int")
        pattern_build.var_tkinter_nom = self.init_variable_tkinter(nom_pattern)
        pattern_build = self.cree_widget_pattern(pattern_build)
        self.dict_pattern_centralle[nom_pattern] = pattern_build
        
    def cree_widget_pattern(self,pattern_info):
            # pattern_info = pattern_constructor()
            pattern_info.widget_label = self.tkinter_affichage_texte(pattern_info.var_tkinter_nom,self.last_row_element,0)
            pattern_info.widget_pattern = self.tkinter_saisi_texte(pattern_info.var_tkinter_pattern,self.last_row_element,1)
            pattern_info.widget_liste_groupe = self.tkinter_bouton_liste(pattern_info.var_tkinter_groupe,pattern_info.liste_groupe,self.last_row_element,2)
            pattern_info.widget_sortie = self.tkinter_affichage_texte(pattern_info.var_tkinter_sortie,self.last_row_element,3)
            self.last_row_element +=1
            return pattern_info
    
    def init_fenetre(self):
        fenetre = tk.Tk()
        # fenetre.geometry("800x800")
        fenetre.title("Fenêtre avec Menu Déroulant")
        return fenetre

    def init_variable_tkinter(self,info_visible,type="str"):
        if type == "str":
            association = tk.StringVar()
            association.set(info_visible)  # Définir la première option comme valeur par défaut
        elif type =="int":
            association = tk.IntVar()
            association.set(info_visible)
        return association
        
    def get_nom_fichier(self):
        return self.dict_variable_widget["nom_fichier"].get()
    
    def cree_fichier_model_facture(self):
        path_complet = os.path.join(FOLDER_LOCAL.MODEL_FACTURE,f"{self.get_nom_fichier()}.py") 
        if os.path.exists(path_complet):
            "le fichier existe dejat, changer de nom"
        else:
            with open(path_complet,"w") as fichier:
                fichier.write(self.contenue_py)
    
    def fichier_py_Rajouter_pattern(self,rajouts="",recherche='#1'):
        for key in list(self.dict_pattern_centralle.keys()):
            pattern = self.dict_pattern_centralle[key]
            pattern = pattern_constructor()
            rajouts = 'self.add_pattern(self,key: str,pattern : str,group : int,type : str,position_sheet: int)'
            element_rechercher = recherche
            with open(FOLDER_LOCAL.TEMPLATE_MODEL,"r") as facture_template:
                contenue_py = facture_template.read()
            position_depart = contenue_py.find(element_rechercher)+len(recherche)
            contenu_py_modifier = contenue_py[:position_depart]+"\n"+"\t\t"+rajouts+contenue_py[position_depart:]
            print(contenu_py_modifier)
            self.contenue_py = contenu_py_modifier
            

        #crée une variable de class 

    def tkinter_saisi_texte(self,tkinter_variable,v_row=1,v_column=2):
        widget_saisi_texte = tk.Entry(self.fenetre,textvariable=tkinter_variable)
        widget_saisi_texte.delete("0", "end")
        widget_saisi_texte.grid(row=v_row,column=v_column)
        return widget_saisi_texte

    def tkinter_affichage_texte(self,texte,v_row,v_col):
        varString = tk.Label(self.fenetre,textvariable=texte)
        varString.grid(row=v_row,column=v_col)
        return varString
    
    def tkinter_bouton_liste(self, var_tkinter, liste=[0, 1, 2], v_row=1, v_column=1) -> object:
        widget_menu_deroulant = tk.OptionMenu(self.fenetre, var_tkinter, *liste )
        widget_menu_deroulant.grid(row=v_row,column= v_column)
        return widget_menu_deroulant
    
    def actualiser_liste(self,pattern_info):
            # pattern_info = pattern_constructor()
            menu = pattern_info.widget_liste_groupe["menu"]
            menu.delete(0, "end")
            for element in pattern_info.liste_groupe:
                menu.add_command(label=element, command=lambda value=element: pattern_info.var_tkinter_groupe.set(value))
            pattern_info.widget_liste_groupe["menu"] = menu 
            return pattern_info
            
    def ActualiseVariable_tchek(self,*args):
            for key in list(self.dict_pattern_centralle.keys()):
                pattern_info = self.dict_pattern_centralle[key]
                pattern = pattern_info.var_tkinter_pattern.get()
                # pattern_info = pattern_constructor()
                pattern_info.liste_groupe = self.get_len_groupe(pattern)
                pattern_info = self.actualiser_liste(pattern_info)
                pattern_info.var_tkinter_sortie.set(self.get_to_contenu(pattern,pattern_info.var_tkinter_groupe.get(),pattern_info.type))
                self.dict_pattern_centralle[key] = pattern_info
            print("\n")
                
    def get_IfKeysPress(self):
        for key in list(self.dict_pattern_centralle.keys()):
            all_widget = self.dict_pattern_centralle[key]
            all_widget.widget_pattern.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
            all_widget.widget_liste_groupe.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
            all_widget.widget_label.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
        
    def set_IfKeysPress(self,widget_tkinter):
        widget_tkinter.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
        
    def main_constructor(self):
        self.cree_pattern_instance("id")
        self.cree_pattern_instance("date")
        self.cree_pattern_instance("ttc",type="int")
        self.cree_pattern_instance("provenance")
        self.get_IfKeysPress()
        self.fenetre.mainloop()
        
# Lancement de la boucle principale

test = grahpique()
test.main_constructor()
