"""
ESA CCI 4km Ocean Colour Data Downloader
Reads parameters from esa_cci_config.yml and downloads monthly L4 CHL data
from the Copernicus Marine Service.

Dataset: c3s_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M
Variable: CHL (chlorophyll-a concentration)
Resolution: 4km global

Prepared by NPEC 
"""

from datetime import datetime
from pathlib import Path

import copernicusmarine
import yaml


CONFIG_FILE = Path(__file__).parent / "esa_cci_config.yml"
DATASET_ID  = "c3s_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M"
VARIABLE    = "CHL"


def load_config(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def parse_date(value: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y%m"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date '{value}'. Use YYYY-MM-DD or YYYY-MM.")


def download(cfg: dict) -> Path:
    start = parse_date(str(cfg["dates"]["start"]))
    end   = parse_date(str(cfg["dates"]["end"]))

    bbox       = cfg["bbox"]
    output_dir = Path(cfg["output_dir"])
    username   = cfg["credentials"]["username"]
    password   = cfg["credentials"]["password"]

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Dataset  : {DATASET_ID}")
    print(f"Variable : {VARIABLE}")
    print(f"Period   : {start.date()} -> {end.date()}")
    print(f"BBox     : lon [{bbox['lon_min']}, {bbox['lon_max']}]  "
          f"lat [{bbox['lat_min']}, {bbox['lat_max']}]")
    print(f"Output   : {output_dir.resolve()}")
    print("-" * 50)

    result = copernicusmarine.subset(
        dataset_id=DATASET_ID,
        variables=[VARIABLE],
        minimum_longitude=bbox["lon_min"],
        maximum_longitude=bbox["lon_max"],
        minimum_latitude=bbox["lat_min"],
        maximum_latitude=bbox["lat_max"],
        start_datetime=start,
        end_datetime=end,
        username=username,
        password=password,
        output_directory=str(output_dir),
    )

    file_path = Path(result.file_path)
    print(f"Saved to : {file_path}")
    return file_path


if __name__ == "__main__":
    cfg = load_config(CONFIG_FILE)
    download(cfg)
