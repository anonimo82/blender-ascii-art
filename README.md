# Image to ASCII Art for Blender

A powerful Blender add-on that analyzes images and converts them into detailed ASCII Art text files. This tool uses a **Sobel Edge Detection** algorithm combined with luminance mapping to preserve the structural integrity and outlines of your images.

## Features

- **Structural Clarity:** Uses Sobel filters to detect edges and represent them with directional characters (`/`, `\`, `|`, `-`).
- **High-Dynamic Range Luminance:** Maps 70 levels of gray to specific ASCII characters for smooth gradients.
- **Customizable Proportions:** Adjustable Font Ratio to compensate for different text editor line heights (preventing "stretched" images).
- **Invert Mode:** Toggle between Dark Theme (white text on black) and Light Theme (black text on white) compatibility.
- **Contrast Control:** Boost image details before conversion.
- **Direct Blender Integration:** Access the tool directly from the 3D Viewport sidebar (N-Panel).

## Installation

1. Download the `ascii_art_addon` folder.
2. Zip the folder (ensure `__init__.py` is inside).
3. In Blender, go to **Edit > Preferences > Add-ons**.
4. Click **Install...** and select your `.zip` file.
5. Enable the add-on by checking the box next to **Image to ASCII Art**.

## How to Use

1. **Load an Image:** Open an image in Blender's Image Editor.
2. **Open the Panel:** In the 3D Viewport, press `N` to open the sidebar and select the **ASCII Art** tab.
3. **Configure Settings:**
   - **Image:** Select the image you want to convert.
   - **Width:** Number of characters per line (resolution).
   - **Font Ratio:** Adjust this (usually `0.45` to `0.55`) to ensure the output isn't squashed.
   - **Edge Threshold:** Lower values detect more subtle lines; higher values focus on main outlines.
4. **Export:** Set your output path and click **Genera ASCII Art**.

## Viewing the Output

To get the best visual results:
- **Use a Monospaced Font:** (e.g., Consolas, Courier New, Lucida Console).
- **Disable Word Wrap:** Ensure the text doesn't wrap to the next line.
- **Zoom Out:** Hold `Ctrl` + `Scroll Down`. The smaller the characters, the more detailed the image appears.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.