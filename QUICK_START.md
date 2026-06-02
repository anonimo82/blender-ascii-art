# Quick Start Guide - Enhanced ASCII Art Add-on v4.0

## Installation (Same as Before)

1. Download the ZIP file
2. Open Blender → **Edit** → **Preferences** → **Add-ons**
3. Click **Install** and select the ZIP
4. Enable **Image: Image to ASCII Art**
5. Open 3D Viewport sidebar (**N** key) → **ASCII Art** tab

---

## 🎬 Basic Workflow

### Step 1: Load an Image
1. Open Image Editor (Shift+F2)
2. Load an image (Image → Open)
3. Return to ASCII Art panel

### Step 2: Select the Image
- In **ASCII Art** panel, click the **Image** dropdown
- Select your loaded image

### Step 3: Configure Settings
```
Width:              200 (start here, increase for detail)
Detail Level:       Standard (balanced quality)
Edge Detection:     Advanced Sobel
Invert Colors:      OFF (unless using white background)
Font Ratio:         0.5 (adjust if stretched)
Fill Contrast:      1.0 (increase for darker images)
Edge Threshold:     0.15 (adjust for more/fewer edges)
Use Dithering:      ON (for smoother gradients)
```

### Step 4: Set Output Path
- Click folder icon or type path
- Must end in `.txt`

### Step 5: Click **Generate ASCII Art**
- Wait for confirmation message
- Open the `.txt` file in your text editor

---

## 🎨 New Features Explained

### Detail Level
Choose your quality/file-size trade-off:

**🚀 Compact (10 chars)**
- Smallest files
- Quick rendering
- Best for: Logos, test previews
- Example: `" .:=#@$"`

**⚖️ Standard (25 chars)** ← RECOMMENDED
- Balanced quality
- Good file size
- Best for: Most photos, general use
- Default character set for best results

**✨ Detailed (40+ chars)**
- Maximum quality
- Larger files
- Best for: High-resolution prints, detailed images
- Smooth tonal gradients

### Edge Detection Modes

**🔍 Advanced Sobel** ← RECOMMENDED
- Full edge detection algorithm
- Normalized for consistency
- Best for: Photos with clear outlines
- Best quality

**📐 Standard**
- Simplified edge detection
- Good for: Artwork, graphics
- Fewer edges detected

**❌ None**
- Disable edge detection entirely
- Fill characters only
- Best for: Extreme detail, artistic effect

### Advanced Options

**🎲 Use Dithering** (ON by default)
- Smooths gradients using Bayer matrix
- Eliminates banding
- No performance cost
- Keep ON for best quality

---

## ⚙️ Parameter Tuning Guide

### Image Looks Too Dark
→ Increase **Fill Contrast** (1.2-1.5)
→ Decrease **Edge Threshold** (0.1-0.05)

### Image Looks Too Bright
→ Decrease **Fill Contrast** (0.7-0.8)
→ Increase **Edge Threshold** (0.2-0.3)

### Missing Fine Details
→ Set **Detail Level** → Detailed
→ Decrease **Edge Threshold** (0.05-0.1)
→ Increase **Width** (300-400 chars)

### Too Much Noise/Texture
→ Increase **Edge Threshold** (0.2-0.3)
→ Switch **Detail Level** → Compact
→ Decrease **Width** (100-150 chars)

### Stretched or Squeezed Vertically
→ Adjust **Font Ratio**
→ Use 0.45-0.55 range
→ Open `.txt` in monospace font first to test

### Too Many Edges
→ Increase **Edge Threshold** (0.2-0.3)
→ Switch **Edge Detection** → Standard

### Not Enough Edges
→ Decrease **Edge Threshold** (0.05-0.1)
→ Switch **Detail Level** → Standard

---

## 📝 Viewing Tips

### Best Practices
1. **Always use monospaced font**
   - Courier New
   - Consolas
   - Lucida Console
   - Menlo (Mac)

2. **Disable word wrap**
   - Notepad++ (Settings → Preferences → Editing)
   - VS Code (Alt+Z to toggle)
   - Sublime (View → Word Wrap)

3. **Adjust zoom**
   - Smaller zoom = more photorealistic
   - Try 50-75% zoom first
   - Zoom out more for portrait-mode images

4. **View from distance**
   - Step back from monitor
   - Better perception of tones
   - Aliasing becomes invisible

### Dark Background (Recommended)
- Use `Invert Colors: OFF`
- White text on black background
- Easy on eyes
- Best contrast

### Light Background
- Use `Invert Colors: ON`
- Black text on white background
- Better for printing
- Similar visual result

---

## 🎯 Presets for Common Tasks

