import opengeode_inspector as Inspector
import GeodeObjects

class Result:
    def __init__(self
                , list_invalidity: list
                , route: str
                , expected_value: any
                , validity_sentence: str = None
                ):
        self.list_invalidity = list_invalidity
        self.is_leaf = len(list_invalidity) == 0
        self.route = route
        self.expected_value = expected_value
        self.value = None
        self.validity_sentence = validity_sentence

def json_return(Result_list: list):
    json_result = []
    for result in Result_list:
        json_temp = {"value": result.value
                , "list_invalidity" : result.list_invalidity if result.is_leaf else json_return(result.list_invalidity)
                , "is_leaf": result.is_leaf
                , "route": result.route
                , "expected_value": result.expected_value
                , "validity_sentence": result.validity_sentence if result.validity_sentence != None else result.route
                }
        json_result.append(json_temp)
    return json_result

def AdjacencyTests(object: str):
    AdjacencyTests = [ 
                    Result([], f"nb_{object}_with_wrong_adjacency", 0, f"Number of {object} with invalid adjacencies")
                    ]
    Wrapper_AdjacencyTests = Result(AdjacencyTests, "adjacency", True)
    return Wrapper_AdjacencyTests

def ColocationTests():
    ColocationTests = [ 
                    Result([], "nb_colocated_points", 0, "Number of colocated points")
                    ]
    Wrapper_ColocationTests = Result(ColocationTests, "colocation", True)
    return Wrapper_ColocationTests
def DegenerationTests():
    DegenerationTests = [ 
                        Result([], "nb_degenerated_edges", 0, "Number of degenerated edges")
                        ]
    Wrapper_DegenerationTests = Result(DegenerationTests, "degeneration", True)
    return Wrapper_DegenerationTests
def ManifoldTests(object: str):
    ManifoldTests = [ 
                        Result([], f"nb_non_manifold_{object}", 0, f"Number of non manifold {object}")
                        ]
    Wrapper_ManifoldTests = Result(ManifoldTests, object, True)
    return Wrapper_ManifoldTests
