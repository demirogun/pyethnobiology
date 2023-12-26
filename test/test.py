import unittest
import pandas as pd

from pyethnobiology import pyethnobiology  # Import the class to be tested


class TestPyEthnobiology(unittest.TestCase):
    """Tests for the pyethnobiology class."""

    def test_init_with_valid_dataframe(self):
        sample_data = pd.read_csv("data/example3_ethnobotanydata.csv")

        ethno = pyethnobiology(data=sample_data, taxon_column="sp_name")

        self.assertEqual(ethno.data.equals(sample_data), True)
        self.assertEqual(ethno.informant_column, "informant")
        self.assertEqual(ethno.taxon_column, "sp_name")
        self.assertEqual(ethno.use_column, "ailments_treated")

    def test_init_with_invalid_dataframe_data_type(self):
        with self.assertRaises((ValueError, AttributeError)):
            pyethnobiology(data="no-dataframe")  # Non-dataframe input

    # Test cases for load_data()
    def test_load_data_with_valid_dataframe(self):
        sample_data = pd.read_csv("data/example3_ethnobotanydata.csv")

        loaded_data = pyethnobiology(sample_data, taxon_column="sp_name")  # Initialize without data

        self.assertEqual(sample_data.equals(sample_data), True)
        self.assertEqual(loaded_data.data.equals(sample_data), True)  # Check if data is assigned to the object

    def test_load_data_with_valid_rda_file(self):
        # Assuming you have a valid RDA file named "test_data.rda"
        rda_file_path = "data/ethnobotanydata.rda"
        ethno = pyethnobiology(data=rda_file_path, taxon_column="sp_name", convert_use_data=True)

    def test_load_data_with_invalid_file_type(self):
        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data="invalid_file.txt")

    def test_load_data_missing_required_columns(self):
        incomplete_data = pd.DataFrame({
            "informant": ["A", "B"],
            "ailments_treated": ["Headache", "Fever"]
        })

        with self.assertRaises(ValueError) as context:
            ethno = pyethnobiology(data=incomplete_data)

        self.assertTrue("Missing required columns" in str(context.exception))

    def test_CI(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough"]
        })

        expected_ci_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "CI": [0.666667, 0.333333, 0.333333]
        })

        ethno = pyethnobiology(data=sample_data)
        ci_results = ethno.CI().calculate()

        pd.testing.assert_frame_equal(ci_results, expected_ci_results)

    def test_CI_with_invalid_data(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.CI().calculate()

    def test_FC(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough"]
        })

        expected_fc_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "FC": [2, 1, 1]
        })

        ethno = pyethnobiology(data=sample_data)
        fc_results = ethno.FC().calculate()

        pd.testing.assert_frame_equal(fc_results, expected_fc_results)

    def test_FC_with_invalid_data(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.FC().calculate()

    def test_NU(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough"]
        })

        expected_nu_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "NU": [1, 1, 1]
        })

        ethno = pyethnobiology(data=sample_data)
        nu_results = ethno.NU().calculate()

        pd.testing.assert_frame_equal(nu_results, expected_nu_results)

    def test_NU_with_invalid_data(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.NU().calculate()

    def test_UR(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough"]
        })

        expected_ur_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "UR": [2, 1, 1]
        })

        ethno = pyethnobiology(data=sample_data)
        ur_results = ethno.UR().calculate()

        pd.testing.assert_frame_equal(ur_results, expected_ur_results)

    def test_UR_with_invalid_data(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A"],
            "taxon": ["Species1", "Species2", "Species1", "Species3"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.UR().calculate()

    def test_RFC(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        expected_rfc_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "RFC": [1.0, 0.6666666666666666, 0.3333333333333333]
        })

        ethno = pyethnobiology(data=sample_data)
        rfc_results = ethno.RFC().calculate()

        pd.testing.assert_frame_equal(rfc_results, expected_rfc_results)

    def test_RFC_with_invalid_data(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.RFC().calculate()

    def test_RI(self):
        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        expected_ri_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "RI": [1.0, 0.8333333333333333, 0.6666666666666666]
        })

        ethno = pyethnobiology(data=sample_data)
        ri_results = ethno.RI().calculate()

        pd.testing.assert_frame_equal(ri_results, expected_ri_results)

    def test_RI_with_invalid_data(self):

        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.RI().calculate()

    def test_UV(self):

        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        expected_uv_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "UV": [1.0, 0.6666666666666666, 0.3333333333333333]
        })

        ethno = pyethnobiology(data=sample_data)
        uv_results = ethno.UV().calculate()

        pd.testing.assert_frame_equal(uv_results, expected_uv_results)

    def test_UV_with_invalid_data(self):

        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.UV().calculate()

    def test_all_taxon_indices(self):

        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "ailments_treated": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        expected_all_taxon_indices_results = pd.DataFrame({
            "taxon": ["Species1", "Species2", "Species3"],
            "CI": [1.0, 0.6666666666666666, 0.3333333333333333],
            "FC": [3, 2, 1],
            "NU": [1, 1, 1],
            "UR": [3, 2, 1],
            "RFC": [1.0, 0.6666666666666666, 0.3333333333333333],
            "RI": [1.000000, 0.833333, 0.666667],
            "UV": [1.0, 0.6666666666666666, 0.3333333333333333],
            "CV": [0.333333, 0.148148, 0.037037]
        })

        ethno = pyethnobiology(data=sample_data)
        all_taxon_indices_results = ethno.all_taxon_indices()

        pd.testing.assert_frame_equal(all_taxon_indices_results, expected_all_taxon_indices_results)

    def test_all_taxon_indices_with_invalid_data(self):

        sample_data = pd.DataFrame({
            "informant": ["A", "B", "C", "A", "B", "C"],
            "taxon": ["Species1", "Species2", "Species1", "Species3", "Species1", "Species2"],
            "invalid_column": ["Headache", "Fever", "Headache", "Cough", "Headache", "Fever"]
        })

        with self.assertRaises(ValueError):
            ethno = pyethnobiology(data=sample_data)
            ethno.all_taxon_indices()

if __name__ == "__main__":
    unittest.main()