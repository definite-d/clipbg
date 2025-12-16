# clipbg

<img width="718" height="308" alt="illustration" src="https://github.com/user-attachments/assets/156e75f1-8c6d-4ebb-a5b7-319149ea5705" />

**ClipBG** is an Inkscape extension to autocrop transparent image backgrounds via clipping.

It analyzes the alpha channel of a selected bitmap, calculates the bounding box of the visible pixels, and applies a non-destructive SVG `clip-path` to the image.

Made for myself (I got tired of having to use GIMP or PS to do this), free for all. Consider dropping a star if you find it useful.

Cheers.

## Installation

### 1. Install the Extension Files

Copy `clipbg.inx` and `clipbg.py` to your Inkscape User Extensions directory. Or just clone this repo in there .

- **Linux:** `~/.config/inkscape/extensions/`
- **Windows:** `%APPDATA%\inkscape\extensions\`
- **macOS:** `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions`

If Inkscape was open before this, you'd need to restart it.

### 2. Install Dependencies

This extension requires the [**Pillow**](https://pillow.readthedocs.io/) library. Depending on your OS, you may need to install this into the Python environment that Inkscape uses.

**Linux Users:**
Chances are, _you already have this_. Otherwise, you just need to install it via your package manager or system pip:

#### Arch (which I use btw)

```bash
sudo pacman -S python-pillow
```

#### System pip

```bash
pip3 install Pillow
```

**Windows Users:**
Inkscape uses its own bundled Python. You must install Pillow into _that_ specific environment. Open PowerShell and run (adjusting for your Inkscape version/location):

```powershell
"C:\Program Files\Inkscape\bin\python.exe" -m pip install Pillow
```

**macOS Users:**
If using the `.dmg` install, Inkscape creates its own environment. You may need to use the pip inside the Inkscape app bundle, or ensure your system `python` (if linked) has Pillow.

## Usage

1. Open Inkscape.
2. Import an image or paste one into the canvas.
3. Select the image object.
4. Navigate to **Extensions > Images > Clip Background**.
5. The extension will calculate the bounds of the visible pixels and apply a clipping rectangle.

## Development

I use [`uv`](https://docs.astral.sh/uv). You should too.

```bash
git clone https://github.com/definite-d/clipbg
cd inkscape-clipbg
uv sync
```

Then activate your virtual environment, and you're set to go.

## Troubleshooting

**Error: `ModuleNotFoundError: No module named 'PIL'`**
This means Inkscape's internal Python cannot find the Pillow library. Please refer to the section on installing dependencies above to ensure Pillow is installed in the correct environment.

**Error: `Image is fully transparent or empty`**
The extension could not find any non-transparent pixels. Check if the image has an alpha channel.

## License

The Unlicense
