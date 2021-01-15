import json
import ifcopenshell
import ifcopenshell.geom

with open("output.json", 'r') as f:
     load_dict = json.load(f)

clash_guids = load_dict[0]['clashes'].keys()
set_clash_guids = set(i for i in clash_guids)
filename1 = "1.ifc"
ifc_file = ifcopenshell.open(filename1)

final_id = set()
for id in set_clash_guids:
    a, b = id.split('-')
    final_id.add(a)
    final_id.add(b)

a = ifc_file[final_id.pop()]

s = ifcopenshell.geom.settings()
s.set(s.USE_PYTHON_OPENCASCADE, True)
viewer = ifcopenshell.geom.utils.initialize_display()
viewer.set_bg_gradient_color([255, 255, 255], [255, 255, 255])

all_guids = set(i.GlobalId for i in ifc_file.by_type("IfcProduct"))

for id in all_guids:
    entity = ifc_file[id]
    if id in final_id:
        clr = (1, 0, 0)
    else:
        clr = (0.105, 0.196, 1)
    if entity is not None and entity.Representation is not None:
        shape = ifcopenshell.geom.create_shape(s, entity)
        display = ifcopenshell.geom.utils.display_shape(shape, clr=clr)

        if id not in final_id:
            ifcopenshell.geom.utils.set_shape_transparency(display, 0.9)

viewer.FitAll()
ifcopenshell.geom.utils.main_loop()
