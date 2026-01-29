import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from transform.transformers import calculate_total_revenue
from load.load_data import read_from_db

st.set_page_config(page_title="Events Dashboard (ETL)", layout="wide")

DB_PATH = Path(__file__).resolve().parents[1] / "dbs" / "events_management.db"
CSV_FALLBACK = Path(__file__).resolve().parents[1] / "data" / "events.csv"

# @st.cache_data
# def load_events():
# 	# Run ETL pipeline to ensure DB is up-to-date
# 	try:
# 		run_etl_pipeline()
# 	except Exception as e:
# 		st.warning(f"ETL pipeline failed: {e}")
# 	# Try sqlite DB first, then fallback to CSV
# 	try:
# 		engine = create_engine(f"sqlite:///{DB_PATH}")
# 		with engine.begin() as conn:
# 			df = pd.read_sql_table("events", conn)
# 		return df
# 	except Exception:
# 		if CSV_FALLBACK.exists():
# 			return pd.read_csv(CSV_FALLBACK)
# 		raise

# def compute_fill_rate(df):
# 	# registrations per event divided by venue_capacity
# 	event_capacity = df.groupby('event_id')['venue_capacity'].first()
# 	regs = df.groupby('event_id').size()
# 	fill = (regs / event_capacity).fillna(0) * 100
# 	return fill

@st.cache_data
def load_events():
	events_df = read_from_db('events')
	return events_df


def main():
	st.title("📊 Events Dashboard (ETL)")
	st.markdown("Interactive dashboard using ETL pipeline and database.")

	df = load_events()
	# ensure datetimes
	if 'scheduled_date_time' in df.columns:
		df['scheduled_date_time'] = pd.to_datetime(df['scheduled_date_time'], errors='coerce')
	if 'reg_timestamp' in df.columns:
		df['reg_timestamp'] = pd.to_datetime(df['reg_timestamp'], errors='coerce')

	st.sidebar.header("Filters")
	# topic filter
	topics = ['All'] + sorted(df['topic'].dropna().unique().tolist())
	sel_topic = st.sidebar.selectbox('Topic', topics)

	# city filter
	city_col = 'city' if 'city' in df.columns else None
	if city_col:
		cities = ['All'] + sorted(df[city_col].dropna().unique().tolist())
		sel_city = st.sidebar.selectbox('City', cities)
	else:
		sel_city = 'All'
	
	# event filter
	# event_ids = ['All'] + sorted(df['event_id'].dropna().unique().tolist())
	# sel_event = st.sidebar.selectbox('Event', event_ids)
	
	# date range filter
	if 'scheduled_date_time' in df.columns:
		min_date = df['scheduled_date_time'].min().date()
		max_date = df['scheduled_date_time'].max().date()
		sel_dates = st.sidebar.date_input('Scheduled date range', value=(min_date, max_date))
	else:
		sel_dates = None

	# apply filters
	df_f = df.copy()
	if sel_topic != 'All':
		df_f = df_f[df_f['topic'] == sel_topic]
	if city_col and sel_city != 'All':
		df_f = df_f[df_f[city_col] == sel_city]
	# if sel_event != 'All':
	# 	df_f = df_f[df_f['event_id'] == sel_event]
	if sel_dates and 'scheduled_date_time' in df.columns:
		start, end = pd.to_datetime(sel_dates[0]), pd.to_datetime(sel_dates[1])
		df_f = df_f[(df_f['scheduled_date_time'] >= start) & (df_f['scheduled_date_time'] <= end)]

	# KPIs
	total_regs = len(df_f)
	total_events = df_f['event_id'].nunique()
	if 'payment_status' in df_f.columns and 'amount_paid' in df_f.columns and not df_f.empty:
		total_revenue = calculate_total_revenue()
	else:
		total_revenue = 0.0
	# avg_fill = compute_fill_rate(df_f).mean()

	k1, k2, k3 = st.columns(3)
	k1.metric("Total registrations", f"{total_regs}")
	k2.metric("Total events", f"{total_events}")
	k3.metric("Total Revenue", f"${total_revenue:.2f}")

	st.markdown("---")

	# Registrations over time
	st.subheader('Registrations over time')
	if 'reg_timestamp' in df_f.columns:
		ts = df_f.copy()
		ts['reg_date'] = ts['reg_timestamp'].dt.date
		daily = ts.groupby('reg_date').size().rename('registrations')
		st.line_chart(daily)
	else:
		st.info('No registration timestamps found to build a time series.')

	# Top topics
	st.subheader('Top topics / events')
	top_topics = df_f['topic'].value_counts().head(10)
	st.bar_chart(top_topics)

	# Registration lead days histogram
	st.subheader('Registration lead days')
	if 'registration_lead_days' in df_f.columns:
		fig, ax = plt.subplots(figsize=(8,3))
		sns.histplot(df_f['registration_lead_days'].dropna(), bins=30, ax=ax, color='#1F77B4')
		ax.set_xlabel('Registration lead days')
		st.pyplot(fig)
	else:
		st.info('No registration lead days column present.')

	# Fill rate distribution
	st.subheader('Event fill rate distribution')
	# fill = compute_fill_rate(df_f)
	# fig2, ax2 = plt.subplots(figsize=(8,3))
	# sns.histplot(fill, bins=25, ax=ax2, color='#2CA02C')
	# ax2.set_xlabel('Fill rate (%)')
	# st.pyplot(fig2)

	# Show raw data
	with st.expander('Show data (sample)'):
		st.dataframe(df_f.sample(min(len(df_f), 200)).reset_index(drop=True))

	st.markdown('---')
	st.write('Built from `events` table in `dbs/events_management.db` (via ETL pipeline)')

if __name__ == '__main__':
	main()
