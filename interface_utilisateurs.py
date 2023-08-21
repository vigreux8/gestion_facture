import tkinter as tk
from Setting.CONSTANTE import FOLDER_LOCAL
from fonctions.fonction_models_commun import facture_fonction_commun
import os

# a faire refactoring pour faciliter la maintenabiliter
#generer un fichier avec les varialbe des pattern trouver
#

class widget_basic():
    def __init__(self) -> None:
        self.var_tkinter_saisie = None 
        self.widget_saisie = None
        
    def get_saisie(self):
        return self.var_tkinter_saisie.get()
            

    
class tool_widget_constructor(widget_basic):
    def __init__(self) -> None:
        super().__init__()
        self.pattern = None
        self.type_date = False
        self.liste_groupe = [0]
        self.var_tkinter_type = None
        self.var_tkinter_groupe = None
        self.var_tkinter_nom = None
        self.var_tkinter_sortie = None
        self.var_tkinter_emplacement_sheets = None
        self.widget_emplacement_sheets = None
        self.widget_liste_groupe = None
        self.widget_nom = None
        self.widget_sortie = None
        self.widget_type = None
    
    def get_var_widget_varchar_groupe(self):
        return self.widget_liste_groupe,self.var_tkinter_groupe



class preset_tkinter_menue():
    
    def template_widget_pattern(self,pattern_info):
            pattern_info.widget_nom = self.tkinter_affichage_texte(pattern_info.var_tkinter_nom,self.last_row_element,0)
            pattern_info.widget_saisie = self.tkinter_saisi_texte(pattern_info.var_tkinter_saisie,self.last_row_element,1)
            pattern_info.widget_liste_groupe = self.tkinter_bouton_liste(pattern_info.var_tkinter_groupe,pattern_info.liste_groupe,self.last_row_element,2)
            pattern_info.widget_type = self.tkinter_bouton_liste(pattern_info.var_tkinter_type,["str","int","date"],self.last_row_element,3)
            pattern_info.widget_sortie = self.tkinter_affichage_texte(pattern_info.var_tkinter_sortie,self.last_row_element,4)
            self.last_row_element +=1
            return pattern_info
    
    

class tools_tkinter(preset_tkinter_menue):
    def __init__(self) -> None:
        super().__init__()
        self.last_row_element = 0
        self.dict_widget_pattern = {}
        self.dict_widget_menu = {}
        
        self.fenetre = self.init_fenetre()  
    
    def widget_saisie_texte_independant(self,nom,valeur_var_tkinter,v_row,v_col):
        nom_fichier_instance = widget_basic()
        nom_fichier_instance.var_tkinter_saisie = self.init_variable_tkinter(valeur_var_tkinter)
        nom_fichier_instance.widget_saisie = self.tkinter_saisi_texte(nom_fichier_instance.var_tkinter_saisie,v_row=v_row,v_column=v_col,texte_default=True)
        self.dict_widget_menu[nom] = nom_fichier_instance
        
    def add_widget_provenance(self,nom,):
        autre_widget_info = tool_widget_constructor()
        #init variable tkinter
        autre_widget_info.var_tkinter_nom = self.init_variable_tkinter(nom)
        autre_widget_info.var_tkinter_saisie = self.init_variable_tkinter("saisir donner fixe ex : tva/siren/adresse")
        autre_widget_info.var_tkinter_sortie = self.init_variable_tkinter("False")
        
        #init widget
        autre_widget_info.widget_nom = self.tkinter_affichage_texte( autre_widget_info.var_tkinter_nom,self.last_row_element,0)
        autre_widget_info.widget_saisie = self.tkinter_saisi_texte(autre_widget_info.var_tkinter_saisie,self.last_row_element,1)
        autre_widget_info.widget_sortie = self.tkinter_affichage_texte(autre_widget_info.var_tkinter_sortie,self.last_row_element,2)
        self.dict_widget_pattern[nom] = autre_widget_info
    
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
        
    def tkinter_saisi_texte(self,varchart_tk,v_row=1,v_column=2,texte_default = False):
        widget_saisi_texte = tk.Entry(self.fenetre,textvariable=varchart_tk)
        if not texte_default:
            widget_saisi_texte.delete("0", "end")
        widget_saisi_texte.grid(row=v_row,column=v_column)
        return widget_saisi_texte

    def tkinter_affichage_texte(self,varchart_tk,v_row,v_col):
        ta_mere =  varchart_tk.get()
        varString = tk.Label(self.fenetre,textvariable=varchart_tk)
        varString.grid(row=v_row,column=v_col)
        return varString
    
    def tkinter_bouton_liste(self, var_tkinter, liste=[0, 1, 2], v_row=1, v_column=1) -> object:
        widget_menu_deroulant = tk.OptionMenu(self.fenetre, var_tkinter, *liste )
        widget_menu_deroulant.grid(row=v_row,column= v_column)
        return widget_menu_deroulant

    def tkinter_menus_bas_page(self):
        self.cree_provenance_tchekeur()
        self.last_row_element +=1
        self.tkinter_boutons("appliquer",self.ActualiseVariable,0,6)
        self.tkinter_boutons("cree models facture",self.cree_fichier_model_facture,0,7)
        self.widget_saisie_texte_independant("nom fichier","nom_default",1,7)
    
    def print_helloworkd(self):
        print("hello_world")
    
    # def get_tkinter_info_IfKeysPress(self):
    #     # for key in list(self.dict_pattern_centralle.keys()):
    #     #     all_widget = self.dict_pattern_centralle[key]
    #     #     all_widget.widget_saisie.bind("<KeyPress-Return>", self.ActualiseVariable_tchek_pattern)
    #     #     all_widget.widget_liste_groupe.bind("<KeyPress-Return>", self.ActualiseVariable_tchek_pattern)
    #     #     all_widget.widget_nom.bind("<KeyPress-Return>", self.ActualiseVariable_tchek_pattern)
    #     # self.dict_widget_pattern["provenance"].widget_saisie.bind("<KeyPress-Return>", self.ActualiseVariable_tchek_pattern)
    #     # self.dict_widget_pattern["provenance"].widget_saisie.bind("<KeyPress-Return>", self.ActualiseVariable_tchek_pattern)

    # def set_tkinter_info_IfKeysPress(self,widget_tkinter):
    #     widget_tkinter.bind("<KeyPress-Return>", self.ActualiseVariable_tchek_pattern)

    def tkinter_boutons(self,texte,fonction_declencher,v_row,v_col):
       bouton = tk.Button(self.fenetre,text=texte,command=fonction_declencher)
       bouton.grid(row=v_row,column=v_col)
        
