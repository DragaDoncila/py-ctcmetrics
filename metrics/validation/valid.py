import numpy as np
import warnings


def valid(masks, tracks, labels_in_frames):
    """ Checks all mask files in a cell tracking result directory if there is
    at least one foreground pixel. If not, the file is reported. A foreground
    pixel is defined as a pixel with a value > 0. The report is written to the
    standard output.
    """

    is_valid = 1
    # Check if all parents are >= 0
    for i, track in enumerate(tracks):
        if track[3] < 0:
            warnings.warn(f"Invalid parent: {track}", UserWarning)
            is_valid = 0

    # Check if all labels are unique
    labels = tracks[:, 0]
    if len(np.unique(labels)) != len(labels):
        warnings.warn("Labels are not unique.", UserWarning)
        is_valid = 0

    # Check if parents endet before children are born
    for i, track in enumerate(tracks):
        label, birth, end, parent = track
        if parent != 0:
            parent_idx = np.argwhere(tracks[:, 0] == parent).squeeze()
            assert parent_idx.size == 1, parent_idx
            parent_track = tracks[parent_idx]
            parent_label, parent_birth, parent_end, parent_parent = parent_track
            if parent_end >= birth:
                warnings.warn(
                    f"Parent ends after child starts: {track} {parent_track}",
                    UserWarning)
                is_valid = 0

    # Check if all labels are used
    max_label = max(labels)
    if max_label != len(labels):
        warnings.warn("Some labels are not used.", UserWarning)
        #is_valid = 0  # TODO: Check out if this is a valid criteria or not

    # Check if all labels are in the frames they are used to be
    frames = [list() for _ in range(len(masks))]
    for i, track in enumerate(tracks):
        label, birth, end, parent = track
        for frame in range(birth, end + 1):
            frames[frame].append(label)

    for labels_in_frame, file, frame in zip(labels_in_frames, masks, frames):
        for label in labels_in_frame:
            if label != 0:
                if label not in frame:
                    warnings.warn(
                        f"Label {label} in mask but not in res_track {file}.",
                        UserWarning)
                    is_valid = 0
        for label in frame:
            if label not in labels_in_frame:
                warnings.warn(
                    f"Label {label} in res_track but not in mask {file}.",
                    UserWarning)
                is_valid = 0

    # Check if frames are empty
    for i, f in enumerate(frames):
        if len(f) == 0:
            warnings.warn(f"Empty frame {i}.", UserWarning)

    return is_valid