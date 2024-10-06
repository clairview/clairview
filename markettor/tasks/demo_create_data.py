from celery import shared_task
from django.core.cache import cache

from markettor.demo.matrix import manager
from markettor.demo.products.hedgebox.matrix import HedgeboxMatrix
from markettor.models.team.team import Team
from markettor.models.user import User


@shared_task(ignore_result=True)
def create_data_for_demo_team(team_id: int, user_id: int, cache_key: str) -> None:
    team = Team.objects.get(pk=team_id)
    user = User.objects.get(pk=user_id)
    if team and user:
        manager.MatrixManager(HedgeboxMatrix(), use_pre_save=True).run_on_team(team, user)
        cache.delete(cache_key)
