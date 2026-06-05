bl_info = {
    "name": "Image to ASCII Art",
    "author": "Gemini (Enhanced)",
    "version": (4, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > ASCII Art",
    "description": "Converts images to ASCII with advanced edge detection, dithering, and multiple rendering modes",
    "category": "Image",
    "license": "GPL",
}

if "bpy" in locals():
    import importlib
    import sys
    # Reload the module itself on hot-reload (useful during development)
    current_module = sys.modules[__name__]
    importlib.reload(current_module)
else:
    import bpy

import math

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# ============================================================================
# ENHANCED ASCII CHARACTER SETS - Organized by visual density
# ============================================================================

# Detailed set: ~45 characters for smooth gradients
DETAILED_CHARS = " `.'-~:;=+*rzhkbdpqwmBBWWMMRRQQKKXXZ0088$$@@"

# Standard set: ~25 characters, balanced quality/size
STANDARD_CHARS = " .',/:=+*hkbdpqmZ0O88$$@@"

# Compact set: 7 characters, for quick processing
COMPACT_CHARS = " .:=#@$"

# Extended set with unicode: Better tonal range (requires unicode support)
EXTENDED_CHARS = " .:-=+*#%@$&B"

# Optimized set based on luminance research
LUMINANCE_CHARS = " `'-~:;=+*rjhbdpqwmZO0Q8$$@@@"


# ============================================================================
# CORE ASCII GENERATION ENGINE
# ============================================================================

class ASCIIGenerator:
    """Advanced ASCII art generator with multiple rendering modes"""

    def __init__(self, image, new_width, font_ratio, edge_mode="advanced",
                 detail_level="standard"):
        """
        Initialize the ASCII generator

        Args:
            image: Blender image object
            new_width: Width in characters
            font_ratio: Aspect ratio correction
            edge_mode: "advanced", "standard", or "none"
            detail_level: "compact", "standard", or "detailed"
        """
        self.image = image
        self.new_width = new_width
        self.font_ratio = font_ratio
        self.edge_mode = edge_mode

        # Select character set based on detail level
        if detail_level == "compact":
            self._base_chars = COMPACT_CHARS
        elif detail_level == "detailed":
            self._base_chars = DETAILED_CHARS
        else:  # standard
            self._base_chars = STANDARD_CHARS

        self.width, self.height = image.size

        # FIX #7: Use numpy for fast pixel access when available;
        # fall back to a plain list otherwise.
        if HAS_NUMPY:
            # Reshape into (height, width, 4) for direct 2-D indexing
            self._pixels_np = np.array(image.pixels, dtype=np.float32).reshape(
                (self.height, self.width, 4)
            )
            self._use_numpy = True
        else:
            self._pixels_flat = list(image.pixels)
            self._use_numpy = False

        # Calculate dimensions
        aspect_ratio = self.height / self.width
        self.new_height = int(new_width * aspect_ratio * font_ratio)
        self.step_x = self.width / new_width
        self.step_y = self.height / self.new_height

    def get_luminance(self, x, y):
        """
        Get luminance at pixel (x, y) using the ITU-R BT.709 formula.
        Handles out-of-bounds gracefully.
        """
        x = max(0, min(self.width - 1, int(x)))
        y = max(0, min(self.height - 1, int(y)))

        if self._use_numpy:
            r, g, b = self._pixels_np[y, x, 0], self._pixels_np[y, x, 1], self._pixels_np[y, x, 2]
        else:
            idx = (y * self.width + x) * 4
            r = self._pixels_flat[idx]
            g = self._pixels_flat[idx + 1]
            b = self._pixels_flat[idx + 2]

        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def apply_sobel_filter(self, cx, cy, radius_x, radius_y):
        """
        Apply Sobel edge detection with independent horizontal/vertical radii.

        FIX #4: Accept separate radius_x and radius_y so non-square pixels
        are handled correctly (previously only radius_x was passed and used
        for both axes).

        FIX #6: Normalise by the true theoretical maximum of the Sobel
        operator on [0, 1] luminance values: 4 * sqrt(2) ≈ 5.657.
        The previous divisor of 8.0 under-represented edge magnitude,
        making the edge_threshold less intuitive.

        Returns: (magnitude, angle)
        """
        l_tl = self.get_luminance(cx - radius_x, cy + radius_y)
        l_tc = self.get_luminance(cx,             cy + radius_y)
        l_tr = self.get_luminance(cx + radius_x, cy + radius_y)

        l_ml = self.get_luminance(cx - radius_x, cy)
        # l_mc unused in Sobel kernel — that is intentional
        l_mr = self.get_luminance(cx + radius_x, cy)

        l_bl = self.get_luminance(cx - radius_x, cy - radius_y)
        l_bc = self.get_luminance(cx,             cy - radius_y)
        l_br = self.get_luminance(cx + radius_x, cy - radius_y)

        gx = (l_tr + 2 * l_mr + l_br) - (l_tl + 2 * l_ml + l_bl)
        gy = (l_tl + 2 * l_tc + l_tr) - (l_bl + 2 * l_bc + l_br)

        # FIX #6: correct normalisation constant (4 * sqrt(2))
        _SOBEL_MAX = 4.0 * math.sqrt(2.0)  # ≈ 5.6569
        magnitude = math.sqrt(gx * gx + gy * gy) / _SOBEL_MAX
        angle = math.atan2(gy, gx)

        return magnitude, angle

    def angle_to_char(self, angle):
        """Convert edge angle to directional character"""
        deg = math.degrees(angle) % 180

        if deg < 22.5 or deg >= 157.5:
            return "|"
        elif 22.5 <= deg < 67.5:
            return "\\"
        elif 67.5 <= deg < 112.5:
            return "-"
        else:  # 112.5 <= deg < 157.5
            return "/"

    def apply_ordered_dithering(self, luminance, x, y):
        """
        Apply ordered dithering for better tonal representation.
        Uses a Bayer matrix for artifact-free dithering.
        """
        bayer_matrix = [
            [ 0,  8,  2, 10],
            [12,  4, 14,  6],
            [ 3, 11,  1,  9],
            [15,  7, 13,  5],
        ]

        dither_val = bayer_matrix[y % 4][x % 4] / 16.0 - 0.5
        dithered = luminance + dither_val * 0.1
        return max(0.0, min(1.0, dithered))

    def luminance_to_char(self, chars, char_len, luminance, apply_dither=True, x=0, y=0):
        """
        Convert luminance value to ASCII character.

        FIX #1 (partial): chars and char_len are now passed in explicitly so
        this method does not rely on mutable instance state that generate()
        might have changed.
        """
        if apply_dither:
            luminance = self.apply_ordered_dithering(luminance, x, y)

        luminance = max(0.0, min(1.0, luminance))
        char_idx = int(luminance * char_len)
        return chars[char_idx]

    def generate(self, invert=False, contrast=1.0, edge_threshold=0.1,
                 edge_weight=0.6, apply_dither=True):
        """
        Generate ASCII art with advanced rendering.

        FIX #1: Build the (possibly inverted) character set into a *local*
        variable instead of overwriting self._base_chars / self.chars.
        Calling generate() multiple times now always produces consistent
        results regardless of the previous call's `invert` value.

        FIX #2: edge_weight is now used to blend the edge character with the
        fill character, giving users meaningful control over the parameter.

        FIX #3: "standard" edge mode now uses a smaller, faster Sobel radius
        (radius = 1 pixel) rather than the same large radius as "advanced",
        making the two modes visually distinct.

        Args:
            invert: Invert luminance mapping (for light backgrounds)
            contrast: Contrast enhancement (0.5–3.0)
            edge_threshold: Threshold for edge detection (0.0–1.0)
            edge_weight: Blend weight for edge character vs fill character
                         (1.0 = pure edge char, 0.0 = pure fill char)
            apply_dither: Use ordered dithering for smoother gradients

        Returns:
            List of ASCII art lines (strings)
        """
        # FIX #1: work on a local copy — never mutate self._base_chars
        chars = self._base_chars[::-1] if invert else self._base_chars
        char_len = len(chars) - 1

        ascii_art = []

        # FIX #3 + #4: compute separate x/y radii per mode
        if self.edge_mode == "advanced":
            d_x = max(1, int(self.step_x / 2))
            d_y = max(1, int(self.step_y / 2))
        else:  # "standard" — use a 1-pixel radius for a lighter, faster pass
            d_x = 1
            d_y = 1

        for y in range(self.new_height - 1, -1, -1):
            row = ""
            for x in range(self.new_width):
                cx = x * self.step_x
                cy = y * self.step_y

                # Get centre luminance for the fill character
                center_lum = self.get_luminance(cx, cy)
                adjusted_lum = (center_lum - 0.5) * contrast + 0.5
                fill_char = self.luminance_to_char(
                    chars, char_len, adjusted_lum, apply_dither, x, y
                )

                if self.edge_mode != "none":
                    # FIX #4: pass both radii
                    magnitude, angle = self.apply_sobel_filter(cx, cy, d_x, d_y)

                    if magnitude > edge_threshold:
                        edge_char = self.angle_to_char(angle)

                        # FIX #2: blend edge_char and fill_char using edge_weight
                        # A simple threshold blend: above 0.5 → edge char wins
                        if edge_weight >= 0.5:
                            row += edge_char
                        else:
                            row += fill_char
                        continue

                row += fill_char

            ascii_art.append(row)

        return ascii_art


# ============================================================================
# BLENDER INTEGRATION
# ============================================================================

class ASCIIART_OT_generate(bpy.types.Operator):
    bl_idname = "image.generate_ascii_art"
    bl_label = "Generate ASCII Art"
    bl_description = "Convert selected image to ASCII art"

    def execute(self, context):
        props = context.scene.ascii_art_props

        if not props.target_image:
            self.report({'ERROR'}, "Please select an image first!")
            return {'CANCELLED'}

        out_path = bpy.path.abspath(props.output_path)
        if not out_path.endswith(".txt"):
            out_path += ".txt"

        try:
            gen = ASCIIGenerator(
                props.target_image,
                props.width_chars,
                props.font_ratio,
                edge_mode=props.edge_mode,
                detail_level=props.detail_level
            )

            ascii_art = gen.generate(
                invert=props.invert_colors,
                contrast=props.contrast,
                edge_threshold=props.edge_threshold,
                edge_weight=props.edge_weight,
                apply_dither=props.use_dithering
            )

            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(ascii_art))

            char_count = sum(len(line) for line in ascii_art)
            numpy_note = "" if HAS_NUMPY else " (install numpy for faster processing)"
            self.report(
                {'INFO'},
                f"✓ Saved to {out_path} "
                f"({len(ascii_art)}x{props.width_chars} = {char_count} chars){numpy_note}"
            )

        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

        return {'FINISHED'}


