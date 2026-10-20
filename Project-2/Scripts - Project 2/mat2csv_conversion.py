import h5py
import numpy as np
import pandas as pd


MAT_FILE = r"C:\Users\utente\Desktop\PowerBI Portfolio\Project 2\Data\MAT files\processed_experiment3_fixations.mat"

CSV_FILE = r"C:\Users\utente\Desktop\PowerBI Portfolio\Project 2\Data\MAT files\processed_experiment3_fixations.csv"


# read MAT file
with h5py.File(MAT_FILE, "r") as f:

    refs = f["#refs#"]

    # Extract the four relevant arrays
    stim_no = np.asarray(refs["A"][()]).flatten()
    time_start = np.asarray(refs["B"][()]).flatten()
    time_end = np.asarray(refs["C"][()]).flatten()
    session_no = np.asarray(refs["z"][()]).flatten()


# check lengths
n = len(stim_no)

if not (
    len(time_start) == n
    and len(time_end) == n
    and len(session_no) == n
):
    raise ValueError("The source arrays do not have the same length.")


print(f"\nNumber of rows: {n:,}")


# create participant id column

participant_id = np.zeros(n, dtype=int)

current_participant = 2

for i in range(n):

    if i == 0:
        # First row belongs to participant 2
        participant_id[i] = current_participant

    else:

        # New participant starts when:
        #
        # current row:
        #   session_no == 1
        #   stim_no == 1
        #
        # previous row:
        #   session_no != 1
        #   stim_no != 1
        #

        new_participant = (
            session_no[i] == 1
            and stim_no[i] == 1
            and session_no[i - 1] != 1
            and stim_no[i - 1] != 1
        )

        if new_participant:
            current_participant += 1

        participant_id[i] = current_participant


# create dataframe

df = pd.DataFrame({
    "Participant_ID": participant_id,
    "session_no": session_no.astype(int),
    "stim_no": stim_no.astype(int),
    "time_start": time_start,
    "time_end": time_end,
})


# save file

df.to_csv(
    CSV_FILE,
    index=False
)


