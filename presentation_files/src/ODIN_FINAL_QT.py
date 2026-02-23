import random
import time

from datetime import datetime
import google.generativeai as genai

from collections import deque
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
import re

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QRunnable, QThreadPool, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtCore import QTimer
from ui_main import Ui_ODIN


nlp = spacy.load("fr_core_news_md")

QaN_GENERAL = {
    "quels sont les horaires de travail ?": "\nLes horaires sont de 8h30 à 17h30, du lundi au vendredi.",
    "est-ce qu’on travaille le samedi ?": "\nNon, les samedis sont généralement non travaillés.",
    "est-il possible de faire du télétravail ?": "\nOui, le télétravail est autorisé jusqu’à 2 jours par semaine, avec l’accord du manager.",
    "à qui dois-je signaler un retard ou une absence imprévue ?": "\nInformez votre manager directement et mettez le service RH en copie si nécessaire.",
    "puis-je aménager mes horaires de travail ?": "\nToute demande d’aménagement horaire doit être validée par votre manager et le service RH.",
    "à quelle date le salaire est-il versé ?": "\nLes salaires sont versés le 28 de chaque mois.",
    "où puis-je consulter mes bulletins de paie ?": "\nVos bulletins de paie sont accessibles depuis l’espace « Ma paie » du portail RH.",
    "que faire si je remarque une erreur sur ma fiche de paie ?": "\nContactez immédiatement le service RH pour signaler l’erreur.",
    "quand aurai-je droit à une prime d’ancienneté ?": "\nLa prime d’ancienneté est versée à partir de 3 années de service, selon les conditions de votre convention collective.",
    "est ce que les heures supplementaire sont payées ?": "\nOui, les heures suppllementaire sont payées.",
    "où puis-je télécharger mon contrat de travail ?": "\nVotre contrat est disponible dans la section « Mon dossier RH » du portail interne.",
    "comment mettre à jour mes informations personnelles ?": "\nVous pouvez mettre à jour vos données personnelles directement depuis votre profil RH.",
    "qui peut me fournir une attestation de travail ?": "\nUne attestation peut être demandée au service RH via le formulaire de contact ou par mail.",
    "est-il possible de demander une copie d’un ancien bulletin de paie ?": "\nOui, vous pouvez demander une copie en contactant le service RH ou via votre espace en ligne.",
    "comment puis-je poser un congé ou une absence ?": "\nVous pouvez faire une demande de congé via le portail RH ou en contactant votre manager.",
    "que faire en cas d’arrêt maladie ?": "\nPrévenez votre supérieur hiérarchique et transmettez votre certificat médical au service RH dans les 48 heures.",
    "combien de jours de congé ai-je par an ?": "\nLes salariés à temps plein disposent de 25 jours ouvrables de congé par an.",
    "puis-je annuler une demande de congé déjà envoyée ?": "\nOui, vous pouvez annuler votre demande via le portail RH, tant qu’elle n’a pas encore été validée.",
    "est ce que je peux compenser mes heures d'absence ?":"Oui, vous pouver compenser vos heures d'absence par des heures supplementaire de travaille",
    "à qui puis-je m’adresser pour une question RH ?": "\nVous pouvez contacter votre référent RH ou écrire à l’adresse générique rh@entreprise.com.",
    "quel est l’email du service des ressources humaines ?": "\nL’adresse email du service RH est rh@entreprise.com.",
    "le service RH est-il joignable en dehors des heures de bureau ?": "\nLe service RH est disponible de 9h00 à 17h00. En dehors de ces horaires, les demandes seront traitées le jour ouvré suivant.",
    "puis-je prendre un rendez-vous avec une personne des RH ?": "\nOui, vous pouvez prendre rendez-vous via le portail RH ou en envoyant une demande par mail.",
}

