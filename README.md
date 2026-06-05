# Image to ASCII Art for Blender

**Image to ASCII Art** is a specialized Blender add-on that analyzes images and converts them into highly detailed ASCII text files.

Unlike basic converters that only map pixels to character brightness, this tool uses a **Sobel Edge Detection** algorithm combined with high-dynamic-range luminance mapping and ordered dithering. This ensures that the structural integrity, sharp outlines, and smooth gradients of your original images are faithfully preserved in text format.

---

## 🚀 Key Features

- **Structural Edge Detection** — Sobel filters actively detect lines and shapes, representing them with directional characters (`/`, `\`, `|`, `-`).
- **Multiple Character Sets** — Choose between Compact (10 chars), Standard (25 chars), and Detailed (40+ chars) sets for different quality/size trade-offs.
- **Ordered Dithering** — Bayer 4×4 matrix dithering eliminates gradient banding for smooth tonal transitions.
- **Aspect Ratio Correction** — Adjustable Font Ratio compensates for line-height variations across different text editors.
- **Theme Adaptability** — Invert Colors toggle for dark or light backgrounds.
- **Fine-Tuning Controls** — Edge Threshold, Fill Contrast, and Edge Weight sliders for precise artistic control.
- **Seamless Blender Integration** — No external libraries required; the UI lives in the 3D Viewport sidebar.

---

## 📋 Requirements

- **Blender Version:** 3.0.0 or higher
- **Dependencies:** None — uses Blender's built-in Python math and image processing capabilities

---

## 🛠️ Installation

1. Click **Code** → **Download ZIP** to download the repository.
2. Open Blender and go to **Edit** → **Preferences** → **Add-ons**.
3. Click **Install...** and select the downloaded ZIP file.
4. Enable the add-on by checking **Image: Image to ASCII Art**.
5. In the **3D Viewport**, press **N** to open the Sidebar and click the **ASCII Art** tab.

---

## 📖 How to Use

### 1. Image Selection

Before generating ASCII art, the target image must be loaded and selected inside Blender.

1. Open the **Image Editor** (Shift+F2).
2. Load your image via **Image → Open**.
3. In the **ASCII Art** panel, click the **Image** dropdown and select the loaded image.

> The image must be fully loaded and unpacked in Blender's memory for the pixel data to be read correctly. If the dropdown is empty, return to the Image Editor and verify the image was opened successfully.

---

### 2. Output Width (Characters)

The **Width** parameter controls how many characters are used per line of output. This directly determines the level of detail and the size of the output file.

| Width | Result |
|-------|--------|
| 100 | Quick preview, low detail |
| 200 | Recommended starting point |
| 300–400 | High detail for photographs |
| 500+ | Maximum detail (may slow Blender) |

**Tip:** Start at 200 and increase only as needed. Widths above 1000 may cause Blender to freeze momentarily during processing.

---

### 3. Edge Detection Algorithm

The add-on uses a **Sobel Edge Detection** filter to identify and render the structural outlines of the image. Three modes are available:

#### Advanced Sobel *(recommended)*
Full Sobel operator with normalized magnitude output. Detects both horizontal and vertical gradients, then combines them into a single edge magnitude (range 0–1) and an edge direction angle.

The edge angle is mapped to a directional character:

| Angle | Character | Description |
|-------|-----------|-------------|
| ~0° / 180° | `\|` | Vertical edge |
| ~45° | `\` | Diagonal edge |
| ~90° | `-` | Horizontal edge |
| ~135° | `/` | Diagonal edge |

**Edge Threshold** controls sensitivity:
- Lower values (0.05–0.1) → more edges detected, finer detail
- Higher values (0.2–0.5) → only strong, dominant edges

**Edge Weight** (0.0–1.0) controls the balance between edge characters and fill characters in the output.

#### Standard
A simplified edge detection pass. Detects fewer edges than Advanced, suitable for graphic-style images or logos where fewer outlines are preferable.

#### None
Disables edge detection entirely. All characters are assigned based on luminance only (fill mode). Useful for artistic effects or when maximum tonal detail is preferred over outlines.

---

### 4. Image Adjustments

These settings control how the source image's pixel data is interpreted before character mapping.

#### Invert Colors
Reverses the luminance mapping. Use this when viewing the output on a **white/light background** (e.g., when printing or using a light-themed text editor). Leave it off for dark backgrounds.

#### Font Ratio
Corrects for the vertical stretching caused by the non-square aspect ratio of monospaced font glyphs. Most text editors render characters taller than they are wide.

- Default: `0.5`
- Typical range: `0.45` – `0.55`
- Increase if the output looks vertically squashed; decrease if it looks stretched

To find the right value, check whether a circle in the source image appears as a circle (not an ellipse) in the output.

#### Fill Contrast
Boosts or reduces the contrast of the fill areas (non-edge pixels). Applies the formula `(luminance − 0.5) × contrast + 0.5` before character mapping.

- `1.0` — No change (default)
- `> 1.0` — More contrast, useful for dark or flat images
- `< 1.0` — Less contrast, softer result

---

### 5. Edge Detection Settings

These parameters fine-tune how edges are detected and rendered.

#### Edge Threshold
Sets the minimum edge magnitude required for a pixel to be rendered as an edge character instead of a fill character. The magnitude is normalized to a 0–1 range.

| Value | Effect |
|-------|--------|
| 0.05 | Detects fine textures and micro-details |
| 0.10–0.15 | Balanced — good for most photographs *(default: 0.15)* |
| 0.20–0.30 | Major outlines only |
| 0.50+ | Only the strongest edges |

#### Edge Weight
Controls the visual balance between edge characters and fill characters. At `0.0`, fills dominate; at `1.0`, edges dominate. The default of `0.6` gives edges moderate prominence while preserving fill tonal detail.

---

### 6. Advanced

#### Use Dithering
Applies **ordered dithering** using a Bayer 4×4 matrix to the fill luminance values before character selection. This breaks up the visible banding that occurs when smooth gradients are quantized to a limited character set.

- **ON** *(default)* — Smooth gradients, ~90% reduction in visible banding. Recommended for photographs and images with gradual tonal transitions.
- **OFF** — Hard tonal steps. Suitable for high-contrast graphics or logos where clean boundaries are preferred.

The dithering intensity is set to 10% of the luminance range, which is enough to eliminate banding without introducing visible noise patterns at normal viewing distances.

---

### 7. Save Path

The **Save to** field sets the output file path for the generated ASCII art.

- The path must end in `.txt` (the extension is appended automatically if missing).
- Use an **absolute path** (e.g., `C:\Users\name\output.txt` or `/home/user/output.txt`) for reliability. Blender's relative paths (starting with `//`) resolve relative to the current `.blend` file.
- Click the **folder icon** to browse for a location.

Once generation completes, a confirmation message in the status bar reports the output dimensions and total character count.

---

## 💡 Tips for Viewing

To get the best visual results when opening the generated `.txt` file:

- **Use a monospaced font** — Courier New, Consolas, Lucida Console, or Menlo.
- **Disable word wrap** — Long lines must not be broken across rows.
- **Zoom out** — The smaller the font size, the more photorealistic the result.
- **View from a distance** — Step back from the monitor to let the tonal transitions resolve.

---

## ⚠️ Known Limitations

- **No color support** — Output is strictly monochromatic ASCII text. ANSI color output is planned for a future version.
- **No animation processing** — The tool processes single static images only.
- **CPU-bound processing** — Generating very wide output (width > 1000 characters) may cause Blender to freeze momentarily.
- **Image must be loaded in memory** — The image must be fully unpacked inside Blender before pixel data can be read.

---

## 📄 License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License v3.0 (GPL-3.0)** as published by the Free Software Foundation. See the [LICENSE](LICENSE) file for full details.
