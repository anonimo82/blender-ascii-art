bl_info = {
    "name": "Image to ASCII Art",
    "author": "Gemini",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar (N) > ASCII Art",
    "description": "Converte un'immagine caricata in Blender in un file di testo ASCII",
    "category": "Image",
}

import bpy
import os

# Set di caratteri dal più scuro al più chiaro
# Puoi modificarli per ottenere effetti diversi!
ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

def generate_ascii(image, output_path, new_width):
    width, height = image.size
    
    # I caratteri in un editor di testo sono solitamente alti circa il doppio di quanto sono larghi.
    # Moltiplichiamo per 0.5 per correggere le proporzioni dell'immagine finale.
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.5)
    
    # Blender memorizza i pixel come un singolo array piatto [R, G, B, A, R, G, B, A...]
    # Trasformarlo in una tupla o lista è molto più veloce per la lettura rispetto ad accedere a image.pixels direttamente nel loop
    pixels = list(image.pixels)
    
    ascii_art = []
    
    # In Blender, l'origine (0,0) delle immagini è in basso a sinistra.
    # I file di testo si leggono dall'alto verso il basso, quindi invertiamo il ciclo Y.
    for y in range(new_height - 1, -1, -1):
        row = ""
        for x in range(new_width):
            # Troviamo il pixel originale corrispondente (Nearest Neighbor)
            orig_x = int(x * width / new_width)
            orig_y = int(y * height / new_height)
            
            # Indice nell'array piatto
            idx = (orig_y * width + orig_x) * 4
            
            # Estraiamo RGB
            r = pixels[idx]
            g = pixels[idx + 1]
            b = pixels[idx + 2]
            
            # Calcoliamo la luminosità (formula standard per la percezione umana)
            luminance = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
            
            # Mappiamo la luminosità (da 0.0 a 1.0) all'indice del nostro array di caratteri
            char_idx = int(luminance * (len(ASCII_CHARS) - 1))
            row += ASCII_CHARS[char_idx]
            
        ascii_art.append(row)
        
    # Salviamo su file
    with open(output_path, "w") as f:
        f.write("\n".join(ascii_art))


class ASCIIART_OT_generate(bpy.types.Operator):
    """Genera l'ASCII Art dall'immagine selezionata"""
    bl_idname = "image.generate_ascii_art"
    bl_label = "Genera ASCII Art"
    
    def execute(self, context):
        props = context.scene.ascii_art_props
        
        if not props.target_image:
            self.report({'ERROR'}, "Seleziona un'immagine prima di procedere!")
            return {'CANCELLED'}
            
        if not props.output_path:
            self.report({'ERROR'}, "Scegli un percorso di salvataggio!")
            return {'CANCELLED'}
            
        # Assicuriamoci che il percorso finisca in .txt
        out_path = bpy.path.abspath(props.output_path)
        if not out_path.endswith(".txt"):
            out_path += ".txt"
            
        try:
            generate_ascii(props.target_image, out_path, props.width_chars)
            self.report({'INFO'}, f"File salvato con successo in {out_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Errore: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}


class ASCIIART_PG_properties(bpy.types.PropertyGroup):
    target_image: bpy.props.PointerProperty(
        name="Immagine",
        type=bpy.types.Image,
        description="L'immagine da convertire"
    )
    width_chars: bpy.props.IntProperty(
        name="Larghezza (Caratteri)",
        default=100,
        min=10,
        max=500,
        description="Quanti caratteri sarà larga la riga di testo"
    )
    output_path: bpy.props.StringProperty(
        name="Salva in",
        subtype='FILE_PATH',
        default="//ascii_output.txt",
        description="Dove salvare il file .txt"
    )


class ASCIIART_PT_panel(bpy.types.Panel):
    """Pannello nella UI di Blender"""
    bl_label = "Creatore ASCII Art"
    bl_idname = "ASCIIART_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'ASCII Art'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.ascii_art_props
        
        layout.prop(props, "target_image")
        layout.prop(props, "width_chars")
        layout.prop(props, "output_path")
        
        layout.separator()
        layout.operator(ASCIIART_OT_generate.bl_idname, icon='TEXT')


# Registrazione delle classi
classes = (
    ASCIIART_PG_properties,
    ASCIIART_OT_generate,
    ASCIIART_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ascii_art_props = bpy.props.PointerProperty(type=ASCIIART_PG_properties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ascii_art_props

if __name__ == "__main__":
    register()