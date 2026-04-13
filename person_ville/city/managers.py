__all__ = [
    'load_quiz_data',
    'normalize_entry_answers',
    'score_entry_answers',
    'build_city_from_scores',
    'apply_street_correction',
]

import json
from pathlib import Path


def load_quiz_data():
    file_path = (
        Path(__file__).resolve().parent.parent / 'quizzes' / 'questions.json'
        )
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def normalize_entry_answers(raw_answers):
    normalized = {}

    for question_id, value in raw_answers.items():
        normalized[str(question_id)] = int(value)

    return normalized


def score_entry_answers(quiz_data, raw_answers):
    answers = normalize_entry_answers(raw_answers)

    trait_scores = {
        'extraversion': 0,
        'agreeableness': 0,
        'conscientiousness': 0,
        'negative_emotionality': 0,
        'openness': 0,
    }

    for question in quiz_data['questions']:
        question_id = question['id']
        trait = question['trait']
        reverse = question['reverse']

        raw_value = int(answers[question_id])
        final_value = 6 - raw_value if reverse else raw_value
        trait_scores[trait] += final_value

    trait_levels = {}
    for trait, score in trait_scores.items():
        if 3 <= score <= 6:
            level = 'low'
        elif 7 <= score <= 11:
            level = 'mid'
        else:
            level = 'high'

        trait_levels[trait] = {
            'score': score,
            'level': level,
        }

    return trait_levels


def build_city_from_scores(quiz_data, scored_traits):
    streets = []

    for trait, trait_result in scored_traits.items():
        level = trait_result['level']
        street_data = quiz_data['streets'][trait]

        streets.append({
            'trait': trait,
            'name': street_data['name'],
            'subtitle': street_data['subtitle'],
            'description': street_data['descriptions'][level],
            'houses': street_data['houses'][level],
            'visual': street_data['visual'][level],
            'score': trait_result['score'],
            'level': level,
            'correction_done': False,
            'correction_answer': None,
            'correction_tone': None,
            'correction_text': None,
        })

    return {
        'title': quiz_data['meta']['title'],
        'streets': streets,
    }


def apply_street_correction(street_data, quiz_data, answer_code):
    effect = quiz_data['correction_effects'][answer_code]

    updated_street = dict(street_data)
    updated_street['correction_done'] = True
    updated_street['correction_answer'] = answer_code
    updated_street['correction_tone'] = effect['tone']
    updated_street['correction_text'] = effect['text']

    return updated_street
