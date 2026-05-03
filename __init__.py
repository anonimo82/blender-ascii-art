bl_info = {
    "name": "Image to ASCII Art",
    "author": "Gemini",
    "version": (2, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > ASCII Art",
    "description": "Converte un'immagine caricata in testo ASCII con opzioni avanzate",
    "category": "Image",
}

# Gestione del reload per add-on multi-file (Best Practice)
if "bpy" in locals():
    import importlib
    # Se in futuro aggiungerai altri file, inserisci qui il reload, es:
    # importlib.reload(operators)
    # importlib.reload(ui)
else:
    import bpy

import math

# Set di caratteri molto più dettagliato (70 livelli di grigio)
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def generate_ascii(image, output_path, new_width, invert, font_ratio, contrast):
    width, height = image.size
    
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * font_ratio)
    
    pixels = list(image.pixels)
    
    chars = ASCII_CHARS[::-1] if invert else ASCII_CHARS
    char_len = len(chars) - 1
    
    ascii_art = []
    
    for y in range(new_height - 1, -1, -1):
        row = ""
        for x in range(new_width):
            orig_x = int(x * width / new_width)
            orig_y = int(y * height / new_height)
            
            idx = (orig_y * width + orig_x) * 4
            r = pixels[idx]
            g = pixels[idx + 1]
            b = pixels[idx + 2]
            
            luminance = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
            
            luminance = (luminance - 0.5) * contrast + 0.5
            luminance = max(0.0, min(1.0, luminance))
            
            char_idx = int(luminance * char_len)
            row += chars[char_idx]
            
        ascii_art.append(row)
        
    with open(output_path, "w") as f:
        f.write("\n".join(ascii_art))


class ASCIIART_OT_generate(bpy.types.Operator):
    bl_idname = "image.generate_ascii_art"
    bl_label = "Genera ASCII Art"
    
    def execute(self, context):
        props = context.scene.ascii_art_props
        
        if not props.target_image:
            self.report({'ERROR'}, "Seleziona un'immagine!")
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
                props.contrast
            )
            self.report({'INFO'}, f"Salvato in {out_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Errore: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}


class ASCIIART_PG_properties(bpy.types.PropertyGroup):
    target_image: bpy.props.PointerProperty(
        name="Immagine", type=bpy.types.Image
    )
    width_chars: bpy.props.IntProperty(
        name="Larghezza", default=150, min=10, max=1000
    )
    invert_colors: bpy.props.BoolProperty(
        name="Inverti Colori (Sfondo Bianco)", default=False,
        description="Utile se visualizzi il testo su sfondo bianco"
    )
    font_ratio: bpy.props.FloatProperty(
        name="Proporzione Font", default=0.5, min=0.1, max=2.0,
        description="Regola per schiacciare o allungare l'immagine"
    )
    contrast: bpy.props.FloatProperty(
        name="Contrasto", default=1.0, min=0.1, max=3.0,
        description="Aumenta per separare meglio chiari e scuri"
    )
    output_path: bpy.props.StringProperty(
        name="Salva in", subtype='FILE_PATH', default="//ascii_output.txt"
    )


class ASCIIART_PT_panel(bpy.types.Panel):
    bl_label = "Creatore ASCII Art"
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
        box.label(text="Regolazioni:")
        box.prop(props, "invert_colors")
        box.prop(props, "font_ratio")
        box.prop(props, "contrast")
        
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

# Rimosso il blocco if __name__ == "__main__": perché 
# in un modulo __init__.py non viene eseguito direttamente.