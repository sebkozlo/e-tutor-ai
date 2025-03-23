import openai
from django.conf import settings
from .schemas import QuizResponseSchema, SolutionResponseSchema


openai.api_key = settings.OPENAI_API_KEY

def generate_quiz(question_count, difficulty, question_type, content):
    response = openai.beta.chat.completions.parse(
        model="gpt-4o",

        messages=[
            {"role": "system",
             "content": "Jesteś pomocnym asystentem do generowania quizów. Twoim zadaniem jest stworzenie pytań w oparciu o określony typ, trudność i temat."},
            {"role": "user",
             "content": f"Wygeneruj {question_count} pytań na poziomie trudności {difficulty} z 10 na temat {content}. Pytania powinny być różnych typów, jak opisano poniżej. "
                        "Dla każdego pytania dopasuj odpowiedni schemat odpowiedzi.\n\n"
                        "- Pytania typu 'single' powinny zawierać jedno pytanie i jedno prawidłowe rozwiązanie (jedna opcja).\n"
                        "- Pytania typu 'multi' powinny zawierać jedno pytanie i 4 propozycje odpowiedzi i wiele poprawnych odpowiedzi (wielokrotny wybór) 'ChoiceQuestionSchema'. \n"
                        "- Pytania typu 'fill' powinny zawierać pytanie z brakującym słowem, które użytkownik ma uzupełnić. Podaj odpowiedź jako brakujące słowo lub frazę.\n"
                        "- Pytania typu 'ordering' powinny zawierać pytanie z zestawem opcji, które należy uporządkować we właściwej kolejności.\n\n"
                        "Upewnij się, że każde pytanie jest poprawnie przypisane do odpowiedniego typu, i że odpowiedzi są zgodne z typem pytania.\n\n"
                        "Odpowiednio zmapuj typy pytań 'question_type':"
                        "'Multi Choice': 'multi', 'Fill In The Blank':'fill', 'Ordering':'ordering', 'Single Choice':'single;"
                        "Przykłady pytań:\n"
                        "1. Pytanie typu 'single': 'Jakie jest stolica Polski? Odpowiedź: Warszawa'\n"
                        "2. Pytanie typu 'multi': 'Wybierz wszystkie stolice krajów europejskich: Warszawa, Moskwa, Tokio, Paryż'. Poprawne odpowiedzi: Warszawa, Moskwa, Paryż\n"
                        "3. Pytanie typu 'fill': 'Polska ma stolicę w ____. Odpowiedź: Warszawa'\n"
                        "4. Pytanie typu 'ordering': 'Ułóż te miasta w kolejności alfabetycznej: 'Warszawa, Paryż, Londyn'. Poprawna kolejność: Londyn, Paryż, Warszawa.\n\n"
                        f"Proszę wygenerować pytania typu: {', '.join(question_type)}. Zapewnij, że każde pytanie będzie pasowało do jednego z tych typów."
                        "Odpowiedzi udzielaj w jezyku plskim"}
        ], response_format=QuizResponseSchema
    )

    try:
        print(response)

        response = response.choices[0].message.parsed

        return response
    except Exception as e:
        return e


def generate_solution(question, solution_level):
    response = openai.beta.chat.completions.parse(
        model="gpt-4o",

        messages=[
            {"role": "system",
             "content": "Jesteś ekspertem w wielu dziedzinach wiedzy, takich jak programowanie, matematyka, nauki przyrodnicze, historia, geografia i inne. Twoim zadaniem jest udzielanie odpowiedzi na pytania w formacie JSON zgodnie z poziomem szczegółowości określonym przez 'solution_level'."},
            {"role": "user",
             "content": f"Odpowiedz na pytanie: {question}\n"
                        f"Poziom podpowiedzi: {solution_level}\n"
                        f"- solution_level = 1: Udziel krótkiej, ogólnej podpowiedzi naprowadzającej na odpowiedź, lecz nie podawaj bezpośredniej odpowiedzi.\n"
                        f"- solution_level = 2: Udziel bardziej szczegółowej podpowiedzi, dokładniej tłumacząc kluczowe pojęcia, możesz pomóc wykluczyć jakąś z poponowanych odpowiedz jeśli taki istnieją w 'options', lecz nie podawaj bezpośredniej prawidłowej odpowiedzi.\n"
                        f"- solution_level = 3: Wskaż prawidłową odpowiedź i dokładnie wyjaśnij, dlaczego jest poprawna.\n"
                        "Odpowiedzi udzielaj w języku polskim."}
        ], response_format=SolutionResponseSchema
    )

    try:
        return response.choices[0].message.parsed

    except Exception as e:
        return e