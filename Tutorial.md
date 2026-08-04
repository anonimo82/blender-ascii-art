# Blender ASCII Art — Typical Workflow

This tutorial describes the standard process for turning an image into an ASCII text file.

## 1. Install and Open the Add-on

Install and enable **Image to ASCII Art** from Blender's Add-ons preferences. In the 3D Viewport, press **N** and open the **ASCII Art** tab.

## 2. Load a Source Image

Open an Image Editor and choose **Image > Open**. Select the image you want to convert. The image must be loaded into Blender before it appears in the add-on's **Image** selector.

## 3. Select the Image

Return to the **ASCII Art Creator** panel and select the loaded image from the **Image** field.

## 4. Choose the Output Size

Set **Width** to the number of characters per line.

- Start around `100` for a quick preview.
- Use about `200` for a balanced result.
- Increase toward `300–500` when the source contains fine details.

The add-on calculates the number of rows automatically from the source aspect ratio and the **Font Ratio** value.

## 5. Choose the Character Detail

Select a **Detail Level**:

- **Compact** creates a bold result with seven characters.
- **Standard** balances tonal range and file size.
- **Detailed** uses the largest character set for smoother shading.

## 6. Configure Edge Rendering

Choose an **Edge Detection** mode:

- **Advanced Sobel** adapts its sampling radius to the output cell size and is the normal choice for detailed images.
- **Standard Sobel** uses a smaller fixed radius for softer, faster outlines.
- **None** creates a luminance-only result without directional edge characters.

Adjust **Edge Threshold** to decide how strong a gradient must be before it becomes an edge. Lower values reveal more texture; higher values preserve only stronger outlines. Use **Edge Weight** to control how readily edge characters replace tonal fill characters.

## 7. Correct the Image Appearance

Use the image-adjustment controls as needed:

- Enable **Invert Colors** when the normal character mapping does not suit the intended background.
- Adjust **Font Ratio** until shapes have the correct proportions in your text editor. Values around `0.45–0.55` are common.
- Increase **Fill Contrast** for a stronger separation between dark and light regions; reduce it for a softer result.

## 8. Decide Whether to Use Dithering

Leave **Use Dithering** enabled for photographs and smooth gradients. Disable it for clean graphic artwork when distinct tonal bands are preferable.

## 9. Choose the Output File

Set **Save to** to an absolute path or a Blender-relative path beginning with `//`. If the filename has no `.txt` extension, the add-on adds it automatically.

## 10. Generate and Review

Click **Generate ASCII Art**. Blender reports the saved path, row count, width, and total number of characters.

Open the generated file in a text editor using a monospaced font, disable word wrapping, and zoom out until the complete image is visible.

## 11. Refine the Result

A common refinement cycle is:

1. Generate a medium-width preview.
2. Correct **Font Ratio** first.
3. Tune **Fill Contrast**.
4. Adjust **Edge Threshold** and **Edge Weight**.
5. Compare the three detail levels.
6. Increase **Width** only after the visual balance is satisfactory.

This approach avoids repeatedly processing an unnecessarily large output while settings are still being tested.
