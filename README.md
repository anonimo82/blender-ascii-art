# Image to ASCII Art for Blender

**Image to ASCII Art** is a Blender add-on that analyzes images and converts them into highly detailed ASCII text files.

Unlike basic converters that only map pixels to character brightness, this tool uses a **Sobel Edge Detection** algorithm combined with high-dynamic-range luminance mapping and ordered dithering. This ensures that the structural integrity, sharp outlines, and smooth gradients of your original images are faithfully preserved in text format.

---

## 🚀 Key Features

- **Structural Edge Detection** — Sobel filters actively detect lines and shapes, representing them with directional characters (`/`, `\`, `|`, `-`).
- **Three Character Sets** — Choose between Compact (7 chars), Standard (25 chars), and Detailed (45+ chars) for different quality/file-size trade-offs.
- **Ordered Dithering** — Bayer 4×4 matrix dithering eliminates gradient banding for smooth tonal transitions.
- **Aspect Ratio Correction** — Adjustable Font Ratio compensates for line-height variations across different text editors.
- **Theme Adaptability** — Invert Colors toggle for dark or light backgrounds.
- **Fine-Tuning Controls** — Edge Threshold, Fill Contrast, and Edge Weight sliders for precise artistic control.
- **NumPy Acceleration** — Automatically uses NumPy for faster pixel access when available; falls back to pure Python otherwise.
- **Seamless Blender Integration** — No mandatory external libraries; the UI lives in the 3D Viewport sidebar.

---

## 📋 Requirements

- **Blender Version:** 3.0.0 or higher
- **Dependencies:** None required. NumPy is optional but recommended for faster processing on large images.

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

> The image must be fully loaded and unpacked in Blender's memory for pixel data to be read correctly. If the dropdown is empty, return to the Image Editor and verify the image was opened successfully.

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

### 3. Detail Level

Selects the **character set** used to represent luminance values. More characters allow finer tonal steps but produce larger output files.

| Level | Characters | Use Case |
|-------|-----------|----------|
| Compact | 7 | Small files, bold graphical style |
| Standard *(default)* | 25 | Balanced quality and file size |
| Detailed | 45+ | Maximum tonal range, best for photographs |

The character sets are ordered from dark (space) to bright, so each character maps to a specific luminance range. Dithering further smooths the transitions between adjacent levels regardless of which set is chosen.

---

### 4. Edge Detection Algorithm

The add-on uses a **Sobel Edge Detection** filter to identify and render the structural outlines of the image. Three modes are available:

#### Advanced Sobel *(recommended)*
Full Sobel operator with normalized magnitude output. Detects both horizontal and vertical gradients using a sample radius proportional to the pixel block size (`radius_x = step_x / 2`, `radius_y = step_y / 2`). This adapts automatically to the output resolution, so edges remain sharp at any width.

The combined gradient magnitude is normalized to the theoretical maximum (`4 × √2 ≈ 5.657`) and mapped to a 0–1 range. The gradient angle is then used to select a directional character:

| Angle Range | Character | Edge Type |
|-------------|-----------|-----------|
| 0° – 22.5° / 157.5° – 180° | `\|` | Vertical |
| 22.5° – 67.5° | `\` | Diagonal (top-left to bottom-right) |
| 67.5° – 112.5° | `-` | Horizontal |
| 112.5° – 157.5° | `/` | Diagonal (top-right to bottom-left) |

#### Standard Sobel
A lighter, faster edge pass using a fixed 1-pixel sampling radius. Detects fewer and softer edges than Advanced mode. Suitable for graphic-style images, logos, or when a cleaner, less busy output is preferred.

#### None
Disables edge detection entirely. All characters are assigned based on luminance only. Useful for artistic effects or when maximum tonal detail is more important than structural outlines.

---

### 5. Image Adjustments

These settings control how the source image's pixel data is interpreted before character mapping.

#### Invert Colors
Reverses the luminance mapping, swapping dark and light characters. Use this when viewing the output on a **white/light background** (e.g., when printing or using a light-themed text editor). Leave it off for dark terminal or code-editor backgrounds.

#### Font Ratio
Corrects for the vertical stretching caused by the non-square aspect ratio of monospaced font glyphs. Most text editors render characters taller than they are wide.

- Default: `0.5`
- Typical range: `0.45` – `0.55`
- Increase if the output looks vertically squashed; decrease if it looks stretched.

To calibrate the value, render a source image containing a perfect circle and adjust Font Ratio until the output appears circular rather than oval.

#### Fill Contrast
Boosts or reduces the contrast of fill areas (non-edge pixels) before character selection. The formula applied is:

```
adjusted_luminance = (luminance − 0.5) × contrast + 0.5
```

| Value | Effect |
|-------|--------|
| `1.0` | No change *(default)* |
| `> 1.0` | Higher contrast — useful for dark or flat images |
| `< 1.0` | Lower contrast — softer, more uniform output |

---

### 6. Edge Detection Settings

These parameters fine-tune how edges are detected and how prominently they appear in the output.

#### Edge Threshold
Sets the minimum normalized edge magnitude (0–1) required for a pixel to be rendered as an edge character. The effective threshold is further scaled by Edge Weight (see below).

| Value | Effect |
|-------|--------|
| 0.05 | Detects fine textures and micro-details |
| 0.10–0.15 | Balanced — good for most photographs *(default: 0.15)* |
| 0.20–0.30 | Major outlines only |
| 0.50+ | Only the strongest, dominant edges |

#### Edge Weight
Controls how aggressively edge characters replace fill characters when an edge is detected. Internally, the effective detection threshold is computed as:

```
effective_threshold = edge_threshold × (1.0 − edge_weight)
```

| Value | Behavior |
|-------|----------|
| `0.0` | Edge characters never appear; output is fill-only |
| `0.5` | Balanced blend of edges and fill *(default: 0.6)* |
| `1.0` | Every detected edge wins; fill characters are suppressed |

This means Edge Weight and Edge Threshold interact: a high Edge Weight lowers the effective threshold, making more edges visible; a low Edge Weight raises it, suppressing all but the strongest edges.

---

### 7. Advanced

#### Use Dithering
Applies **ordered dithering** using a Bayer 4×4 matrix to the fill luminance values before character selection. This breaks up visible banding that occurs when smooth gradients are quantized to a limited character set.

- **ON** *(default)* — Smooth gradients, recommended for photographs and images with gradual tonal transitions. The dither intensity is 10% of the luminance range, which eliminates banding without introducing visible noise at normal viewing distances.
- **OFF** — Hard tonal steps. Suitable for high-contrast graphics or logos where clean boundaries are preferred.

---

### 8. Save Path

The **Save to** field sets the output file path for the generated ASCII art.

- The path must end in `.txt`; the extension is appended automatically if missing.
- Use an **absolute path** (e.g., `C:\Users\name\output.txt` or `/home/user/output.txt`) for reliability. Blender's relative paths (starting with `//`) resolve relative to the current `.blend` file.
- Click the **folder icon** to browse for a location.

Once generation completes, a status bar confirmation reports the output dimensions (rows × width) and the total character count.

---

## 💡 Tips for Viewing

To get the best visual results when opening the generated `.txt` file:

- **Use a monospaced font** — Courier New, Consolas, Lucida Console, or Menlo.
- **Disable word wrap** — Long lines must not be broken across rows.
- **Zoom out** — The smaller the font size, the more photorealistic the result.
- **View from a distance** — Step back from the monitor to let tonal transitions resolve visually.

---

## ⚙️ Performance Notes

- **NumPy** — If NumPy is installed in Blender's Python environment, the add-on uses it to load the full pixel array into a NumPy array reshaped to `(height, width, 4)` for fast 2D indexing. Without NumPy, it falls back to a flat Python list. The panel will display a reminder if NumPy is not detected.
- **Large outputs** — Widths above 1000 characters may cause Blender to freeze momentarily because image processing runs on the main thread. This is expected behavior; Blender will recover once generation is complete.
- **Memory** — Very high-resolution source images are kept fully unpacked in Blender's memory during processing. If memory is a concern, consider resizing the source image before running the add-on.

---

## ⚠️ Known Limitations

- **No color support** — Output is strictly monochromatic ASCII text. ANSI color output is planned for a future version.
- **No animation processing** — The tool processes single static images only.
- **CPU-bound processing** — Generating very wide output (width > 1000 characters) may cause Blender to freeze momentarily.
- **Image must be loaded in memory** — The image must be fully unpacked inside Blender before pixel data can be read.

---

## 🔧 Technical Reference

### Luminance Formula

Pixel luminance is calculated using the ITU-R BT.709 standard:

```
L = 0.2126 × R + 0.7152 × G + 0.0722 × B
```

This matches how human vision perceives relative brightness and gives more accurate tonal representation than a simple average.

### Sobel Operator

The Sobel operator samples an 8-pixel neighborhood around each cell center and computes horizontal (`Gx`) and vertical (`Gy`) gradients:

```
Gx = (TR + 2·MR + BR) − (TL + 2·ML + BL)
Gy = (TL + 2·TC + TR) − (BL + 2·BC + BR)
```

The gradient magnitude is normalized by the theoretical maximum `4√2 ≈ 5.657`, and the angle is computed as `atan2(Gy, Gx)`.

### Bayer Dithering Matrix

The 4×4 Bayer matrix used for ordered dithering:

```
 0   8   2  10
12   4  14   6
 3  11   1   9
15   7  13   5
```

Values are divided by 16 and centered around 0 (`− 0.5`), then scaled by 10% before being added to the luminance value. The result is clamped to [0, 1].

---

## 📄 License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License v3.0 (GPL-3.0)** as published by the Free Software Foundation. See the [LICENSE](LICENSE) file for full details.
