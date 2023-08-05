class ModelFacture(facture_fonction_commun):
    def __init__(self,path_facture_amazon_prime) -> None:
        super().__init__()
        self.provenance = "Adobe"
        print(f"instance : {self.provenance} active")
        self.facture["path"] = path_facture_amazon_prime
        self.facture["name"] = os.path.basename(path_facture_amazon_prime) 
        self.PATTERN_ID = r'inserer pattern en Regex'
        self.PATTERN_DATE =  r"inserer pattern en Regex"
        self.PATTERN_PRIX_TTC = r"inserer pattern en Regex"
        self.pattern_provenance_siren = "inserer le siret ou un qui dure dans le temps (les information legal sont ideals)"
        print(re.search(self.pattern_provenance_siren,self.contenue_pdf))
        self.get_contenue_pdf()
        if  self.pattern_provenance_siren in self.contenue_pdf:
            self.run_programme_model()
        else:
            print(f"se n'ai pas une facture {self.provenance}")
        
    def get_ID(self,contenue):
        numero_commande = re.search(self.PATTERN_ID,contenue)
        if numero_commande:
           return str(numero_commande.group(1))
            # print("Numéro de commande:", numero_commande)
        else:
            return None
            print("Aucun numéro de commande trouvé.")

    def get_nom_produit(self,contenue):
        return "amazon_prime"
    
    def get_date_achat(self,contenue):
        date_commande = re.search(self.PATTERN_DATE,contenue)

        if date_commande:
                return str(date_commande.group(0))
            # print("Date :", self.DATE_ACHAT)
                # print("Aucune date trouvée.")
        else:
            return None

    def get_prix_ttc(self,contenue):
        prix_total_TTC = re.search(self.PATTERN_PRIX_TTC,contenue)
        if prix_total_TTC:
            return prix_total_TTC.group(1)
            # print("Prix :", prix_total_TTC)
        else:
            return None
            # print("Aucun prix trouvé.")
        