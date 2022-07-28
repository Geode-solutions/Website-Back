import opengeode_inspector as Inspector
import GeodeObjects

class Result:
    def __init__(self
                , list_invalidity: list
                , route: str
                , validity_sentence: str = None
                ):
        self.list_invalidity = list_invalidity
        self.is_leaf = len(list_invalidity) == 0
        self.route = route
        self.value = None
        self.validity_sentence = validity_sentence

def json_return(Result_list: list):
    json_result = []
    for result in Result_list:
        json_temp = {"value": result.value
                , "list_invalidity" : result.list_invalidity if result.is_leaf else json_return(result.list_invalidity)
                , "is_leaf": result.is_leaf
                , "route": result.route
                , "validity_sentence": result.validity_sentence if result.validity_sentence != None else result.route
                }
        json_result.append(json_temp)
    return json_result

def AdjacencyTests(object: str):
    AdjacencyTests = [ 
        Result([], f"nb_{object}_with_wrong_adjacency", f"Number of {object} with invalid adjacencies")
    ]
    Wrapper_AdjacencyTests = Result(AdjacencyTests, "adjacency", True)
    return Wrapper_AdjacencyTests

def ColocationTests():
    ColocationTests = [
        Result([], "nb_colocated_points", "Number of colocated points")
    ]
    Wrapper_ColocationTests = Result(ColocationTests, "colocation", True)
    return Wrapper_ColocationTests
def DegenerationTests():
    DegenerationTests = [ 
        Result([], "nb_degenerated_edges", "Number of degenerated edges")
    ]
    Wrapper_DegenerationTests = Result(DegenerationTests, "degeneration", True)
    return Wrapper_DegenerationTests
def ManifoldTests(object: str):
    ManifoldTests = [ 
        Result([], f"nb_non_manifold_{object}", f"Number of non manifold {object}")
    ]
    Wrapper_ManifoldTests = Result(ManifoldTests, object, True)
    return Wrapper_ManifoldTests
