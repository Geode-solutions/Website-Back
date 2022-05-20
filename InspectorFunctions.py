import opengeode_inspector as I
import GeodeObjects

class Result:
    def __init__(self
                , value: bool
                , validity_sentence: str
                , list_invalidity: list
                , is_leaf: bool
                , route: str
                , expected_value: any
                ):
        self.value = value
        self.validity_sentence = validity_sentence
        self.list_invalidity = list_invalidity
        self.is_leaf = is_leaf
        self.route = route
        self.expected_value = expected_value

    def json_return(self):
        return {"value": self.value
                , "validity_sentence": self.validity_sentence
                , "list_invalidity" : self.list_invalidity
                , "is_leaf": self.is_leaf
                , "route": self.route
                , "expected_value": self.expected_value
                }

def AdjacencyTests():
    AdjacencyTests = [ 
                    Result(None, "nb_edges_with_wrong_adjacency", [], True, "nb_edges_with_wrong_adjacency", 0).json_return()
                    ]
    Wrapper_AdjacencyTests = Result(None, "Adjacency", AdjacencyTests, False, "adjacency", True).json_return()
    return Wrapper_AdjacencyTests

def ColocationTests():
    ColocationTests = [ 
                    Result(None, "nb_colocated_points", [], True, "nb_colocated_points", 0).json_return()
                    ]
    Wrapper_ColocationTests = Result(None, "Colocation", ColocationTests, False, "colocation", True).json_return()
    return Wrapper_ColocationTests
def DegenerationTests():
    DegenerationTests = [ 
                        Result(None, "mesh_has_wrong_adjacencies", [], True, "mesh_has_wrong_adjacencies", 0).json_return()
                        ]
    Wrapper_DegenerationTests = Result(None, "Degeneration", DegenerationTests, False, "degeneration", True).json_return()
    return Wrapper_DegenerationTests
def ManifoldTests(object: str):
    ManifoldTests = [ 
                        Result(None, f"nb_non_manifold_{object}", [], True, f"nb_non_manifold_{object}", 0).json_return()
                        ]
    Wrapper_ManifoldTests = Result(None, "Manifold", ManifoldTests, False, "manifold", True).json_return()
    return Wrapper_ManifoldTests
