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
# 256 samples @ 128 Hz = 2.0 s -> 0.5 Hz frequency resolution.
# Alpha (8-13 Hz) is wide enough that short segments are less
# of a problem than for Delta, but the same consistent handling
# is used here for comparability with the other scripts.
NPERSEG_TARGET = 256

ALPHA_BAND = (8.0, 13.0)

LEFT_CHANNEL = "F3"
RIGHT_CHANNEL = "F4"

REQUIRED_CHANNELS = [LEFT_CHANNEL, RIGHT_CHANNEL]

# Load data
print("Loading input file...")

df = pd.read_csv(INPUT_FILE)

print("Input file loaded.")
print(f"Number of rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

# Check required columns

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
    channel for channel in REQUIRED_CHANNELS
    if channel not in df.columns
]

if missing_channels:
    raise ValueError(
        f"The following EEG channels are missing from the CSV: {missing_channels}"
    )

# Calculate alpha band power

def calculate_alpha_power(signal, fs):
    signal = np.asarray(signal, dtype=float)


    # Remove NaN / infinite values

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


    # Select alpha band (half-open on the upper edge)

    low_freq, high_freq = ALPHA_BAND
    mask = (frequencies >= low_freq) & (frequencies < high_freq)

    if not np.any(mask):
        return np.nan


    # Integrate PSD over the alpha band

    power = trapezoid(
        psd[mask],
        frequencies[mask]
    )

    return power


# Process each subject, session, condition, stimulus

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
print("Calculating Frontal Alpha Asymmetry (FAA)...")
print()

# Loop through groups

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

    group = group.sort_values("Time")


    # Alpha power for left (F3) and right (F4) channels

    left_signal = group[LEFT_CHANNEL].to_numpy(dtype=float)
    right_signal = group[RIGHT_CHANNEL].to_numpy(dtype=float)

    left_alpha_power = calculate_alpha_power(left_signal, FS)
    right_alpha_power = calculate_alpha_power(right_signal, FS)


    # FAA = ln(right alpha power) - ln(left alpha power)
    # Both powers must be positive and finite for the log to
    # be defined; otherwise FAA is left as NaN.

    if (
        np.isfinite(left_alpha_power) and left_alpha_power > 0 and
        np.isfinite(right_alpha_power) and right_alpha_power > 0
    ):
        faa = np.log(right_alpha_power) - np.log(left_alpha_power)
    else:
        faa = np.nan

    result = {
        "Subject": subject,
        "Session": session,
        "Condition": condition,
        "Stimulus": stimulus,
        f"{LEFT_CHANNEL}_Alpha_Power": left_alpha_power,
        f"{RIGHT_CHANNEL}_Alpha_Power": right_alpha_power,
        "FAA": faa,
    }

    results.append(result)

# Create output dataframe

output_df = pd.DataFrame(results)

output_df = output_df[
    [
        "Subject",
        "Session",
        "Condition",
        "Stimulus",
        f"{LEFT_CHANNEL}_Alpha_Power",
        f"{RIGHT_CHANNEL}_Alpha_Power",
        "FAA",
    ]
]

# Save output file

output_df.to_csv(
    OUTPUT_FILE,
    index=False
)