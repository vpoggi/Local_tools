import libs.maptool as mp

m = mp.geomap()

m.cfg['Bounds'] = [10., -40., 60., 20.]
# m.cfg['Background']= ['etopo']
m.cfg['Background']= ['esri','World_Terrain_Base',1500]
m.cfg['Grid'] = [10., 10.]

m.baseplot()
m.pointplot(30., -10.)
m.show()
m.savefig('test.png')