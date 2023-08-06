# Nom du projet

![Badge de version](https://img.shields.io/badge/version-1.0.0-blue)
<!-- Vous pouvez ajouter d'autres badges ici à partir de shields.io -->

Description courte de ce que fait votre projet.

## 🚀 Démarrage

Ces instructions vous permettront d'obtenir une copie du projet en cours d'exécution sur votre machine locale à des fins de développement et de test.

### 📋 Prérequis
- python 3.10.7
- virtualenv

```bash
Exemple de commande
```


# Clonez ce dépot
git clone https://lien-de-votre-projet.git

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
- cliquer sur consolle, il vas vous demander de créez un espace créez le ![image_1](image_readme\photo_1.png)
- créez un projets
![image_3](image_readme\photo_3.png)

- accédez à l'API 
![image_2](image_readme\photo_2.png)

- accédez à Identifiant
![image_4](image_readme\photo_4.png)



- créez un ID clients OAuth 2.0(permet de deplacer, suprimer, upload les fichier)
- Crée un Comptes de service(modifier le fichier google sheets)
![image_5](image_readme\photo_5.png)

- Téléchargez le json OAuth 2.0
![image_6](image_readme\photo_6.png)


- Téléchargez créez une clés dans le compte service
![image_7](image_readme\photo_7.png)
![image_8](image_readme\photo_8.png)
![image_9](image_readme\photo_9.png)
![image_10](image_readme\photo_10.png)

- ajoutez le compte cles et service dans le fichier google sheets (acceder au sheets que vous voulez utiliser) la feuille 1 doit se nommer feuille1 
![image_13](image_readme\photo_13.png)

- ajoutez votre mail compte et service en editeurs
![image_14](image_readme\photo_14.png)

- etape final rajouter les fichier json dans google_api (garder les bien precisement et en securiter)
![image_11](image_readme\photo_11.png)

- renommer votre fichier json optenue avec OAuth 2.0 en : client_secrets.json
- renommer votre fichier json optenue avec le mails en : service_account.json
![image_12](image_readme\photo_12.png)

- lancer le run.bat
- Au premier lancement il vas vous demander de vous connecter a votre compte google
![image_15](image_readme\photo_15.png)

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