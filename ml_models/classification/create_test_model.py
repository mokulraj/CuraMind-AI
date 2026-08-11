from pathlib import Path

import skops.io as sio
from sklearn.linear_model import LogisticRegression


MODEL_PATH = Path(
    "ml_models/classification/"
    "curamind_classifier.skops"
)


def main():
    model = LogisticRegression(
        max_iter=1000,
        random_state=42,
    )

    features = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0],
    ]

    labels = [
        0,
        0,
        1,
        1,
    ]

    model.fit(
        features,
        labels,
    )

    sio.dump(
        model,
        str(
            MODEL_PATH
        ),
    )

    print(
        f"Model created: {MODEL_PATH}"
    )


if __name__ == "__main__":
    main()