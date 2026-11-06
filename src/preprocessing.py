import pandas as pd
import numpy as np

def engineer_features(sales: list[float], promos: list[int]) -> pd.DataFrame:
    df = pd.DataFrame({'sales': sales, 'promo': promos})
    df['day_of_week'] = np.arange(len(df)) % 7
    df['rolling_avg_7'] = df['sales'].rolling(window=7, min_periods=1).mean()
    df['lag_1'] = df['sales'].shift(1).fillna(0)
    return df.fillna(0)