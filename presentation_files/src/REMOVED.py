# def keyword_matcher(text):
#     """Instant answers for clear keywords"""
#     keyword_responses = {
#         "malade": "Pour un arrêt maladie: \n1) Prévenez votre manager \n2) Envoyez le certificat médical au RH sous 48h",
#         "télétravail": "Télétravail possible 2j/semaine sur accord manager",
#         "congé": "25 jours congés/an. Demande via portail RH"
#     }
#     for keyword, response in keyword_responses.items():
#         if keyword in text:
#             return response
#     return None

# def keyword_fallback(text):
#     """Handle partial matches"""
#     keyword_responses = {
#         "horaire": "Je peux vous informer sur les horaires de travail standards (8h30-17h30).",
#         "congé": "Pour les congés, vous avez droit à 25 jours par an. Voulez-vous plus de détails ?",
#         "salaire": "Les salaires sont versés le 28 de chaque mois. Quelle information spécifique cherchez-vous ?",
#     }
    
#     doc = nlp(text)
#     for token in doc:
#         if token.text in keyword_responses:
#             return keyword_responses[token.text]
    
#     return random.choice(FALLBACK_101)

#client = genai.Client(api_key=api_key)


#def ask_openai(prompt):
    #try:
        #response = client.models.generate_content(
            #model="gemini-2.5-flash",
            #messages=[
                #{"role": "system", "content": "Tu es un assistant RH professionnel et formel."},
                #{"role": "user", "content": prompt}
            #],
            #temperature=0.5,
            #max_tokens=200,
        #)
    #except Exception as e:
        #return f"[System] Erreur OpenAI : {str(e)}"

# def get_ai_response(user_input):
#     """Enhanced AI response with conversation context"""
#     context = "\n".join([
#         "Conversation History:",
#         *conversation_history,
#         f"Current Question: {user_input}"
#     ])
    
#     prompt = f"""
#     [ROLE]
#     Tu es ODIN, assistant RH français. Réponds de manière:
#     - Professionnelle mais amicale
#     - Concise (1-2 phrases max)
#     - En français correct
#     - Basé sur ces informations:
#       * Télétravail: 2j/semaine
#       * Horaires: 8h30-17h30
#       * Contact RH: rh@entreprise.com

#     [CONTEXTE]
#     {context}

#     [QUESTION]
#     {user_input}
#     """
    
#     try:
#         # Example using OpenAI (replace with your preferred API)
#         response = ask_openai(prompt)
#         conversation_history.extend([f"User: {user_input}", f"Bot: {response}"])
#         return response
#     except Exception as e:
#         print(f"\n[System] Error: {str(e)}")
#         return None