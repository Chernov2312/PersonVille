__all__ = (
    'load_quiz_data',
    'normalize_entry_answers',
    'score_entry_answers',
    'build_city_from_scores',
    'apply_house_answer',
    'build_final_character',
    'apply_street_correction',
)

import json
from pathlib import Path

from django.utils import timezone

STREET_IMAGE_MAP = {
    'negative_emotionality': 'images/streets/Weather Street.png',
    'openness': 'images/streets/Street of Windows.png',
    'conscientiousness': 'images/streets/Rhythm Street.png',
    'extraversion': 'images/streets/Presence Lane.png',
    'agreeableness': 'images/streets/Communication Street.png',
}


TRAIT_ORDER = [
    'extraversion',
    'agreeableness',
    'conscientiousness',
    'negative emotionality',
    'openness',
]


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


def _build_houses(trait, houses):
    result = []

    for index, text in enumerate(houses[:3], start=1):
        result.append(
            {
                'house_id': f'{trait}_{index}',
                'base_text': text,
                'final_text': text,
                'answer_value': None,
                'completed': False,
                'position': index,
            },
        )

    return result


def build_city_from_scores(quiz_data, scored_traits):
    streets = []

    for trait, trait_result in scored_traits.items():
        level = trait_result['level']
        street_data = quiz_data['streets'][trait]
        house_texts = street_data['houses'][level]
        houses = _build_houses(trait, house_texts)

        streets.append(
            {
                'trait': trait,
                'name': street_data['name'],
                'subtitle': street_data['subtitle'],
                'description': street_data['descriptions'][level],
                'houses': houses,
                'image': STREET_IMAGE_MAP.get(trait, ''),
                'visual': street_data['visual'][level],
                'score': trait_result['score'],
                'level': level,
                'answered_count': 0,
                'completed': False,
            },
        )

    return {
        'title': quiz_data['meta']['title'],
        'streets': streets,
        'all_completed': False,
        'is_finalized': False,
    }


def apply_house_answer(house_data, answer_value):
    updated_house = dict(house_data)
    updated_house['answer_value'] = answer_value
    updated_house['completed'] = True
    updated_house['final_text'] = updated_house['base_text']
    return updated_house


def _pick_trait_allegory(quiz_data, trait, level):
    final_character = quiz_data.get('final_character_v2', {})
    trait_allegories = final_character.get('trait_allegories', {})
    trait_variants = trait_allegories.get(trait, {})
    texts = trait_variants.get(level, [])

    if texts:
        return texts[0]

    return ''


def _match_summary_conditions(scored_traits, conditions):
    for trait, required_level in conditions.items():
        current_level = scored_traits.get(trait, {}).get('level')
        if current_level != required_level:
            return False
    return True


def _pick_city_summary(quiz_data, scored_traits):
    final_character = quiz_data.get('final_character_v2', {})
    summary_selector = final_character.get('final_city_summary_selector', {})
    summary_templates = final_character.get('final_city_summary_templates', {})

    for summary_key, conditions in summary_selector.items():
        if _match_summary_conditions(scored_traits, conditions):
            variants = summary_templates.get(summary_key, [])
            if variants:
                return variants[0]

    fallback_variants = summary_templates.get('fallback', [])
    if fallback_variants:
        return fallback_variants[0]

    return ''


def build_final_character(city_result, scored_traits):
    quiz_data = load_quiz_data()

    trait_allegories = []
    for trait in TRAIT_ORDER:
        trait_data = scored_traits.get(trait, {})
        level = trait_data.get('level', 'mid')
        text = _pick_trait_allegory(quiz_data, trait, level)

        trait_allegories.append(
            {
                'trait': trait,
                'level': level,
                'text': text,
            },
        )

    city_summary = _pick_city_summary(quiz_data, scored_traits)
    server_date = timezone.localdate().strftime('%d.%m.%Y')

    return {
        'title': 'Итог PersonVille',
        'trait_allegories': trait_allegories,
        'city_summary': city_summary,
        'server_created_at': server_date,
        'image_export_enabled': True,
        'copy_link_enabled': True,
        'download_enabled': True,
    }


def apply_street_correction(street_data, quiz_data, answer_code):
    effect = quiz_data['correction_effects'][answer_code]

    updated_street = dict(street_data)
    updated_street['correction_done'] = True
    updated_street['correction_answer'] = answer_code
    updated_street['correction_tone'] = effect['tone']
    updated_street['correction_text'] = effect['text']

    return updated_street