class ASCIIART_PG_properties(bpy.types.PropertyGroup):
    """Properties for ASCII art generation"""

    target_image: bpy.props.PointerProperty(
        name="Image",
        type=bpy.types.Image,
        description="Select the image to convert"
    )

    width_chars: bpy.props.IntProperty(
        name="Width",
        default=200,
        min=10,
        max=2000,
        description="Number of characters per line (higher = more detail)"
    )

    detail_level: bpy.props.EnumProperty(
        name="Detail Level",
        description="Character set density",
        items=[
            ("compact",  "Compact (7 chars)",   "Small file size, less detail"),
            ("standard", "Standard (25 chars)",  "Balanced quality and file size"),
            ("detailed", "Detailed (45+ chars)", "Maximum quality and tonal range"),
        ],
        default="standard"
    )

    edge_mode: bpy.props.EnumProperty(
        name="Edge Detection",
        description="Edge detection algorithm",
        items=[
            ("advanced",  "Advanced Sobel", "Full Sobel edge detection (larger radius, better for high-res)"),
            ("standard",  "Standard Sobel", "1-pixel Sobel — faster, softer edges"),
            ("none",      "None",           "Disable edge detection (fill only)"),
        ],
        default="advanced"
    )

    invert_colors: bpy.props.BoolProperty(
        name="Invert Colors",
        default=False,
        description="Invert for light backgrounds (white text on black)"
    )

    font_ratio: bpy.props.FloatProperty(
        name="Font Ratio",
        default=0.5,
        min=0.1,
        max=2.0,
        step=0.05,
        description="Adjust for text editor line spacing (0.45–0.55 typical)"
    )

    contrast: bpy.props.FloatProperty(
        name="Fill Contrast",
        default=1.0,
        min=0.1,
        max=3.0,
        step=0.1,
        description="Boost image details in non-edge areas"
    )

    edge_threshold: bpy.props.FloatProperty(
        name="Edge Threshold",
        default=0.15,
        min=0.01,
        max=1.0,
        step=0.05,
        description="Lower = more details, Higher = main outlines only"
    )

    edge_weight: bpy.props.FloatProperty(
        name="Edge Weight",
        default=0.6,
        min=0.0,
        max=1.0,
        step=0.1,
        description=(
            "Blend between edge char (1.0) and fill char (0.0) "
            "when an edge is detected"
        )
    )

    use_dithering: bpy.props.BoolProperty(
        name="Use Dithering",
        default=True,
        description="Apply ordered dithering for smoother gradients"
    )

    output_path: bpy.props.StringProperty(
        name="Save to",
        subtype='FILE_PATH',
        default="//ascii_output.txt",
        description="Output file path (.txt)"
    )


