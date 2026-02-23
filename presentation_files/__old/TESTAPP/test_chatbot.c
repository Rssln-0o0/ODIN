// Written by Raslen Azaiez

#include <stdio.h>
#include <string.h>

char FLAG_USER[256];
int FLAG_FIRST_RESPONSE;

int main()
{
    // printf("Comment puis-je vous aider aujourd'hui : ");

    const char *FLAG_Q1 = "Quels sont les horaires de travail ?";
    const char *FLAG_R1 = "Les horaires sont de 8h30 à 17h30, du lundi au vendredi.";

    const char *FLAG_Q2 = "Est-ce qu’on travaille le samedi ?";
    const char *FLAG_R2 = "Non, les samedis sont généralement non travaillés.";

    const char *FLAG_Q3 = "Qui contacter pour un problème de paie ?";
    const char *FLAG_R3 = "Veuillez contacter Mme Ben Ali à l’adresse paie@entreprise.com.";

    const char *FLAG_ERROR = "Desole, je ne comprends pas votre question.";

    FLAG_FIRST_RESPONSE = 1;

    while (1)
    {
        if (FLAG_FIRST_RESPONSE)
        {
            printf("Comment puis-je vous aider aujourd'hui : ");
            FLAG_FIRST_RESPONSE = 0;
        }
        else
        {
            printf("Souhaitez-vous plus d'informations ? ");
        }

        fgets(FLAG_USER, sizeof(FLAG_USER), stdin);
        FLAG_USER[strcspn(FLAG_USER, "\n")] = 0;

        if (strcmp(FLAG_USER, FLAG_Q1) == 0)
        {
            printf("%s", FLAG_R1);
        }

        else if (strcmp(FLAG_USER, FLAG_Q2) == 0)
        {

            printf("%s", FLAG_R2);
        }

        else if (strcmp(FLAG_USER, FLAG_Q3) == 0)
        {

            printf("%s", FLAG_R3);
        }

        else
        {
            printf("%s", FLAG_ERROR);
        }

        return 0;
    }
}