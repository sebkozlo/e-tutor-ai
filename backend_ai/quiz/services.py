from celery import shared_task
from openai import OpenAI
from typing import Dict, List
from django.conf import settings
from .schemas import QuizResponseListSchema, SolutionResponseSchema
import json

client = OpenAI()
client.api_key = settings.OPENAI_API_KEY


def generate_quiz(
    question_count: int, difficulty: str, question_type: list[str], content: str
) -> Dict:
    type_descriptions = {
        "SINGLE": "- Pytania typu 'SINGLE' powinny zawierać jedno pytanie i jedno prawidłowe rozwiązanie (jedna opcja).\n",
        "MULTI": "- Pytania typu 'MULTI' powinny zawierać jedno pytanie i 4 propozycje odpowiedzi i wiele poprawnych odpowiedzi (wielokrotny wybór).\n",
        "FILL": "- Pytania typu 'FILL' powinny zawierać pytania z brakującymi słowami. Odpowiedź to lista brakujących słów lub fraz.\n",
        "ORDER": "- Pytania typu 'ORDER' powinny zawierać opcje do uporządkowania we właściwej kolejności.\n",
        "TRUE_FALSE": "- Pytania typu 'TRUE_FALSE' powinny być w formie twierdzenia, na które odpowiedź to tylko 'PRAWDA' lub 'FAŁSZ'.\n",
    }

    examples = {
        "SINGLE": "1. Pytanie typu 'SINGLE': 'Jakie jest stolica Polski? Odpowiedź: Warszawa'\n",
        "MULTI": "2. Pytanie typu 'MULTI': 'Wybierz wszystkie stolice krajów europejskich: Warszawa, Moskwa, Tokio, Paryż'. Poprawne odpowiedzi: Warszawa, Moskwa, Paryż\n",
        "FILL": "3. Pytanie typu 'FILL': Pytanie: 'Uzupełnij'. Options: ['Polska ma stolicę w ____.' , 'Klasa bazowa w Javie nosi nazwę ____'] Odpowiedź: ['Warszawa', 'Object']. \n",
        "ORDER": "4. Pytanie typu 'ORDER': 'Ułóż miasta w kolejności alfabetycznej: Warszawa, Paryż, Londyn'. Poprawna kolejność: Londyn, Paryż, Warszawa\n",
        "TRUE_FALSE": "5. Pytanie typu 'TRUE_FALSE': 'Warszawa jest stolicą Polski'. Odpowiedź: PRAWDA\n",
    }

    difficulty_descriptions = {
        "EASY": "Łatwy – proste pytania podstawowe, wymagające ogólnej wiedzy.",
        "MEDIUM": "Średni – pytania wymagające pewnej wiedzy, ale nadal dostępne.",
        "HARD": "Trudny – pytania szczegółowe, wymagające dobrej znajomości tematu.",
        "EXPERT": "Ekspercki – pytania dla bardzo zaawansowanych, wymagające głębokiego zrozumienia.",
        "MASTER": "Mistrzowski – pytania wyjątkowo trudne, często podchwytliwe, wymagające biegłości eksperckiej.",
    }

    selected_descriptions = "".join([type_descriptions[t] for t in question_type])
    selected_examples = "".join([examples[t] for t in question_type])
    joined_types = ", ".join(question_type)

    difficulty_text = difficulty_descriptions.get(difficulty, difficulty)

    prompt = (
        f"Wygeneruj {question_count} pytań na poziomie trudności {difficulty} "
        f"({difficulty_text}) na temat: {content}.\n"
        f"Pytania powinny być wyłącznie typu: {joined_types}.\n\n"
        f"Dla każdego pytania dopasuj odpowiedni schemat odpowiedzi:\n"
        f"{selected_descriptions}\n"
        f"Upewnij się, że każde pytanie ma poprawnie ustawione pole 'question_type' "
        f"i poprawne pole 'correct_answer'.\n\n"
        f"Przykłady:\n{selected_examples}\n"
        "Przy zadaniu typu 'FILL' liczba zdań do uzupełnienia powinna wynosić 5.\n"
        "Nie twórz pytań innych typów niż podane. "
        "Odpowiedzi udziel w języku polskim. "
        "Zwróć wynik jako JSON w polu 'quiz', zawierający listę pytań."
    )

    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Jesteś pomocnym asystentem do generowania quizów. Twoim zadaniem jest stworzenie pytań w oparciu o określony typ, trudność i temat.",
            },
            {"role": "user", "content": prompt},
        ],
        text_format=QuizResponseListSchema,
    )
    # print(response)
    try:
        return response.output_parsed
    except Exception as e:
        return e


def generate_solution(question: str, solution_level: int) -> Dict:
    response = client.responses.parse(
        model="gpt-4o",
        input=[
            {
                "role": "system",
                "content": "Jesteś ekspertem w wielu dziedzinach wiedzy, takich jak programowanie, matematyka, nauki przyrodnicze, historia, geografia i inne. Twoim zadaniem jest udzielanie odpowiedzi na pytania w formacie JSON zgodnie z poziomem szczegółowości określonym przez 'solution_level'.",
            },
            {
                "role": "user",
                "content": f"Odpowiedz na pytanie: {question}\n"
                f"Poziom podpowiedzi: {solution_level}\n"
                f"- solution_level = 1: Udziel krótkiej, ogólnej podpowiedzi naprowadzającej na odpowiedź, lecz nie podawaj bezpośredniej odpowiedzi.\n"
                f"- solution_level = 2: Udziel bardziej szczegółowej podpowiedzi, dokładniej tłumacząc kluczowe pojęcia, możesz pomóc wykluczyć jakąś z poponowanych odpowiedz jeśli taki istnieją w 'options', lecz nie podawaj bezpośredniej prawidłowej odpowiedzi.\n"
                f"- solution_level = 3: Wskaż prawidłową odpowiedź i dokładnie wyjaśnij, dlaczego jest poprawna.\n"
                "Odpowiedzi udzielaj w języku polskim.",
            },
        ],
        text_format=SolutionResponseSchema,
    )

    try:
        return response.output_parsed

    except Exception as e:
        return e
