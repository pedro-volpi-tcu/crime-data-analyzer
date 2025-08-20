import logging
from abc import ABC, abstractmethod
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

logger = logging.getLogger(__name__)


class Plotter(ABC):
    @abstractmethod
    def plot(self, data: pd.DataFrame, title: str, output_path: Path) -> None:
        pass


class BarPlotter(Plotter):
    def plot(self, data: pd.DataFrame, title: str, output_path: Path) -> None:
        """
        Generates a horizontal bar chart from a DataFrame.
        Assumes the DataFrame has two columns: a category (y-axis) and a value (x-axis).
        """
        if data.empty or len(data.columns) < 2:
            logger.warning(f"Dados insuficientes para gerar o gráfico de barras '{title}'.")
            return

        # Use a professional and pleasant style
        sns.set_theme(style="whitegrid")

        plt.figure(figsize=(12, 8))

        # Assume the first column is the category (y) and the second is the value (x)
        y_axis = data.columns[0]
        x_axis = data.columns[1]

        # Create the barplot
        barplot = sns.barplot(
            x=x_axis,
            y=y_axis,
            data=data,
            palette="viridis",
            hue=y_axis,  # Color bars by category
            legend=False,  # Disable the legend which is redundant here
        )

        # Add labels on the bars for clarity
        barplot.bar_label(barplot.containers[0], fmt="%.0f", padding=3)

        plt.title(title, fontsize=16)
        plt.xlabel(x_axis, fontsize=12)
        plt.ylabel(y_axis, fontsize=12)
        plt.tight_layout()  # Adjust layout to prevent labels from being cut off

        try:
            plt.savefig(output_path)
            logger.info(f"Gráfico de barras salvo em: '{output_path}'")
        except Exception as e:
            logger.error(f"Erro ao salvar o gráfico: {e}")
        finally:
            plt.close()
