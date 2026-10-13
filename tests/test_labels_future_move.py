"""Tests for future mid move label."""

import pandas as pd

from research.labels.future_mid_move import build_future_mid_move_label


def test_build_future_mid_move_label() -> None:
    df = pd.DataFrame({
        "mid_px": [100.0, 100.1, 100.05, 100.3, 100.15, 100.1] + [100.0] * 4,
    })
    label = build_future_mid_move_label(df, horizon_rows=2, bucket_threshold=0.001)
    # Row 0: future mid=100.05, ret=0.05/100=0.0005 < 0.001 -> 0
    # Row 1: future mid=100.3, ret=0.2/100.1~0.002 > 0.001 -> 1
    # Row 3: future mid=100.1, ret=-0.2/100.3~-0.002 < -0.001 -> -1
    assert label.iloc[0] == 0
    assert label.iloc[1] == 1
    assert label.iloc[3] == -1
    assert label.iloc[-1] == 0  # last rows have NaN future

