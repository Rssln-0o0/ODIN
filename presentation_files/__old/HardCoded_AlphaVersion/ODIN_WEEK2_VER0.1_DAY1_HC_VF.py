import random

# - Optimized Digital Assistant for Internals -

TIME_Q1 = "quels sont les horaires de travail ?"
TIME_R1 = "Les horaires sont de 8h30 à 17h30, du lundi au vendredi."

TIME_Q2 = "est-ce qu’on travaille le samedi ?"
TIME_R2 = "Non, les samedis sont généralement non travaillés."

PAY_Q1 = "qui contacter pour un problème de paie ?"
PAY_R1 = "Veuillez contacter Mme Ben Ali à l’adresse paie@entreprise.com."

PAY_Q2 = "à quelle date le salaire est-il versé ?"
PAY_R2 = "Les salaires sont versés le 28 de chaque mois."

DOC_Q1 = "où puis-je télécharger mon contrat de travail ?"
DOC_R1 = "Votre contrat est disponible dans la section « Mon dossier RH » du portail interne."

DOC_Q2 = "comment mettre à jour mes informations personnelles ?"
DOC_R2 = "Vous pouvez mettre à jour vos données personnelles directement depuis votre profil RH."

ABS_Q1 = "comment puis-je poser un congé ou une absence ?"
ABS_R1 = "Vous pouvez faire une demande de congé via le portail RH ou en contactant votre manager."

ABS_Q2 = "que faire en cas d’arrêt maladie ?"
ABS_R2 = "Prévenez votre supérieur hiérarchique et transmettez votre certificat médical au service RH dans les 48 heures."

RH_Q1 = "quel est l’email du service des ressources humaines ?"
RH_R1 = "L’adresse email du service RH est rh@entreprise.com."

RH_Q2 = "le service RH est-il joignable en dehors des heures de bureau ?"
RH_R2 = "Le service RH est disponible de 8h00 à 18h00. En dehors de ces horaires, les demandes seront traitées le jour ouvré suivant."

STUPIDITY_101 = [
    "Désolé, je n'ai pas bien compris.",
    "Je ne sais pas encore comment répondre à cette question.",
    "Pourriez-vous s'il vous plaît reformuler votre question ?",
    "Je peux vous aider sur des sujets tels que les congés, les salaires ou les horaires de travail.",
]

LOOP_101 = [
    "\nPuis-je vous aider avec autre chose ?",
    "\nSi vous souhaitez plus d'informations n'hésitez pas à demander à nouveau",
]

WELCOME_101 = [
    "\nPose toutes les questions que tu souhaites :",
    "\nInterroge-moi sur ce que tu désires connaître :",
    "\nPour toute question, je suis à votre écoute :",
    "\nN'hésite pas à me questionner sur ce que tu veux :",
    "\nPour toute demande d'information, je suis à votre entière disposition :",
]

REP = random.choices(STUPIDITY_101, weights=[3, 3, 3, 1])[0]
LOOP = random.choices(LOOP_101, weights=[1, 1])[0]
WELCOME = random.choices(WELCOME_101, weights=[1, 1, 1, 1,1])[0]

STARTOVER = 0 #Implemented yet still unused, poor me

NAIL = False

print("\nODIN, à votre service ! ")

print(WELCOME)

while True:

    FLAG_USER = input("\n").strip().lower()

    if FLAG_USER in ["exit", "quitter"]:
        print("Merci et à bientôt !")
        break
    
    if FLAG_USER == TIME_Q1:
        print(TIME_R1)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == TIME_Q2:
        print(TIME_R2)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == PAY_Q1:
        print(PAY_R1)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == PAY_Q2:
        print(PAY_R2)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == DOC_Q1:
        print(DOC_R1)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == DOC_Q2:
        print(DOC_R2)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == ABS_Q1:
        print(ABS_R1)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == ABS_Q2:
        print(ABS_R2)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == RH_Q1:
        print(RH_R1)
        NAIL = True
        STARTOVER = 1
    elif FLAG_USER == RH_Q2:
        print(RH_R2)
        NAIL = True
        STARTOVER = 1

    if not NAIL:
       print(REP)
    else:
       print(LOOP)
