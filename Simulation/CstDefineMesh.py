def CstDefineMesh(mws, steps_per_box_near, steps_per_box_far):
    mesh = mws.Mesh
    mesh_settings = mws.MeshSettings

    mesh.MeshType("Tetrahedral")
    mesh.SetCreator("High Frequency")

    mesh_settings.SetMeshType("Tet")
    mesh_settings.Set("Version", 1)
    # MAX CELL - WAVELENGTH REFINEMENT
    mesh_settings.Set("StepsPerWaveNear", "4")
    mesh_settings.Set("StepsPerWaveFar", "4")
    mesh_settings.Set("PhaseErrorNear", "0.02")
    mesh_settings.Set("PhaseErrorFar", "0.02")
    mesh_settings.Set("CellsPerWavelengthPolicy", "automatic")
    # MAX CELL - GEOMETRY REFINEMENT
    mesh_settings.Set("StepsPerBoxNear", str(steps_per_box_near))
    mesh_settings.Set("StepsPerBoxFar", str(steps_per_box_far))
    mesh_settings.Set("ModelBoxDescrNear", "maxedge")
    mesh_settings.Set("ModelBoxDescrFar", "maxedge")
    # MIN CELL
    mesh_settings.Set("UseRatioLimit", "0")
    mesh_settings.Set("RatioLimit", "100")
    mesh_settings.Set("MinStep", "0")
    # MESHING METHOD
    mesh_settings.SetMeshType("Unstr")
    mesh_settings.Set("Method", "0")

    mesh_settings.SetMeshType("Tet")
    mesh_settings.Set("CurvatureOrder", "1")
    mesh_settings.Set("CurvatureOrderPolicy", "automatic")
    mesh_settings.Set("CurvRefinementControl", "NormalTolerance")
    mesh_settings.Set("NormalTolerance", "22.5")
    mesh_settings.Set("SrfMeshGradation", "1.5")
    mesh_settings.Set("SrfMeshOptimization", "1")

    mesh_settings.SetMeshType("Unstr")
    mesh_settings.Set("UseMaterials", "1")
    mesh_settings.Set("MoveMesh", "0")

    mesh_settings.SetMeshType("All")
    mesh_settings.Set("AutomaticEdgeRefinement", "0")

    mesh_settings.SetMeshType("Tet")
    mesh_settings.Set("UseAnisoCurveRefinement", "1")
    mesh_settings.Set("UseSameSrfAndVolMeshGradation", "1")
    mesh_settings.Set("VolMeshGradation", "1.5")
    mesh_settings.Set("VolMeshOptimization", "1")

    mesh_settings.SetMeshType("Unstr")
    mesh_settings.Set("SmallFeatureSize", "0")
    mesh_settings.Set("CoincidenceTolerance", "1e-06")
    mesh_settings.Set("SelfIntersectionCheck", "1")
    mesh_settings.Set("OptimizeForPlanarStructures", "0")

    mesh.SetParallelMesherMode("Tet", "maximum")
    mesh.SetMaxParallelMesherThreads("Tet", "1")