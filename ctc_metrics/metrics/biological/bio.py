
def bio(
        ct: float,
        tf: float,
        bc: float,
        cca: float,
):
    """
    Computes the BIO. As described by
        [celltrackingchallenge](http://celltrackingchallenge.net/).

    Args:
        ct: The complete tracking metric.
        tf: The track fractions metric.
        bc: The branching correctness metric.
        cca: The cell cycle accuracy metric.

    Returns:
        The bio metric.
    """
    total_metrics = 0
    if ct is not None:
        total_metrics += 1
    else:
        ct = 0
    if tf is not None:
        total_metrics += 1
    else:
        tf = 0
    if bc is not None:
        total_metrics += 1
    else:
        bc = 0
    if cca is not None:
        total_metrics += 1
    else:
        cca = 0
    bio_score = (ct + tf + bc + cca) / total_metrics
    return bio_score
