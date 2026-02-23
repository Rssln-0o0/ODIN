import string
import time
import random

from langdetect import detect
from translate import Translator
from datetime import datetime

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from collections import defaultdict

nlp = spacy.load("fr_core_news_lg")

QaN_GENERAL = {
    "quels sont les horaires de travail ?":"\nLes horaires sont de 8h30 à 17h30, du lundi au vendredi.",
    "est-ce qu’on travaille le samedi ?":"\nNon, les samedis sont généralement non travaillés.",
    "est-il possible de faire du télétravail ?":"\nOui, le télétravail est autorisé jusqu’à 2 jours par semaine, avec l’accord du manager.",
    "à qui dois-je signaler un retard ou une absence imprévue ?":"\nInformez votre manager directement et mettez le service RH en copie si nécessaire.",
    "puis-je aménager mes horaires de travail ?":"\nToute demande d’aménagement horaire doit être validée par votre manager et le service RH.",
    # "VOID"
    "à quelle date le salaire est-il versé ?":"\nLes salaires sont versés le 28 de chaque mois.",
    "où puis-je consulter mes bulletins de paie ?":"\nVos bulletins de paie sont accessibles depuis l’espace « Ma paie » du portail RH.",
    "que faire si je remarque une erreur sur ma fiche de paie ?":"\nContactez immédiatement le service RH pour signaler l’erreur.",
    "quand aurai-je droit à une prime d’ancienneté ?":"\nLa prime d’ancienneté est versée à partir de 3 années de service, selon les conditions de votre convention collective.",
    # "VOID"
    "où puis-je télécharger mon contrat de travail ?":"\nVotre contrat est disponible dans la section « Mon dossier RH » du portail interne.",
    "comment mettre à jour mes informations personnelles ?":"\nVous pouvez mettre à jour vos données personnelles directement depuis votre profil RH.",
    "qui peut me fournir une attestation de travail ?":"\nUne attestation peut être demandée au service RH via le formulaire de contact ou par mail.",
    "est-il possible de demander une copie d’un ancien bulletin de paie ?":"\nOui, vous pouvez demander une copie en contactant le service RH ou via votre espace en ligne.",
    # "VOID"
    "comment puis-je poser un congé ou une absence ?":"\nVous pouvez faire une demande de congé via le portail RH ou en contactant votre manager.",
    "que faire en cas d’arrêt maladie ?":"\nPrévenez votre supérieur hiérarchique et transmettez votre certificat médical au service RH dans les 48 heures.",
    "combien de jours de congé ai-je par an ?":"\nLes salariés à temps plein disposent de 25 jours ouvrables de congé par an.",
    "puis-je annuler une demande de congé déjà envoyée ?":"\nOui, vous pouvez annuler votre demande via le portail RH, tant qu’elle n’a pas encore été validée.",
    # "VOID"
    "à qui puis-je m’adresser pour une question RH ?":"\nVous pouvez contacter votre référent RH ou écrire à l’adresse générique rh@entreprise.com.",
    "quel est l’email du service des ressources humaines ?":"\nL’adresse email du service RH est rh@entreprise.com.",
    "le service RH est-il joignable en dehors des heures de bureau ?":"\nLe service RH est disponible de 9h00 à 17h00. En dehors de ces horaires, les demandes seront traitées le jour ouvré suivant.",
    "puis-je prendre un rendez-vous avec une personne des RH ?":"\nOui, vous pouvez prendre rendez-vous via le portail RH ou en envoyant une demande par mail.",
}

SYNONYMS = {
    "salaire": ["paie", "rémunération", "paye"],
    "congé": ["vacances", "repos"],
    "rh": ["ressources humaines", "hr", "service personnel"]
}

FALLBACK_101 = [
    "\nDésolé, je n'ai pas bien compris.",
    "\nJe ne sais pas encore comment répondre à cette question.",
    "\nPourriez-vous s'il vous plaît reformuler votre question ?",
    "\nJe peux vous aider sur des sujets tels que les congés, les salaires ou les horaires de travail.",
]

LOOP_101 = [
    "\nPuis-je vous aider avec autre chose ?",
    "\nSi vous souhaitez plus d'informations n'hésitez pas à demander à nouveau",
    "\nSouhaitez-vous poser une autre question ?",
]

WELCOME_101 = [
    "\nPose toutes les questions que tu souhaites :",
    "\nInterroge-moi sur ce que tu désires connaître :",
    "\nPour toute question, je suis à votre écoute :",
    "\nN'hésite pas à me questionner sur ce que tu veux :",
    "\nPour toute demande d'information, je suis à votre entière disposition :",
]

def get_greeting():

    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "\nBonjour ! ODIN est à votre service"
    elif 12 <= hour < 18:
        return "\nBon après-midi ! ODIN est à votre service"
    elif 18 <= hour < 22:
        return "\nBonsoir ! ODIN est à votre service"
    else:
        return "\nBonne nuit ! ODIN est à votre service"
    

def get_best_match(user_input, threshold=0.80):
    doc1 = nlp(user_input)
    best_score = 0
    best_answer = None

    for question, answer in QaN_GENERAL.items():
        doc2 = nlp(question)
        score = doc1.similarity(doc2)

        if score > best_score:
            best_score = score
            best_answer = answer

    if best_score >= threshold:
        return best_answer
    return None
    
FALL = random.choices(FALLBACK_101, weights=[3, 3, 3, 1])[0]
LOOP = random.choices(LOOP_101, weights=[4, 4, 2])[0]
WELCOME = random.choices(WELCOME_101, weights=[1, 1, 1, 1,1])[0]

print(get_greeting())
print(WELCOME)


while True:

    user_input = input("\n").strip().lower()
    response = get_best_match(user_input)

    if user_input in ["exit", "quitter"]:
        print("\nMerci, à bientôt !")
        break
    
    if response:
        print("", response)
    else:
        print(random.choice(FALLBACK_101))
    
    time.sleep (0.2)
    print(random.choice(LOOP_101))

