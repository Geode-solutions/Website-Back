import opengeode_inspector as I
import GeodeObjects

class Result:
    def __init__(self
                , value: bool
                , list_invalidity: list
                , route: str
                , expected_value: any
                ):
        self.value = value
        self.validity_sentence = route.replace("_", " ").capitalize()
        self.list_invalidity = list_invalidity
        self.is_leaf = len(list_invalidity) == 0
        self.route = route
        self.expected_value = expected_value

def json_return(Result_list: list):
    json_result = []
    for result in Result_list:
        if result.is_leaf:
            json_temp = {"value": result.value
                    , "validity_sentence": result.validity_sentence
                    , "list_invalidity" : result.list_invalidity
                    , "is_leaf": result.is_leaf
                    , "route": result.route
                    , "expected_value": result.expected_value
                    }
            json_result.append(json_temp)
        else:
            json_temp = {"value": result.value
                    , "validity_sentence": result.validity_sentence
                    , "list_invalidity" : json_return(result.list_invalidity)
                    , "is_leaf": result.is_leaf
                    , "route": result.route
                    , "expected_value": result.expected_value
                    }
            json_result.append(json_temp)
            
    return json_result

def AdjacencyTests():
    AdjacencyTests = [ 
                    Result(None, [], "nb_edges_with_wrong_adjacency", 0)
                    ]
    Wrapper_AdjacencyTests = Result(None, AdjacencyTests, "adjacency", True)
    return Wrapper_AdjacencyTests

def ColocationTests():
    ColocationTests = [ 
                    Result(None, [], "nb_colocated_points", 0)
                    ]
    Wrapper_ColocationTests = Result(None, ColocationTests, "colocation", True)
    return Wrapper_ColocationTests
def DegenerationTests():
    DegenerationTests = [ 
                        Result(None, [], "mesh_has_wrong_adjacencies", 0)
                        ]
    Wrapper_DegenerationTests = Result(None, DegenerationTests, "degeneration", True)
    return Wrapper_DegenerationTests
def ManifoldTests(object: str):
    ManifoldTests = [ 
                        Result(None, [], f"nb_non_manifold_{object}", 0)
                        ]
    Wrapper_ManifoldTests = Result(None, ManifoldTests, "manifold", True)
    return Wrapper_ManifoldTests
