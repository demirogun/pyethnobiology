import pandas as pd
from sklearn.metrics import jaccard_score


class Jaccard:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def convert_data(self, literature_column: str, taxon_column: str, use_column: str) -> pd.DataFrame:
        """Converts data to a specified format, handling varying ailment names and extracting literature references.

        Args:
            data (pd.DataFrame): The input DataFrame containing the data to be converted.
            literature_column (str): The name of the column containing literature references.
            taxon_column (str): The name of the column containing taxon names.
            use_column (str): The name of the column containing ailment names.

        Returns:
            pd.DataFrame: The converted DataFrame with the following columns:
                - "study": Study identifier (either "My Study" or literature references)
                - taxon_column (str): Taxon name
                - Ailment columns (one for each unique ailment): 0 or 1 indicating presence/absence
        """

        # Ensure literature column is string type
        if not pd.api.types.is_string_dtype(self.data[literature_column]):
            self.data[literature_column] = self.data[literature_column].astype(str)

        # Create an empty DataFrame with the desired columns
        converted_data = pd.DataFrame(columns=["study", taxon_column])
        unique_ailments = set(self.data[use_column])
        for ailment in unique_ailments:
            converted_data[ailment] = 0  # Add columns for all unique ailments

        # Iterate through each row efficiently using itertuples
        for row in self.data.itertuples():
            taxon = getattr(row, taxon_column)
            use = getattr(row, use_column)

            # Extract literature references (handling potential errors)
            try:
                literature_references = getattr(row, literature_column).split(";")
            except (AttributeError, ValueError):
                literature_references = []

            # Create rows for "My Study" and literature references
            rows_to_add = [
                {"study": "My Study", taxon_column: taxon, use: 1}  # Row for "My Study"
            ]
            rows_to_add.extend(
                {
                    "study": ref,
                    taxon_column: taxon,
                    use: 1,  # Set the relevant ailment column to 1
                }
                for ref in literature_references
            )

            # Concatenate new rows efficiently using list comprehension
            converted_data = pd.concat(
                [
                    converted_data,
                    pd.DataFrame(rows_to_add),  # Create a DataFrame from the list of rows
                ],
                ignore_index=True,
            )

        # Fill missing values with 0 and group data
        converted_data = converted_data.fillna(0).groupby(["study", taxon_column]).sum().clip(upper=1)

        return converted_data

    def fill_missing_taxa_dynamic(self) -> pd.DataFrame:

        """Fills missing taxa in a DataFrame with appropriate ailment values based on other studies.

        Args:
            data (pd.DataFrame): The input DataFrame containing the data to be processed.

        Returns:
            pd.DataFrame: The DataFrame with missing taxa filled in.
        """

        study_data = {}
        ailment_names = list(self.data.columns[:-2])  # Get ailment names from DataFrame columns

        for index, row in self.data.iterrows():
            study_name = row['study']
            taxon = row['taxon']
            ailments = row[:-2].tolist()  # Extract ailments as a list

            if study_name not in study_data:
                study_data[study_name] = {}

            study_data[study_name][taxon] = ailments

        for study in study_data:
            taxa_in_my_study = study_data["My Study"].keys()
            for taxon in taxa_in_my_study:
                if taxon not in study_data[study]:
                    study_data[study][taxon] = [0] * len(ailment_names)

        # Create a list to hold the transformed data
        transformed_data = []
        for study, study_values in study_data.items():
            for taxon, ailments in study_values.items():
                row_data = [study, taxon] + ailments
                transformed_data.append(row_data)

        # Create a DataFrame from the transformed data
        columns = ['study', 'taxon'] + ailment_names
        result_df = pd.DataFrame(transformed_data, columns=columns)

        return result_df

    def calculate_jaccard_similarity(self, study_column: str, taxon_column: str, ailment_columns: list[str],
                                     my_study: str) -> dict[tuple[str, str], float]:

        """Calculates pairwise Jaccard similarity between 'My Study' and other studies based on ailments.

        Args:
            data (pd.DataFrame): The input DataFrame containing the dataset.
            study_column (str): Column name for the study identifier.
            taxon_column (str): Column name for the taxon information.
            ailment_columns (List[str]): List of ailment column names.
            my_study (str): Identifier for 'My Study'.

        Returns:
            Dict[Tuple[str, str], float]: Dictionary containing Jaccard similarities between 'My Study' and other studies.
        """
        # Get unique studies
        studies = self.data[study_column].unique()

        # Create a dictionary to store Jaccard similarity between 'My Study' and other studies
        jaccard_similarities = []

        # Calculate Jaccard similarity for 'My Study' against other studies
        for other_study in studies:
            if other_study != my_study:
                subset1 = self.data[self.data[study_column] == my_study][ailment_columns]
                subset2 = self.data[self.data[study_column] == other_study][ailment_columns]

                # Flatten ailment columns for Jaccard similarity calculation
                subset1_flattened = subset1.values.flatten()
                subset2_flattened = subset2.values.flatten()

                # Calculate Jaccard similarity for ailment columns using sklearn's jaccard_score
                jaccard_sim = jaccard_score(subset1_flattened, subset2_flattened)

                jaccard_similarities.append({"study": other_study, "similarity": jaccard_sim})

        return pd.DataFrame(jaccard_similarities)

    def run_analysis(self, literature_column: str, taxon_column: str, use_column: str, my_study: str = "My Study"):
        self.data = self.convert_data(literature_column, taxon_column, use_column)
        self.data['study'] = self.data.index.get_level_values("study")
        self.data['taxon'] = self.data.index.get_level_values(taxon_column)
        self.data = self.fill_missing_taxa_dynamic()
        ailment_columns = self.data.columns[2:]
        return self.calculate_jaccard_similarity(study_column="study", taxon_column="taxon",
                                                 ailment_columns=ailment_columns, my_study=my_study)