def TopologyTests(object: str):
    unique_vertices_colocation = [
        Result([], "unique_vertices_linked_to_different_points", 0, "Number of unique vertices linked to different points in space")
        , Result([], "colocated_unique_vertices_groups", 0, "Number of unique vertices colocqted in space")
    ]
    if object == "brep":
        brep_components_are_linked_to_a_unique_vertex = [
            Result([], "nb_corners_not_linked_to_a_unique_vertex", 0, "Number of corners not linked to a unique vertex")
            , Result([], "nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0, "Number of lines not linked to a unique vertex")
            , Result([], "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0, "Number of surfaces not linked to a unique vertex")
            , Result([], "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", 0, "Number of blocks not linked to a unique vertex")
        ]

        brep_invalid_components_topology_unique_vertices = [
            Result([], "multiple_corners_unique_vertices", 0, "Unique vertices linked to multiple corners")
            , Result([], "multiple_internals_corner_vertices", 0, "Unique vertices linked to a corner with multiple internal relations")
            , Result([], "not_internal_nor_boundary_corner_vertices", 0, "Unique vertices linked to a corner which is neither internal nor boundary")
            , Result([], "line_corners_without_boundary_status", 0, "Unique vertices linked to a line and a corner not boundary of the line")
            , Result([], "part_of_not_boundary_nor_internal_line_unique_vertices", 0, "Unique vertices part of a line without boundary or internal relations")
            , Result([], "part_of_line_with_invalid_internal_topology_unique_vertices", 0, "Unique vertices part of a line with invalid internal topology relations")
            , Result([], "part_of_invalid_unique_line_unique_vertices", 0, "Unique vertices part of a single line with invalid topology")
            , Result([], "part_of_lines_but_not_corner_unique_vertices", 0, "Unique vertices part of multiple lines with invalid topology")
            , Result([], "part_of_not_boundary_nor_internal_surface_unique_vertices", 0, "Unique vertices part of a surface which has no boundary or internal relations")
            , Result([], "part_of_surface_with_invalid_internal_topology_unique_vertices", 0, "Unique vertices part of a surface with invalid internal topology")
            , Result([], "part_of_invalid_unique_surface_unique_vertices", 0, "Unique vertices part of a unique surface with invalid topology")
            , Result([], "part_of_invalid_multiple_surfaces_unique_vertices", 0, "Unique vertices part of multiple surfaces with invalid topology")
            , Result([], "part_of_line_and_not_on_surface_border_unique_vertices", 0, "Unique vertices part of a line and a surface but not on the border of the surface mesh")
            , Result([], "part_of_invalid_blocks_unique_vertices", 0, "Unique vertices part of blocks with invalid topology")
        ]

        TopologyTests = [
                        Result(brep_components_are_linked_to_a_unique_vertex, "Meshed components are linked to a unique vertex", True)
                        , Result(brep_invalid_components_topology_unique_vertices, "Unique vertices linked to components with invalid topology", True)
                        , Result(unique_vertices_colocation, "Unique vertices with colocation issues", True)
                        
                        ]
    elif object == "section":
        section_components_are_linked_to_a_unique_vertex = [
            Result([], "nb_corners_not_linked_to_a_unique_vertex", 0, "Number of corners not linked to a unique vertex")
            , Result([], "nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0, "Number of lines not linked to a unique vertex")
            , Result([], "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0, "Number of surfaces not linked to a unique vertex")
            , Result([], "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", 0, "Number of blocks not linked to a unique vertex")
        ]

        section_invalid_components_topology_unique_vertices = [
            Result([], "multiple_corners_unique_vertices", 0, "Unique vertices linked to multiple corners")
            , Result([], "multiple_internals_corner_vertices", 0, "Unique vertices linked to a corner with multiple internal relations")
            , Result([], "not_internal_nor_boundary_corner_vertices", 0, "Unique vertices linked to a corner which is neither internal nor boundary")
            , Result([], "line_corners_without_boundary_status", 0, "Unique vertices linked to a line and a corner not boundary of the line")
            , Result([], "part_of_not_boundary_nor_internal_line_unique_vertices", 0, "Unique vertices part of a line without boundary or internal relations")
            , Result([], "part_of_line_with_invalid_internal_topology_unique_vertices", 0, "Unique vertices part of a line with invalid internal topology relations")
            , Result([], "part_of_invalid_unique_line_unique_vertices", 0, "Unique vertices part of a single line with invalid topology")
            , Result([], "part_of_lines_but_not_corner_unique_vertices", 0, "Unique vertices part of multiple lines with invalid topology")
            , Result([], "part_of_invalid_surfaces_unique_vertices", 0, "Unique vertices part of surfaces with invalid topology")
            , Result([], "part_of_line_and_not_on_surface_border_unique_vertices", 0, "Unique vertices part of a line and a surface but not on the border of the surface mesh")
        ]

        TopologyTests = [
                        Result(section_components_are_linked_to_a_unique_vertex, "Meshed components are linked to a unique vertex", True)
                        , Result(section_invalid_components_topology_unique_vertices, "Unique vertices linked to components with invalid topology", True)
                        , Result(unique_vertices_colocation, "Unique vertices with colocation issues", True)
                        ]
    Wrapper_TopologyTests = Result(TopologyTests, "Topology", True)
    return Wrapper_TopologyTests

def Inspectors():

    BRep_Tests = [Result([TopologyTests("brep")], "BRep", True)]
    CrossSection_Tests = [Result([TopologyTests("section")], "CrossSection", True)]
    EdgedCurve2D_Tests = [Result([ColocationTests(), DegenerationTests()], "EdgedCurve2D", True)]
    EdgedCurve3D_Tests = [Result([ColocationTests(), DegenerationTests()], "EdgedCurve3D", True)]
    Graph_Tests = [Result([], "Graph", True, True)]
    HybridSolid3D_Tests = [Result([AdjacencyTests("facets"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("facets"), ManifoldTests("vertices")], "manifold", True)], "HybridSolid3D", True)]
    PointSet2D_Tests = [Result([ColocationTests()], "PointSet2D", True)]
    PointSet3D_Tests = [Result([ColocationTests()], "PointSet3D", True)]
    PolygonalSurface2D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold", True)], "PolygonalSurface2D", True)]
    PolygonalSurface3D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold", True)], "PolygonalSurface3D", True)]
    PolyhedralSolid3D_Tests = [Result([AdjacencyTests("facets"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("facets"), ManifoldTests("vertices")], "manifold", True)], "PolyhedralSolid3D", True)]
    RegularGrid2D_Tests = [Result([], "RegularGrid2D", True, True)]
    RegularGrid3D_Tests = [Result([], "RegularGrid3D", True, True)]
    Section_Tests = [Result([TopologyTests("section")], "Section", True)]
    StructuralModel_Tests = [Result([TopologyTests("brep")], "StructuralModel", True)]
    TetrahedralSolid3D_Tests = [Result([AdjacencyTests("facets"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("facets"), ManifoldTests("facets"), ManifoldTests("vertices")], "manifold", True)], "TetrahedralSolid3D", True)]
    TriangulatedSurface2D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold", True)], "TriangulatedSurface2D", True)]
    TriangulatedSurface3D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold", True)], "TriangulatedSurface3D", True)]
    VertexSet_Tests = [Result([], "VertexSet", True, True)]

    return {
            "BRep": { "inspector": Inspector.BRepInspector, "testsnames": BRep_Tests }
            , "CrossSection": { "inspector": Inspector.SectionInspector, "testsnames": CrossSection_Tests }
            , "EdgedCurve2D": { "inspector": Inspector.EdgedCurveInspector2D, "testsnames": EdgedCurve2D_Tests }
            , "EdgedCurve3D": { "inspector": Inspector.EdgedCurveInspector3D, "testsnames": EdgedCurve3D_Tests }
            , "Graph": { "inspector": "", "testsnames": Graph_Tests }
            , "HybridSolid3D": { "inspector": Inspector.SolidMeshInspector3D, "testsnames": HybridSolid3D_Tests }
            , "PointSet2D": { "inspector": Inspector.PointSetInspector2D, "testsnames": PointSet2D_Tests }
            , "PointSet3D": { "inspector": Inspector.PointSetInspector3D, "testsnames": PointSet3D_Tests }
            , "PolygonalSurface2D": { "inspector": Inspector.SurfaceMeshInspector2D, "testsnames": PolygonalSurface2D_Tests }
            , "PolygonalSurface3D": { "inspector": Inspector.SurfaceMeshInspector3D, "testsnames": PolygonalSurface3D_Tests }
            , "PolyhedralSolid3D": { "inspector": Inspector.SolidMeshInspector3D, "testsnames": PolyhedralSolid3D_Tests }
            , "RegularGrid2D": { "inspector": "", "testsnames": RegularGrid2D_Tests }
            , "RegularGrid3D": { "inspector": "", "testsnames": RegularGrid3D_Tests }
            , "Section": { "inspector": Inspector.SectionInspector, "testsnames": Section_Tests }
            , "StructuralModel": { "inspector": Inspector.BRepInspector, "testsnames": StructuralModel_Tests }
            , "TetrahedralSolid3D": { "inspector": Inspector.SolidMeshInspector3D, "testsnames": TetrahedralSolid3D_Tests }
            , "TriangulatedSurface2D": { "inspector": Inspector.SurfaceMeshInspector2D, "testsnames": TriangulatedSurface2D_Tests }
            , "TriangulatedSurface3D": { "inspector": Inspector.SurfaceMeshInspector3D, "testsnames": TriangulatedSurface3D_Tests }
            , "VertexSet": { "inspector": "", "testsnames": VertexSet_Tests }
            }
