import opengeode
import opengeode_io
import opengeode_geosciences
import opengeode_geosciencesio

def ObjectsList():
    return {"BRep": {"input": opengeode.BRepInputFactory, "output": opengeode.BRepOutputFactory, "load": opengeode.load_brep, "save": opengeode.save_brep},
            "EdgedCurve2D": {"input": opengeode.EdgedCurveInputFactory2D, "output": opengeode.EdgedCurveOutputFactory2D, "load": opengeode.load_edged_curve2D, "save": opengeode.save_edged_curve2D},
            "EdgedCurve3D": {"input": opengeode.EdgedCurveInputFactory3D, "output": opengeode.EdgedCurveOutputFactory3D, "load": opengeode.load_edged_curve3D, "save": opengeode.save_edged_curve3D},
            "Graph": {"input": opengeode.GraphInputFactory, "output": opengeode.GraphOutputFactory, "load": opengeode.load_graph, "save": opengeode.save_graph},
            "HybridSolidy3D": {"input": opengeode.HybridSolidInputFactory3D, "output": opengeode.HybridSolidOutputFactory3D, "load": opengeode.load_hybrid_solid3D, "save": opengeode.save_hybrid_solid3D},
            "PointSet2D": {"input": opengeode.PointSetInputFactory2D, "output": opengeode.PointSetOutputFactory2D, "load": opengeode.load_point_set2D, "save": opengeode.save_point_set2D},
            "PointSet3D": {"input": opengeode.PointSetInputFactory3D, "output": opengeode.PointSetOutputFactory3D, "load": opengeode.load_point_set3D, "save": opengeode.save_point_set3D},
            "PolygonalSurface2D": {"input": opengeode.PolygonalSurfaceInputFactory2D, "output": opengeode.PolygonalSurfaceOutputFactory2D, "load": opengeode.load_polygonal_surface2D, "save": opengeode.save_polygonal_surface2D},
            "PolygonalSurface3D": {"input": opengeode.PolygonalSurfaceInputFactory3D, "output": opengeode.PolygonalSurfaceOutputFactory3D, "load": opengeode.load_polygonal_surface3D, "save": opengeode.save_polygonal_surface3D},
            "PolyhedralSolid3D": {"input": opengeode.PolyhedralSolidInputFactory3D, "output": opengeode.PolyhedralSolidOutputFactory3D, "load": opengeode.load_polyhedral_solid3D, "save": opengeode.save_polyhedral_solid3D},
            "Section": {"input": opengeode.SectionInputFactory, "output": opengeode.SectionOutputFactory, "load": opengeode.load_section, "save": opengeode.save_section},
            "TetrahedralSolid3D": {"input": opengeode.TetrahedralSolidInputFactory3D, "output": opengeode.TetrahedralSolidOutputFactory3D, "load": opengeode.load_tetrahedral_solid3D, "save": opengeode.save_tetrahedral_solid3D},
            "TriangulatedSurface2D": {"input": opengeode.TriangulatedSurfaceInputFactory2D, "output": opengeode.TriangulatedSurfaceOutputFactory2D, "load": opengeode.load_triangulated_surface2D, "save": opengeode.save_triangulated_surface2D},
            "TriangulatedSurface3D": {"input": opengeode.TriangulatedSurfaceInputFactory3D, "output": opengeode.TriangulatedSurfaceOutputFactory3D, "load": opengeode.load_triangulated_surface3D, "save": opengeode.save_triangulated_surface3D},
            "VertexSet": {"input": opengeode.VertexSetInputFactory, "output": opengeode.VertexSetOutputFactory, "load": opengeode.load_vertex_set, "save": opengeode.save_vertex_set}}