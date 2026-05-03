bl_info = {
    "name": "Image to ASCII Art",
    "author": "Gemini",
    "version": (3, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > ASCII Art",
    "description": "Converts an image to ASCII using Sobel Edge Detection and Luminance",
    "category": "Image",
    "license": "GPL",
}

if "bpy" in locals():
    import importlib
else:
    import bpy

import math

# Character set for fills
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft1{}[]?_+~<>i!lI;:,\"^`'. "

def generate_ascii(image, output_path, new_width, invert, font_ratio, contrast, edge_thresh):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * font_ratio)
    
    pixels = list(image.pixels)
    chars = ASCII_CHARS[::-1] if invert else ASCII_CHARS
    char_len = len(chars) - 1
    
    step_x = width / new_width
    step_y = height / new_height
    d_x = max(1, int(step_x / 2))
    d_y = max(1, int(step_y / 2))
    
    ascii_art = []
    
    def get_lum(px, py):
        px = max(0, min(width - 1, px))
        py = max(0, min(height - 1, py))
        idx = (py * width + px) * 4
        return 0.2126 * pixels[idx] + 0.7152 * pixels[idx + 1] + 0.0722 * pixels[idx + 2]

    for y in range(new_height - 1, -1, -1):
        row = ""
        for x in range(new_width):
            cx = int(x * step_x)
            cy = int(y * step_y)
            
            l_tl = get_lum(cx - d_x, cy + d_y)
            l_tc = get_lum(cx,       cy + d_y)
            l_tr = get_lum(cx + d_x, cy + d_y)
            l_ml = get_lum(cx - d_x, cy)
            l_mc = get_lum(cx,       cy)
            l_mr = get_lum(cx + d_x, cy)
            l_bl = get_lum(cx - d_x, cy - d_y)
            l_bc = get_lum(cx,       cy - d_y)
            l_br = get_lum(cx + d_x, cy - d_y)
            
            # Sobel Filter
            gx = (l_tr + 2*l_mr + l_br) - (l_tl + 2*l_ml + l_bl)
            gy = (l_tl + 2*l_tc + l_tr) - (l_bl + 2*l_bc + l_br)
            
            magnitude = math.sqrt(gx*gx + gy*gy)
            
            if magnitude > edge_thresh:
                deg = math.degrees(math.atan2(gy, gx)) % 180
                
                if deg < 22.5 or deg >= 157.5:
                    row += "|"
                elif 22.5 <= deg < 67.5:
                    row += "\\"
                elif 67.5 <= deg < 112.5:
                    row += "-"
                else:
                    row += "/"
            else:
                lum = (l_mc - 0.5) * contrast + 0.5
                lum = max(0.0, min(1.0, lum))
                char_idx = int(lum * char_len)
                row += chars[char_idx]
                
        ascii_art.append(row)
        
    with open(output_path, "w") as f:
        f.write("\n".join(ascii_art))


class ASCIIART_OT_generate(bpy.types.Operator):
    bl_idname = "image.generate_ascii_art"
    bl_label = "Generate ASCII Art"
    
    def execute(self, context):
        props = context.scene.ascii_art_props
        
        if not props.target_image:
            self.report({'ERROR'}, "Please select an image first!")
            return {'CANCELLED'}
            
        out_path = bpy.path.abspath(props.output_path)
        if not out_path.endswith(".txt"):
            out_path += ".txt"
            
        try:
            generate_ascii(
                props.target_image, 
                out_path, 
                props.width_chars, 
                props.invert_colors,
                props.font_ratio,
                props.contrast,
                props.edge_threshold
            )
            self.report({'INFO'}, f"Successfully saved to {out_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}


class ASCIIART_PG_properties(bpy.types.PropertyGroup):
    target_image: bpy.props.PointerProperty(
        name="Image", type=bpy.types.Image
    )
    width_chars: bpy.props.IntProperty(
        name="Width", default=200, min=10, max=1000,
        description="Number of characters per line"
    )
    invert_colors: bpy.props.BoolProperty(
        name="Invert Colors", default=False,
        description="Check this if viewing the text on a light background"
    )
    font_ratio: bpy.props.FloatProperty(
        name="Font Ratio", default=0.5, min=0.1, max=2.0,
        description="Adjust to compensate for text editor line height"
    )
    contrast: bpy.props.FloatProperty(
        name="Fill Contrast", default=1.0, min=0.1, max=3.0,
        description="Boosts image details for the fill characters"
    )
    edge_threshold: bpy.props.FloatProperty(
        name="Edge Threshold", default=0.3, min=0.01, max=1.0,
        description="Lower values detect subtle lines; higher values focus on main outlines"
    )
    output_path: bpy.props.StringProperty(
        name="Save to", subtype='FILE_PATH', default="//ascii_output.txt"
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
        
        layout.prop(props, "target_image")
        layout.prop(props, "width_chars")
        
        box = layout.box()
        box.label(text="Image Adjustments:")
        box.prop(props, "invert_colors")
        box.prop(props, "font_ratio")
        box.prop(props, "contrast")
        
        box = layout.box()
        box.label(text="Edge Adjustments:")
        box.prop(props, "edge_threshold")
        
        layout.prop(props, "output_path")
        layout.separator()
        layout.operator(ASCIIART_OT_generate.bl_idname, icon='TEXT')


classes = (
    ASCIIART_PG_properties, 
    ASCIIART_OT_generate, 
    ASCIIART_PT_panel
)

def register():
    for cls in classes: 
        bpy.utils.register_class(cls)
    bpy.types.Scene.ascii_art_props = bpy.props.PointerProperty(type=ASCIIART_PG_properties)

def unregister():
    for cls in reversed(classes): 
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ascii_art_props