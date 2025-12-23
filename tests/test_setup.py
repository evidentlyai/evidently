from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


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

    with open(path / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)
    install_reqs = {
        k.split("[")[0]: _get_min_version(v) for r in config["project"]["dependencies"] for k, v in (r.split(">="),)
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
    ), f"project.dependencies has extra reqs {extra} and wrong versions of {wrong_version}"


def _get_min_version(value):
    return value.split(",")[0]
