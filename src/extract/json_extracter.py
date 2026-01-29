from pandas import DataFrame, read_json
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_DIR.parents[2]

def extract(filepath: Path) -> DataFrame:
    """
    Extracts data from a JSON file.

    :param filepath: Path to the JSON file.
    :type filepath: Path
    :return: DataFrame containing the extracted data.
    :rtype: DataFrame
    """

    try:
        if not filepath.exists():
            raise FileNotFoundError(f"The file {filepath} does not exist.")

        df = read_json(filepath)
        return df
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return DataFrame()

if __name__ == "__main__":
    attendees = PROJECT_ROOT/ "data"/"attendees.json"
    df = extract(attendees)
    print(df.head())