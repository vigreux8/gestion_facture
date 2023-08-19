# central_facture


![Badge de version](https://img.shields.io/badge/version-1.0.0-blue)
<!-- Vous pouvez ajouter d'autres badges ici à partir de shields.io -->
# to-do-list
- [ ] Gerer la gestion des messages dans le terminal
  - [ ] indiquer le nb de fichier present dans chaque dossier
  - [ ] indiquer si il a rajouter la facture avec succées ou non 
  - [ ] proposer de fermer de le programme (le mettre dans une boucle while)
- [ ] crée un system pour tester les facture simplement
  - [ ] dossier test 
  - [ ] fonction pour recuperer le fichier dans le dossier test


  - [ ] '''recrire pattern id, date, ttc de base dans une fonction basique 
        format patterne
        def cree_pattern(self,nom_pattern,pattern:str,type:str,):
        self.list_pattern[nom_pattern] = {"pattern":pattern,
                                    "Nb_groupe": None,
                                    "type" : type ,
                                    "colonne_sheets" : None
                                    }
        '''


# **Gestion Centralisée des Factures**

## **1. Stockage Centralisé et Sécurisé**
- Centralisation de toutes vos factures en un seul endroit grâce à l'intégration avec Google Drive.

## **2. Gestion Dynamique des Modèles de Factures**
- Détection automatique de la provenance des factures grâce à un système dynamique de modèles.
- Création et téléchargement de modèles de factures personnalisés pour une flexibilité accrue.

## **3. Intégration Avancée avec Google Sheets**
- Vérification de la présence du fichier dans Google Sheets à l'aide de l'ID pour éviter les doublons.
- Renommage automatique des fichiers selon un format standardisé (exemple : `provenance_id.pdf`).

## **4. Traitement Intelligent des Erreurs**
- Placement automatique des factures inconnues dans un dossier spécifique sur Google Drive et localement.
- Gestion des factures avec des informations manquantes en les plaçant dans un dossier dédié sur Google Drive et localement.
- Pas besoin de communications supplémentaires : vérifiez simplement le dossier Google Drive pour des mises à jour, en particulier si plusieurs collègues utilisent l'application.

## **5. Capture et Conversion Automatisée des Données**
- Extraction automatique des dates avec prise en charge de divers formats.
- Capture précise du prix TTC.
- Flexibilité pour ajouter d'autres informations de capture selon les besoins.

## **6. Creation de prompt Intelligente**
- En cas de facture inconnue, un prompte chatgpt et générer dans contenue pdf(evite de payer l'api chatgpt)
# 🚀 Démarrage

# Clonez ce dépot
```bash
git clone https://github.com/vigreux8/gestion_facture.git
```

### 📋 Prérequis
- python 3.10.7
- virtualenv



# Allez dans le dossier de votre projet
cd nom-du-projet

# Installation
### installer virtualenv
```bash
pip install virtualenv
```
### créez l'environnement virtuels

```bash
virtualenv .venv
```
### activer l'environnement virtuelle
```bash
venv\Scripts\activate
```

### installer les dépendances
```bash
pip install -r requirements.txt
```

# créez un espace dans votre google drive avec se format de fichier
Recuperer l'id de chaque dossier
```bash
-Facture 
    --sheets
    --facture
        ---facture_tampon
        ---facture_archiver
        ---facture_inconnue
        ---facture_donner manquante
```
# récupérez l'id de chaque fichier 
acceder au fichier CONSTANTE  qui se trouve --> Setting/CONSTANTE.PY 
```python
# mettez vos identifiants
""".......code ...... ligne 47"""
class FOLDER_GOOGLEDRIVE():
    ID_DOSSIER_FACTURE_ARCHIVER = "Coller l'id"
    ID_DOSSIER_FACTURE_INCONNUE = "Coller l'id"
    ID_DOSSIER_FACTURE_TAMPON = "Coller l'id"
    ID_DOSSIER_FACTURE_DONNER_MANQUANTE = "Coller l'id"
```

# connectez votre google drive au projet
- [Accédez a google clound](https://cloud.google.com/gcp/?hl=fr&utm_source=google&utm_medium=cpc&utm_campaign=emea-fr-all-fr-bkws-all-all-trial-e-gcp-1011340&utm_content=text-ad-none-any-DEV_c-CRE_529432261646-ADGP_Hybrid+%7C+BKWS+-+EXA+%7C+Txt+~+GCP+~+General%23v3-KWID_43700060384861690-aud-606988878614:kwd-6458750523-userloc_9056158&utm_term=KW_google%20cloud-NET_g-PLAC_&&gad=1&gclid=Cj0KCQjwib2mBhDWARIsAPZUn_lFq39O7ticwfEIsx7AMnbhlse5DV5EMA0qQ9WPwyRBP3mAV1bJl8EaAvSPEALw_wcB&gclsrc=aw.ds)


- cliquer sur consolle, il vas vous demander de créez un espace créez le ![image_1](https://user-images.githubusercontent.com/88383709/258649902-6fbad69a-b3e2-4b4c-b5b1-8413a29c4782.png)
- créez un projets
![image_3](https://user-images.githubusercontent.com/88383709/258649906-81fa8aba-e64b-4a1b-ac3d-279d9c543a8b.png)

- accédez à l'API 
![image_2](https://user-images.githubusercontent.com/88383709/258649905-ee56a1fc-fa72-436f-a57b-fa092f4425fd.png)

- accédez à Identifiant
![image_4](https://user-images.githubusercontent.com/88383709/258649908-39b987fc-96fa-4203-8921-45e142361e06.png)



- créez un ID clients OAuth 2.0(permet de deplacer, suprimer, upload les fichier)
- Crée un Comptes de service(modifier le fichier google sheets)
![image_5](https://user-images.githubusercontent.com/88383709/258649909-1226170d-24ea-4fff-8285-184b99ed8148.png)

- Téléchargez le json OAuth 2.0
![image_6](https://user-images.githubusercontent.com/88383709/258649910-34c23d0c-87c0-4507-8a76-c2e32c4c3d3c.png)


- Téléchargez créez une clés dans le compte service
![image_7](https://user-images.githubusercontent.com/88383709/258649912-e780912f-2274-400b-9e54-1a948ee54cf2.png)
![image_8](https://user-images.githubusercontent.com/88383709/258649913-d54b65f9-9629-4465-84f8-087cefb69040.png)
![image_9](https://user-images.githubusercontent.com/88383709/258649914-f19d196f-5d03-42c7-8940-023bdada0a8f.png)
![image_10](https://user-images.githubusercontent.com/88383709/258649915-35ee9ad5-6ce1-4b3b-8c36-c498f4be0054.png)

- ajoutez le compte cles et service dans le fichier google sheets (acceder au sheets que vous voulez utiliser) la feuille 1 doit se nommer feuille1 
![image_13](https://user-images.githubusercontent.com/88383709/258649919-ef62f2fd-b327-416b-a905-c255b4081270.png)

- ajoutez votre mail compte et service en editeurs
![image_14](https://user-images.githubusercontent.com/88383709/258649920-725d9829-bda1-49aa-9d00-ce8b17876819.png)

- etape final rajouter les fichier json dans google_api (garder les bien precisement et en securiter)
![image_11](https://user-images.githubusercontent.com/88383709/258649916-01b0a2a1-8a92-44a2-864e-3ab35c1f0aa4.png)

- renommer votre fichier json optenue avec OAuth 2.0 en : client_secrets.json
- renommer votre fichier json optenue avec le mails en : service_account.json
![image_12](https://user-images.githubusercontent.com/88383709/258649917-b4ba65ad-a6da-4503-9834-939e44b55d21.png)

- lancer le run.bat
- Au premier lancement il vas vous demander de vous connecter a votre compte google
![image_15](https://user-images.githubusercontent.com/88383709/258649921-f669d158-9e0d-4d81-a914-e5077d700133.png)

# Lancer le projet
```bath
py main.py
```
ou 
```
lancer
- run.bat
```

🖋️ Auteur
Vigreux - développeur junior - vigreux8