class grahpique_constructors(facture_fonction_commun,tools_tkinter):
    def __init__(self) -> None:
        facture_fonction_commun.__init__(self,self.get_instance_Test_facture())
        tools_tkinter.__init__(self)
        self.contenue_py = None
        self.nom_provenance = None
        self.dict_pattern_centralle = {}
        self.get_contenue_pdf()


    def cree_pattern(self,nom_pattern : str, type = "str",):
        pattern_build = tool_widget_constructor()
        pattern_build.var_tkinter_nom = self.init_variable_tkinter(nom_pattern)
        pattern_build.var_tkinter_sortie = self.init_variable_tkinter("None")
        pattern_build.var_tkinter_saisie = self.init_variable_tkinter("saisir pattern")
        pattern_build.var_tkinter_groupe = self.init_variable_tkinter(0,"int")
        pattern_build.var_tkinter_type = self.init_variable_tkinter("str")
        pattern_build.var_tkinter_emplacement_sheets = self.init_variable_tkinter("None")
        
        pattern_build = self.template_widget_pattern(pattern_build)
        self.dict_pattern_centralle[nom_pattern] = pattern_build
        
    
    
    def cree_fichier_model_facture(self):
        self.fichier_py_Rajouter_pattern()
        path_complet = os.path.join(FOLDER_LOCAL.MODEL_FACTURE,f"model_{self.nom_provenance}.py") 
        if os.path.exists(path_complet):
            "le fichier existe dejat, changer de nom"
        else:
            with open(path_complet,"w", encoding="utf-8" ) as fichier:
                fichier.write(self.contenue_py)
    
    def fichier_py_Rajouter_pattern(self,recherche='#1'):
        with open(FOLDER_LOCAL.TEMPLATE_MODEL,"r") as facture_template:
            facture_template = facture_template.read()
            self.contenue_py = facture_template.replace('"numero unique"',f'"{self.dict_widget_pattern["provenance"].var_tkinter_saisie.get()}"')
            self.contenue_py = self.contenue_py.replace('"nom_provenance"',f'"{self.nom_provenance}"')
            
        for key in list(self.dict_pattern_centralle.keys()):
            contenu_py_modifier = self.contenue_py
            pattern_info = self.dict_pattern_centralle[key]
            nom = pattern_info.var_tkinter_nom.get()
            pattern = pattern_info.var_tkinter_saisie.get()
            groupe = pattern_info.var_tkinter_groupe.get()
            type = pattern_info.var_tkinter_type.get()
            emplacement_sheet =  pattern_info.var_tkinter_emplacement_sheets.get()
            rajouts = f'self.add_pattern(self,"{nom}","{pattern}",{groupe},"{type}","{emplacement_sheet}")'
            element_rechercher = recherche
            position_depart = contenu_py_modifier.find(element_rechercher)+len(recherche)
            contenu_py_modifier = contenu_py_modifier[:position_depart]+"\n"+"        "+rajouts+contenu_py_modifier[position_depart:]
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
        
    def ActualiseVariable(self,*args):
            self.nom_provenance = self.dict_widget_menu["nom fichier"].get_saisie()
            pattern_de_provenance = self.dict_widget_pattern["provenance"].var_tkinter_saisie.get()
            
            if self.if_motif_in_pdf(pattern_de_provenance):
                self.dict_widget_pattern["provenance"].var_tkinter_sortie.set("True")
            else :
                self.dict_widget_pattern["provenance"].var_tkinter_sortie.set("False")
            for key in list(self.dict_pattern_centralle.keys()):
                pattern_info = self.dict_pattern_centralle[key]
                if pattern_info.var_tkinter_type == "date":
                    pattern_info.type_date = True
                else:
                    pattern_info.type_date = False
                pattern = pattern_info.var_tkinter_saisie.get()
                pattern_info.liste_groupe = self.get_len_groupe(pattern)
                pattern_info = self.actualiser_liste(pattern_info)
                pattern_info.var_tkinter_sortie.set(self.get_to_contenu(pattern,pattern_info.var_tkinter_groupe.get(),pattern_info.var_tkinter_type.get()))
                self.dict_pattern_centralle[key] = pattern_info
      
            print("\n")       

    def main_constructor(self):
        self.cree_pattern("id")
        self.cree_pattern("date")
        self.cree_pattern("ttc",type="int")
        self.tkinter_menus_bas_page()
        # self.get_tkinter_info_IfKeysPress()
        self.fenetre.mainloop()
        
# Lancement de la boucle principale

test = grahpique_constructors()
test.main_constructor()
