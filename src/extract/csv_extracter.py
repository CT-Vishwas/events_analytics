from pandas import DataFrame, read_csv
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_DIR.parents[2]

def extract(filepath: Path) -> DataFrame:
    """
    Extracts data from a CSV file.

    :param filepath: Path to the CSV file.
    :type filepath: Path
    :return: DataFrame containing the extracted data.
    :rtype: DataFrame
    """

    try:
        if not filepath.exists():
            raise FileNotFoundError(f"The file {filepath} does not exist.")
        
        df = read_csv(filepath)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return DataFrame()

if __name__ == "__main__":
    events_file = PROJECT_ROOT/ "data"/"events.csv"
    df = extract(events_file)
    print(df.head())