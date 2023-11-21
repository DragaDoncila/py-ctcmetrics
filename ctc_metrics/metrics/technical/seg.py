import numpy as np


def seg(
    labels_ref,
    intersection_over_unions,
):
    """
    Calculates the segmentation metric. The metric describes the average overlap
    between the reference labels and an assigned result labels.

    Args:
        labels_ref: A list of lists with the labels of the ground truth masks
            according to the respective frame.
        intersection_over_unions: A list of lists with the intersection over
            union values of matched reference and computed result labels.

    Returns:
        The segmentation metric, the number of true positives and the number of
        false negatives.

    """
    number_of_reference_labels = np.sum([len(l) for l in labels_ref])
    intersection_over_unions = np.concatenate(intersection_over_unions)
    true_positives = int(intersection_over_unions.size)
    false_negatives = int(number_of_reference_labels - true_positives)
    total_intersection = np.sum(intersection_over_unions)
    seg_measure = total_intersection / np.maximum(number_of_reference_labels, 1)
    return float(seg_measure), int(true_positives), int(false_negatives)