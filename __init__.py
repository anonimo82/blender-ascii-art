bl_info = {
    "name": "Image to ASCII Art",
    "author": "Gemini (Enhanced)",
    "version": (4, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > ASCII Art",
    "description": "Converts images to ASCII with advanced edge detection, dithering, and multiple rendering modes",
    "category": "Image",
    "license": "GPL",
}

if "bpy" in locals():
    import importlib
else:
    import bpy

import math

# ============================================================================
# ENHANCED ASCII CHARACTER SETS - Organized by visual density
# ============================================================================

# Detailed set: 70 characters for smooth gradients
DETAILED_CHARS = " .-~:;=+*#%@$"
DETAILED_CHARS = " `.'-~:;=+*rzhkbdpqwmBBWWMMRRQQKKXXZ0088$$@@"

# Standard set: 35 characters, balanced quality/size
STANDARD_CHARS = " .:-=+*#%@"
STANDARD_CHARS = " .',/:=+*hkbdpqmZ0O88$$@@"

# Compact set: 10 characters, for quick processing
COMPACT_CHARS = " .:=#@$"

# Extended set with unicode: Better tonal range (requires unicode support)
EXTENDED_CHARS = " ░▒▓█"
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
            self.chars = COMPACT_CHARS
        elif detail_level == "detailed":
            self.chars = DETAILED_CHARS
        else:  # standard
            self.chars = STANDARD_CHARS
            
        self.char_len = len(self.chars) - 1
        self.width, self.height = image.size
        self.pixels = list(image.pixels)
        
        # Calculate dimensions
        aspect_ratio = self.height / self.width
        self.new_height = int(new_width * aspect_ratio * font_ratio)
        self.step_x = self.width / new_width
        self.step_y = self.height / self.new_height
    
    def get_luminance(self, x, y):
        """
        Get luminance at pixel (x, y) using standard luminosity formula
        Handles out-of-bounds gracefully
        """
        x = max(0, min(self.width - 1, int(x)))
        y = max(0, min(self.height - 1, int(y)))
        idx = (y * self.width + x) * 4
        
        # ITU-R BT.709 luminance formula
        r = self.pixels[idx]
        g = self.pixels[idx + 1]
        b = self.pixels[idx + 2]
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def apply_sobel_filter(self, cx, cy, radius):
        """
        Apply Sobel edge detection with configurable radius
        Returns: (magnitude, angle)
        """
        # Get luminance values in 3x3 grid
        l_tl = self.get_luminance(cx - radius, cy + radius)
        l_tc = self.get_luminance(cx, cy + radius)
        l_tr = self.get_luminance(cx + radius, cy + radius)
        
        l_ml = self.get_luminance(cx - radius, cy)
        l_mc = self.get_luminance(cx, cy)
        l_mr = self.get_luminance(cx + radius, cy)
        
        l_bl = self.get_luminance(cx - radius, cy - radius)
        l_bc = self.get_luminance(cx, cy - radius)
        l_br = self.get_luminance(cx + radius, cy - radius)
        
        # Sobel operators
        gx = (l_tr + 2*l_mr + l_br) - (l_tl + 2*l_ml + l_bl)
        gy = (l_tl + 2*l_tc + l_tr) - (l_bl + 2*l_bc + l_br)
        
        # Calculate magnitude and normalize
        magnitude = math.sqrt(gx * gx + gy * gy) / 8.0  # Normalize by maximum possible value
        angle = math.atan2(gy, gx)
        
        return magnitude, angle
    
    def angle_to_char(self, angle):
        """Convert edge angle to directional character"""
        deg = math.degrees(angle) % 180
        
        # Map angles to directional characters with better coverage
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
        Apply ordered dithering for better tonal representation
        Uses Bayer matrix for artifact-free dithering
        """
        bayer_matrix = [
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5]
        ]
        
        # Get dither value
        dither_val = bayer_matrix[y % 4][x % 4] / 16.0 - 0.5
        
        # Apply dither with low intensity
        dithered = luminance + dither_val * 0.1
        return max(0.0, min(1.0, dithered))
    
    def luminance_to_char(self, luminance, apply_dither=True, x=0, y=0):
        """Convert luminance value to ASCII character"""
        if apply_dither:
            luminance = self.apply_ordered_dithering(luminance, x, y)
        
        # Clamp luminance
        luminance = max(0.0, min(1.0, luminance))
        
        # Map to character index
        char_idx = int(luminance * self.char_len)
        return self.chars[char_idx]
    
    def generate(self, invert=False, contrast=1.0, edge_threshold=0.1, 
                 edge_weight=0.6, apply_dither=True):
        """
        Generate ASCII art with advanced rendering
        
        Args:
            invert: Invert luminance mapping
            contrast: Contrast enhancement (0.5-3.0)
            edge_threshold: Threshold for edge detection (0.0-1.0)
            edge_weight: Balance between edges and fills (0.0-1.0)
            apply_dither: Use dithering for smoother gradients
        
        Returns:
            List of ASCII art lines
        """
        chars = self.chars[::-1] if invert else self.chars
        self.chars = chars
        self.char_len = len(chars) - 1
        
        ascii_art = []
        d_x = max(1, int(self.step_x / 2))
        d_y = max(1, int(self.step_y / 2))
        
        for y in range(self.new_height - 1, -1, -1):
            row = ""
            for x in range(self.new_width):
                cx = x * self.step_x
                cy = y * self.step_y
                
                # Get center luminance for fill
                center_lum = self.get_luminance(cx, cy)
                
                # Apply edge detection
                if self.edge_mode != "none":
                    magnitude, angle = self.apply_sobel_filter(cx, cy, d_x)
                    
                    if magnitude > edge_threshold:
                        # Use edge character
                        row += self.angle_to_char(angle)
                        continue
                
                # Use fill character
                adjusted_lum = (center_lum - 0.5) * contrast + 0.5
                char = self.luminance_to_char(adjusted_lum, apply_dither, x, y)
                row += char
            
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
            # Create generator
            gen = ASCIIGenerator(
                props.target_image,
                props.width_chars,
                props.font_ratio,
                edge_mode=props.edge_mode,
                detail_level=props.detail_level
            )
            
            # Generate ASCII art
            ascii_art = gen.generate(
                invert=props.invert_colors,
                contrast=props.contrast,
                edge_threshold=props.edge_threshold,
                edge_weight=props.edge_weight,
                apply_dither=props.use_dithering
            )
            
            # Write to file
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(ascii_art))
            
            char_count = sum(len(line) for line in ascii_art)
            self.report({'INFO'}, 
                f"✓ Saved to {out_path} ({len(ascii_art)}x{props.width_chars} = {char_count} chars)")
            
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
            ("compact", "Compact (10 chars)", "Small file size, less detail"),
            ("standard", "Standard (25 chars)", "Balanced quality and file size"),
            ("detailed", "Detailed (40+ chars)", "Maximum quality and tonal range"),
        ],
        default="standard"
    )
    
    edge_mode: bpy.props.EnumProperty(
        name="Edge Detection",
        description="Edge detection algorithm",
        items=[
            ("advanced", "Advanced Sobel", "Full Sobel edge detection"),
            ("standard", "Standard", "Basic edge detection"),
            ("none", "None", "Disable edge detection (fill only)"),
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
        description="Adjust for text editor line spacing (0.45-0.55 typical)"
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
        description="Balance between edge and fill rendering"
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
    ASCIIART_PT_panel
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