def TopologyTests(object: str):
    if object == "brep":
        TopologyTests = [
                        Result(None, [], "brep_meshed_components_are_linked_to_a_unique_vertex", True)
                        , Result(None, [], "nb_corners_not_linked_to_a_unique_vertex", 0)
                        , Result(None, [], "nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0)
                        , Result(None, [], "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0)
                        , Result(None, [], "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", 0)
                        , Result(None, [], "invalid_components_topology_unique_vertices", 0)
                        , Result(None, [], "multiple_corners_unique_vertices", 0)
                        , Result(None, [], "multiple_internals_corner_vertices", 0)
                        , Result(None, [], "not_internal_nor_boundary_corner_vertices", 0)
                        , Result(None, [], "internal_with_multiple_incidences_corner_vertices", 0)
                        , Result(None, [], "line_corners_without_boundary_status", 0)
                        , Result(None, [], "part_of_not_boundary_nor_internal_line_unique_vertices", 0)
                        , Result(None, [], "part_of_line_with_invalid_internal_topology_unique_vertices", 0)
                        , Result(None, [], "part_of_invalid_unique_line_unique_vertices", 0)
                        , Result(None, [], "part_of_lines_but_not_corner_unique_vertices", 0)
                        , Result(None, [], "part_of_not_boundary_nor_internal_surface_unique_vertices", 0)
                        , Result(None, [], "part_of_surface_with_invalid_internal_topology_unique_vertices", 0)
                        , Result(None, [], "part_of_invalid_unique_surface_unique_vertices", 0)
                        , Result(None, [], "part_of_invalid_multiple_surfaces_unique_vertices", 0)
                        , Result(None, [], "part_of_invalid_blocks_unique_vertices", 0)
                        ]
    elif object == "section":
        TopologyTests = [
                        Result(None, [], "section_meshed_components_are_linked_to_a_unique_vertex", True)
                        , Result(None, [], "nb_corners_not_linked_to_a_unique_vertex", 0)
                        , Result(None, [], "nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0)
                        , Result(None, [], "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0)
                        , Result(None, [], "invalid_components_topology_unique_vertices", 0)
                        , Result(None, [], "multiple_corners_unique_vertices", 0)
                        , Result(None, [], "multiple_internals_corner_vertices", 0)
                        , Result(None, [], "not_internal_nor_boundary_corner_vertices", 0)
                        , Result(None, [], "internal_with_multiple_incidences_corner_vertices", 0)
                        , Result(None, [], "line_corners_without_boundary_status", 0)
                        , Result(None, [], "part_of_not_boundary_nor_internal_line_unique_vertices", 0)
                        , Result(None, [], "part_of_line_with_invalid_internal_topology_unique_vertices",0)
                        , Result(None, [], "part_of_invalid_unique_line_unique_vertices", 0)
                        , Result(None, [], "part_of_lines_but_not_corner_unique_vertices", 0)
                        , Result(None, [], "part_of_invalid_surfaces_unique_vertices", 0)
                        ]
    Wrapper_TopologyTests = Result(None, TopologyTests, "topology", True)
    return Wrapper_TopologyTests

def Inspectors():

    BRep_Tests = [Result(None, [TopologyTests("brep")], "BRep", True)]
    CrossSection_Tests = [Result(None, [TopologyTests("section")], "CrossSection", True)]
    EdgedCurve2D_Tests = [Result(None, [ColocationTests()], "EdgedCurve2D", True)]
    EdgedCurve3D_Tests = [Result(None, [ColocationTests()], "EdgedCurve3D", True)]
    Graph_Tests = [Result(True, [ColocationTests()], "Graph", True)]
    HybridSolid3D_Tests = [Result(None, [ColocationTests(), DegenerationTests()], "HybridSolid3D", True)]
    PointSet2D_Tests = [Result(None, [ColocationTests()], "PointSet2D", True)]
    PointSet3D_Tests = [Result(None, [ColocationTests()], "PointSet3D", True)]
    PolygonalSurface2D_Tests = [Result(None, [AdjacencyTests(), ColocationTests(), DegenerationTests()], "PolygonalSurface2D", True)]
    PolygonalSurface3D_Tests = [Result(None, [AdjacencyTests(), ColocationTests(), DegenerationTests()], "PolygonalSurface3D", True)]
    PolyhedralSolid3D_Tests = [Result(None, [], "PolyhedralSolid3D", True)]
    RegularGrid2D_Tests = [Result(True, [], "RegularGrid2D", True)]
    RegularGrid3D_Tests = [Result(True, [], "RegularGrid3D", True)]
    Section_Tests = [Result(None, [TopologyTests("section")], "Section", True)]
    StructuralModel_Tests = [Result(None, [TopologyTests("brep")], "StructuralModel", True)]
    TetrahedralSolid3D_Tests = [Result(None, [ColocationTests(), DegenerationTests()], "TetrahedralSolid3D", True)]
    TriangulatedSurface2D_Tests = [Result(None, [AdjacencyTests(), ColocationTests(), DegenerationTests()], "TriangulatedSurface2D", True)]
    TriangulatedSurface3D_Tests = [Result(None, [AdjacencyTests(), ColocationTests(), DegenerationTests()], "TriangulatedSurface3D", True)]
    VertexSet_Tests = [Result(True, [], "VertexSet", True)]

    return {
            "BRep": { "inspector": I.BRepInspector, "testsnames": BRep_Tests }
            , "CrossSection": { "inspector": I.SectionInspector, "testsnames": CrossSection_Tests }
            , "EdgedCurve2D": { "inspector": I.EdgedCurveInspector2D, "testsnames": EdgedCurve2D_Tests }
            , "EdgedCurve3D": { "inspector": I.EdgedCurveInspector3D, "testsnames": EdgedCurve3D_Tests }
            , "Graph": { "inspector": "", "testsnames": Graph_Tests }
            , "HybridSolid3D": { "inspector": I.SolidMeshInspector3D, "testsnames": HybridSolid3D_Tests }
            , "PointSet2D": { "inspector": I.PointSetInspector2D, "testsnames": PointSet2D_Tests }
            , "PointSet3D": { "inspector": I.PointSetInspector3D, "testsnames": PointSet3D_Tests }
            , "PolygonalSurface2D": { "inspector": I.SurfaceMeshInspector2D, "testsnames": PolygonalSurface2D_Tests }
            , "PolygonalSurface3D": { "inspector": I.SurfaceMeshInspector3D, "testsnames": PolygonalSurface3D_Tests }
            , "PolyhedralSolid3D": { "inspector": I.SolidMeshInspector3D, "testsnames": PolyhedralSolid3D_Tests }
            , "RegularGrid2D": { "inspector": "", "testsnames": RegularGrid2D_Tests }
            , "RegularGrid3D": { "inspector": "", "testsnames": RegularGrid3D_Tests }
            , "Section": { "inspector": I.SectionInspector, "testsnames": Section_Tests }
            , "StructuralModel": { "inspector": I.BRepInspector, "testsnames": StructuralModel_Tests }
            , "TetrahedralSolid3D": { "inspector": I.SolidMeshInspector3D, "testsnames": TetrahedralSolid3D_Tests }
            , "TriangulatedSurface2D": { "inspector": I.SurfaceMeshInspector2D, "testsnames": TriangulatedSurface2D_Tests }
            , "TriangulatedSurface3D": { "inspector": I.SurfaceMeshInspector3D, "testsnames": TriangulatedSurface3D_Tests }
            , "VertexSet": { "inspector": "", "testsnames": VertexSet_Tests }
            }