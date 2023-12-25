import pandas as pd

from pyethnobiology.visualization import RadialPlot
from pyethnobiology.visualization import HeatmapPlot

class FC:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs. Defaults to "informant".
            taxon_column (str, optional): Name of the column containing species names. Defaults to "taxon".
            use_column (str, optional): Name of the column containing plant uses. Defaults to "ailments_treated".
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column

    def calculate(self):
        """
        Calculates the frequency of citation (FC) for each species.

        Returns:
            pd.DataFrame: DataFrame containing taxon and FC columns.
        """

        # Calculate FC per species by counting unique informants for each taxon
        fc_df = (
            self.data.groupby(self.taxon_column)[self.informant_column]
            .nunique()
            .reset_index(name="FC")
        )

        # Sort FC values in descending order
        fc_df = fc_df.sort_values(by="FC", ascending=False).reset_index(drop=True)

        return fc_df

    def save_data(self):
        FC_df = self.calculate()
        FC_df.to_csv("frequency_of_citation_FC.csv", index=False)
        print("Saved to frequency_of_citation_FC.csv")

    def plot_radial(self, filename="FC.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), "Frequency of Citation (FC)", "FC", num_row, ytick_position, colors,
                                 show_colorbar, self.informant_column, self.taxon_column, self.use_column)

        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class NU:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs.
            taxon_column (str, optional): Name of the column containing species names.
            use_column (str, optional): Name of the column containing plant uses.
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Number of Uses (NU) per Species"

    def calculate(self):
        """
        Calculates the NU for each species.

        Returns:
            pd.DataFrame: DataFrame containing taxon and NU columns.
        """

        nu_df = (
            self.data.groupby(self.taxon_column)[self.use_column]
            .nunique()
            .reset_index(name="NU")
        )
        nu_df = nu_df.sort_values(by="NU", ascending=False).reset_index(drop=True)
        return nu_df
    def save_data(self):
        NU_df = self.calculate()
        NU_df.to_csv("number_of_uses_NU.csv", index=False)
        print("Saved to number_of_uses_NU.csv")

    def plot_radial(self, filename="NU.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "NU", num_row, ytick_position, colors, show_colorbar, self.informant_column, self.taxon_column, self.use_column)

        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class UR:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs.
            taxon_column (str, optional): Name of the column containing species names.
            use_column (str, optional): Name of the column containing plant uses.
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Use Report (UR) per Species"

    def calculate(self):
        """
        Calculates the UR for each species.

        Returns:
            pd.DataFrame: DataFrame containing taxon and UR columns.
        """

        ur_df = (
            self.data.groupby(self.taxon_column, observed=True)
            .size()
            .reset_index(name="UR")
            .sort_values(by="UR", ascending=False)
            .reset_index(drop=True)
        )
        return ur_df

    def save_data(self):
        UR_df = self.calculate()
        UR_df.to_csv("use_report_UR.csv", index=False)
        print("Saved to use_report_UR.csv")

    def plot_radial(self, filename="UR.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "UR", num_row, ytick_position, colors, show_colorbar,
                                 self.informant_column, self.taxon_column, self.use_column)
        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class CI:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs. Defaults to "informant".
            taxon_column (str, optional): Name of the column containing species names. Defaults to "taxon".
            use_column (str, optional): Name of the column containing plant uses. Defaults to "ailments_treated".
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Cultural Importance (CI) Index"

    def calculate(self):
        """
        Calculates the cultural importance index (CI) for each species.

        Returns:
            pd.DataFrame: DataFrame containing taxon and CI columns.
        """

        # Calculate Use Reports (UR) per species
        ur_df = UR(self.data, self.informant_column, self.taxon_column, self.use_column).calculate()

        # Count unique informants
        informants_count = self.data[self.informant_column].nunique()

        # Merge UR and informants count based on 'taxon'
        ci_df = pd.merge(
            ur_df,
            self.data[[self.taxon_column, self.informant_column]]
            .drop_duplicates()
            .groupby(self.taxon_column, observed=False)
            .size()
            .reset_index(name=f"{self.informant_column}s_count"),
            on=self.taxon_column,
        )

        # Calculate CI index (UR divided by the number of informants)
        ci_df["CI"] = ci_df["UR"] / informants_count

        # Keep only relevant columns
        ci_df = ci_df[[self.taxon_column, "CI"]]

        return ci_df

    def save_data(self):
        CI_df = self.calculate()
        CI_df.to_csv("cultural_importance_CI.csv", index=False)
        print("Saved to cultural_importance_CI.csv")

    def plot_radial(self, filename="CI.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "CI", num_row, ytick_position,
                                 colors, show_colorbar, self.informant_column, self.taxon_column, self.use_column)
        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class CV:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs. Defaults to "informant".
            taxon_column (str, optional): Name of the column containing species names. Defaults to "taxon".
            use_column (str, optional): Name of the column containing plant uses. Defaults to "ailments_treated".
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Cultural Value (CV) for Ethnospecies"

    def calculate(self):
        """
        Calculates the cultural value (CV) for each ethnospecies.

        Returns:
            pd.DataFrame: DataFrame containing taxon and CV columns.
        """

        # Calculate Use Reports (UR) per species
        ur_df = UR(self.data, self.informant_column, self.taxon_column, self.use_column).calculate()

        # Calculate Number of Uses (NU) per species
        nu_df = NU(self.data, self.informant_column, self.taxon_column, self.use_column).calculate()

        # Calculate Frequency of Citation (FC) per species
        fc_df = FC(self.data, self.informant_column, self.taxon_column, self.use_column).calculate()

        # Calculate Uce (Use Citation for Ethnospecies)
        potential_uses = self.data[self.use_column].nunique()
        nu_df["Uce"] = nu_df["NU"] / potential_uses

        # Calculate Ice (Informant Citation Index)
        ice = fc_df["FC"] / self.data[self.informant_column].nunique()
        fc_df["Ice"] = ice

        # Calculate IUce (Informant Use Index)
        iuce = ur_df["UR"] / self.data[self.informant_column].nunique()
        ur_df["IUce"] = iuce

        # Merge dataframes to calculate CV
        merged_df = pd.merge(nu_df[[self.taxon_column, "Uce"]], ur_df[[self.taxon_column, "IUce"]], on=self.taxon_column)
        merged_df = pd.merge(merged_df, fc_df[[self.taxon_column, "Ice"]], on=self.taxon_column)

        # Calculate CV = Uce * Ice * IUce
        merged_df["CV"] = merged_df["Uce"] * merged_df["Ice"] * merged_df["IUce"]

        # Sort and round CV values
        cv_df = merged_df[[self.taxon_column, "CV"]].sort_values(by="CV", ascending=False)

        return cv_df

    def save_data(self):
        CV_df = self.calculate()
        CV_df.to_csv("cultural_value_CV.csv", index=False)
        print("Saved to cultural_value_CV.csv")

    def plot_radial(self, filename="CV.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "CV", num_row, ytick_position, colors, show_colorbar, self.informant_column, self.taxon_column, self.use_column)
        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class FIC:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs.
            taxon_column (str, optional): Name of the column containing species names.
            use_column (str, optional): Name of the column containing plant uses.
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Informant Consensus Factor (FIC)"

    def calculate(self):
        """
        Calculates the FIC for each ailment category.

        Returns:
            pd.DataFrame: DataFrame containing ailment category and FIC columns.
        """

        unique_ailment_categories = self.data[self.use_column].unique()
        fic_values = []

        for ailment_category in unique_ailment_categories:
            specific_data = self.data[self.data[self.use_column] == ailment_category]

            # Calculate Nur (number of use reports)
            nur = specific_data.shape[0]

            # Calculate Nt (number of taxa used)
            nt = specific_data[self.taxon_column].nunique()

            # Calculate FIC value
            if nur > nt:
                fic = (nur - nt) / (nur - 1)
            else:
                fic = 0  # Set FIC to 0 if Nur <= Nt

            fic_values.append({self.use_column: ailment_category, "FIC": fic})

        fic_df = pd.DataFrame(fic_values)
        fic_df = fic_df.sort_values(by="FIC", ascending=False).reset_index(drop=True)
        return fic_df

    def save_data(self):
        FIC_df = self.calculate()
        FIC_df.to_csv("informant_consensus_factor_FIC.csv", index=False)
        print("Saved to informant_consensus_factor_FIC.csv")

    def plot_radial(self, filename="FIC.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "FIC", num_row, ytick_position, colors, show_colorbar, self.informant_column, self.taxon_column, self.use_column)
        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class FL:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs. Defaults to "informant".
            taxon_column (str, optional): Name of the column containing species names. Defaults to "taxon".
            use_column (str, optional): Name of the column containing plant uses. Defaults to "ailments_treated".
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Fidelity Level (FL) per Species"

    def calculate(self):
        """
        Calculates the fidelity level (FL) for each species-use combination.

        Returns:
            pd.DataFrame: DataFrame containing taxon, use, and FL columns.
        """

        # Calculate Frequency of Citation (FC) per species
        fc_df = FC(self.data, self.informant_column, self.taxon_column, self.use_column).calculate()

        # Count informants for each species-use combination
        ns_df = (
            self.data.groupby([self.taxon_column, self.use_column])[self.informant_column]
            .nunique()
            .reset_index(name="Ns")
        )

        # Merge FC and Ns dataframes
        merged_df = pd.merge(ns_df, fc_df, on=self.taxon_column)

        # Calculate FL = (Ns * 100) / FC
        merged_df["FL"] = (merged_df["Ns"] * 100) / merged_df["FC"]

        # Exclude rows with FL of 0
        merged_df = merged_df[merged_df["FL"] != 0]

        return merged_df[[self.taxon_column, self.use_column, "FL"]]

    def save_data(self, filename="fidelity_level_FL.csv"):
        """
        Saves the calculated FL data to a CSV file.

        Args:
            filename (str, optional): Name of the CSV file to save. Defaults to "fidelity_level_FL.csv".
        """

        fl_df = self.calculate()
        fl_df.to_csv(filename, index=False)
        print(f"Saved to {filename}")

    def plot_heatmap(self,
                     filename="FL.png",
                     cmap="coolwarm",
                     show_colorbar=True,
                     colorbar_shrink=0.50,
                     plot_width=10,
                     plot_height=8,
                     dpi=300,
                     fillna_zero=True):
        """
        Creates a heatmap of FL values for each species-use combination,
        with customizable features for plot appearance and layout.
        """

        data = self.calculate()
        heatmap_plot = HeatmapPlot(
            data=data,
            title="Fidelity Level (FL)",
            value_column="FL",
            row_column=self.taxon_column,
            column_column=self.use_column,
            cmap=cmap,
            show_colorbar=show_colorbar,
            colorbar_shrink=colorbar_shrink,
            plot_width=plot_width,
            plot_height=plot_height,
            dpi=dpi,
            fillna_zero=fillna_zero,
        )
        heatmap_plot.save_plot(filename, dpi=dpi)
        return heatmap_plot.plot()

class RFC:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs.
            taxon_column (str, optional): Name of the column containing species names.
            use_column (str, optional): Name of the column containing plant uses.
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Relative Frequency of Citation (RFC) per Species"

    def calculate(self):
        """
        Calculates the RFC for each species.

        Returns:
            pd.DataFrame: DataFrame containing taxon and RFC columns.
        """

        # Get frequency of citation (FC) for each species
        fc_df = FC(self.data, self.informant_column, self.taxon_column, self.use_column).calculate()

        # Get total number of informants
        total_informants = self.data[self.informant_column].nunique()

        # Calculate use reports (UR) for each species
        ur_df = (
            self.data[[self.taxon_column, self.informant_column]]
            .groupby(self.taxon_column)
            .size()
            .reset_index(name="UR")
        )

        # Merge FC, UR, and total informants
        rfc_df = pd.merge(fc_df, ur_df, on=self.taxon_column)
        rfc_df["RFC"] = rfc_df["FC"] / total_informants

        # Keep only taxon and RFC columns
        rfc_df = rfc_df[[self.taxon_column, "RFC"]]
        return rfc_df

    def save_data(self):
        RFC_df = self.calculate()
        RFC_df.to_csv("relative_frequency_of_citation_RFC.csv", index=False)
        print("Saved to relative_frequency_of_citation_RFC.csv")

    def plot_radial(self, filename="RFC.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "RFC", num_row, ytick_position, colors, show_colorbar, self.informant_column, self.taxon_column, self.use_column)
        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class RI:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs.
            taxon_column (str, optional): Name of the column containing species names.
            use_column (str, optional): Name of the column containing plant uses.
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Relative Importance (RI) Index per Species"

    def calculate(self):
        """
        Calculates the RI for each species.

        Returns:
            pd.DataFrame: DataFrame containing taxon and RI columns.
        """

        # Get RFC and NU for each species
        rfc_df = RFC(
            self.data, self.informant_column, self.taxon_column, self.use_column
        ).calculate()
        nu_df = NU(
            self.data, self.informant_column, self.taxon_column, self.use_column
        ).calculate()

        # Normalize RFC and NU
        max_rfc = rfc_df["RFC"].max()
        max_nu = nu_df["NU"].max()
        rfc_df["RFC(max)"] = rfc_df["RFC"] / max_rfc
        nu_df["RNU(max)"] = nu_df["NU"] / max_nu

        # Merge RFC(max) and RNU(max)
        ri_df = pd.merge(
            rfc_df[[self.taxon_column, "RFC(max)"]],
            nu_df[[self.taxon_column, "RNU(max)"]],
            on=self.taxon_column,
        )

        # Calculate RI index
        ri_df["RI"] = (ri_df["RFC(max)"] + ri_df["RNU(max)"]) / 2

        # Sort and return RI values
        ri_df = ri_df.sort_values(by="RI", ascending=False).reset_index(drop=True)
        return ri_df[[self.taxon_column, "RI"]]

    def save_data(self):
        RI_df = self.calculate()
        RI_df.to_csv("relative_importance_RI.csv", index=False)
        print("Saved to relative_importance_RI.csv")

    def plot_radial(self, filename="RI.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "RI", num_row, ytick_position, colors, show_colorbar,
                                 self.informant_column, self.taxon_column, self.use_column)
        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()

class UV:

    def __init__(self, data, informant_column="informant", taxon_column="taxon", use_column="ailments_treated"):
        """
        Initializes the class with necessary data and column names.

        Args:
            data (pd.DataFrame): DataFrame containing plant usage information.
            informant_column (str, optional): Name of the column containing informant IDs.
            taxon_column (str, optional): Name of the column containing species names.
            use_column (str, optional): Name of the column containing plant uses.
        """

        self.data = data
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.title = "Use Value (UV) per Species"

    def calculate(self):
        """
        Calculates the UV for each species.

        Returns:
            pd.DataFrame: DataFrame containing taxon and UV columns.
        """

        # Get UR for each species grouped by informants
        ur_by_informant = (
            self.data.groupby([self.informant_column, self.taxon_column], observed=True)
            .size()
            .to_frame(name="UR")
            .reset_index()
        )

        # Calculate UV (number of informants mentioning each use)
        uv_df = (
            ur_by_informant.groupby(self.taxon_column, observed=True)
            .size()
            .reset_index(name="UV")
            .sort_values(by="UV", ascending=False)
            .reset_index(drop=True)
        )
        return uv_df

    def save_data(self):
        UV_df = self.calculate()
        UV_df.to_csv("use_value_UV.csv", index=False)
        print("Saved to use_value_UV.csv")

    def plot_radial(self, filename="UV.png", dpi=300, num_row=10, ytick_position="onbar", colors=None, show_colorbar=True):
        # Plot radial bar chart
        radial_plot = RadialPlot(self.calculate(), self.title, "UV", num_row, ytick_position, colors, show_colorbar, self.informant_column, self.taxon_column, self.use_column)
        radial_plot.save_plot(filename, dpi=dpi)
        radial_plot.plot()
