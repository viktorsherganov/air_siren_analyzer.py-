import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_mock_data():
    data = {
        'region': ['Київ', 'Харків', 'Київ', 'Одеса', 'Харків', 'Київ'],
        'start_time': [
            '2026-06-20 02:15:00', '2026-06-20 03:00:00', '2026-06-20 14:20:00',
            '2026-06-21 08:05:00', '2026-06-21 23:30:00', '2026-06-21 11:10:00'
        ],
        'end_time': [
            '2026-06-20 03:45:00', '2026-06-20 05:10:00', '2026-06-20 15:00:00',
            '2026-06-21 09:15:00', '2026-06-22 01:15:00', '2026-06-21 13:40:00'
        ]
    }
    df = pd.DataFrame(data)
    df.to_csv('air_alerts_data.csv', index=False)

def load_and_clean_data(filepath):
    if not os.path.exists(filepath):
        generate_mock_data()
    df = pd.read_csv(filepath)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df = df[df['end_time'] > df['start_time']]
    return df

def analyze_time_series(df):
    df['duration_minutes'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60.0
    df['start_hour'] = df['start_time'].dt.hour
    avg_duration = df['duration_minutes'].mean()
    total_alerts = len(df)
    print(f"Загальна кількість тривог: {total_alerts}")
    print(f"Середня тривалість: {avg_duration:.2f} хв")
    return df

def generate_analytics_chart(df):
    plt.figure(figsize=(10, 5))
    hourly_counts = df['start_hour'].value_counts().sort_index()
    hourly_counts.plot(kind='bar', color='crimson', edgecolor='black')
    plt.title('Розподіл частоти повітряних тривог за годинами доби')
    plt.tight_layout()
    plt.savefig('siren_hourly_distribution.png')

if __name__ == "__main__":
    DATA_FILE = 'air_alerts_data.csv'
    alerts_df = load_and_clean_data(DATA_FILE)
    analyzed_df = analyze_time_series(alerts_df)
    generate_analytics_chart(analyzed_df)
