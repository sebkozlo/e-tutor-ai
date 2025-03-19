import openai
from django.conf import settings
from .schemas import QuizResponseSchema, SolutionSchema



openai.api_key = settings.OPENAI_API_KEY

def generate_quiz(question_count, difficulty, question_type, content):
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-mini",

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
        return []


def question_solution(question):
    response = openai.beta.chat.completions.parse(
        model="gpt-4o-mini",

        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem w rozwiązywaniu problemów."},
            {"role": "user",
             "content": f"Daj podpowiedz do pytania: {question}, ale dawaj bezpośredniej informacji jaka jest prawidłowa odpowiedź"}
        ], response_format=SolutionSchema
    )

    try:
        return response.choices[0].message.parsed

    except Exception as e:
        return []