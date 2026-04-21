__all__ = ('QuizStatisticsMiddleware',)
from datetime import datetime
import json
from pathlib import Path

from django.utils.timezone import now


class QuizStatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.stats_file = (
            Path(__file__).parent / 'statistics' / 'quiz_stats.json'
        )

    def __call__(self, request):
        if hasattr(request, 'session'):
            if 'quiz_statistics' not in request.session:
                request.session['quiz_statistics'] = self._init_statistics(
                    request,
                )

            if 'entry_answers' in request.session:
                stats = request.session['quiz_statistics']
                current_answers_count = len(
                    request.session.get('entry_answers', {}),
                )
                if current_answers_count > stats.get(
                    'total_questions_answered',
                    0,
                ):
                    stats['total_questions_answered'] = current_answers_count
                    stats['entry_answers_history'].append(
                        {
                            'timestamp': now().isoformat(),
                            'answers_count': current_answers_count,
                            'answers': request.session['entry_answers'].copy(),
                        },
                    )
                    request.session.modified = True

        response = self.get_response(request)

        if hasattr(request, 'session'):
            if (
                'city_result' in request.session
                and request.session['city_result'] is not None
            ):
                stats = request.session.get('quiz_statistics', {})
                city_result = request.session['city_result']

                if city_result and not stats.get('quiz_completed', False):
                    self._check_completion_status(request, stats, city_result)

                self._track_city_progress(request, stats, city_result)

            if (
                'final_character' in request.session
                and 'quiz_statistics' in request.session
            ):
                stats = request.session['quiz_statistics']
                if not stats.get('final_character_result'):
                    stats['final_character_result'] = request.session[
                        'final_character'
                    ].copy()
                    stats['quiz_completion_time'] = now().isoformat()
                    if stats.get('quiz_start_time'):
                        start = datetime.fromisoformat(
                            stats['quiz_start_time'],
                        )
                        end = datetime.fromisoformat(
                            stats['quiz_completion_time'],
                        )
                        stats['quiz_duration_seconds'] = (
                            end - start
                        ).total_seconds()
                    stats['quiz_completed'] = True
                    request.session.modified = True
                    self._save_statistics(request, stats)

            if (
                'quizzes:close' in request.path
                or 'quizzes:restart' in request.path
            ):
                self._save_final_statistics(request)

        return response

    def _init_statistics(self, request):
        return {
            'session_id': request.session.session_key,
            'user_id': (
                request.user.id if request.user.is_authenticated else None
            ),
            'quiz_start_time': now().isoformat(),
            'quiz_completion_time': None,
            'quiz_duration_seconds': None,
            'entry_answers_history': [],
            'scored_traits_history': [],
            'city_progress_history': [],
            'street_correction_history': [],
            'final_character_result': None,
            'quiz_completed': False,
            'total_questions_answered': 0,
            'streets_completed_count': 0,
            'houses_completed_count': 0,
        }

    def _check_completion_status(self, request, stats, city_result):
        if city_result.get('all_completed') and not stats.get(
            'quiz_completed',
        ):
            stats['quiz_completed'] = True
            if 'scored_traits' in request.session:
                stats['scored_traits_history'].append(
                    {
                        'timestamp': now().isoformat(),
                        'traits': request.session['scored_traits'].copy(),
                    },
                )

            streets_completed = sum(
                1
                for street in city_result.get('streets', [])
                if street.get('completed', False)
            )
            houses_completed = sum(
                sum(
                    1
                    for house in street.get('houses', [])
                    if house.get('completed', False)
                )
                for street in city_result.get('streets', [])
            )

            stats['streets_completed_count'] = streets_completed
            stats['houses_completed_count'] = houses_completed
            request.session.modified = True

    def _track_city_progress(self, request, stats, city_result):
        if city_result is None:
            return

        current_progress = {
            'timestamp': now().isoformat(),
            'all_completed': city_result.get('all_completed', False),
            'is_finalized': city_result.get('is_finalized', False),
            'streets': [
                {
                    'trait': street.get('trait'),
                    'completed': street.get('completed', False),
                    'answered_count': street.get('answered_count', 0),
                    'houses_count': len(street.get('houses', [])),
                }
                for street in city_result.get('streets', [])
            ],
        }

        if not stats.get('city_progress_history'):
            stats['city_progress_history'] = []

        last_progress = (
            stats['city_progress_history'][-1]
            if stats['city_progress_history']
            else None
        )
        if last_progress != current_progress:
            stats['city_progress_history'].append(current_progress)
            request.session.modified = True

    def _save_statistics(self, request, stats):
        self._ensure_directory_exists()

        all_stats = self._load_all_statistics()

        session_key = request.session.session_key
        all_stats[session_key] = stats

        self._write_statistics(all_stats)

    def _save_final_statistics(self, request):
        if 'quiz_statistics' in request.session:
            stats = request.session['quiz_statistics']
            stats['quiz_completion_time'] = now().isoformat()
            if stats.get('quiz_start_time'):
                start = datetime.fromisoformat(stats['quiz_start_time'])
                end = datetime.fromisoformat(stats['quiz_completion_time'])
                stats['quiz_duration_seconds'] = (end - start).total_seconds()
            self._save_statistics(request, stats)

    def _ensure_directory_exists(self):
        self.stats_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_all_statistics(self):
        if self.stats_file.exists():
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _write_statistics(self, data):
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
