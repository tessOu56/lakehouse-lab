from lakehouse_lab.assets.github_events import github_events_bronze
from dagster import Definitions

defs = Definitions(assets=[github_events_bronze])
