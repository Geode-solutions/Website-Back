import opengeode


def ObjectsList():
    return {"BRep": {"input": opengeode.BRepInputFactory, "output": opengeode.BRepOutputFactory},
            "EdgedCurve2D": {"input": opengeode.EdgedCurveInputFactory2D, "output": opengeode.EdgedCurveOutputFactory2D},
            "EdgedCurve3D": {"input": opengeode.EdgedCurveInputFactory3D, "output": opengeode.EdgedCurveOutputFactory3D},
            "Graph": {"input": opengeode.GraphInputFactory, "output": opengeode.GraphOutputFactory},
            "HybridSolidy3D": {"input": opengeode.HybridSolidInputFactory3D, "output": opengeode.HybridSolidOutputFactory3D},
            "PointSet2D": {"input": opengeode.PointSetInputFactory2D, "output": opengeode.PointSetOutputFactory2D},
            "PointSet3D": {"input": opengeode.PointSetInputFactory3D, "output": opengeode.PointSetOutputFactory3D},
            "PolygonalSurface2D": {"input": opengeode.PolygonalSurfaceInputFactory2D, "output": opengeode.PolygonalSurfaceOutputFactory2D},
            "PolygonalSurface3D": {"input": opengeode.PolygonalSurfaceInputFactory3D, "output": opengeode.PolygonalSurfaceOutputFactory3D},
            "PolyhedralSolid3D": {"input": opengeode.PolyhedralSolidInputFactory3D, "output": opengeode.PolyhedralSolidOutputFactory3D},
            "Section": {"input": opengeode.SectionInputFactory, "output": opengeode.SectionOutputFactory},
            "TetrahedralSolid3D": {"input": opengeode.TetrahedralSolidInputFactory3D, "output": opengeode.TetrahedralSolidOutputFactory3D},
            "TriangulatedSurface2D": {"input": opengeode.TriangulatedSurfaceInputFactory2D, "output": opengeode.TriangulatedSurfaceOutputFactory2D},
            "TriangulatedSurface3D": {"input": opengeode.TriangulatedSurfaceInputFactory3D, "output": opengeode.TriangulatedSurfaceOutputFactory3D},
            "VertexSet": {"input": opengeode.VertexSetInputFactory, "output": opengeode.VertexSetOutputFactory}}
