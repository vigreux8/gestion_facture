import tkinter as tk

class VotreClasse:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.main_constructor()

    def main_constructor(self):
        options = ["Option 1", "Option 2", "Option 3"]
        self.var_selection = tk.StringVar(value=options[0])  # Sélection par défaut
        
        option_menu = tk.OptionMenu(self.fenetre, self.var_selection, *options)
        option_menu.pack()

        self.var_selection.trace_add("write", self.actualiser_selection)

        self.fenetre.mainloop()

    def actualiser_selection(self, *args):
        nouvelle_selection = self.var_selection.get()
        print("Nouvelle sélection :", nouvelle_selection)

# Création de la fenêtre principale
root = tk.Tk()
app = VotreClasse(root)
root.mainloop()
