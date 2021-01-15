import ifcopenshell
import ifcopenshell.geom
s = ifcopenshell.geom.settings()
s.set(s.USE_PYTHON_OPENCASCADE, True)
viewer = ifcopenshell.geom.utils.initialize_display()
viewer.set_bg_gradient_color([255, 255, 255], [255, 255, 255])
filename1 = "hello_wall1.ifc"
ifc_file = ifcopenshell.open(filename1)
entities = ifc_file.by_type('IfcProduct')
for entity in entities:
    if entity.Representation is not None:
        shape = ifcopenshell.geom.create_shape(s, entity)
        display = ifcopenshell.geom.utils.display_shape(shape)
viewer.FitAll()
ifcopenshell.geom.utils.main_loop()



































