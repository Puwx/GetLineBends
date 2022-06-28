def getAngle(a, b, c):
    #Credit to: https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def getBends(line_path):
    line = pd.DataFrame.spatial.from_featureclass(line_path)
    sr = arcpy.Describe(line_path).spatialreference
    geom = [i for i in line.loc[0,"SHAPE"].as_shapely.geoms][0]
    coords = geom.coords
    outPts = []
    for pt in range(2,len(coords)):
        p1,p2,p3 = coords[pt-2],coords[pt-1],coords[pt]
        ang = getAngle(p1,p2,p3)
        mid = arcpy.PointGeometry(arcpy.Point(*p2),spatial_reference=sr).WKT
        cleanAng = abs(180-ang)
        outPts.append([mid,ang,cleanAng,round(cleanAng,1)])
    return pd.DataFrame(outPts,columns=["WKT","ANGLE","SEC_ANGLE","APPRX_ANG"])
    
