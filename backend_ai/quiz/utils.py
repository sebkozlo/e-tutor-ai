from http.client import responses

import openai
from django.conf import settings
from .schemas import QuizResponseSchema, SolutionResponseSchema


openai.api_key = settings.OPENAI_API_KEY

def generate_quiz(question_count, difficulty, question_type, content):
    type_descriptions = {
        "Single": "- Pytania typu 'Single' powinny zawierać jedno pytanie i jedno prawidłowe rozwiązanie (jedna opcja).\n",
        "Multi": "- Pytania typu 'Multi' powinny zawierać jedno pytanie i 4 propozycje odpowiedzi i wiele poprawnych odpowiedzi (wielokrotny wybór).\n",
        "Fill": "- Pytania typu 'Fill' powinny zawierać pytania z brakującymi słowami. Odpowiedź to lista brakujących słów lub fraz.\n",
        "Order": "- Pytania typu 'Order' powinny zawierać opcje do uporządkowania we właściwej kolejności.\n"
    }

    examples = {
        "Single": "1. Pytanie typu 'Single': 'Jakie jest stolica Polski? Odpowiedź: Warszawa'\n",
        "Multi": "2. Pytanie typu 'Sulti': 'Wybierz wszystkie stolice krajów europejskich: Warszawa, Moskwa, Tokio, Paryż'. Poprawne odpowiedzi: Warszawa, Moskwa, Paryż\n",
        "Fill": "3. Pytanie typu 'Fill': Pytanie: 'Uzupełnij'. Options: ['Polska ma stolicę w ____.' , 'Klasa bazowa w Javie nosi nazwę ____'] Odpowiedź: ['Warszawa', 'Object']\n",
        "Order": "4. Pytanie typu 'Order': 'Ułóż miasta w kolejności alfabetycznej: Warszawa, Paryż, Londyn'. Poprawna kolejność: Londyn, Paryż, Warszawa\n"
    }

    selected_descriptions = "".join([type_descriptions[t] for t in question_type])
    selected_examples = "".join([examples[t] for t in question_type])
    joined_types = ", ".join(question_type)

    prompt = (
        f"Wygeneruj {question_count} pytań na poziomie trudności {difficulty}/10 na temat: {content}.\n"
        f"Pytania powinny być wyłącznie typu: {joined_types}.\n\n"
        f"Dla każdego pytania dopasuj odpowiedni schemat odpowiedzi:\n"
        f"{selected_descriptions}\n"
        f"Upewnij się, że każde pytanie ma poprawnie ustawione pole 'question_type' i poprawne pole 'correct_answer'.\n\n"
        f"Przykłady:\n{selected_examples}\n"
        "Nie twórz pytań innych typów niż podane. Odpowiedzi udziel w języku polskim. Zwróć wynik jako JSON w polu 'quiz', zawierający listę pytań."
    )

    response = openai.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem do generowania quizów. Twoim zadaniem jest stworzenie pytań w oparciu o określony typ, trudność i temat."},
            {"role": "user", "content": prompt}
        ], response_format=QuizResponseSchema
    )
    print(response)
    try:
        data = {
            "id": response.id,
            "questions": response.choices[0].message.parsed.questions
        }
        return data
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

