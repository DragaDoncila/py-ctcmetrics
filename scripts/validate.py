import argparse
from os.path import join
from multiprocessing import Pool, cpu_count

from ctc_metrics.metrics import valid
from ctc_metrics.utils.handle_results import print_results
from ctc_metrics.utils.filesystem import \
    parse_directories, read_tracking_file, parse_masks
from ctc_metrics.utils.representations import match as match_tracks


def validate_sequence(
        res: str,
        multiprocessing: bool = True,
):
    """ Evaluate a single sequence """
    print("\r", res, end="")
    res_tracks = read_tracking_file(join(res, "res_track.txt"))
    res_masks = parse_masks(res)
    assert len(res_masks) > 0, res

    args = zip([None for x in res_masks], res_masks)
    if multiprocessing:
        with Pool(cpu_count()) as p:
            matches = p.starmap(match_tracks, args)
    else:
        matches = [match_tracks(*x) for x in args]
    labels_gt, labels_res, mapped_gt, mapped_res = [], [], [], []
    for match in matches:
        labels_gt.append(match[0])
        labels_res.append(match[1])
        mapped_gt.append(match[2])
        mapped_res.append(match[3])

    results = dict()
    results["Valid"] = valid(res_masks, res_tracks, labels_res)

    print("\r", end="")

    return results


def validate_all(
        res_root: str,
):
    """ Evaluate all sequences in a directory """
    results = list()

    ret = parse_directories(res_root, None)
    for res, gt, st, num_digits, name in zip(*ret):
        results.append([name, validate_sequence(res, gt)])

    return results


def parse_args():
    parser = argparse.ArgumentParser(
        description='Evaluates CTC-Sequences. '
    )

    parser.add_argument('--res', type=str, required=True)
    parser.add_argument('--full-directory', action="store_true")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    if args.full_directory:
        res = validate_all(args.res)
    else:
        res = validate_sequence(args.res)

    print_results(res)

# python scripts/evaluate.py --res="C:\Users\kaiser\Desktop\data\CTC\Inference\original\train" --gt="C:\Users\kaiser\Desktop\data\CTC\Inference\original\train" --csv-path="C:\Users\kaiser\Desktop\data\CTC\Inference\original\eval.csv" --full-directory
# python scripts/evaluate.py --res="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_1_1_no_mitosis\train" --gt="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_1_1_no_mitosis\train" --csv-path="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_1_1_no_mitosis\eval.csv" --full-directory
# python scripts/evaluate.py --res="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_20_5_no_mitosis\train" --gt="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_20_5_no_mitosis\train" --csv-path="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_20_5_no_mitosis\eval.csv" --full-directory


# python scripts/evaluate.py --res="C:\Users\kaiser\Desktop\data\CTC\Inference\original\train\BF-C2DL-HSC\01_RES" --gt="C:\Users\kaiser\Desktop\data\CTC\Inference\original\train\BF-C2DL-HSC\01_GT" --Valid
# python scripts/evaluate.py --res="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_1_1_no_mitosis\train\BF-C2DL-HSC\01_RES" --gt="C:\Users\kaiser\Desktop\data\CTC\Inference\ours_1_1_no_mitosis\train\BF-C2DL-HSC\01_GT" --Valid
