# Image to ASCII Art for Blender

**Image to ASCII Art** is a specialized Blender add-on that analyzes your images and converts them into highly detailed ASCII text files. 

Unlike basic converters that only map pixels to character brightness, this tool utilizes a **Sobel Edge Detection** algorithm combined with high-dynamic-range luminance mapping. This ensures that the structural integrity, sharp outlines, and smooth gradients of your original images are beautifully preserved in text format.

## 🚀 Key Features

* **Structural Edge Detection:** Uses Sobel filters to actively detect lines and shapes, representing them dynamically with directional characters (`/`, `\`, `|`, `-`).
* **Advanced Luminance Mapping:** Maps approximately 70 different levels of gray to specific ASCII characters to recreate smooth, accurate shading.
* **Aspect Ratio Correction:** Includes an adjustable *Font Ratio* setting. This compensates for the line-height variations in different text editors, preventing your final ASCII art from looking stretched or squashed.
* **Theme Adaptability:** Includes an *Invert Colors* toggle, allowing you to generate text optimized for either Dark Mode (white text on black backgrounds) or Light Mode (black text on white backgrounds).
* **Fine-Tuning Controls:** Boost image details via the *Fill Contrast* slider, or adjust the *Edge Threshold* to determine whether the algorithm picks up subtle interior lines or only stark, main outlines.
* **Seamless Integration:** Operates entirely within Blender. No external libraries are required, and the UI is cleanly integrated into the 3D Viewport sidebar.

## 📋 Requirements

* **Blender Version:** 3.0.0 or higher.
* **Dependencies:** None. It uses Blender's built-in Python math and image processing capabilities.

## 🛠️ Installation

1. Click on `Code` > `Download ZIP` to download the repository.
2. Open Blender and navigate to **Edit** > **Preferences** > **Add-ons**.
3. Click the **Install...** button in the top right corner.
4. Locate and select the downloaded ZIP file, then click **Install Add-on**.
5. Enable the add-on by checking the box next to **Image: Image to ASCII Art**.
6. Go to your **3D Viewport**, press the **N** key to open the Sidebar, and click on the **ASCII Art** tab.

## 📖 How to Use

1. **Load an Image:** Open the image you want to convert inside Blender's native Image Editor.
2. **Select the Image:** In the ASCII Art panel, pick your loaded image from the dropdown.
3. **Configure Settings:**
   - **Width:** Set the number of characters per line (higher = more detail, but a larger text file).
   - **Invert Colors:** Check this if you plan to view the text on a white background.
   - **Font Ratio:** Adjust this (usually between `0.45` and `0.55`) to fix vertical stretching depending on your text editor's line spacing.
   - **Fill Contrast:** Increase to boost the visibility of darker/lighter areas.
   - **Edge Threshold:** Lower values detect micro-details; higher values only draw the strongest outlines.
4. **Export:** Choose your output file path (`.txt`) and click **Generate ASCII Art**.

### 💡 Tips for Viewing
To get the best visual results when opening your generated `.txt` file:
* **Use a Monospaced Font:** Always use fonts like Consolas, Courier New, or Lucida Console.
* **Disable Word Wrap:** Ensure your text editor does not wrap long lines to the next row.
* **Zoom Out:** The smaller the font size, the more photorealistic the ASCII image will appear.

## ⚠️ Known Limitations

The following limitations exist due to the nature of text generation and current script processing:

* **No Color Support:** The output is strictly monochromatic ASCII text. It cannot generate ANSI-colored text or colored HTML.
* **No Animation Processing:** The tool currently processes single static images. It does not export image sequences or video to ASCII animations.
* **CPU-Bound Processing:** The pixel analysis and Sobel filtering are calculated on the CPU via Python. Generating extremely high-resolution ASCII files (e.g., width > 1000 characters) may cause Blender to freeze momentarily while processing.
* **Image Data Access:** The image must be fully loaded and unpacked in Blender's memory for the pixel data to be read accurately.

## 📄 License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License v3.0 (GPL-3.0)** as published by the Free Software Foundation.
See the [LICENSE](LICENSE) file for more details.