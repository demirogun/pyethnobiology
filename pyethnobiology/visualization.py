import numpy as np
import pandas as pd
from pycirclize import Circos
from pycirclize.parser import Matrix
import matplotlib.pyplot as plt
import matplotlib.colors as mplcolors
from matplotlib.cm import ScalarMappable
from textwrap import wrap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

class ChordPlot:

    def __init__(

            self,
            data: pd.DataFrame,
            by: str = "taxon",
            informant_column: str = "informant",
            taxon_column: str = "taxon",
            use_column: str = "ailments_treated",
            colors: str = None,
            min_info_count: int = None,
            get_first: int = None
    ):

        """
            Initialize a ChordPlot object for visualizing relationships between data elements.

            Args:
                data (pd.DataFrame): The data frame containing relevant information.
                by (str, optional): The column to group data by, defaults to "informant".
                informant_column (str, optional): The column name for informant data, defaults to "informant".
                taxon_column (str, optional): The column name for taxon data, defaults to "taxon".
                use_column (str, optional): The column name for additional data associated with each pair, defaults to "ailments_treated".
                colors (list, optional): A list of colors for the links in the plot.
                min_info_count (int, optional): The minimum information count to include in the plot.
                get_first (int, optional): The number of top entries to show in the plot.

            Returns:
                A ChordPlot object.

        """

        self.data = data
        self.colors = colors
        self.by = by
        self.min_info_count = min_info_count
        self.get_first = get_first
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column

    def plot(self):

        """
            Generate and display a circular chord plot using the prepared data.

            Returns:
                A Circos object containing the plot figure.

            Raises:
                Exception: If any error occurs during plot generation.
        """

        # Prepare data for visualization
        matrix, order = self._prepare_data()

        # Create the Circos plot
        circos = self._create_plot(matrix, order)

        return circos.plotfig()

    def save_plot(self, filename: str, dpi: int = 300):

            """
                Generate and save a circular chord plot using the prepared data.

                Args:
                    filename (str): The name of the file to save the plot to.
                    dpi (int, optional): The resolution of the plot, defaults to 300.

                Raises:
                    Exception: If any error occurs during plot generation.
            """

            # Prepare data for visualization
            matrix, order = self._prepare_data()

            # Create the Circos plot
            circos = self._create_plot(matrix, order)

            # Save the plot to a file
            circos.savefig(filename, dpi=dpi)


    def _prepare_data(self) -> pd.DataFrame:

        """
            Prepare the data for generating the ChordPlot by counting occurrences and creating a matrix.

            Returns:
                A tuple containing:
                    - matrix (pd.DataFrame): A data frame with informant counts for each pair.
                    - order (list): A list of labels for the circular plot.
        """

        if self.by == "informant":
            taxon_column = self.informant_column
            ailments_treated_column = self.use_column
        else:
            taxon_column = self.taxon_column
            ailments_treated_column = self.use_column

        informant_counts = (
            self.data.groupby([taxon_column, ailments_treated_column])
            .size()
            .reset_index(name="informant_count")
            .sort_values(by="informant_count", ascending=False)
        )  # Remove slicing for now

        # Apply filtering based on user preference
        if self.get_first is not None:
            informant_counts = informant_counts.head(self.get_first)  # Limit by number of species
        elif self.min_info_count is not None:
            informant_counts = informant_counts[
                informant_counts["informant_count"] >= self.min_info_count]  # Limit by minimum count

        informant_counts = informant_counts.reset_index(drop=True)

        matrix_data = [[row[taxon_column], row[ailments_treated_column], row["informant_count"]] for idx, row in
                       informant_counts.iterrows()]
        matrix = Matrix.parse_fromto_table(pd.DataFrame(matrix_data))
        order = list(set(informant_counts[taxon_column].to_list())) + list(
            set(informant_counts[ailments_treated_column].to_list()))
        return matrix, order

    def _create_plot(self, matrix: pd.DataFrame, order: list) -> Circos:

        """
            Create the Circos plot using the prepared data and configuration.

            Args:
                matrix (pd.DataFrame): The data frame with informant counts for each pair.
                order (list): The list of labels for the circular plot.

            Returns:
                A Circos object containing the plot figure.
        """

        circos = Circos.initialize_from_matrix(
            matrix=matrix,
            space=3,
            r_lim=(97, 100),
            cmap=self.colors if self.colors else "tab10",
            label_kws=dict(size=9, orientation="vertical"),
            link_kws=dict(ec="black", lw=0.1),
            order=order,
        )
        return circos

