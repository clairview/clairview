from markettor.settings import EE_AVAILABLE

if EE_AVAILABLE:
    from ee.clickhouse.queries.paths import ClickhousePaths as Paths
    from ee.clickhouse.queries.paths import ClickhousePathsActors as PathsActors
else:
    from markettor.queries.paths.paths import Paths  # type: ignore
    from markettor.queries.paths.paths_actors import PathsActors  # type: ignore
