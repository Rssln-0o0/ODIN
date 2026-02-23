import spacy

nlp = spacy.load("fr_core_news_md")

faq = {
    "Quels sont les horaires de travail ?":
        "Les horaires sont de 8h30 à 17h30, du lundi au vendredi.",
    "Est-ce qu’on travaille le samedi ?":
        "Non, les samedis sont généralement non travaillés.",
    "Qui contacter pour un problème de paie ?":
        "Veuillez contacter Mme Ben Ali à l’adresse paie@entreprise.com."
}

def trouver_reponse(question_utilisateur):
    doc_utilisateur = nlp(question_utilisateur)
    meilleure_similarite = 0
    meilleure_question = None

    for question_faq in faq:
        doc_faq = nlp(question_faq)
        similarite = doc_utilisateur.similarity(doc_faq)
        if similarite > meilleure_similarite:
            meilleure_similarite = similarite
            meilleure_question = question_faq

    if meilleure_similarite > 0.75:
        return faq[meilleure_question]
    else:
        return "Désolé, je ne comprends pas votre question."

def chatbot():
    premier = True
    while True:
        if premier:
            question = input("Comment puis-je vous aider aujourd'hui ?\n> ")
            premier = False
        else:
            question = input("Souhaitez-vous plus d'informations ? (tapez 'non' pour quitter)\n> ")

        if question.lower().strip() == "non":
            print("D'accord, à bientôt !")
            break

        reponse = trouver_reponse(question)
        print(reponse)

if __name__ == "__main__":
    chatbot()
