# ESA CCI 4km Ocean Colour Downloader

Downloads monthly global chlorophyll-a (CHL) data via the Copernicus Marine Service.

- Dataset: `c3s_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M`
- Variable: CHL (chlorophyll-a, mg m⁻³)
- Resolution: 4 km, monthly composites
- Coverage: Global, 1997 – present

---

## Files


- `esa_cci_config.yml` : Configuration file (edit this before running) 
- `environment.yml`    : Conda environment with all dependencies 
- `download_esa_cci.py`: Main download script 

## Setup

### 1. Create and activate the conda environment

```bash
conda env create -f environment.yml
conda activate env
```

### 2. Register on Copernicus Marine Service

Create a free account at https://marine.copernicus.eu/ and take your username and password.

---

## Configuration

Open `esa_cci_config.yml` and fill in your details:

```yaml
credentials:
  username: "your_username"
  password: "your_password"

dates:
  start: "2020-01"   # start month  (YYYY-MM or YYYY-MM-DD)
  end:   "2020-12"   # end month

bbox:
  lon_min: -180.0
  lon_max:  180.0
  lat_min:  -90.0
  lat_max:   90.0

output_dir: "./data"
```

To download a regional subset, change the `bbox` values. For example, for the Northwest Pacific:

```yaml
bbox:
  lon_min: 117.0
  lon_max: 160.0
  lat_min:  24.0
  lat_max:  52.0
```

---

## Usage

```bash
python download_esa_cci.py 
```

The downloaded NetCDF file will be saved in the directory specified by `output_dir` (./data by default).

---

## Output

The script saves a single NetCDF (`.nc`) file containing the CHL variable for the
requested time period and spatial extent. Example filename:

```
data/c3s_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M_CHL_..._.nc
```

You can open it with Python:

```python
import xarray as xr

ds = xr.open_dataset("data/<filename>.nc")
print(ds)
print(ds["CHL"])
```

---

## Requirements

All dependencies are listed in `environment.yml`. Key packages:

- `copernicusmarine` — Copernicus Marine Service client
- `pyyaml` — reads the config file
- `xarray`, `netCDF4` — for working with the downloaded data

Script prepared and organized by NPEC 
