import matplotlib.pyplot as plt
import io

def generate_trend_plot(actual: list[float], predicted: list[float]) -> bytes:
    plt.figure(figsize=(10, 5))
    plt.plot(actual, label='Actual')
    plt.plot(predicted, label='Predicted', linestyle='--')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf.read()