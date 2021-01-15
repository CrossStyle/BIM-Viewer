import ifcopenshell
import math
import ifcopenshell.geom


class fuzzy_dict(object):
    def __init__(self, d, eps=1e-5, guid=None):
        self.d = d
        self.eps = eps
        self.guid = guid
        mod = - int(round(math.log10(eps * 100)))

        def c(v):
            if isinstance(v, float):
                # print "round(%r, %r) = %r" % (v, mod, round(v, mod))
                return round(v, mod)
            elif isinstance(v, dict):
                return tuple(sorted((k, c(v)) for k, v in v.items()))
            elif isinstance(v, (tuple, list)):
                return type(v)(map(c, v))
            else:
                return v
        self.h = hash(c(self.d))

    def __hash__(self):
        return self.h

    def __eq__(self, other):
        def eq(v1, v2):
            if type(v1) != type(v2):
                return False
            if isinstance(v1, float):
                if abs(v1 - v2) > self.eps:
                    return False
            elif isinstance(v1, dict):
                if not (fuzzy_dict(v1, eps=self.eps) == fuzzy_dict(v2, eps=self.eps)):
                    return False
            elif isinstance(v1, (tuple, list)):
                if len(v1) != len(v2):
                    return False
                for a, b in zip(v1, v2):
                    if not eq(a, b):
                        return False
            else:
                if v1 != v2:
                    return False
            return True
        if set(self.d.keys()) != set(other.d.keys()):
            return
        for v1, v2 in ((self.d[k], other.d[k]) for k in self.d):
            if not eq(v1, v2):
                return False
        return True


def info_as_dictionary(e):
    return e.get_info(recursive=True, include_identifier=False, ignore={"GlobalId", "OwnerHistory"})


def to_fuzzy(e):
    return fuzzy_dict(info_as_dictionary(e), guid=e.GlobalId)


class Difference(object):
    def __init__(self, old, new):
        self.old_file = ifcopenshell.open(old)
        self.old_file_guids = set(i.GlobalId for i in self.old_file.by_type("IfcBuildingElement"))
        self.old_file_hashes = set()
        for guid in self.old_file_guids:
            entity = self.old_file[guid]
            immut_dict_old = to_fuzzy(entity)
            self.old_file_hashes.add(immut_dict_old)
        self.new_file = ifcopenshell.open(new)
        self.new_file_guids = set(i.GlobalId for i in self.new_file.by_type("IfcBuildingElement"))
        self.new_file_hashes = set()
        for guid in self.new_file_guids:
            entity = self.new_file[guid]
            immut_dict_new = to_fuzzy(entity)
            self.new_file_hashes.add(immut_dict_new)
        self.added_in_new = set()
        self.unchanged_in_new = set()
        self.deleted_from_old = set()

    def calculate_differences(self):
        for entity_guid in self.new_file_guids:
            entity = self.new_file[entity_guid]
            if to_fuzzy(entity) in self.old_file_hashes:
                self.unchanged_in_new.add(entity_guid)
            else:
                self.added_in_new.add(entity_guid)
        for entity_guid in self.old_file_guids:
            entity = self.old_file[entity_guid]
            if to_fuzzy(entity) not in self.new_file_hashes:
                self.deleted_from_old.add(entity_guid)
        return {'unchanged': self.unchanged_in_new, 'added': self.added_in_new, 'deleted': self.deleted_from_old}


filename1 = "hello_wall.ifc"
filename2 = "hello_wall1.ifc"
difference = Difference(filename1, filename2)  # difference是一个类
differences = difference.calculate_differences()  # differences 是计算后的结果
print("Unchanged: ", len(differences['unchanged']))
print("Added: ", len(differences['added']))
print("Deleted: ", len(differences['deleted']))
present_in_both_files = set(differences['deleted'] & set(differences['added']))

s = ifcopenshell.geom.settings()
s.set(s.USE_PYTHON_OPENCASCADE, True)
viewer = ifcopenshell.geom.utils.initialize_display()

viewer.set_bg_gradient_color([255, 255, 255], [255, 255, 255])

of = set(i for i in difference.old_file_guids)
nf = set(i for i in difference.new_file_guids)
of.update(nf)  # adds elements from a set

for guid in of:
    entity = None

    if guid in differences['added']:
        clr = (0.239, 0.839, 0.372)
        entity = difference.new_file[guid]

    if guid in differences['unchanged']:
        clr = (0.105, 0.196, 1)
        entity = difference.new_file[guid]
        # entity = None

    if guid in differences['deleted']:
        clr = (0.980, 0.419, 0.474)
        entity = difference.old_file[guid]

    if guid in differences['added'] and guid in differences['deleted']:
        clr = (1, 0.4, 0)
        entity = difference.new_file[guid]

    if entity is not None and entity.Representation is not None:
        shape = ifcopenshell.geom.create_shape(s, entity)
        display = ifcopenshell.geom.utils.display_shape(shape, clr=clr)

        if guid in differences['unchanged']:
            ifcopenshell.geom.utils.set_shape_transparency(display, 0.9)

    viewer.FitAll()
ifcopenshell.geom.utils.main_loop()
