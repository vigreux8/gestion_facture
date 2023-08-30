import tkinter as tk
from Setting.CONSTANTE import FOLDER_LOCAL, ALPHABET
from fonctions.fonction_models_commun import facture_fonction_commun
import os

# permettre au fichier google sheet d'être 
#quand on upload des fichier le programme regarde les dossier inconnue et facture a traiter


class widget_basic():
    def __init__(self) -> None:
        self.var_tkinter_saisie : tk.StringVar = None 
        self.widget_saisie : tk.Entry  = None
        
    def get_saisie(self):
        return self.var_tkinter_saisie.get()
            

    
class all_var_widget_info(widget_basic):
    def __init__(self) -> None:
        super().__init__()
        self.pattern = None
        self.type_traduit = None
        self.liste_groupe = [0]
        self.var_tkinter_type :tk.StringVar = None
        self.var_tkinter_groupe :tk.IntVar = None
        self.var_tkinter_nom :tk.StringVar = None
        self.var_tkinter_sortie :tk.StringVar or tk.IntVar  = None
        self.var_tkinter_emplacement_sheets : tk.StringVar = None
        self.widget_emplacement_sheets = None
        self.widget_liste_groupe : tk.OptionMenu = None
        self.widget_nom : tk.Label = None
        self.widget_sortie : tk.Entry = None
        self.widget_type : tk.OptionMenu = None
    
    def get_var_widget_varchar_groupe(self):
        return self.widget_liste_groupe,self.var_tkinter_groupe

class tkinter_tools():
    def __init__(self) -> None:
        self.last_row_element = 0
        self.fenetre = self.init_fenetre()  
        self.widget_pattern_id_unique : widget_basic= ""
        self.dict_pattern_centralle : dict[str,all_var_widget_info] = {}
        self.dict_widget_menu : dict[str,widget_basic] = {}
        self.dict_translate_type : dict[str,str] ={
            "montant" : "int",
            "date" : "date",
            "normale" : "str"
        }
        self.dict_transle_type_inver = {valeur : clé for clé, valeur in self.dict_pattern_centralle.items()}
    
    def _init_widget_var_saisie_texte(self,nom,valeur_var_tkinter,v_row,v_col):
        nom_fichier_instance = widget_basic()
        nom_fichier_instance.var_tkinter_saisie = self.init_variable_tkinter(valeur_var_tkinter)
        nom_fichier_instance.widget_saisie = self.tkinter_saisi_texte(nom_fichier_instance.var_tkinter_saisie,v_row=v_row,v_column=v_col,keep_texte_default=True)
        self.dict_widget_menu[nom] = nom_fichier_instance
        
    def add_widget_provenance(self,nom,):
        autre_widget_info = all_var_widget_info()
        #init variable tkinter
        autre_widget_info.var_tkinter_nom = self.init_variable_tkinter(nom)
        autre_widget_info.var_tkinter_saisie = self.init_variable_tkinter("saisir donner fixe ex : tva/siren/adresse")
        autre_widget_info.var_tkinter_sortie = self.init_variable_tkinter("False")
        
        #init widget
        autre_widget_info.widget_nom = self.tkinter_affichage_texte( autre_widget_info.var_tkinter_nom,self.last_row_element,0)
        autre_widget_info.widget_saisie = self.tkinter_saisi_texte(autre_widget_info.var_tkinter_saisie,self.last_row_element,1)
        autre_widget_info.widget_sortie = self.tkinter_affichage_texte(autre_widget_info.var_tkinter_sortie,self.last_row_element,2)
        self.widget_pattern_id_unique = autre_widget_info
    
    def cree_provenance_tchekeur(self):
        self.add_widget_provenance("provenance")
        
    def init_fenetre(self):
        fenetre = tk.Tk()
        # fenetre.geometry("800x800")
        fenetre.title("Fenêtre avec Menu Déroulant")
        return fenetre

    def tkinter_saisi_texte(self,varchart_tk,v_row=1,v_column=2,keep_texte_default = False):
        widget_saisi_texte = tk.Entry(self.fenetre,textvariable=varchart_tk)
        if not keep_texte_default:
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

  
    
    def print_helloworkd(self):
        print("hello_world")
    
    def tkinter_boutons(self,texte,fonction_declencher,v_row,v_col):
       bouton = tk.Button(self.fenetre,text=texte,command=fonction_declencher)
       bouton.grid(row=v_row,column=v_col)
    
    def set_variable_tkinter_in_instance_pattern(self,nom_pattern,type = "str" , Emplacement_google_sheets = None) -> all_var_widget_info:
        pattern_build = all_var_widget_info()
        pattern_build.var_tkinter_nom = self.init_variable_tkinter(nom_pattern)
        pattern_build.var_tkinter_sortie = self.init_variable_tkinter("None")
        pattern_build.var_tkinter_saisie = self.init_variable_tkinter("saisir pattern")
        pattern_build.var_tkinter_groupe = self.init_variable_tkinter(0,"int")
        pattern_build.var_tkinter_type = self.init_variable_tkinter(type)
        pattern_build.type_traduit = self.dict_translate_type[type]
        if Emplacement_google_sheets:
            pattern_build.var_tkinter_emplacement_sheets = self.init_variable_tkinter(f"{ALPHABET.COLONNE_GOOGLE_SHEETS[len(self.dict_pattern_centralle)]}")
        else:
            pattern_build.var_tkinter_emplacement_sheets = self.init_variable_tkinter(Emplacement_google_sheets)
        return pattern_build
        
    def init_variable_tkinter(self,info_visible,type="str"):
        if type == "str":
            association = tk.StringVar()
            association.set(info_visible)  # Définir la première option comme valeur par défaut
        elif type =="int":
            association = tk.IntVar()
            association.set(info_visible)
        return association
        
    def set_widget_pattern(self,pattern_info : all_var_widget_info) ->all_var_widget_info:
            pattern_info.widget_nom = self.tkinter_affichage_texte(pattern_info.var_tkinter_nom,self.last_row_element,0)
            pattern_info.widget_saisie = self.tkinter_saisi_texte(pattern_info.var_tkinter_saisie,self.last_row_element,1)
            pattern_info.widget_liste_groupe = self.tkinter_bouton_liste(pattern_info.var_tkinter_groupe,pattern_info.liste_groupe,self.last_row_element,2)
            pattern_info.widget_type = self.tkinter_bouton_liste(pattern_info.var_tkinter_type,["normale","montant","date"],self.last_row_element,3)
            pattern_info.widget_sortie = self.tkinter_affichage_texte(pattern_info.var_tkinter_sortie,self.last_row_element,4)
            pattern_info.widget_emplacement_sheets = self.tkinter_saisi_texte(pattern_info.var_tkinter_emplacement_sheets,self.last_row_element,5,keep_texte_default=True)
            self.last_row_element +=1
            return pattern_info
        
    def copy_to_clipboard(self):
            self.fenetre.clipboard_clear()
            self.fenetre.clipboard_append(self.contenue_pdf_str.decode('utf-8'))
        
    

