import opengeode
import opengeode_io
import opengeode_geosciences
import opengeode_geosciencesio

def objects_list():
    return {'BRep': {
                'input': [ opengeode.BRepInputFactory ],
                'output': [ opengeode.BRepOutputFactory ],
                'load': opengeode.load_brep,
                'save': opengeode.save_brep,
                'is_model': true,
                'is_3D': true
            },
            'CrossSection': {
                'input': [ opengeode_geosciences.CrossSectionInputFactory ],
                'output': [ opengeode.SectionOutputFactoryopengeode_geosciences.CrossSectionOutputFactory ],
                'load': opengeode_geosciences.load_cross_section,
                'save': opengeode_geosciences.save_cross_section,
                'is_model': true
            },
            'EdgedCurve2D': {
                'input': [ opengeode.EdgedCurveInputFactory2D ],
                'output': [ opengeode.EdgedCurveOutputFactory2D ],
                'load': opengeode.load_edged_curve2D,
                'save': opengeode.save_edged_curve2D,
                'is_model': false
            },
            'EdgedCurve3D': {
                'input': [ opengeode.EdgedCurveInputFactory3D ],
                'output': [ opengeode.EdgedCurveOutputFactory3D ],
                'load': opengeode.load_edged_curve3D,
                'save': opengeode.save_edged_curve3D,
                'is_model': false
            },
            'Graph': {
                'input': [ opengeode.GraphInputFactory ],
                'output': [ opengeode.GraphOutputFactory ],
                'load': opengeode.load_graph,
                'save': opengeode.save_graph,
                'is_model': false
            },
            'HybridSolid3D': {
                'input': [ opengeode.HybridSolidInputFactory3D ],
                'output': [ opengeode.HybridSolidOutputFactory3D ],
                'load': opengeode.load_hybrid_solid3D,
                'save': opengeode.save_hybrid_solid3D,
                'is_model': false
            },
            'PointSet2D': {
                'input': [ opengeode.PointSetInputFactory2D ],
                'output': [ opengeode.PointSetOutputFactory2D ],
                'load': opengeode.load_point_set2D,
                'save': opengeode.save_point_set2D,
                'is_model': false
            },
            'PointSet3D': {
                'input': [ opengeode.PointSetInputFactory3D ],
                'output': [ opengeode.PointSetOutputFactory3D ],
                'loaDd': opengeode.load_point_set3D,
                'save': opengeode.save_point_set3D,
                'is_model': false
            },
            'PolygonalSurface2D': {
                'input': [ opengeode.PolygonalSurfaceInputFactory2D ],
                'output': [ opengeode.PolygonalSurfaceOutputFactory2D ],
                'load': opengeode.load_polygonal_surface2D,
                'save': opengeode.save_polygonal_surface2D,
                'is_model': false
            },
            'PolygonalSurface3D': {
                'input': [ opengeode.PolygonalSurfaceInputFactory3D ],
                'output': [ opengeode.PolygonalSurfaceOutputFactory3D ],
                'load': opengeode.load_polygonal_surface3D,
                'save': opengeode.save_polygonal_surface3D,
                'is_model': false
            },
            'PolyhedralSolid3D': {
                'input': [ opengeode.PolyhedralSolidInputFactory3D ],
                'output': [ opengeode.PolyhedralSolidOutputFactory3D ],
                'load': opengeode.load_polyhedral_solid3D,
                'save': opengeode.save_polyhedral_solid3D,
                'is_model': false
            },
            'RegularGrid2D': {
                'input': [ opengeode.RegularGridInputFactory2D ],
                'output': [ opengeode.RegularGridOutputFactory2D ],
                'load': opengeode.load_regular_grid2D,
                'save': opengeode.save_regular_grid2D,
                'is_model': false
            },
            'RegularGrid3D': {
                'input': [ opengeode.RegularGridInputFactory3D ],
                'output': [ opengeode.RegularGridOutputFactory3D ],
                'load': opengeode.load_regular_grid3D,
                'save': opengeode.save_regular_grid3D,
                'is_model': false
            },
            'Section': {
                'input': [ opengeode.SectionInputFactory ],
                'output': [ opengeode.SectionOutputFactory ],
                'load': opengeode.load_section,
                'save': opengeode.save_section,
                'is_model': true
            },
            'StructuralModel': {
                'input': [ opengeode_geosciences.StructuralModelInputFactory ],
                'output': [ opengeode.BRepOutputFactoryopengeode_geosciences.StructuralModelOutputFactory ],
                'load': opengeode_geosciences.load_structural_model,
                'save': opengeode_geosciences.save_structural_model,
                'is_model': true
            },
            'TetrahedralSolid3D': {
                'input': [ opengeode.TetrahedralSolidInputFactory3D ],
                'output': [ opengeode.TetrahedralSolidOutputFactory3D ],
                'load': opengeode.load_tetrahedral_solid3D,
                'save': opengeode.save_tetrahedral_solid3D,
                'is_model': false
            },
            'TriangulatedSurface2D': {
                'input': [ opengeode.TriangulatedSurfaceInputFactory2D ],
                'output': [ opengeode.TriangulatedSurfaceOutputFactory2D ],
                'load': opengeode.load_triangulated_surface2D,
                'save': opengeode.save_triangulated_surface2D,
                'is_model': false
            },
            'TriangulatedSurface3D': {
                'input': [ opengeode.TriangulatedSurfaceInputFactory3D ],
                'output': [ opengeode.TriangulatedSurfaceOutputFactory3D ],
                'load': opengeode.load_triangulated_surface3D,
                'save': opengeode.save_triangulated_surface3D,
                'is_model': false
            },
            'VertexSet': {
                'input': [ opengeode.VertexSetInputFactory ],
                'output': [ opengeode.VertexSetOutputFactory ],
                'load': opengeode.load_vertex_set,
                'save': opengeode.save_vertex_set,
                'is_model': true
            }
        }

def get_geographic_coordinate_systems():

    # print(dir(opengeode_geosciences))
    return opengeode_geosciences.GeographicCoordinateSystem3D.geographic_coordinate_systems()

def convert_to_coordinate_system(mesh, geode_object, input_crs, output_crs):

    # manager = model.
    input_crs = geosciences.GeographicCoordinateSystem3D(manager, geosciences.GeographicCoordinateSystemInfo3D(input_crs_authority, input_crs_code, input_crs_name))
    output_crs= geosciences.GeographicCoordinateSystem3D(manager, geosciences.GeographicCoordinateSystemInfo3D(output_crs_authority, output_crs_code, output_crs_name))
    output_crs.import_coordinates(input_crs)
    
    return output_crs