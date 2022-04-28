import opengeode_inspector as inspector

def ObjectsList(model):
    return {"BRep": {"is_valid": inspector.BRepTopologyInspector(model).brep_topology_is_valid(), "inspect": inspector},
            "CrossSection": {"is_valid": inspector.SectionTopologyInspector(model).section_topology_is_valid(), "inspect": inspector},
            "EdgedCurve2D": {"is_valid": inspector.EdgedCurveColocation2D(model).mesh_has_colocated_points(), "inspect": inspector.EdgedCurveColocation2D(model).colocated_points_groups()},
            "EdgedCurve3D": {"is_valid": inspector.EdgedCurveColocation3D(model).mesh_has_colocated_points(), "inspect": inspector.EdgedCurveColocation3D(model).colocated_points_groups()},
            "Graph": {"is_valid":inspector},
            "HybridSolid3D": {"is_valid":inspector},
            "PointSet2D": {"is_valid":inspector.PointSetColocation2D},
            "PointSet3D": {"is_valid":inspector.PointSetColocation3D},
            "PolygonalSurface2D": {"is_valid":inspector},
            "PolygonalSurface3D": {"is_valid":inspector},
            "PolyhedralSolid3D": {"is_valid":inspector},
            "RegularGrid2D": {"is_valid":inspector},
            "RegularGrid3D": {"is_valid":inspector},
            "Section": {"is_valid":inspector.SectionTopologyInspector},
            "StructuralModel": {"is_valid":inspector},
            "TetrahedralSolid3D": {"is_valid": inspector},
            "TriangulatedSurface2D": {"is_valid": inspector},
            "TriangulatedSurface3D": {"is_valid": inspector},
            "VertexSet": {"is_valid": inspector}}