def TopologyTests(object: str):
    unique_vertices_colocation = [
        Result([], "unique_vertices_linked_to_different_points", "Number of unique vertices linked to different points in space")
        , Result([], "colocated_unique_vertices_groups", "Number of unique vertices colocated in space")
    ]
    
    components_are_linked_to_a_unique_vertex = [
        Result([], "nb_corners_not_linked_to_a_unique_vertex", "Number of corners not linked to a unique vertex")
        , Result([], "nb_lines_meshed_but_not_linked_to_a_unique_vertex", "Number of lines not linked to a unique vertex")
        , Result([], "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex", "Number of surfaces not linked to a unique vertex")
    ]

    invalid_components_topology_unique_vertices = [
        Result([], "multiple_corners_unique_vertices", "Unique vertices linked to multiple corners")
        , Result([], "multiple_internals_corner_vertices", "Unique vertices linked to a corner with multiple internal relations")
        , Result([], "not_internal_nor_boundary_corner_vertices", "Unique vertices linked to a corner which is neither internal nor boundary")
        , Result([], "line_corners_without_boundary_status", "Unique vertices linked to a line and a corner not boundary of the line")
        , Result([], "part_of_not_boundary_nor_internal_line_unique_vertices", "Unique vertices part of a line without boundary or internal relations")
        , Result([], "part_of_line_with_invalid_internal_topology_unique_vertices", "Unique vertices part of a line with invalid internal topology relations")
        , Result([], "part_of_invalid_unique_line_unique_vertices", "Unique vertices part of a single line with invalid topology")
        , Result([], "part_of_lines_but_not_corner_unique_vertices", "Unique vertices part of multiple lines with invalid topology")
        , Result([], "part_of_line_and_not_on_surface_border_unique_vertices", "Unique vertices part of a line and a surface but not on the border of the surface mesh")
    ]

    if object == "brep":
        brep_components_are_linked_to_a_unique_vertex = components_are_linked_to_a_unique_vertex
        brep_components_are_linked_to_a_unique_vertex.append(Result([], "nb_blocks_meshed_but_not_linked_to_a_unique_vertex", "Number of blocks not linked to a unique vertex"))

        brep_invalid_components_topology_unique_vertices = invalid_components_topology_unique_vertices
        brep_invalid_components_topology_unique_vertices.append(Result([], "part_of_not_boundary_nor_internal_surface_unique_vertices", "Unique vertices part of a surface which has no boundary or internal relations"))
        brep_invalid_components_topology_unique_vertices.append(Result([], "part_of_surface_with_invalid_internal_topology_unique_vertices", "Unique vertices part of a surface with invalid internal topology"))
        brep_invalid_components_topology_unique_vertices.append(Result([], "part_of_invalid_unique_surface_unique_vertices", "Unique vertices part of a unique surface with invalid topology"))
        brep_invalid_components_topology_unique_vertices.append(Result([], "part_of_invalid_multiple_surfaces_unique_vertices", "Unique vertices part of multiple surfaces with invalid topology"))
        brep_invalid_components_topology_unique_vertices.append(Result([], "part_of_invalid_blocks_unique_vertices", "Unique vertices part of blocks with invalid topology"))

        TopologyTests = [
            Result(brep_components_are_linked_to_a_unique_vertex, "Meshed components are linked to a unique vertex")
            , Result(brep_invalid_components_topology_unique_vertices, "Unique vertices linked to components with invalid topology")
            , Result(unique_vertices_colocation, "Unique vertices with colocation issues")
        ]
    elif object == "section":
        section_invalid_components_topology_unique_vertices = invalid_components_topology_unique_vertices
        section_invalid_components_topology_unique_vertices.append(Result([], "part_of_invalid_surfaces_unique_vertices", "Unique vertices part of surfaces with invalid topology"))

        TopologyTests = [
            Result(components_are_linked_to_a_unique_vertex, "Meshed components are linked to a unique vertex")
            , Result(section_invalid_components_topology_unique_vertices, "Unique vertices linked to components with invalid topology")
            , Result(unique_vertices_colocation, "Unique vertices with colocation issues")
        ]
    Wrapper_TopologyTests = Result(TopologyTests, "Topology")
    return Wrapper_TopologyTests

def ComponentMeshesTests(object: str):
    component_meshes_adjacency = [
        Result([], "surfaces_nb_edges_with_wrong_adjacencies", "")
    ]
    component_meshes_colocation = [
        Result([], "components_nb_colocated_points", "")
    ]
    component_meshes_degeneration = [
        Result([], "components_nb_degenerated_edges", "")
    ]
    component_meshes_manifold = [
        Result([], "component_meshes_nb_non_manifold_vertices", "")
        , Result([], "component_meshes_nb_non_manifold_edges", "")
    ]

    if object == "brep":
        brep_component_meshes_adjacency = component_meshes_adjacency
        brep_component_meshes_adjacency.append(Result([], "blocks_nb_facets_with_wrong_adjacencies", ""))

        brep_component_meshes_manifold = component_meshes_manifold
        brep_component_meshes_manifold.append(Result([], "component_meshes_nb_non_manifold_facets", ""))

        ComponentMeshesTests = [
            Result(brep_component_meshes_adjacency, "Adjacency")
            , Result(component_meshes_colocation, "Colocation")
            , Result(component_meshes_degeneration, "Degeneration")
            , Result(brep_component_meshes_manifold, "Manifold")
        ]

    elif object == "section":

        ComponentMeshesTests = [
            Result(component_meshes_adjacency, "Adjacency")
            , Result(component_meshes_colocation, "Colocation")
            , Result(component_meshes_degeneration, "Degeneration")
            , Result(component_meshes_manifold, "Manifold")
        ]

    Wrapper_ComponentMeshesTests = Result(ComponentMeshesTests, "Component Meshes")
    return Wrapper_ComponentMeshesTests

