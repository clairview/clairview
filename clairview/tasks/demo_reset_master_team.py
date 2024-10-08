from django.db import transaction

from clairview.demo.matrix import MatrixManager
from clairview.demo.products import HedgeboxMatrix


def demo_reset_master_team() -> None:
    matrix = HedgeboxMatrix()
    manager = MatrixManager(matrix)
    with transaction.atomic():
        manager.reset_master()