### Photograph / Realistic Image
```
Width:           250
Detail Level:    Standard
Edge Detection:  Advanced Sobel
Edge Threshold:  0.12-0.15
Contrast:        1.0
Use Dithering:   ON
Font Ratio:      0.5
```

### Logo / Vector Graphics
```
Width:           150-200
Detail Level:    Compact
Edge Detection:  Advanced Sobel
Edge Threshold:  0.08-0.12
Contrast:        1.3-1.5
Use Dithering:   OFF
Font Ratio:      0.5
```

### High-Detail / Art Print
```
Width:           400-500
Detail Level:    Detailed
Edge Detection:  Advanced Sobel
Edge Threshold:  0.1
Contrast:        0.9
Use Dithering:   ON
Font Ratio:      0.5
```

### Quick Preview
```
Width:           100
Detail Level:    Compact
Edge Detection:  Standard
Edge Threshold:  0.15
Contrast:        1.0
Use Dithering:   OFF
Font Ratio:      0.5
```

### Dark/Moody Effect
```
Width:           200-300
Detail Level:    Standard
Edge Detection:  Advanced Sobel
Edge Threshold:  0.05-0.1 (more edges)
Contrast:        1.2-1.5
Use Dithering:   ON
Font Ratio:      0.5
```

---

## 🐛 Troubleshooting

### "Please select an image first!"
- Open Image Editor (Shift+F2)
- Load an image using Image → Open
- Return to ASCII Art panel and refresh

### Output file is empty
- Check output path is writable
- Use absolute path instead of relative (`//`)
- Ensure `.txt` extension

### Characters are stretched
- Adjust **Font Ratio** value
- Try 0.45-0.55 range
- Test different values until square looks square

### Lines wrap unexpectedly
- Disable word wrap in text editor
- Check `width_chars` isn't too high
- Increase editor window width

### Image looks grainy
- Decrease **Edge Threshold**
- Increase **Width** (more characters)
- Toggle **Use Dithering** ON

### Blender freezes during generation
- Reduce **Width** value (start at 150)
- Switch to **Compact** detail level
- Large images (10MB+) may take time

---

## 💡 Pro Tips

1. **Test with standard settings first**
   - Get baseline result
   - Then tweak parameters
   - Start with 200 width

2. **Use dithering always**
   - Turns on by default
   - Improves quality dramatically
   - No performance cost

3. **Edge threshold is powerful**
   - Small changes have big impact
   - 0.05-0.3 is the useful range
   - Start at 0.15

4. **Different images need different settings**
   - High contrast: Lower threshold
   - Low contrast: Higher contrast slider
   - Experiment and save good presets

5. **Print previews**
   - ASCII art prints surprisingly well
   - Use narrow margins
   - Courier New at 8-10pt is classic

6. **Layer multiple passes**
   - Generate at different widths
   - Blend them in image editor
   - Create unique effects

---

## 📊 Performance Notes

| Setting | Impact | Notes |
|---------|--------|-------|
| Width | Huge | 100 chars = instant, 1000 chars = seconds |
| Detail Level | Medium | Detailed is 1.1x slower than Compact |
| Dithering | Minimal | <1% slower |
| Edge Mode | Small | Standard ~5% faster than Advanced |
| Image Size | Large | 4K image is slower than 1K |

**Recommendations:**
- Start with 200 width for testing
- Increase width only as needed
- Use Compact for quick previews
- Use Detailed only for final output

---

## ❓ FAQ

**Q: Can I use color?**
A: Not yet. This version outputs monochrome ASCII only. Color ANSI output is planned for v5.0.

**Q: Can I process videos?**
A: Not currently. The add-on works with static images only.

**Q: Can I create custom character sets?**
A: In v4.0, use the three presets. Custom sets coming in v5.0.

**Q: What about Unicode characters?**
A: Fully supported! Just edit the EXTENDED_CHARS in the code.

**Q: Is there a preview feature?**
A: Not yet. Real-time preview is planned for v5.0.

**Q: Will very large images work?**
A: Yes, but may freeze Blender briefly. Reduce width if needed.

---

## 🚀 Getting Started Right Now

### Simplest First Run:
1. Open Image Editor → Load image
2. Go to ASCII Art panel
3. Select image from dropdown
4. Click **Generate ASCII Art**
5. Done! Open the `.txt` file

### Expected Result:
- Recognizable ASCII version of your image
- Should look much better than v3.0
- File is readable in any text editor

### Next Step:
- If too bright/dark, adjust **Contrast**
- If edges look wrong, adjust **Edge Threshold**
- If image is stretched, adjust **Font Ratio**

---

## 📞 Support

For issues:
1. Check **Troubleshooting** section above
2. Review **IMPROVEMENTS.md** for technical details
3. Check Blender system console for error messages (Window → Toggle System Console)

---

**Happy ASCII Art generating! 🎨✨**
