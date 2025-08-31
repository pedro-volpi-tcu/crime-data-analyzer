import logging

import pandas as pd

from .models import AprehensionCategory, BaseCategory, CrimeEvent, VictimCategory, WeightCategory

logger = logging.getLogger(__name__)


class CrimeEventsBuilder:
    """Receives a processed dataframe (grouped by 'crime_type') and returns a list of CrimeEvent objects."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    def build(self) -> list[CrimeEvent]:
        events: list[CrimeEvent] = []
        for row in self._df.itertuples(index=False):
            try:
                event = CrimeEvent(
                    name=getattr(row, "crime_type"),
                    victims=getattr(row, "victims", 0),
                    weight=getattr(row, "weight", 0.0),
                    aprehensions=getattr(row, "aprehensions", 0),
                )
                events.append(event)

            except (AttributeError, TypeError, ValueError) as e:
                logger.critical(f"Skipping malformed Dataframe row: {row}. Error: {e}")

        return events


class CrimeCategoryBuilder:
    """Receives a list of CrimeEvent objects and returns a dict of each crime category aggregate."""

    def __init__(self, events: list[CrimeEvent]) -> None:
        self._events = events

    def build(self) -> dict[str, BaseCategory]:
        logger.info("--- Building aggregate Category objects from list of CrimeEvents. ---")

        return {
            "victims": VictimCategory([e.victims for e in self._events]),
            "weight": WeightCategory([e.weight for e in self._events]),
            "aprehensions": AprehensionCategory([e.aprehensions for e in self._events]),
        }
