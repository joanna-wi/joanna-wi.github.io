import pandas as pd
import numpy as np

INPUT_FILE = "path"
OUTPUT_FILE = "path"

GROUP_COLS = ["Subject", "Condition", "#refs#_A"]
STIMULUS_LABEL = "Stimulus"

# Set range to physiologically plausible RR intervals (ms). Corresponds to ~30-200 bpm.
RR_MIN_MS = 300
RR_MAX_MS = 2000


def calculate_rmssd(rr_intervals_ms: pd.Series) -> float:
    """
    Calculate RMSSD (ms). Any NaN (artifact-flagged) values are treated as
    gaps: the differences immediately before and after a gap are excluded
    entirely.
    """
    rr = rr_intervals_ms.to_numpy()
    if len(rr) < 2:
        return np.nan
    successive_diffs = np.diff(rr)          # NaN wherever either side is NaN
    successive_diffs = successive_diffs[~np.isnan(successive_diffs)]
    if len(successive_diffs) == 0:
        return np.nan
    rmssd = np.sqrt(np.mean(successive_diffs ** 2))
    return rmssd


def main():
    df = pd.read_csv(INPUT_FILE)

    # Flag RR intervals outside the physiologically plausible range as artifacts.
    # These are set to NaN (excluded) rather than dropped as rows.
    is_artifact = (df["RR_interval_ms"] < RR_MIN_MS) | (df["RR_interval_ms"] > RR_MAX_MS)
    n_artifacts = is_artifact.sum()
    df.loc[is_artifact, "RR_interval_ms"] = np.nan

    # Sort so successive differences are computed in the correct temporal order
    # within each Subject/Condition/Stimulus group (Sample reflects recording order).
    df = df.sort_values(GROUP_COLS + ["Sample"])

    results = (
        df.groupby(GROUP_COLS)["RR_interval_ms"]
        .apply(calculate_rmssd)
        .reset_index(name="RMSSD_ms")
    )

    # Report how many valid (non-missing) RR intervals fed into each RMSSD.
    counts = (
        df.groupby(GROUP_COLS)["RR_interval_ms"]
        .apply(lambda s: s.dropna().shape[0])
        .reset_index(name="N_valid_RR_intervals")
    )

    results = results.merge(counts, on=GROUP_COLS)
    results = results.rename(columns={"#refs#_A": STIMULUS_LABEL})

    results.to_csv(OUTPUT_FILE, index=False)

    print(f"Excluded {n_artifacts} RR intervals outside {RR_MIN_MS}-{RR_MAX_MS} ms "
          f"as artifacts (out of {len(df)} total rows).\n")

    print(results.to_string(index=False))
    print(f"\nSaved results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
