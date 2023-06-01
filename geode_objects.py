import opengeode as og
import opengeode_io as og_io
import opengeode_geosciences as og_gs
import opengeode_geosciencesio as og_gs_io

def objects_list():
    return {
        'BRep': {
            'input': [ og.BRepInputFactory ],
            'output': [ og.BRepOutputFactory ],
            'load': og.load_brep,
            'save': og.save_brep,
            'builder': og.BRepBuilder,
            'crs': {
                'assign': og_gs.assign_brep_geographic_coordinate_system_info,
                'convert': og_gs.convert_brep_coordinate_reference_system
            },
            'is_model': True,
            'is_3D': True
        },
        'CrossSection': {
            'input': [ og_gs.CrossSectionInputFactory ],
            'output': [ og.SectionOutputFactory, og_gs.CrossSectionOutputFactory ],
            'load': og_gs.load_cross_section,
            'save': og_gs.save_cross_section,
            'builder': og_gs.CrossSectionBuilder,
            'crs': {
                'assign': og_gs.assign_section_geographic_coordinate_system_info,
                'convert': og_gs.convert_section_coordinate_reference_system
            },
            'is_model': True,
            'is_3D': False
        },
        'EdgedCurve2D': {
            'input': [ og.EdgedCurveInputFactory2D ],
            'output': [ og.EdgedCurveOutputFactory2D ],
            'load': og.load_edged_curve2D,
            'save': og.save_edged_curve2D,
            'builder': og.EdgedCurveBuilder2D.create,
            'crs': {
                'assign': og_gs.assign_edged_curve_geographic_coordinate_system_info2D,
                'convert': og_gs.convert_edged_curve_coordinate_reference_system2D
            },
            'is_model': False,
            'is_3D': False
        },
        'EdgedCurve3D': {
            'input': [ og.EdgedCurveInputFactory3D ],
            'output': [ og.EdgedCurveOutputFactory3D ],
            'load': og.load_edged_curve3D,
            'save': og.save_edged_curve3D,
            'builder': og.EdgedCurveBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_edged_curve_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_edged_curve_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'Graph': {
            'input': [ og.GraphInputFactory ],
            'output': [ og.GraphOutputFactory ],
            'load': og.load_graph,
            'save': og.save_graph,
            'builder': og.GraphBuilder.create,
            'is_model': False,
            'is_3D': False
        },
        'HybridSolid3D': {
            'input': [ og.HybridSolidInputFactory3D ],
            'output': [ og.HybridSolidOutputFactory3D ],
            'load': og.load_hybrid_solid3D,
            'save': og.save_hybrid_solid3D,
            'builder': og.HybridSolidBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_solid_mesh_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_solid_mesh_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'PointSet2D': {
            'input': [ og.PointSetInputFactory2D ],
            'output': [ og.PointSetOutputFactory2D ],
            'load': og.load_point_set2D,
            'save': og.save_point_set2D,
            'builder': og.PointSetBuilder2D.create,
            'crs': {
                'assign': og_gs.assign_point_set_geographic_coordinate_system_info2D,
                'convert': og_gs.convert_point_set_coordinate_reference_system2D
            },
            'is_model': False,
            'is_3D': False
        },
        'PointSet3D': {
            'input': [ og.PointSetInputFactory3D ],
            'output': [ og.PointSetOutputFactory3D ],
            'loaDd': og.load_point_set3D,
            'save': og.save_point_set3D,
            'builder': og.PointSetBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_point_set_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_point_set_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'PolygonalSurface2D': {
            'input': [ og.PolygonalSurfaceInputFactory2D ],
            'output': [ og.PolygonalSurfaceOutputFactory2D ],
            'load': og.load_polygonal_surface2D,
            'save': og.save_polygonal_surface2D,
            'builder': og.PolygonalSurfaceBuilder2D.create,
            'crs': {
                'assign': og_gs.assign_surface_mesh_geographic_coordinate_system_info2D,
                'convert': og_gs.convert_surface_mesh_coordinate_reference_system2D
            },
            'is_model': False,
            'is_3D': False
        },
        'PolygonalSurface3D': {
            'input': [ og.PolygonalSurfaceInputFactory3D ],
            'output': [ og.PolygonalSurfaceOutputFactory3D ],
            'load': og.load_polygonal_surface3D,
            'save': og.save_polygonal_surface3D,
            'builder': og.PolygonalSurfaceBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_surface_mesh_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_surface_mesh_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'PolyhedralSolid3D': {
            'input': [ og.PolyhedralSolidInputFactory3D ],
            'output': [ og.PolyhedralSolidOutputFactory3D ],
            'load': og.load_polyhedral_solid3D,
            'save': og.save_polyhedral_solid3D,
            'builder': og.PolyhedralSolidBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_solid_mesh_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_solid_mesh_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'RegularGrid2D': {
            'input': [ og.RegularGridInputFactory2D ],
            'output': [ og.RegularGridOutputFactory2D ],
            'load': og.load_regular_grid2D,
            'save': og.save_regular_grid2D,
            'builder': og.RegularGridBuilder2D.create,
            'crs': {
                'assign': og_gs.assign_surface_mesh_geographic_coordinate_system_info2D,
                'convert': og_gs.convert_surface_mesh_coordinate_reference_system2D
            },
            'is_model': False,
            'is_3D': False
        },
        'RegularGrid3D': {
            'input': [ og.RegularGridInputFactory3D ],
            'output': [ og.RegularGridOutputFactory3D ],
            'load': og.load_regular_grid3D,
            'save': og.save_regular_grid3D,
            'builder': og.RegularGridBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_solid_mesh_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_solid_mesh_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'Section': {
            'input': [ og.SectionInputFactory ],
            'output': [ og.SectionOutputFactory ],
            'load': og.load_section,
            'save': og.save_section,
            'builder': og.SectionBuilder,
            'crs': {
                'assign': og_gs.assign_section_geographic_coordinate_system_info,
                'convert': og_gs.convert_section_coordinate_reference_system
            },
            'is_model': True,
            'is_3D': False
        },
        'StructuralModel': {
            'input': [ og_gs.StructuralModelInputFactory ],
            'output': [ og.BRepOutputFactory, og_gs.StructuralModelOutputFactory ],
            'load': og_gs.load_structural_model,
            'save': og_gs.save_structural_model,
            'builder': og_gs.StructuralModelBuilder,
            'crs': {
                'assign': og_gs.assign_brep_geographic_coordinate_system_info,
                'convert': og_gs.convert_brep_coordinate_reference_system
            },
            'is_model': True,
            'is_3D': True
        },
        'TetrahedralSolid3D': {
            'input': [ og.TetrahedralSolidInputFactory3D ],
            'output': [ og.TetrahedralSolidOutputFactory3D ],
            'load': og.load_tetrahedral_solid3D,
            'save': og.save_tetrahedral_solid3D,
            'builder': og.TetrahedralSolidBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_solid_mesh_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_solid_mesh_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'TriangulatedSurface2D': {
            'input': [ og.TriangulatedSurfaceInputFactory2D ],
            'output': [ og.TriangulatedSurfaceOutputFactory2D ],
            'load': og.load_triangulated_surface2D,
            'save': og.save_triangulated_surface2D,
            'builder': og.TriangulatedSurfaceBuilder2D.create,
            'crs': {
                'assign': og_gs.assign_surface_mesh_geographic_coordinate_system_info2D,
                'convert': og_gs.convert_surface_mesh_coordinate_reference_system2D
            },
            'is_model': False,
            'is_3D': False
        },
        'TriangulatedSurface3D': {
            'input': [ og.TriangulatedSurfaceInputFactory3D ],
            'output': [ og.TriangulatedSurfaceOutputFactory3D ],
            'load': og.load_triangulated_surface3D,
            'save': og.save_triangulated_surface3D,
            'builder': og.TriangulatedSurfaceBuilder3D.create,
            'crs': {
                'assign': og_gs.assign_surface_mesh_geographic_coordinate_system_info3D,
                'convert': og_gs.convert_surface_mesh_coordinate_reference_system3D
            },
            'is_model': False,
            'is_3D': True
        },
        'VertexSet': {
            'input': [ og.VertexSetInputFactory ],
            'output': [ og.VertexSetOutputFactory ],
            'load': og.load_vertex_set,
            'save': og.save_vertex_set,
            'builder': og.VertexSetBuilder.create,
            'is_model': True,
            'is_3D': False
        }
    }

def is_model(geode_object):
    return objects_list()[geode_object]['is_model']

def is_3D(geode_object):
    return objects_list()[geode_object]['is_3D']

def get_builder(geode_object):
    return objects_list()[geode_object]['builder']

def get_geographic_coordinate_systems(geode_object):
    if is_3D(geode_object):
        return og_gs.GeographicCoordinateSystem3D.geographic_coordinate_systems()
    else:
        return og_gs.GeographicCoordinateSystem2D.geographic_coordinate_systems()


def asign_geographic_coordinate_system_info(data, builder, crs_name, input_crs):
    og_gs.assign_brep_geographic_coordinate_system_info(data, builder, crs_name, input_crs)

def convert_geographic_coordinate_system_info():
    og_gs.convert_brep_coordinate_reference_system()
    return a


def convert_to_coordinate_system(data, geode_object, input_crs, output_crs):
    
    if is_model(geode_object):
        for corner in data.corners():
            convert_mesh_coordinate_system(corner.mesh(), geode_object, input_crs, output_crs)
        for line in data.lines():
            convert_mesh_coordinate_system(line.mesh(), geode_object, input_crs, output_crs)
        for surface in data.surfaces():
            convert_mesh_coordinate_system(surface.mesh(), geode_object, input_crs, output_crs)
        if is_3D(geode_object):
            for block in data.blocks():
                convert_mesh_coordinate_system(block.mesh(), geode_object, input_crs, output_crs)
    else:
        convert_mesh_coordinate_system(data, geode_object, input_crs, output_crs)
    return data

def convert_mesh_coordinate_system(mesh, geode_object, input_crs, output_crs):
    print(f'{input_crs=}')
    print(f'{output_crs=}')
    manager = mesh.vertex_attribute_manager()

    if is_3D(geode_object):
        input_graphic_coodinates_system_info = og_gs.GeographicCoordinateSystemInfo3D(input_crs['authority'], input_crs['code'], input_crs['name'])
        output_graphic_coodinates_system_info = og_gs.GeographicCoordinateSystemInfo3D(output_crs['authority'], output_crs['code'], output_crs['name'])
    else:
        input_graphic_coodinates_system_info = og_gs.GeographicCoordinateSystemInfo2D(input_crs['authority'], input_crs['code'], input_crs['name'])
        output_graphic_coodinates_system_info = og_gs.GeographicCoordinateSystemInfo2D(output_crs['authority'], output_crs['code'], output_crs['name'])

    crs_I = og_gs.GeographicCoordinateSystem3D(manager, input_graphic_coodinates_system_info)
    crs_II = og_gs.GeographicCoordinateSystem3D(manager, output_graphic_coodinates_system_info)
    crs_II.import_coordinates(crs_I)

    return mesh