def Inspectors():

    BRep_Tests = [Result([TopologyTests("brep"), ComponentMeshesTests("brep")], "BRep")]
    CrossSection_Tests = [Result([TopologyTests("section"), ComponentMeshesTests("section")], "CrossSection")]
    EdgedCurve2D_Tests = [Result([ColocationTests(), DegenerationTests()], "EdgedCurve2D")]
    EdgedCurve3D_Tests = [Result([ColocationTests(), DegenerationTests()], "EdgedCurve3D")]
    Graph_Tests = [Result([], "Graph", True)]
    HybridSolid3D_Tests = [Result([AdjacencyTests("facets"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("facets"), ManifoldTests("vertices")], "manifold")], "HybridSolid3D")]
    PointSet2D_Tests = [Result([ColocationTests()], "PointSet2D", True)]
    PointSet3D_Tests = [Result([ColocationTests()], "PointSet3D", True)]
    PolygonalSurface2D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold")], "PolygonalSurface2D")]
    PolygonalSurface3D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold")], "PolygonalSurface3D")]
    PolyhedralSolid3D_Tests = [Result([AdjacencyTests("facets"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("facets"), ManifoldTests("vertices")], "manifold")], "PolyhedralSolid3D")]
    RegularGrid2D_Tests = [Result([], "RegularGrid2D", True)]
    RegularGrid3D_Tests = [Result([], "RegularGrid3D", True)]
    Section_Tests = [Result([TopologyTests("section"), ComponentMeshesTests("section")], "Section")]
    StructuralModel_Tests = [Result([TopologyTests("brep"), ComponentMeshesTests("brep")], "StructuralModel")]
    TetrahedralSolid3D_Tests = [Result([AdjacencyTests("facets"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("facets"), ManifoldTests("facets"), ManifoldTests("vertices")], "manifold")], "TetrahedralSolid3D")]
    TriangulatedSurface2D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold")], "TriangulatedSurface2D")]
    TriangulatedSurface3D_Tests = [Result([AdjacencyTests("edges"), ColocationTests(), DegenerationTests(), Result([ManifoldTests("edges"), ManifoldTests("vertices")], "manifold")], "TriangulatedSurface3D")]
    VertexSet_Tests = [Result([], "VertexSet", True)]

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


def InpectorExpectedResult(object: str):
    return {
        f"nb_{object}_with_wrong_adjacency" : 0
        , "nb_colocated_points" : 0
        , "nb_degenerated_edges" : 0
        , f"nb_non_manifold_{object}" : 0
        , "unique_vertices_linked_to_different_points" : 0
        , "colocated_unique_vertices_groups" : 0
        , "nb_corners_not_linked_to_a_unique_vertex" : 0
        , "nb_lines_meshed_but_not_linked_to_a_unique_vertex" : 0
        , "nb_surfaces_meshed_but_not_linked_to_a_unique_vertex" : 0
        , "multiple_corners_unique_vertices" : 0
        , "multiple_internals_corner_vertices" : 0
        , "not_internal_nor_boundary_corner_vertices" : 0
        , "line_corners_without_boundary_status" : 0
        , "part_of_not_boundary_nor_internal_line_unique_vertices" : 0
        , "part_of_line_with_invalid_internal_topology_unique_vertices" : 0
        , "part_of_invalid_unique_line_unique_vertices" : 0
        , "part_of_lines_but_not_corner_unique_vertices" : 0
        , "part_of_line_and_not_on_surface_border_unique_vertices" : 0
        , "nb_blocks_meshed_but_not_linked_to_a_unique_vertex" : 0
        , "part_of_not_boundary_nor_internal_surface_unique_vertices" : 0
        , "part_of_surface_with_invalid_internal_topology_unique_vertices" : 0
        , "part_of_invalid_unique_surface_unique_vertices" : 0
        , "part_of_invalid_multiple_surfaces_unique_vertices" : 0
        , "part_of_invalid_blocks_unique_vertices" : 0
        , "surfaces_nb_edges_with_wrong_adjacencies" : {}
        , "components_nb_colocated_points" : {}
        , "components_nb_degenerated_edges" : {}
        , "component_meshes_nb_non_manifold_vertices" : {}
        , "component_meshes_nb_non_manifold_edges" : {}
    }


