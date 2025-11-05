
This repository focuses on automating the hardness testing process through image processing techniques. It provides tools to measure Brinell indentation diameters from images and compute HBW (Brinell Hardness) values. The project features both an automatic circle detection mode and a manual measurement mode.

## Contents
- `Working code/Manual.py` — Interactive manual measurement: click two points (horizontal line) to measure diameter, choose test load, calculate HBW, show results on image and save output.
- `Working code/Autocircle.py` — Automatic detection using contour filtering and HoughCircles, shows measurement on image, allows test selection, calculates HBW and saves output.
- `Images/` — (user) image files used for testing.
- `Results/` — Saved annotated outputs (created automatically).

## Features
- Manual point-based diameter measurement with optional calibration.
- Automatic circle/indentation detection (contour + Hough fallback).
- On-image display of measured diameter and HBW.
- Saves result images with timestamp and HBW in filename.
- Simple key-based selection of Brinell test parameters:
    - Press `1` → 750 kg, ball 5 mm
    - Press `2` → 3000 kg, ball 10 mm
    - Press `3` → 1000 kg, ball 10 mm

## Requirements
- Python 3.8+ (tested)
- OpenCV (cv2)
- NumPy

Install dependencies:
```bash
pip install opencv-python numpy
```

## Quick Start

1. Open the project in VS Code (or run from terminal).
2. Set image path and optional calibration parameters at top of each script:
     - `IMAGE_PATH` / `image_path` — path to input image
     - `pixel_per_mm` — set to `None` to run calibration in manual mode, or set a known value to measure directly
3. Run either script:
```bash
python "Working code/Manual.py"
python "Working code/Autocircle.py"
```

## Manual Mode (Manual.py)
- Click two points on the indentation diameter (the code uses horizontal distance; second click snaps to same y as first).
- Press `r` to reset points.
- Press `Enter` after measuring to proceed to test selection.
- The first image window is automatically closed when the HBW window appears.
- Final annotated image is displayed and saved to `Results/` with filename `{timestamp}_HBW-{HBW}.jpg`.

Notes:
- To calibrate pixel/mm, set `pixel_per_mm = None` and set `ref_length_mm` to the known length used for calibration. Click the two calibration points then the scripts compute pixels/mm.

## Automatic Mode (Autocircle.py)
- Attempts contour-based circle detection first; falls back to `HoughCircles` if needed.
- Draws detected circle, displays diameter (converted using `pixel_per_mm`), prompts for test selection, computes HBW, and saves annotated image.
- Tweak detection parameters (morphology kernel, Hough params, min/max radius) if detection fails.

## Output & Saving
- Results are saved to `Results/` (created automatically).
- Filenames use timestamps and HBW value for easy tracking.

## Troubleshooting
- Image not loading? Verify `IMAGE_PATH` is correct.
- No circle detected in auto mode? Try:
    - Adjust contrast/lighting or pre-process the image.
    - Tweak Hough/contour parameters in `Autocircle.py`.
    - Use `Manual.py` to measure manually.
- Text not visible on image? Text color is black `(0,0,0)` or green for highlighted fields—adjust colors in code if needed.

## Contributing
- Improve detection by adding more preprocessing (CLAHE, denoising) or refining parameter tuning.
- Add batch processing to annotate multiple images.

## License
This project is licensed under the MIT License — see the accompanying `LICENSE` file for details.