QaN_GENERAL_DLC1 = {
    "quels sont les horaires flexibles disponibles ?": "Les horaires flexibles varient selon le département, merci de consulter le responsable RH.",
    "comment poser un congé parental ?": "Vous devez faire une demande formelle par écrit et la soumettre au service RH.",
    "puis-je changer mon type de contrat ?": "Cela dépend de votre ancienneté et des postes disponibles, contactez votre RH.",
    "comment demander une mutation ?": "Une demande écrite est nécessaire, suivie d’un entretien avec votre supérieur hiérarchique.",
    "que faire en cas de harcèlement au travail ?": "Signalez immédiatement au responsable RH ou utilisez la ligne confidentielle.",
    "comment puis-je obtenir un avenant à mon contrat ?": "Veuillez formuler une demande auprès du service RH.",
    "puis-je cumuler plusieurs postes dans l’entreprise ?": "Cela nécessite l'approbation de la direction, demandez conseil à votre RH.",
    "à qui dois-je signaler une erreur sur ma fiche de paie ?": "Adressez-vous directement au service paie ou RH.",
    "y a-t-il une politique de télétravail ?": "Oui, consultez la charte du télétravail ou demandez à votre responsable.",
    "comment modifier mes coordonnées bancaires ?": "Vous devez remplir un formulaire et le remettre au service RH.",
    "quels sont les avantages sociaux offerts ?": "Mutuelle, tickets restaurant, abonnements de transport… voir la brochure RH.",
    "combien de jours de congé puis-je cumuler ?": "Cela dépend de votre contrat. Les congés non pris peuvent être reportés sous conditions.",
    "comment fonctionne l’entretien annuel ?": "Un entretien est organisé chaque année avec votre supérieur pour discuter de vos objectifs.",
    "que faire en cas d’arrêt maladie ?": "Prévenez votre responsable et envoyez un certificat médical sous 48h.",
    "comment accéder à mon dossier RH ?": "Il est consultable via l’intranet RH ou en le demandant directement.",
    "le stage peut-il être prolongé ?": "Oui, sous réserve de validation par l’établissement et l’entreprise.",
    "puis-je bénéficier d’une formation ?": "Des formations sont disponibles. Adressez une demande à votre supérieur.",
    "comment déclarer un accident de travail ?": "Remplissez le formulaire prévu et informez RH dans les 24h.",
    "quels sont les jours fériés chômés ?": "La liste est disponible sur l’intranet RH ou auprès du service RH.",
    "quelles sont les règles pour le travail en heures supplémentaires ?": "Elles doivent être validées et seront majorées conformément à la loi.",
    "comment obtenir une attestation de travail ?": "Faites-en la demande à RH, elle vous sera transmise sous quelques jours.",
    "mon contrat se termine bientôt, que dois-je faire ?": "Contactez RH pour discuter de la suite et récupérer vos documents.",
    "puis-je demander un aménagement de poste ?": "Oui, pour raisons médicales ou personnelles, demandez à votre RH.",
    "comment signaler un changement de situation familiale ?": "Transmettez les justificatifs nécessaires au service RH.",
    "comment obtenir un duplicata de badge ou carte d’accès ?": "Signalez la perte à RH, un duplicata pourra être émis."
}


SYNONYMS = {
    "congé": ["vacances", "repos", "absence", "jour libre", "pause"],
    "salaire": ["paie", "paiement", "rémunération", "fiche de paie", "bulletin"],
    "horaire": ["temps", "heures", "emploi du temps", "planning"],
    "contrat": ["document", "papier de travail", "engagement"],
    "contact": ["joindre", "email", "téléphone", "appeler"],
    "bureau": ["service", "département", "local", "salle"],
    "document": ["formulaire", "papier", "fiche", "pièce"],
    "adresse": ["lieu", "emplacement", "localisation"],
    "travail": ["job", "emploi", "mission", "poste"],
    "début": ["commencement", "démarrage", "entrée", "ouverture", "commence", "commencé"],
    "fin": ["clôture", "terminaison", "sortie"],
    "justifier": ["prouver", "motiver", "expliquer"],
    "informations": ["données", "coordonnées", "détails"],
    "modifier": ["changer", "mettre à jour", "corriger"],
    "question": ["interrogation", "requête", "demande"],
    "envoyer": ["soumettre", "faire parvenir", "transmettre"],
    "travailler": ["œuvrer", "activer", "opérer"],
}


FRENCH_ESSENTIAL_WORDS = {
    "peux", "puis", "est", "suis", "ai",  # Critical verbs
    "malade", "télétravail", "congé",      # HR keywords
    "quand", "comment", "où"               # Question words
}

