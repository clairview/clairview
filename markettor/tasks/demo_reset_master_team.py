from django.db import transaction

from markettor.demo.matrix import MatrixManager
from markettor.demo.products import HedgeboxMatrix


def demo_reset_master_team() -> None:
    matrix = HedgeboxMatrix()
    manager = MatrixManager(matrix)
    with transaction.atomic():
        manager.reset_master()
