from pandas import DataFrame, read_json
from pathlib import Path
from src.utils.logger import get_logger

CURRENT_DIR = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_DIR.parents[2]

logger = get_logger(__name__)

def extract(filepath: Path) -> dict:
    """
    Extracts data from a JSON file.

    :param filepath: Path to the JSON file.
    :type filepath: Path
    :return: DataFrame containing the extracted data.
    :rtype: DataFrame
    """

    try:
        if not filepath.exists():
            logger.error(f"The file {filepath} does not exist.")
            raise FileNotFoundError(f"The file {filepath} does not exist.")

        df = read_json(filepath)
        logger.info(f"Successfully extracted data from {filepath}")
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return DataFrame()

if __name__ == "__main__":
    attendees = PROJECT_ROOT/ "data"/"attendees.json"
    df = extract(attendees)
    print(df.head())