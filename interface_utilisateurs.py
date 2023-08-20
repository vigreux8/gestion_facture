import tkinter as tk
from Setting.CONSTANTE import FOLDER_LOCAL
from fonctions.fonction_models_commun import facture_fonction_commun
import os


class tool_pattern_constructor():
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

class provenance_tchekeur_constructors():
    def __init__(self) -> None:
        
        self.varchar_name = None
        self.varchar_entree =  None
        self.varchar_out =  None
        
        self.widget_name = None
        self.widget_entree = None
        self.widget_out = None


class tools_tkinter():
    def __init__(self) -> None:
        self.last_row_element = 0
        self.dict_widget_centralle = {}
        self.fenetre = self.init_fenetre()        
        
    def add_widget_provenance(self,nom,):
        autre_widget_info = provenance_tchekeur_constructors()
        #init variable tkinter
        autre_widget_info.varchar_name = self.init_variable_tkinter(nom)
        autre_widget_info.varchar_entree = self.init_variable_tkinter("saisir donner fixe ex : tva/siren/adresse")
        autre_widget_info.varchar_out = self.init_variable_tkinter("False")
        
        #init widget
        autre_widget_info.widget_name = self.tkinter_affichage_texte( autre_widget_info.varchar_name,self.last_row_element,0)
        autre_widget_info.widget_entree = self.tkinter_saisi_texte(autre_widget_info.varchar_entree,self.last_row_element,1)
        autre_widget_info.widget_out = self.tkinter_affichage_texte(autre_widget_info.varchar_out,self.last_row_element,2)
        self.dict_widget_centralle[nom] = autre_widget_info
    
    def cree_provenance_tchekeur(self):
        self.add_widget_provenance("provenance")
        
        
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
        
    def tkinter_saisi_texte(self,tkinter_variable,v_row=1,v_column=2):
        widget_saisi_texte = tk.Entry(self.fenetre,textvariable=tkinter_variable)
        widget_saisi_texte.delete("0", "end")
        widget_saisi_texte.grid(row=v_row,column=v_column)
        return widget_saisi_texte

    def tkinter_affichage_texte(self,varchart_tk,v_row,v_col):
        varString = tk.Label(self.fenetre,textvariable=varchart_tk)
        varString.grid(row=v_row,column=v_col)
        return varString
    
    def tkinter_bouton_liste(self, var_tkinter, liste=[0, 1, 2], v_row=1, v_column=1) -> object:
        widget_menu_deroulant = tk.OptionMenu(self.fenetre, var_tkinter, *liste )
        widget_menu_deroulant.grid(row=v_row,column= v_column)
        return widget_menu_deroulant

    def tkinter_menus_bas_page(self):
        self.cree_provenance_tchekeur()
    
    def get_tkinter_info_IfKeysPress(self):
        for key in list(self.dict_pattern_centralle.keys()):
            all_widget = self.dict_pattern_centralle[key]
            all_widget.widget_pattern.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
            all_widget.widget_liste_groupe.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
            all_widget.widget_label.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
        self.dict_widget_centralle["provenance"].widget_entree.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
    def set_tkinter_info_IfKeysPress(self,widget_tkinter):
        widget_tkinter.bind("<KeyPress-Return>", self.ActualiseVariable_tchek)
        
        
class grahpique_constructors(facture_fonction_commun,tools_tkinter):
    def __init__(self) -> None:
        facture_fonction_commun.__init__(self,self.get_instance_Test_facture())
        tools_tkinter.__init__(self)
        self.contenue_py = None
        self.nom_fichier_sortie = None
        self.dict_pattern_centralle = {}
        self.get_contenue_pdf()

    def cree_pattern_instance(self,nom_pattern : str, type = "str",):
        pattern_build = tool_pattern_constructor()
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
            pattern = tool_pattern_constructor()
            rajouts = 'self.add_pattern(self,key: str,pattern : str,group : int,type : str,position_sheet: int)'
            element_rechercher = recherche
            with open(FOLDER_LOCAL.TEMPLATE_MODEL,"r") as facture_template:
                contenue_py = facture_template.read()
            position_depart = contenue_py.find(element_rechercher)+len(recherche)
            contenu_py_modifier = contenue_py[:position_depart]+"\n"+"\t\t"+rajouts+contenue_py[position_depart:]
            print(contenu_py_modifier)
            self.contenue_py = contenu_py_modifier
            

        #crée une variable de class 

    def actualiser_liste(self,pattern_info):
            # pattern_info = pattern_constructor()
            menu = pattern_info.widget_liste_groupe["menu"]
            menu.delete(0, "end")
            for element in pattern_info.liste_groupe:
                menu.add_command(label=element, command=lambda value=element: pattern_info.var_tkinter_groupe.set(value))
            pattern_info.widget_liste_groupe["menu"] = menu 
            return pattern_info
    
    def if_motif_in_pdf(self,motif):
        if motif == "" or len(motif) < 3:
            motif = "notinpdf"
        if motif in self.contenue_pdf_byte:
            return True
        else : 
            return False
    
    def ActualiseVariable_tchek(self,*args):
            pattern_de_provenance = self.dict_widget_centralle["provenance"].varchar_entree.get()
            
            if self.if_motif_in_pdf(pattern_de_provenance):
                self.dict_widget_centralle["provenance"].varchar_out.set("True")
            else :
                self.dict_widget_centralle["provenance"].varchar_out.set("False")
                    
            for key in list(self.dict_pattern_centralle.keys()):
                pattern_info = self.dict_pattern_centralle[key]
                pattern = pattern_info.var_tkinter_pattern.get()
                # pattern_info = pattern_constructor()
                pattern_info.liste_groupe = self.get_len_groupe(pattern)
                pattern_info = self.actualiser_liste(pattern_info)
                pattern_info.var_tkinter_sortie.set(self.get_to_contenu(pattern,pattern_info.var_tkinter_groupe.get(),pattern_info.type))
                self.dict_pattern_centralle[key] = pattern_info
      
            print("\n")       

    def main_constructor(self):
        self.cree_pattern_instance("id")
        self.cree_pattern_instance("date")
        self.cree_pattern_instance("ttc",type="int")
        self.tkinter_menus_bas_page()
        self.get_tkinter_info_IfKeysPress()
        self.fenetre.mainloop()
        
# Lancement de la boucle principale

test = grahpique_constructors()
test.main_constructor()
