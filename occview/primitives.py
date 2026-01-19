"""
Primitive shape creation and transformation utilities
Factory functions for common CAD primitives
"""
from OCC.Core.BRepPrimAPI import (BRepPrimAPI_MakeBox,
                                   BRepPrimAPI_MakeSphere,
                                   BRepPrimAPI_MakeCylinder)
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp_Vec


def make_box(dx=80, dy=50, dz=30):
    """
    Create a rectangular box

    Args:
        dx: Width (X dimension) in mm
        dy: Depth (Y dimension) in mm
        dz: Height (Z dimension) in mm

    Returns:
        TopoDS_Shape: The box shape
    """
    box_maker = BRepPrimAPI_MakeBox(dx, dy, dz)
    return box_maker.Shape()


def make_sphere(r=25):
    """
    Create a sphere

    Args:
        r: Radius in mm

    Returns:
        TopoDS_Shape: The sphere shape
    """
    sphere_maker = BRepPrimAPI_MakeSphere(r)
    return sphere_maker.Shape()


def make_cylinder(r=15, h=60):
    """
    Create a cylinder

    Args:
        r: Radius in mm
        h: Height in mm

    Returns:
        TopoDS_Shape: The cylinder shape
    """
    cylinder_maker = BRepPrimAPI_MakeCylinder(r, h)
    return cylinder_maker.Shape()


def translate_shape(shape, x=0, y=0, z=0):
    """
    Translate a shape by the given offset

    Args:
        shape: TopoDS_Shape to translate
        x: X offset in mm
        y: Y offset in mm
        z: Z offset in mm

    Returns:
        TopoDS_Shape: The translated shape
    """
    # Create transformation
    transformation = gp_Trsf()

    # Set translation vector
    translation_vector = gp_Vec(x, y, z)
    transformation.SetTranslation(translation_vector)

    # Apply transformation
    transform_builder = BRepBuilderAPI_Transform(shape, transformation, False)

    return transform_builder.Shape()
