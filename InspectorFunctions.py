# from importlib.util import module_for_loader
# from jinja2 import Undefined
import opengeode_inspector as I
import json

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

def GetTestNames():
    def BRep():
        def Topology():
            BRepTopologyTests = [ Result(None, "brep_meshed_components_are_linked_to_a_unique_vertex", [], True, "/brep_meshed_components_are_linked_to_a_unique_vertex", True).json_return()
                                , Result(None, "nb_corners_not_linked_to_a_unique_vertex", [], True, "/nb_corners_not_linked_to_a_unique_vertex", 0).json_return()
                                , Result(None, "nb_lines_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                                , Result(None, "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                                , Result(None, "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_blocks_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                                , Result(None, "invalid_components_topology_unique_vertices", [], True, "/invalid_components_topology_unique_vertices", True).json_return()
                                , Result(None, "multiple_corners_unique_vertices", [], True, "/multiple_corners_unique_vertices", True).json_return()
                                , Result(None, "multiple_internals_corner_vertices", [], True, "/multiple_internals_corner_vertices", True).json_return()
                                , Result(None, "not_internal_nor_boundary_corner_vertices", [], True, "/not_internal_nor_boundary_corner_vertices", True).json_return()
                                , Result(None, "internal_with_multiple_incidences_corner_vertices", [], True, "/internal_with_multiple_incidences_corner_vertices", True).json_return()
                                , Result(None, "line_corners_without_boundary_status", [], True, "/line_corners_without_boundary_status", True).json_return()
                                , Result(None, "part_of_not_boundary_nor_internal_line_unique_vertices", [], True, "/part_of_not_boundary_nor_internal_line_unique_vertices", True).json_return()
                                , Result(None, "part_of_line_with_invalid_internal_topology_unique_vertices", [], True, "/part_of_line_with_invalid_internal_topology_unique_vertices", True).json_return()
                                , Result(None, "part_of_invalid_unique_line_unique_vertices", [], True, "/part_of_invalid_unique_line_unique_vertices", True).json_return()
                                , Result(None, "part_of_lines_but_not_corner_unique_vertices", [], True, "/part_of_lines_but_not_corner_unique_vertices", True).json_return()
                                , Result(None, "part_of_not_boundary_nor_internal_surface_unique_vertices", [], True, "/part_of_not_boundary_nor_internal_surface_unique_vertices", True).json_return()
                                , Result(None, "part_of_surface_with_invalid_internal_topology_unique_vertices", [], True, "/part_of_surface_with_invalid_internal_topology_unique_vertices", True).json_return()
                                , Result(None, "part_of_invalid_unique_surface_unique_vertices", [], True, "/part_of_invalid_unique_surface_unique_vertices", True).json_return()
                                , Result(None, "part_of_invalid_multiple_surfaces_unique_vertices", [], True, "/part_of_invalid_multiple_surfaces_unique_vertices", True).json_return()
                                , Result(None, "part_of_invalid_blocks_unique_vertices", [], True, "/part_of_invalid_blocks_unique_vertices", True).json_return()
                                ]
            BRepTopologyTests = Result(None, "Topology", BRepTopologyTests, False, "/topology", True).json_return()
            return BRepTopologyTests
        BRep_GlobalTests = Result(None, "BRep", [Topology()], False, "/BRep", True).json_return()
        return BRep_GlobalTests

    def Section():
        def Topology():
            SectionTopologyTests = [ Result(None, "section_meshed_components_are_linked_to_a_unique_vertex", [], True, "/brep_meshed_components_are_linked_to_a_unique_vertex", True).json_return()
                                    , Result(None, "nb_corners_not_linked_to_a_unique_vertex", [], True, "/nb_corners_not_linked_to_a_unique_vertex", 0).json_return()
                                    , Result(None, "nb_lines_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_lines_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                                    , Result(None, "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                                    , Result(None, "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", [], True, "/nb_blocks_meshed_but_not_linked_to_a_unique_vertex", 0).json_return()
                                    , Result(None, "invalid_components_topology_unique_vertices", [], True, "/invalid_components_topology_unique_vertices", True).json_return()
                                    , Result(None, "multiple_corners_unique_vertices", [], True, "/multiple_corners_unique_vertices", True).json_return()
                                    , Result(None, "multiple_internals_corner_vertices", [], True, "/multiple_internals_corner_vertices", True).json_return()
                                    , Result(None, "not_internal_nor_boundary_corner_vertices", [], True, "/not_internal_nor_boundary_corner_vertices", True).json_return()
                                    , Result(None, "internal_with_multiple_incidences_corner_vertices", [], True, "/internal_with_multiple_incidences_corner_vertices", True).json_return()
                                    , Result(None, "line_corners_without_boundary_status", [], True, "/line_corners_without_boundary_status", True).json_return()
                                    , Result(None, "part_of_not_boundary_nor_internal_line_unique_vertices", [], True, "/part_of_not_boundary_nor_internal_line_unique_vertices", True).json_return()
                                    , Result(None, "part_of_line_with_invalid_internal_topology_unique_vertices", [], True, "/part_of_line_with_invalid_internal_topology_unique_vertices", True).json_return()
                                    , Result(None, "part_of_invalid_unique_line_unique_vertices", [], True, "/part_of_invalid_unique_line_unique_vertices", True).json_return()
                                    , Result(None, "part_of_lines_but_not_corner_unique_vertices", [], True, "/part_of_lines_but_not_corner_unique_vertices", True).json_return()
                                    , Result(None, "part_of_not_boundary_nor_internal_surface_unique_vertices", [], True, "/part_of_not_boundary_nor_internal_surface_unique_vertices", True).json_return()
                                    , Result(None, "part_of_surface_with_invalid_internal_topology_unique_vertices", [], True, "/part_of_surface_with_invalid_internal_topology_unique_vertices", True).json_return()
                                    , Result(None, "part_of_invalid_unique_surface_unique_vertices", [], True, "/part_of_invalid_unique_surface_unique_vertices", True).json_return()
                                    , Result(None, "part_of_invalid_multiple_surfaces_unique_vertices", [], True, "/part_of_invalid_multiple_surfaces_unique_vertices", True).json_return()
                                    , Result(None, "part_of_invalid_blocks_unique_vertices", [], True, "/part_of_invalid_blocks_unique_vertices", True).json_return()
                                    ]

            Return_SectionTopologyTests = Result(None, "Topology", SectionTopologyTests, False, "/topology", True).json_return()
            return Return_SectionTopologyTests
        Section_GlobalTests = Result(None, "Section", [Topology()], False, "/Section", True).json_return()
        return Section_GlobalTests

    def Surface():
        def Adjacency():
            SurfaceAdjacencyTests = [ Result(None, "mesh_has_wrong_adjacencies", [], True, "/mesh_has_wrong_adjacencies", True).json_return()
                                    , Result(None, "nb_edges_with_wrong_adjacency", [], True, "/nb_edges_with_wrong_adjacency", 0).json_return()
                                    , Result(None, "polygon_edges_with_wrong_adjacency", [], True, "/polygon_edges_with_wrong_adjacency", 0).json_return()
                                    ]
            Return_SurfaceAdjacencyTests = Result(None, "Adjacency", SurfaceAdjacencyTests, False, "/adjacency", True).json_return()
            return Return_SurfaceAdjacencyTests
        def Colocation():
            SurfaceColocationTests = [ Result(None, "mesh_has_colocated_points", [], True, "/mesh_has_colocated_points", True).json_return()
                                    , Result(None, "nb_colocated_points", [], True, "/nb_colocated_points", 0).json_return()
                                    , Result(None, "colocated_points_groups", [], True, "/colocated_points_groups", 0).json_return()
                                    ]
            Return_SurfaceColocationTests = Result(None, "Adjacency", SurfaceColocationTests, False, "/adjacency", True).json_return()
            return Return_SurfaceColocationTests
        def Degeneration():
            SurfaceDegenerationTests = [ Result(None, "mesh_has_wrong_adjacencies", [], True, "/mesh_has_wrong_adjacencies", True).json_return()
                                    , Result(None, "polygon_edges_with_wrong_adjacency", [], True, "/polygon_edges_with_wrong_adjacency", 0).json_return()
                                    ]
            Return_SurfaceDegenerationTests = Result(None, "Degeneration", SurfaceDegenerationTests, False, "/degeneration", True).json_return()
            return Return_SurfaceDegenerationTests


        Surface_GlobalTests = Result(None, "Surface", [Adjacency(), Colocation(), Degeneration()], False, "/Surface", True).json_return()
        return Surface_GlobalTests
    # def Colocation():
    #     return 1   
    # def Degeneration():
    #     return 1   
    # def Manifold():
    #     return 1 
    # def Colocation():
    #     return 1  

    return {"BRep": [BRep()]
            , "CrossSection": [Section()]
            # , "EdgedCurve2D": I.EdgedCurveColocation2D(model),
            # , "EdgedCurve3D": I.EdgedCurveColocation3D(model),
            # , "Graph": I.PointSetColocation(model),
            # , "HybridSolid3D": I.SolidMeshColocation(model),
            # , "PointSet2D": I.PointSetColocation2D(model),
            # , "PointSet3D": I.PointSetColocation3D(model),
            # , "PolygonalSurface2D": I.SolidMeshColocation(model),
            # , "PolygonalSurface3D": I.SolidMeshColocation(model),
            # , "PolyhedralSolid3D": I.SolidMeshColocation(model),
            # , "RegularGrid2D": I,
            # , "RegularGrid3D": I,
            , "Section": [Section()]
            # , "StructuralModel": I,
            # , "TetrahedralSolid3D": I.SolidMeshColocation(model),
            # , "TriangulatedSurface2D": I.SolidMeshColocation(model),
            # , "TriangulatedSurface3D": I.SolidMeshColocation(model),
            # , "VertexSet": I
            }