class tkinter_menu_creators(tkinter_tools):
    #initalise tout les menus
    def __init__(self) -> None:
        super().__init__()
        
    def tkinter_haut_page(self):
        self.tkinter_affichage_texte(self.init_variable_tkinter("nom"),0,0)
        self.tkinter_affichage_texte(self.init_variable_tkinter("pattern"),0,1)
        self.tkinter_affichage_texte(self.init_variable_tkinter("groupe"),0,2)
        self.tkinter_affichage_texte(self.init_variable_tkinter("type"),0,3)
        self.tkinter_affichage_texte(self.init_variable_tkinter("sortie"),0,4)
        self.last_row_element +=1
        
        
    def tkinter_cree_pattern(self,nom_pattern : str, type = "normale",emplacement_google_sheet = None):
        pattern_build = self.set_widget_pattern(self.set_variable_tkinter_in_instance_pattern(nom_pattern,type,emplacement_google_sheet))

        self.dict_pattern_centralle[nom_pattern] = pattern_build
    
    def tkinter_options(self):
        self.cree_provenance_tchekeur()
        self.last_row_element +=1
        self.tkinter_boutons("appliquer",self.ActualiseVariable,1,7)
        self.tkinter_boutons("cree models facture",self.cree_fichier_model_facture,1,6)
        self._init_widget_var_saisie_texte("nom fichier","nom_default",2,6)
        self.tkinter_boutons("copy texte pdf",self.copy_to_clipboard,self.last_row_element,1)
        
        
        
