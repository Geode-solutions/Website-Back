import opengeode_inspector as I

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
                    Result(None, "nb_edges_with_wrong_adjacency", [], True, "/nb_edges_with_wrong_adjacency", 0).json_return()
                    , Result(None, "polygon_edges_with_wrong_adjacency", [], True, "/polygon_edges_with_wrong_adjacency", 0).json_return()
                    ]
    Wrapper_AdjacencyTests = Result(None, "Adjacency", AdjacencyTests, False, "/adjacency", True).json_return()
    return Wrapper_AdjacencyTests

def ColocationTests():
    ColocationTests = [ Result(None, "mesh_has_colocated_points", [], True, "/mesh_has_colocated_points", True).json_return()
                    , Result(None, "nb_colocated_points", [], True, "/nb_colocated_points", 0).json_return()
                    , Result(None, "colocated_points_groups", [], True, "/colocated_points_groups", 0).json_return()
                    ]
    Wrapper_ColocationTests = Result(None, "Colocation", ColocationTests, False, "/colocation", True).json_return()
    return Wrapper_ColocationTests
def DegenerationTests():
    DegenerationTests = [ Result(None, "mesh_has_wrong_adjacencies", [], True, "/mesh_has_wrong_adjacencies", True).json_return()
                        , Result(None, "polygon_edges_with_wrong_adjacency", [], True, "/polygon_edges_with_wrong_adjacency", 0).json_return()
                        ]
    Wrapper_DegenerationTests = Result(None, "Degeneration", DegenerationTests, False, "/degeneration", True).json_return()
    return Wrapper_DegenerationTests
def ManifoldTests(object: str):
    ManifoldTests = [ Result(None, f"mesh_{object}_are_manifold", [], True, f"/mesh_{object}_are_manifold", True).json_return()
                        , Result(None, f"nb_non_manifold_{object}", [], True, f"/nb_non_manifold_{object}", 0).json_return()
                        , Result(None, f"non_manifold_{object}", [], True, f"/non_manifold_{object}", 0).json_return()
                        ]
    Wrapper_ManifoldTests = Result(None, "Manifold", ManifoldTests, False, "/manifold", True).json_return()
    return Wrapper_ManifoldTests
def TopologyTests(object: str):
    TopologyTests = [
                    Result(None, f"{object}_meshed_components_are_linked_to_a_unique_vertex", [], True, f"/{object}_meshed_components_are_linked_to_a_unique_vertex", 1).json_return()
                    , Result(None, "nb_corners_not_linked_to_a_unique_vertex", [], True, "/nb_corners_not_linked_to_a_unique_vertex", 1).json_return()
                    , Result(None, "nb_lines_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_lines_meshed_but_not_linked_to_a_unique_vertex", 1).json_return()
                    , Result(None, "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_surfaces_meshed_but_not_linked_to_a_unique_vertex",1).json_return()
                    , Result(None, "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_blocks_meshed_but_not_linked_to_a_unique_vertex", 1).json_return()
                    , Result(None, "invalid_components_topology_unique_vertices", [], True, "/invalid_components_topology_unique_vertices", 1).json_return()
                    , Result(None, "multiple_corners_unique_vertices", [], True, "/multiple_corners_unique_vertices", 1).json_return()
                    , Result(None, "multiple_internals_corner_vertices", [], True, "/multiple_internals_corner_vertices", 1).json_return()
                    , Result(None, "not_internal_nor_boundary_corner_vertices", [], True, "/not_internal_nor_boundary_corner_vertices", 1).json_return()
                    , Result(None, "internal_with_multiple_incidences_corner_vertices", [], True, "/internal_with_multiple_incidences_corner_vertices", 1).json_return()
                    , Result(None, "line_corners_without_boundary_status", [], True, "/line_corners_without_boundary_status", 1).json_return()
                    , Result(None, "part_of_not_boundary_nor_internal_line_unique_vertices", [], True, "/part_of_not_boundary_nor_internal_line_unique_vertices", 1).json_return()
                    , Result(None, "part_of_line_with_invalid_internal_topology_unique_vertices", [], True, "/part_of_line_with_invalid_internal_topology_unique_vertices", 1).json_return()
                    , Result(None, "part_of_invalid_unique_line_unique_vertices", [], True, "/part_of_invalid_unique_line_unique_vertices", 1).json_return()
                    , Result(None, "part_of_lines_but_not_corner_unique_vertices", [], True, "/part_of_lines_but_not_corner_unique_vertices", 1).json_return()
                    , Result(None, "part_of_not_boundary_nor_internal_surface_unique_vertices", [], True, "/part_of_not_boundary_nor_internal_surface_unique_vertices", 1).json_return()
                    , Result(None, "part_of_surface_with_invalid_internal_topology_unique_vertices", [], True, "/part_of_surface_with_invalid_internal_topology_unique_vertices", 1).json_return()
                    , Result(None, "part_of_invalid_unique_surface_unique_vertices", [], True, "/part_of_invalid_unique_surface_unique_vertices", 1).json_return()
                    , Result(None, "part_of_invalid_multiple_surfaces_unique_vertices", [], True, "/part_of_invalid_multiple_surfaces_unique_vertices", 1).json_return()
                    , Result(None, "part_of_invalid_blocks_unique_vertices", [], True, "/part_of_invalid_blocks_unique_vertices", 1).json_return()
                    ]
    Wrapper_TopologyTests = Result(None, "Topology", TopologyTests, False, "/topology", True).json_return()
    return Wrapper_TopologyTests


def Inspector(model = None):
    '''"inspector": I.BRepTopologyInspector(model), '''
    return {
            "BRep": { "testsnames": [Result(None, "BRep", [TopologyTests("brep")], False, "/BRep", True).json_return()], "testsresults": ""}
            # , "CrossSection": [{"inspector": I.BRepTopologyInspector(model), "testsnames": TopologyTests("section"), "testsresults": ""}]
            # , "EdgedCurve2D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "EdgedCurve3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "Graph": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "HybridSolid3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "PointSet2D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "PointSet3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "PolygonalSurface2D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "PolygonalSurface3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "PolyhedralSolid3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "RegularGrid2D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "RegularGrid3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "Section": [{"inspector": I.BRepTopologyInspector(model), "testsnames": TopologyTests("section"), "testsresults": ""}]
            # , "StructuralModel": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "TetrahedralSolid3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "TriangulatedSurface2D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "TriangulatedSurface3D": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            # , "VertexSet": [{"inspector": "", "testsnames": "", "testsresults": ""}]
            }

def GetTestsResults(object: str, test_name: str):
    Inspector = Inspector()[object]['inspector']
    print(object, " ", test_name)
    # result = getattr(Inspector, test_name)()
    result = 1
    return result