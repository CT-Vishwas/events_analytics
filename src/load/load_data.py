
import pandas as pd
from pathlib import Path
from src.extract.csv_extracter import extract as extract_csv
from src.extract.json_extracter import extract as extract_json
from src.transform import transformers
from src.utils.database import DatabaseConnection
from src.models.schemas import AttendeeSchema
import logging

DATA_DIR = Path(__file__).parents[2] / 'data'

def load_attendees():
    attendees_path = DATA_DIR / 'attendees.json'
    # Extract
    attendees_records = extract_json(attendees_path)
    # Validate
    attendees_valid = [AttendeeSchema(**item).dict() for item in attendees_records]
    attendees_df = pd.DataFrame(attendees_valid)
    return attendees_df

def load_events():
    events_path = DATA_DIR / 'events.csv'
    events_records = extract_csv(events_path)
    events_df = pd.DataFrame(events_records)
    return events_df

def load_registrations():
    registrations_path = DATA_DIR / 'registrations.csv'
    registrations_records = extract_csv(registrations_path)
    registrations_df = pd.DataFrame(registrations_records)
    return registrations_df

def load_pricing():
    pricing_path = DATA_DIR / 'pricing.csv'
    pricing_records = extract_csv(pricing_path)
    pricing_df = pd.DataFrame(pricing_records)
    return pricing_df

def load_channels():
    channels_path = DATA_DIR / 'channels.csv'
    channels_records = extract_csv(channels_path)
    channels_df = pd.DataFrame(channels_records)
    return channels_df

def load_logs():
    logs_path = DATA_DIR / 'logs.csv'
    logs_records = extract_csv(logs_path)
    logs_df = pd.DataFrame(logs_records)
    return logs_df

def transform_data():
    # Example: add event duration, encode event type, etc.
    events_df = load_events()
    events_df = transformers.add_event_duration(events_df)
    # Add more transformations as needed
    return events_df

def load_to_db(df: pd.DataFrame, table_name: str):
    db = DatabaseConnection().get_connection()
    df.to_sql(table_name, db, if_exists='replace', index=False)
    logging.info(f"Loaded {len(df)} records into table '{table_name}'")

def main():
    # Extract & Validate
    attendees_df = load_attendees()
    events_df = load_events()
    registrations_df = load_registrations()
    pricing_df = load_pricing()
    channels_df = load_channels()
    logs_df = load_logs()

    # Transform (example: add event duration)
    events_df = transformers.add_event_duration(events_df)

    # Load to DB
    load_to_db(attendees_df, 'attendees')
    load_to_db(events_df, 'events')
    load_to_db(registrations_df, 'registrations')
    load_to_db(pricing_df, 'pricing')
    load_to_db(channels_df, 'channels')
    load_to_db(logs_df, 'logs')

if __name__ == '__main__':
    main()