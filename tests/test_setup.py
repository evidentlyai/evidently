from pathlib import Path

from setup import setup_args


def test_minimal_requirements():
    path = Path(__file__).parent.parent
    with open(path / "requirements.min.txt") as f:
        lines = {line.strip().split("#")[0] for line in f.readlines()}
        min_reqs = {
            k.split("[")[0]: _get_min_version(v)
            for line in lines
            if line.strip()
            for k, v in (line.strip().split("=="),)
        }

    install_reqs = {
        k.split("[")[0]: _get_min_version(v) for r in setup_args["install_requires"] for k, v in (r.split(">="),)
    }
    extra = []
    wrong_version = []
    for m, v in install_reqs.items():
        if m not in min_reqs:
            extra.append(f"{m}>={v}")
            continue
        if v != min_reqs[m]:
            wrong_version.append(f"{m}>={v}")
            continue

    assert (
        len(extra) == 0 and len(wrong_version) == 0
    ), f"install_requires has extra reqs {extra} and wrong versions of {wrong_version}"


def _get_min_version(value):
    return value.split(",")[0]