class HeatmapPlot:
    """
    Creates a heatmap plot to visualize data in a grid format.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 title: str,
                 value_column: str,
                 row_column: str,
                 column_column: str,
                 cmap: str = "coolwarm",
                 show_colorbar: bool = True,
                 colorbar_shrink: float = 0.50,
                 plot_width: float = 10,
                 plot_height: float = 8,
                 dpi: int = 300,
                 fillna_zero: bool = True):

        self.data = data
        self.title = title
        self.value_column = value_column
        self.row_column = row_column
        self.column_column = column_column
        self.cmap = cmap
        self.show_colorbar = show_colorbar
        self.colorbar_shrink = colorbar_shrink
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.dpi = dpi
        self.fillna_zero = fillna_zero

    def plot(self):
        """Creates and displays the heatmap plot."""

        self._prepare_data()
        self._create_plot()
        self._customize_plot()
        return self.fig, self.ax

    def save_plot(self, filename: str, dpi: int = 300):
        """Saves the heatmap plot to a file."""

        self._prepare_data()
        self._create_plot()
        self._customize_plot()
        self.fig.savefig(filename, bbox_inches="tight", dpi=dpi)

    def _prepare_data(self):
        """Pivots data into a suitable format for heatmap."""

        self.heatmap_data = self.data.pivot(index=self.row_column, columns=self.column_column, values=self.value_column)
        if self.fillna_zero:
            self.heatmap_data = self.heatmap_data.fillna(0)

    def _create_plot(self):
        """Creates the base heatmap plot."""

        self.fig, self.ax = plt.subplots(figsize=(self.plot_width, self.plot_height), dpi=self.dpi)
        self.im = self.ax.imshow(self.heatmap_data, cmap=self.cmap)

    def _customize_plot(self):
        """Customizes plot appearance."""

        plt.rcParams["text.color"] = "#1f1f1f"
        plt.rcParams.update({"font.family": "serif"})
        plt.rc("axes", unicode_minus=False)

        # Set tick labels
        if len(self.heatmap_data.columns) > 10:
            rotation, ha = (90, "center")
        else:
            rotation, ha = (45, "right")

        plt.xticks(ticks=range(len(self.heatmap_data.columns)), labels=self.heatmap_data.columns, rotation=rotation,
                   ha=ha)
        plt.yticks(ticks=range(len(self.heatmap_data.index)), labels=self.heatmap_data.index)

        # Add colorbar if enabled
        if self.show_colorbar:
            self._add_colorbar()

        # Customize labels and title
        plt.xlabel(self.column_column)
        plt.ylabel(self.row_column)
        plt.title(self.title)  # Add a title if needed

    def _add_colorbar(self):
        """Adds a colorbar to the plot."""

        plt.colorbar(self.im, label=self.title, shrink=self.colorbar_shrink)

class RadialPlot:
    """
    Creates a radial bar plot to visualize data in a circular layout.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 colorbar_title: str,
                 indice: str = None,
                 num_rows: int = 10,
                 ytick_position: str = "onbar",
                 colors: list = None,
                 show_colorbar: bool = True,
                 informant_column: str = "informant",
                 taxon_column: str = "taxon",
                 use_column: str = "ailments_treated"):

        self.data = data
        self.colorbar_title = colorbar_title
        self.indice = indice
        self.num_rows = num_rows
        self.yticks = None
        self.num_ticks = 5
        self.ytick_position = ytick_position
        self.colors = colors
        self.show_colorbar = show_colorbar
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column

    def plot(self):
        """Creates and displays the radial bar plot."""

        self._prepare_data()
        self._create_plot()
        self._customize_plot()
        return self.fig, self.ax

    def save_plot(self, filename: str, dpi: int = 300):
        """Saves the radial bar plot to a file."""

        self._prepare_data()
        self._create_plot()
        self._customize_plot()
        self.fig.savefig(filename, bbox_inches="tight", dpi=dpi)

    def _prepare_data(self):
        """Prepares data for plotting."""

        self.indice_df = self.data.head(self.num_rows) if isinstance(self.num_rows, int) else self.data
        self.angles = np.linspace(0.05, 2 * np.pi - 0.05, len(self.indice_df), endpoint=False)
        self.indice_values = self.indice_df[self.indice].values
        self.taxon_values = self.indice_df[self.use_column].values if self.indice == "FIC" else self.indice_df[
            self.taxon_column].values

    def _create_plot(self):
        """Creates the base plot."""

        self.fig, self.ax = plt.subplots(figsize=(9, 12.6), subplot_kw={"projection": "polar"})
        self.ax.set_theta_offset(1.2 * np.pi / 2)
        self.ax.set_ylim(0 - (self.indice_values.min() * 0.4), self.indice_values.max())

        self._set_colormap()

        if len(self.indice_values) < 6:
            width = 1.4
        else:
            width = 0.52

        self.bars = self.ax.bar(self.angles, self.indice_values, color=self.colors, alpha=0.9, width=width, zorder=10)

    def _customize_plot(self):
        """Customizes plot appearance."""

        plt.rcParams["text.color"] = "#1f1f1f"
        plt.rcParams.update({"font.family": "serif"})
        plt.rc("axes", unicode_minus=False)

        # Wrap taxon labels for better readability
        self.taxon_values = ["\n".join(wrap(r, 5, break_long_words=False)) for r in self.taxon_values]

        # Customize axes and ticks
        self.ax.xaxis.grid(False)
        self.ax.spines["start"].set_color("none")
        self.ax.spines["polar"].set_color("none")
        self.ax.set_xticks(self.angles)
        self.ax.set_xticklabels(self.taxon_values, size=12)

        # Set y-ticks and labels based on position preference
        self._set_yticks_and_labels()

        # Add colorbar if enabled
        if self.show_colorbar:
            self._add_colorbar()

    def _set_colormap(self):
        """Sets the colormap for the bars."""

        if self.colors is None:
            # Use default colors
            self.colors = ["#ffcc70", "#c63d2f"]
        else:
            # Use provided colors
            self.colors = self.colors

        # Create colormap and normalize values
        self.cmap = mplcolors.LinearSegmentedColormap.from_list("my_colormap", self.colors, N=256)
        self.norm = mplcolors.Normalize(vmin=self.indice_values.min(), vmax=self.indice_values.max())
        self.colors = self.cmap(self.norm(self.indice_values))

    def _set_yticks_and_labels(self):
        """Sets y-ticks and labels based on the specified position."""

        self.ax.set_yticklabels([])
        self.yticks = np.linspace(0, self.indice_values.max() + (self.indice_values.max() * .20), self.num_ticks)
        self.ax.set_yticks(list(self.yticks))

        if self.ytick_position == "on_line":
            # Place y-tick labels on a separate line
            pad = self.indice_values.min() * 0.1
            for yt in self.yticks:
                self.ax.text(-0.2 * np.pi / 2, yt + pad, round(yt, 3), ha="center", size=11, zorder=15)
        else:
            # Place y-tick labels on the bars
            for bar, length in zip(self.bars, self.indice_values):
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width() / 2, height, f'{length:.3f}', ha='center', va='bottom',
                             fontsize=10, zorder=15)

    def _add_colorbar(self):
        """Adds a colorbar to the plot."""

        cax = inset_axes(
            self.ax,
            width="100%",
            height="100%",
            loc="center",
            bbox_to_anchor=(0.325, 0.1, 0.35, 0.01),
            bbox_transform=self.fig.transFigure
        )

        # Access the already-defined yticks
        yticks = np.linspace(self.indice_values.min(), self.indice_values.max(), self.num_ticks)

        cbar = self.fig.colorbar(
            ScalarMappable(norm=self.norm, cmap=self.cmap),
            cax=cax,
            orientation="horizontal",
            ticks=yticks
        )

        cbar.outline.set_visible(False)
        cbar.ax.xaxis.set_tick_params(size=0)
        cbar.set_label(self.colorbar_title, size=12, labelpad=-40)