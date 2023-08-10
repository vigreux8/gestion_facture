import tkinter as tk

def afficher_selection():
    selected_item = combo.get()
    print("Choix sélectionné:", selected_item)

# Liste des choix
choix_liste = ["Option 1", "Option 2", "Option 3", "Option 4"]


class grahpique():
    def __init__(self) -> None:
        self.fenetre = self.init_fenetre()
        self.group_valeur = self.init_variable_tkinter("groupe_valeurs")
        self.pattern_id = self.init_variable_tkinter("saisir patern_id")
        self.main_constructor()

    def init_fenetre(self):
        fenetre = tk.Tk()
        # fenetre.geometry("800x800")
        fenetre.title("Fenêtre avec Menu Déroulant")
        return fenetre
    
    @staticmethod
    def init_variable_tkinter(nom):
        association = tk.StringVar()
        association.set(nom)  # Définir la première option comme valeur par défaut
        return association
    
    def bouton_liste(self,variable_tkinter,liste,v_row=1,v_column=1):
        menu_deroulant = tk.OptionMenu(self.fenetre,variable_tkinter,*liste )
        menu_deroulant.grid(row=v_row,column= v_column)
        return menu_deroulant
    
    def actualiser_selection(self,*args):
            nouvelle_selection = self.group_valeur.get()
            print("Nouvelle sélection :", nouvelle_selection)
            saisi = self.pattern_id.get()
            print(saisi)

    def main_constructor(self):
        liste =  self.bouton_liste(self.group_valeur,["1","2","3"],1,1)
        liste.pack()
        saisi = tk.Entry(self.fenetre,textvariable=self.pattern_id)
        saisi.pack()
        saisi.bind("<KeyPress-Return>", self.actualiser_selection)
        self.fenetre.mainloop()
        
# Lancement de la boucle principale

test = grahpique()