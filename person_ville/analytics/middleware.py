# statistics/middleware.py
from datetime import datetime

from django.utils.timezone import now

from analytics.models import CompletedQuizSession


class QuizStatisticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'quiz_start_time' not in request.session:
            request.session['quiz_start_time'] = now().isoformat()

        response = self.get_response(request)

        if request.session.get('final_character') and not request.session.get(
            '_saved',
        ):
            self._save_session(request)
            request.session['_saved'] = True

        return response

    def _save_session(self, request):
        start_str = request.session.get('quiz_start_time')
        if not start_str:
            return

        start_time = datetime.fromisoformat(start_str)
        end_time = now()
        duration = int((end_time - start_time).total_seconds())

        CompletedQuizSession.objects.create(
            session_key=request.session.session_key,
            user=request.user if request.user.is_authenticated else None,
            started_at=start_time,
            completed_at=end_time,
            duration_seconds=duration,
            final_character=request.session.get('final_character'),
        )
