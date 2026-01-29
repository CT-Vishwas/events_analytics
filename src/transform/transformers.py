import pandas as pd

def calculate_registration_lead_time(registrations_df: pd.DataFrame, events_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a 'lead_time_days' column to registrations, representing days between registration and event start.
    """
    df = registrations_df.copy()
    events = events_df[['event_id', 'scheduled_date_time']].copy()
    events['scheduled_date_time'] = pd.to_datetime(events['scheduled_date_time'])
    df['reg_timestamp'] = pd.to_datetime(df['reg_timestamp'])
    df = df.merge(events, on='event_id', how='left')
    df['lead_time_days'] = (df['scheduled_date_time'] - df['reg_timestamp']).dt.days
    return df

def calculate_total_revenue(events_df: pd.DataFrame, pricing_df: pd.DataFrame, registrations_df: pd.DataFrame) -> float:
    """
    Adds a 'price_per_hour' column to events, calculated as price divided by duration.
    """
    df = events_df.copy()
    pricing = pricing_df.copy()
    df = df.merge(pricing, on='event_id', how='left')
    df["effective_price"] = df["base_price"] * (1 - (df["discount_pct"]/100))

    # Calculate total revenue
    df = df.merge(registrations_df[['event_id', 'registration_id']], on='event_id', how='left')
    total_revenue = df['effective_price'].sum()
    return total_revenue