SPECIAL_LEMMAS = {
    "peur": "pouvoir",  # Fix bad lemmatization
    "malady": "malade",
    "telettravailer": "télétravail"
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

GEM_101 = [
    "\nPensée...",
    "\nJe précise ma recherche...",
]


def get_greeting():

    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "\n ☀️ Bonjour ! ODIN est à votre service"
    elif 12 <= hour < 18:
        return "\n 🌤️ Bon après-midi ! ODIN est à votre service"
    elif 18 <= hour < 22:
        return "\n 🌙 Bonsoir ! ODIN est à votre service"
    else:
        return "\n 🌌 Bonne nuit ! ODIN est à votre service"


def french_preprocessor(text):
    """Robust French text normalization"""
    # 1. Manual corrections first
    for wrong, right in SPECIAL_LEMMAS.items():
        text = re.sub(rf"\b{wrong}\b", right, text)

    # 2. Custom token handling
    doc = nlp(text.lower())
    tokens = []
    for token in doc:
        # Keep essential words even if stopwords
        if token.text in FRENCH_ESSENTIAL_WORDS:
            tokens.append(token.text)
            continue

        # Normal processing
        if not token.is_punct and not token.is_stop:
            lemma = token.lemma_
            tokens.append(lemma if len(lemma) > 2 else token.text)

    return " ".join(tokens)


def calculate_similarity(text1, text2):
    """Safe similarity calculation with vector checks"""
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    if not doc1.vector_norm or not doc2.vector_norm:
        return 0.0  # Default score if empty vectors

    return doc1.similarity(doc2)


def expand_with_synonyms(text):
    words = text.split()
    expanded = []
    for word in words:
        expanded.append(word)
        if word in SYNONYMS:
            expanded.extend(SYNONYMS[word])
    return " ".join(list(set(expanded)))


def get_follow_up(score):
    if score > 0.9:
        return random.choice([
            "\nCette réponse vous est-elle utile ?",
            "\nAvez-vous besoin de précisions ?"
        ])
    return random.choice(LOOP_101)


def type_writer(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    # print()  # New line after finished


DEBUG = False


def get_best_match(user_input, threshold=0.68):
    processed = french_preprocessor(expand_with_synonyms(user_input))
    # Then try semantic similarity
    best_score = 0
    best_answer = None

    for question, answer in QaN_GENERAL.items():
        for q_var in question.split("|"):  # Handle multiple variants
            q_processed = french_preprocessor(q_var)
            similarity = calculate_similarity(processed, q_processed)

            # Boost scores for keyword matches
            if any(word in processed.split() for word in q_var.split("|")):
                similarity = min(1.0, similarity + 0.25)

            if similarity > best_score:
                best_score = similarity
                best_answer = answer

    return best_answer if best_score >= threshold else None


while True:
    api_key = input("Enter votre Gemini API Clé :").strip()

    if api_key.strip() == "":
        print("Veuillez entrer une clé valide.")
        continue

    if not api_key:
        print("Veuillez entrer une clé valide.")
        continue

    if api_key:
        break

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')


def gemini_best_match(user_input):
    full_QaN = {**QaN_GENERAL, **QaN_GENERAL_DLC1}

    prompt = (
        "Vous êtes un assistant RH intelligent nommé ODIN. Utilisez les exemples suivants pour répondre au mieux à la question. En cas de doute, proposez une réponse polie.\n\n"
        "Voici une base de données de questions et réponses fréquentes :\n\n"
    )
    for q, r in full_QaN.items():
        prompt += f"Q: {q}\nA: {r}\n"

        if SYNONYMS:
            prompt += "\nMots clés pertinents pour aider à faire correspondre des termes similaires:\n"
            prompt += ", ".join(SYNONYMS) + "\n"

    prompt += (
        "---\n\n"
        f"Si elle en français, réponds directement et brièvement à cette question, sans introduction. Si elle est en anglais, traduis la réponse exacte en anglais sans autre commentaire :\n\"{user_input}\""
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Erreur Gemini] {str(e)}"


conversation_history = deque(maxlen=4)


def update_history(user_input, bot_response):
    """Maintains conversation context"""
    conversation_history.append(f"User: {user_input}")
    conversation_history.append(f"Assistant: {bot_response}")


def handle_complex_case(user_input):
    """Placeholder for API fallback"""
    return random.choice([
        "Je consulte les ressources RH et je vous réponds rapidement...",
        "Je transfère votre question au service RH compétent."
    ])


FALL = random.choices(FALLBACK_101, weights=[3, 3, 3, 1])[0]
LOOP = random.choices(LOOP_101, weights=[4, 4, 2])[0]
WELCOME = random.choices(WELCOME_101, weights=[1, 1, 1, 1, 1])[0]
GEM = random.choices(GEM_101)

class WorkerSignals(QObject):

    finished = pyqtSignal(str)


class ChatWorker(QRunnable):
    def __init__(self, user_input):
        super().__init__()
        self.user_input = user_input
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        # Step 1: Dictionary match
        response = get_best_match(self.user_input)
        response = gemini_best_match(self.user_input)

        # Step 2: Gemini fallback
        if not response:
            response = gemini_best_match(self.user_input)

        # Step 3: Still nothing
        if not response:
            response = handle_complex_case(self.user_input)
            response = gemini_best_match(self.user_input)

        self.signals.finished.emit(response)


class OdinApp(QMainWindow, Ui_ODIN):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect ENTER key and button
        self.GO.clicked.connect(self.handle_query)
        self.LINE.returnPressed.connect(self.handle_query)

        # Optional greeting
        self.type_writer_effect(get_greeting() + "\n" + random.choice(WELCOME_101))

    def handle_query(self):
        user_input = self.LINE.text().strip()
        if not user_input or user_input.isspace():
            self.type_writer_effect("❌ Veuillez entrer une question valide.")
            return
        if user_input.lower() in ["exit", "quitter", "quit"]:
            self.type_writer_effect("👋 Merci, à bientôt !")
            QApplication.quit()
            return
        
        self.type_writer_effect(random.choice(GEM_101))  # Temporary thinking message
        QApplication.processEvents()

        self.threadpool = QThreadPool.globalInstance()
        worker = ChatWorker(user_input)
        worker.signals.finished.connect(self.display_response)
        self.threadpool.start(worker)
        
    def type_writer_effect(self, full_text, delay=30):
        self.current_text = ""
        self.full_text = full_text
        self.char_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.timer.start(delay)

    def update_text(self):
        if self.char_index < len(self.full_text):
            self.current_text += self.full_text[self.char_index]
            self.TEXT.setPlainText(self.current_text)
            self.char_index += 1
        else:
            self.timer.stop()

    def display_response(self, response):
        final_response = f"\n🤖 ODIN : {response}\n" + random.choice(LOOP_101)
        self.type_writer_effect(final_response)
        self.LINE.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OdinApp()
    window.show()
    sys.exit(app.exec_())
