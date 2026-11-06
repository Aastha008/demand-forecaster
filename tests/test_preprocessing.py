from src.preprocessing import engineer_features

def test_feature_engineering():
    df = engineer_features([10, 20], [0, 1])
    assert 'rolling_avg_7' in df.columns
    assert len(df) == 2