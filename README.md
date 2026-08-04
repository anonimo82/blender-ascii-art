# Blender ASCII Art

Blender ASCII Art is a compact Blender add-on that converts any image loaded in Blender into monochrome ASCII art and saves the result as a UTF-8 text file.

The add-on combines luminance-based character mapping with optional Sobel edge detection, ordered dithering, contrast adjustment, output aspect-ratio correction, and three character-density presets. It is designed for quick previews as well as detailed text-based renders, while keeping the workflow inside Blender's 3D Viewport sidebar.

## Main Features

- Convert Blender images to plain-text ASCII art.
- Choose an output width from 10 to 2,000 characters.
- Select Compact, Standard, or Detailed character sets.
- Use Advanced Sobel, Standard Sobel, or fill-only rendering.
- Adjust inversion, font aspect ratio, fill contrast, edge threshold, and edge weight.
- Apply optional ordered dithering for smoother gradients.
- Save the result to a `.txt` file using Blender-relative or absolute paths.
- Use NumPy automatically when available, with a pure-Python fallback.

## Installation

1. Download or clone this repository.
2. In Blender, open **Edit > Preferences > Add-ons**.
3. Click **Install**, select the add-on ZIP or `__init__.py`, and enable **Image to ASCII Art**.
4. Open the 3D Viewport, press **N**, and select the **ASCII Art** tab.

## Basic Use

Load an image in Blender's Image Editor, select it in the add-on panel, choose the output settings and destination, then click **Generate ASCII Art**.

See [Tutorial.md](Tutorial.md) for a complete typical workflow. Full feature documentation is available in the project's GitHub Wiki.

## Requirements

- Blender 3.0 or newer.
- NumPy is optional and improves pixel-access performance when available.

## Limitations

The add-on exports monochrome text from one static image at a time. It does not generate colored ANSI output or process animation sequences.

## License

Released under the GNU General Public License v3.0. See [LICENSE](LICENSE).