def TopologyTests(object: str):
    if object == "brep":
        TopologyTests = [
                        Result(None, "brep_meshed_components_are_linked_to_a_unique_vertex", [], True, f"{object}_meshed_components_are_linked_to_a_unique_vertex", True).json_return()
                        , Result(None, "nb_corners_not_linked_to_a_unique_vertex", [], True, "nb_corners_not_linked_to_a_unique_vertex", 0).json_return()
                        , Result(None, "nb_lines_meshed_but_not_linked_to_a_unique_vertex", [], True, "nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                        , Result(None, "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", [], True, "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                        , Result(None, "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", [], True, "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                        , Result(None, "invalid_components_topology_unique_vertices", [], True, "invalid_components_topology_unique_vertices", 0).json_return()
                        , Result(None, "multiple_corners_unique_vertices", [], True, "multiple_corners_unique_vertices", 0).json_return()
                        , Result(None, "multiple_internals_corner_vertices", [], True, "multiple_internals_corner_vertices", 0).json_return()
                        , Result(None, "not_internal_nor_boundary_corner_vertices", [], True, "not_internal_nor_boundary_corner_vertices", 0).json_return()
                        , Result(None, "internal_with_multiple_incidences_corner_vertices", [], True, "internal_with_multiple_incidences_corner_vertices", 0).json_return()
                        , Result(None, "line_corners_without_boundary_status", [], True, "line_corners_without_boundary_status", 0).json_return()
                        , Result(None, "part_of_not_boundary_nor_internal_line_unique_vertices", [], True, "part_of_not_boundary_nor_internal_line_unique_vertices", 0).json_return()
                        , Result(None, "part_of_line_with_invalid_internal_topology_unique_vertices", [], True, "part_of_line_with_invalid_internal_topology_unique_vertices", 0).json_return()
                        , Result(None, "part_of_invalid_unique_line_unique_vertices", [], True, "part_of_invalid_unique_line_unique_vertices", 0).json_return()
                        , Result(None, "part_of_lines_but_not_corner_unique_vertices", [], True, "part_of_lines_but_not_corner_unique_vertices", 0).json_return()
                        , Result(None, "part_of_not_boundary_nor_internal_surface_unique_vertices", [], True, "part_of_not_boundary_nor_internal_surface_unique_vertices", 0).json_return()
                        , Result(None, "part_of_surface_with_invalid_internal_topology_unique_vertices", [], True, "part_of_surface_with_invalid_internal_topology_unique_vertices", 0).json_return()
                        , Result(None, "part_of_invalid_unique_surface_unique_vertices", [], True, "part_of_invalid_unique_surface_unique_vertices", 0).json_return()
                        , Result(None, "part_of_invalid_multiple_surfaces_unique_vertices", [], True, "part_of_invalid_multiple_surfaces_unique_vertices", 0).json_return()
                        , Result(None, "part_of_invalid_blocks_unique_vertices", [], True, "part_of_invalid_blocks_unique_vertices", 0).json_return()
                        ]
    elif object == "section":
        TopologyTests = [
                        Result(None, "section_meshed_components_are_linked_to_a_unique_vertex", [], True, f"{object}_meshed_components_are_linked_to_a_unique_vertex", True).json_return()
                        , Result(None, "nb_corners_not_linked_to_a_unique_vertex", [], True, "nb_corners_not_linked_to_a_unique_vertex", 0).json_return()
                        , Result(None, "nb_lines_meshed_but_not_linked_to_a_unique_vertex", [], True, "nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                        , Result(None, "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", [], True, "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                        , Result(None, "invalid_components_topology_unique_vertices", [], True, "invalid_components_topology_unique_vertices", 0).json_return()
                        , Result(None, "multiple_corners_unique_vertices", [], True, "multiple_corners_unique_vertices", 0).json_return()
                        , Result(None, "multiple_internals_corner_vertices", [], True, "multiple_internals_corner_vertices", 0).json_return()
                        , Result(None, "not_internal_nor_boundary_corner_vertices", [], True, "not_internal_nor_boundary_corner_vertices", 0).json_return()
                        , Result(None, "internal_with_multiple_incidences_corner_vertices", [], True, "internal_with_multiple_incidences_corner_vertices", 0).json_return()
                        , Result(None, "line_corners_without_boundary_status", [], True, "line_corners_without_boundary_status", 0).json_return()
                        , Result(None, "part_of_not_boundary_nor_internal_line_unique_vertices", [], True, "part_of_not_boundary_nor_internal_line_unique_vertices", 0).json_return()
                        , Result(None, "part_of_line_with_invalid_internal_topology_unique_vertices", [], True, "part_of_line_with_invalid_internal_topology_unique_vertices",0).json_return()
                        , Result(None, "part_of_invalid_unique_line_unique_vertices", [], True, "part_of_invalid_unique_line_unique_vertices", 0).json_return()
                        , Result(None, "part_of_lines_but_not_corner_unique_vertices", [], True, "part_of_lines_but_not_corner_unique_vertices", 0).json_return()
                        , Result(None, "part_of_invalid_surfaces_unique_vertices", [], True, "part_of_invalid_surfaces_unique_vertices", 0).json_return()
                        ]
    Wrapper_TopologyTests = Result(None, "Topology", TopologyTests, False, "topology", True).json_return()
    return Wrapper_TopologyTests

def Inspectors():

    BRep_Tests = [Result(None, "BRep", [TopologyTests("brep")], False, "BRep", True).json_return()]
    CrossSection_Tests = [Result(None, "CrossSection", [TopologyTests("section")], False, "CrossSection", True).json_return()]
    EdgedCurve2D_Tests = [Result(None, "EdgedCurve2D", [ColocationTests()], False, "EdgedCurve2D", True).json_return()]
    EdgedCurve3D_Tests = [Result(None, "EdgedCurve3D", [ColocationTests()], False, "EdgedCurve3D", True).json_return()]
    Graph_Tests = [Result(True, "Graph", [ColocationTests()], False, "Graph", True).json_return()]
    HybridSolid3D_Tests = [Result(None, "HybridSolid3D", [ColocationTests(), DegenerationTests()], False, "HybridSolid3D", True).json_return()]
    PointSet2D_Tests = [Result(None, "PointSet2D", [ColocationTests()], False, "PointSet2D", True).json_return()]
    PointSet3D_Tests = [Result(None, "PointSet3D", [ColocationTests()], False, "PointSet3D", True).json_return()]
    PolygonalSurface2D_Tests = [Result(None, "PolygonalSurface2D", [AdjacencyTests(), ColocationTests(), DegenerationTests()], False, "PolygonalSurface2D", True).json_return()]
    PolygonalSurface3D_Tests = [Result(None, "PolygonalSurface3D", [AdjacencyTests(), ColocationTests(), DegenerationTests()], False, "PolygonalSurface3D", True).json_return()]
    PolyhedralSolid3D_Tests = [Result(None, "PolyhedralSolid3D", [], False, "PolyhedralSolid3D", True).json_return()]
    RegularGrid2D_Tests = [Result(True, "RegularGrid2D", [], False, "RegularGrid2D", True).json_return()]
    RegularGrid3D_Tests = [Result(True, "RegularGrid3D", [], False, "RegularGrid3D", True).json_return()]
    Section_Tests = [Result(None, "Section", [TopologyTests("section")], False, "Section", True).json_return()]
    StructuralModel_Tests = [Result(None, "StructuralModel", [TopologyTests("brep")], False, "StructuralModel", True).json_return()]
    TetrahedralSolid3D_Tests = [Result(None, "TetrahedralSolid3D", [ColocationTests(), DegenerationTests()], False, "TetrahedralSolid3D", True).json_return()]
    TriangulatedSurface2D_Tests = [Result(None, "TriangulatedSurface2D", [AdjacencyTests(), ColocationTests(), DegenerationTests()], False, "TriangulatedSurface2D", True).json_return()]
    TriangulatedSurface3D_Tests = [Result(None, "TriangulatedSurface3D", [AdjacencyTests(), ColocationTests(), DegenerationTests()], False, "TriangulatedSurface3D", True).json_return()]
    VertexSet_Tests = [Result(True, "VertexSet", [], False, "VertexSet", True).json_return()]

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