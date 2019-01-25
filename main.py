#   Pour le plugin c++ :
#   Open MayaAnim.lib
#   MFnIKJoint / MFnAnimeCurve

# Capteurs :
# roll = rotation autour de l'axe des X ?
# pitch = rotation autour de l'axe des Y ?
# yaw = rotation autour de l'axe des Z ?


import maya.cmds as cm
from operator import add

def create_joints(obj):
    if obj.name:
        current_obj = obj
        print(current_obj.name)
        print(current_obj.offset)
        cmds.joint(p=(float(current_obj.offset[0]), float(current_obj.offset[1]), float(current_obj.offset[2])))

        for child in current_obj.children:
            if child:
                create_joints(child)


def read_clean_line():
    return f.readline().replace("\t", "").replace("\n", "").split(" ")


class SolidObject:

    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.offset = []
        self.world_offset = []
        self.n_channels = 0
        self.channels = []
        self.children = []
        self.parent = None

    def to_string(self):
        if self.name:
            print(self.name + " : ")
            if self.offset : print(self.world_offset)
            for child in self.children:
                if child:
                    child.to_string()


def read_bvh():
    root = SolidObject(type="root", name=None)
    current_object = root
    while True:
        line = read_clean_line()
        if line[0] == 'HIERARCHY':
            print("reading object hierarchy")
        if line[0] == 'ROOT':
            root.name = line[1]
        if line[0] == 'OFFSET':
            current_object.offset = [float(line[1]), float(line[2]), float(line[3])]
            if current_object.parent:
                current_object.world_offset = list( map(add, current_object.parent.world_offset, current_object.offset))
            else:
                current_object.world_offset = current_object.offset
        if line[0] == 'CHANNELS':
            current_object.n_channels = int(line[1])
            current_object.channels = line[2:current_object.n_channels + 2]
        if line[0] == 'JOINT':
            new_object = SolidObject(type="join", name=line[1])
            new_object.parent = current_object
            current_object.children.append(new_object)
            current_object = new_object
        if line[0] == 'End':
            new_object = SolidObject(type="End", name=None)
            current_object.children.append(new_object)
            read_clean_line()
            line = read_clean_line()
            current_object.offset = line[1:4]
            read_clean_line()
        if line[0] == '}':
            current_object = current_object.parent
        if line[0] == '':
            break
    return root


f = open("D:/documents/python projects/animation/run.bvh", "r")
root = read_bvh()
root.to_string()
create_joints(root)