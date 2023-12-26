import pandas as pd

import rdata

from .indices import UR, CI, FC, NU, RFC, RI, UV, CV, FL, FIC
from .stats import Jaccard

from .visualization import ChordPlot


class pyethnobiology:
    """
    Encapsulates ethnobotanical data and analysis.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        informant_column: str = "informant",
        taxon_column: str = "taxon",
        use_column: str = "ailments_treated",
        literature_column: str = "literature",
        convert_use_data: bool = False,
    ) -> None:
        """
        Initializes the Ethnobotany class.

        Args:
            data: DataFrame containing ethnobotanical information.
            informant_column: Name of the column containing informant IDs.
            taxon_column: Name of the column containing species names.
            use_column: Name of the column containing plant uses.
            convert_use_data: Whether to convert use data format (optional).
        """

        self.data = self.load_data(data, informant_column, taxon_column, use_column, convert_use_data)
        self.informant_column = informant_column
        self.taxon_column = taxon_column
        self.use_column = use_column
        self.literature_column = literature_column

    def CI(self):
        CI_class = CI(self.data, self.informant_column, self.taxon_column, self.use_column)
        return CI_class

    def FC(self):
        FC_class = FC(self.data, self.informant_column, self.taxon_column, self.use_column)
        return FC_class

    def NU(self):
        NU_class = NU(self.data, self.informant_column, self.taxon_column, self.use_column)
        return NU_class

    def UR(self):
        UR_class = UR(self.data, self.informant_column, self.taxon_column, self.use_column)
        return UR_class

    def RFC(self):
        RFC_class = RFC(self.data, self.informant_column, self.taxon_column, self.use_column)
        return RFC_class

    def RI(self):
        RI_class = RI(self.data, self.informant_column, self.taxon_column, self.use_column)
        return RI_class

    def UV(self):
        UV_class = UV(self.data, self.informant_column, self.taxon_column, self.use_column)
        return UV_class

    def CV(self):
        CV_class = CV(self.data, self.informant_column, self.taxon_column, self.use_column)
        return CV_class

    def FL(self):
        FL_class = FL(self.data, self.informant_column, self.taxon_column, self.use_column)
        return FL_class

    def FIC(self):
        FIC_class = FIC(self.data, self.informant_column, self.taxon_column, self.use_column)
        return FIC_class

    def all_taxon_indices(self, sort_values_by=None, ascending=True):
        methods_to_calculate = [self.CI, self.FC, self.NU, self.UR, self.RFC, self.RI, self.UV, self.CV]
        dfs_to_merge = []
        
        for method in methods_to_calculate:
            df = method().calculate()
            dfs_to_merge.append(df)
        
        merged_df = dfs_to_merge[0]
        for df in dfs_to_merge[1:]:
            merged_df = merged_df.merge(df, on=self.taxon_column, how='outer')
        
        if sort_values_by:
            return merged_df.sort_values(by=sort_values_by, ascending=ascending)
        else:
            return merged_df
  
    def plot_chord(self, filename="chord_plot.png", dpi=300, by="taxon", colors=None, min_info_count=0, get_first=None):
        chord_plot = ChordPlot(self.data, by, self.informant_column, self.taxon_column, self.use_column, colors, min_info_count, get_first)
        chord_plot.save_plot(filename=filename, dpi=dpi)
        chord_plot.plot()
        
    def jaccard(self, ):
        jaccard_analyzer = Jaccard(data=self.data)
        return jaccard_analyzer.run_analysis(literature_column=self.literature_column, taxon_column=self.taxon_column, use_column=self.use_column)
    
    def load_data(
        self,
        data: pd.DataFrame | str,
        informant_column: str,
        taxon_column: str,
        use_column: str,
        convert_use_data: bool,
    ) -> pd.DataFrame:
        """
        Loads ethnobotanical data from various sources.

        Args:
            data: DataFrame or path to RDA file.
            informant_column: Name of the column containing informant IDs.
            taxon_column: Name of the column containing species names.
            use_column: Name of the column containing plant uses.
            convert_use_data: Whether to convert use data format (optional).

        Returns:
            DataFrame containing ethnobotanical data.
        """
                
        if not isinstance(data, pd.DataFrame):
            if len(data.split(".rda")) > 1:
                parsed = rdata.parser.parse_file(data)
                converted = rdata.conversion.convert(parsed)
                data = converted[list(converted.keys())[0]]
            else:
                raise ValueError("Input data is not a valid DataFrame.")

        # Check if required columns are present
        if convert_use_data:
            required_columns = [informant_column, taxon_column]
        else:
            required_columns = [informant_column, taxon_column, use_column]
            
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
        if convert_use_data:
            melted_df = pd.melt(data, id_vars=[informant_column, taxon_column], var_name=use_column, value_name='value')
            converted = melted_df[melted_df['value'] == 1][[informant_column, taxon_column, use_column]].sort_values([informant_column, taxon_column])
            data = converted
        
        self.data = data
        
        return data