class grahpique_constructors(tkinter_menu_creators,facture_fonction_commun,):
    '''
    set_all_content_to_pdf() : fonctions surecrite elle ecrase celle present dans facture_fonction_commun()
    '''
    
    def __init__(self) -> None:
        facture_fonction_commun.__init__(self,self.get_instance_Test_facture())
        tkinter_menu_creators.__init__(self)
        self.contenue_py = None
        self.nom_provenance = None

    def set_all_content_to_pdf(self,instance_pattern : all_var_widget_info) -> all_var_widget_info:  
        #fonctions sur-ecrite  elle existe aussi sur fonction model communs qui utiliser tout les pattern trouver dans les model de facture
            sortie = self.get_to_contenu(instance_pattern.pattern,instance_pattern.var_tkinter_groupe.get(),instance_pattern.type_traduit)
            try:
                if instance_pattern.type_traduit == "date":
                    instance_pattern.var_tkinter_sortie.set(self.f_date(sortie.strip().lower()))
                    return instance_pattern
                elif  instance_pattern.type_traduit == "int":
                    instance_pattern.var_tkinter_sortie.set(sortie.replace(".",","))
                    return instance_pattern
            except:
                if instance_pattern.type_traduit == "date" or instance_pattern.type_traduit == "int":
                    print("la date ne se transforme pas correctement")
                instance_pattern.var_tkinter_sortie.set(sortie) 
                return instance_pattern
            else:
                instance_pattern.var_tkinter_sortie.set(sortie) 
                return instance_pattern
                
   

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
            self.contenue_py = facture_template.replace('"numero unique"',f'"{self.widget_pattern_id_unique.var_tkinter_saisie.get()}"')
            self.contenue_py = self.contenue_py.replace('"nom_provenance"',f'"{self.nom_provenance}"')
            
        for key in list(self.dict_pattern_centralle.keys()):
            contenu_py_modifier = self.contenue_py
            pattern_info = self.dict_pattern_centralle[key]
            nom = pattern_info.var_tkinter_nom.get()
            pattern = pattern_info.var_tkinter_saisie.get()
            groupe = pattern_info.var_tkinter_groupe.get()
            type = pattern_info.type_traduit
            emplacement_sheet =  pattern_info.var_tkinter_emplacement_sheets.get()
            rajouts = f'self.add_pattern(r"{nom}","{pattern}",{groupe},"{type}","{emplacement_sheet}")'
            element_rechercher = recherche
            position_depart = contenu_py_modifier.find(element_rechercher)+len(recherche)
            contenu_py_modifier = contenu_py_modifier[:position_depart]+"\n"+"        "+rajouts+"\n"+contenu_py_modifier[position_depart:]
            self.contenue_py = contenu_py_modifier
        

        #crée une variable de class 

    def actualiser_liste(self,pattern_info :all_var_widget_info):
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
            pattern_de_provenance = self.widget_pattern_id_unique.var_tkinter_saisie.get()
            
            if self.if_motif_in_pdf(pattern_de_provenance):
                self.widget_pattern_id_unique.var_tkinter_sortie.set("True")
            else :
                self.widget_pattern_id_unique.var_tkinter_sortie.set("False")
            for key in list(self.dict_pattern_centralle.keys()):
                pattern_info = self.dict_pattern_centralle[key]
                pattern_info.type_traduit = self.dict_translate_type[pattern_info.var_tkinter_type.get()]
                pattern_info.pattern = pattern_info.var_tkinter_saisie.get().strip()
                pattern_info.liste_groupe = self.get_len_groupe(pattern_info.pattern)
                pattern_info = self.actualiser_liste(pattern_info)
                pattern_info = self.set_all_content_to_pdf(pattern_info)
                self.dict_pattern_centralle[key] = pattern_info
      
            print("\n")       
    
    def if_set_tkinter_type(self,pattern_info : all_var_widget_info,cles : str):
        if cles in list(self.dict_translate_type.keys()) :
            pattern_info.type_traduit.set(self.dict_translate_type[cles])
        elif cles in list(self.dict_transle_type_inver) : 
             pattern_info.type_traduit.set[self.dict_transle_type_inver[cles]]
        return pattern_info
            
        
    def rename_all_type(self,pattern_info : all_var_widget_info):
        pattern_info = self.if_set_tkinter_type(pattern_info,"normale")
        pattern_info = self.if_set_tkinter_type(pattern_info,"date")
        pattern_info = self.if_set_tkinter_type(pattern_info,"montant")
        return pattern_info

        
    
    
    def main_constructor(self):
        if self.if_fichier_test_present:
            self.get_contenue_pdf()
            self.tkinter_haut_page()
            self.tkinter_cree_pattern("id","normale","D")
            self.tkinter_cree_pattern("date","date","B")
            self.tkinter_cree_pattern("ttc","montant","C")
            self.tkinter_options()
            # self.get_tkinter_info_IfKeysPress()
            self.fenetre.mainloop()
        
# Lancement de la boucle principale


