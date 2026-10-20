import pandas as pd
import numpy as np
from scipy.signal import welch
from scipy.integrate import trapezoid
from pathlib import Path


INPUT_FILE = Path(
    r"path"
)

OUTPUT_FILE = Path(
    r"path"
)


# EEG sampling frequency
FS = 128  # Hz

# Welch window length in samples.
# 256 samples @ 128 Hz = 2.0 s -> 0.5 Hz frequency resolution,
# which is the minimum needed to resolve the Delta band (0.5-4 Hz).
# If a segment is shorter than this, nperseg falls back to the
# segment length (lower resolution) and a warning is printed.
NPERSEG_TARGET = 256


BANDS = {
    "Delta": (0.5, 4.0),
    "Theta": (4.0, 8.0),
    "Alpha": (8.0, 13.0),
    "Beta": (13.0, 30.0),
    "Gamma": (30.0, 45.0),
}

LAST_BAND = list(BANDS.keys())[-1]


EEG_CHANNELS = [
    "Fp1", "Fp2",
    "F7", "F3", "Fz", "F4", "F8",
    "T7", "C3", "Cz", "C4", "T8",
    "P7", "P3", "Pz", "P4", "P8",
    "O1", "O2"
]

# load data
print("Loading input file...")

df = pd.read_csv(INPUT_FILE)

print("Input file loaded.")
print(f"Number of rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# check required columns
required_columns = [
    "Subject",
    "Session",
    "Condition",
    "Stimulus",
    "Time",
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    raise ValueError(
        f"The following required columns are missing from the CSV: {missing}"
    )

missing_channels = [
    channel for channel in EEG_CHANNELS
    if channel not in df.columns
]

if missing_channels:
    raise ValueError(
        f"The following EEG channels are missing from the CSV: {missing_channels}"
    )

# calculate band power
def calculate_band_power(signal, fs, low_freq, high_freq, is_last_band):
    """
    Calculate absolute power in a frequency band using Welch PSD.

    - nperseg is explicitly set (capped at NPERSEG_TARGET, or the
      signal length if shorter) so that resolution is consistent
      and predictable across segments, instead of relying on
      scipy's default fallback behaviour.
    - Bands are half-open [low, high) to avoid double-counting a
      PSD bin that lands exactly on a shared boundary between two
      bands. The last band (Gamma) is inclusive of its upper edge.
    """

    signal = np.asarray(signal, dtype=float)

    # remove NaN/infinite values

    signal = signal[np.isfinite(signal)]

    if len(signal) < 4:
        return np.nan


    # Determine Welch segment length

    nperseg = min(NPERSEG_TARGET, len(signal))
    noverlap = nperseg // 2

    if len(signal) < NPERSEG_TARGET:
        print(
            f"  Warning: segment has only {len(signal)} samples "
            f"(< {NPERSEG_TARGET}). Using nperseg={nperseg}, "
            f"which reduces frequency resolution for this segment."
        )


    # Welch PSD

    frequencies, psd = welch(
        signal,
        fs=fs,
        window="hann",
        nperseg=nperseg,
        noverlap=noverlap,
        detrend="constant",
        scaling="density"
    )


    # Select frequencies inside requested band (half-open, except the last band which is inclusive on both ends)

    if is_last_band:
        mask = (frequencies >= low_freq) & (frequencies <= high_freq)
    else:
        mask = (frequencies >= low_freq) & (frequencies < high_freq)

    if not np.any(mask):
        return np.nan


    # Integrate PSD over frequency band

    power = trapezoid(
        psd[mask],
        frequencies[mask]
    )

    return power



# process each subject, session, condition, stimulus

group_columns = [
    "Subject",
    "Session",
    "Condition",
    "Stimulus",
]

results = []

groups = df.groupby(
    group_columns,
    sort=True
)

total_groups = len(groups)

print()
print(f"Number of stimulus segments: {total_groups}")
print()
print("Calculating PSD for all frequency bands...")
print()


# loop through groups

for group_number, (group_key, group) in enumerate(groups, start=1):

    subject, session, condition, stimulus = group_key

    print(
        f"[{group_number}/{total_groups}] "
        f"Subject={subject}, "
        f"Session={session}, "
        f"Condition={condition}, "
        f"Stimulus={stimulus}"
    )


    # Ensure samples are in time order before running Welch.
    # groupby preserves original row order, but this makes the
    # assumption explicit and protects against any upstream
    # resorting or interleaving.

    group = group.sort_values("Time")

    result = {
        "Subject": subject,
        "Session": session,
        "Condition": condition,
        "Stimulus": stimulus,
    }


    # Calculate all frequency bands for every EEG channel

    for channel in EEG_CHANNELS:

        signal = group[channel].to_numpy(dtype=float)

        for band_name, (low, high) in BANDS.items():

            column_name = f"{channel}_{band_name}"

            result[column_name] = calculate_band_power(
                signal,
                FS,
                low,
                high,
                is_last_band=(band_name == LAST_BAND)
            )

    results.append(result)

# create output dataframe

output_df = pd.DataFrame(results)

identifier_columns = [
    "Subject",
    "Session",
    "Condition",
    "Stimulus",
]

band_columns = [
    f"{channel}_{band}"
    for channel in EEG_CHANNELS
    for band in BANDS.keys()
]

output_df = output_df[
    identifier_columns + band_columns
]

# save output file

output_df.to_csv(
    OUTPUT_FILE,
    index=False
)