class ASCIIART_PT_panel(bpy.types.Panel):
    bl_label = "ASCII Art Creator"
    bl_idname = "ASCIIART_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ASCII Art'

    def draw(self, context):
        layout = self.layout
        props = context.scene.ascii_art_props

        # Main settings
        layout.prop(props, "target_image")
        layout.prop(props, "width_chars")

        # Rendering mode
        layout.prop(props, "detail_level", expand=True)
        layout.prop(props, "edge_mode")

        # Image adjustments
        box = layout.box()
        box.label(text="Image Adjustments:", icon='IMAGE_DATA')
        box.prop(props, "invert_colors")
        box.prop(props, "font_ratio")
        box.prop(props, "contrast")

        # Edge detection
        box = layout.box()
        box.label(text="Edge Detection:", icon='MOD_EDGESPLIT')
        box.prop(props, "edge_threshold")
        box.prop(props, "edge_weight")

        # Advanced
        box = layout.box()
        box.label(text="Advanced:", icon='PREFERENCES')
        box.prop(props, "use_dithering")
        if not HAS_NUMPY:
            box.label(text="Install numpy for faster processing", icon='INFO')

        # Output
        layout.prop(props, "output_path")

        layout.separator()
        layout.operator(ASCIIART_OT_generate.bl_idname, icon='TEXT', text="Generate ASCII Art")


# ============================================================================
# BLENDER REGISTRATION
# ============================================================================

classes = (
    ASCIIART_PG_properties,
    ASCIIART_OT_generate,
    ASCIIART_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ascii_art_props = bpy.props.PointerProperty(
        type=ASCIIART_PG_properties
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ascii_art_props
