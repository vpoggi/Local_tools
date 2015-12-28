from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

class geomap:

  def __init__(self):

    # Defaults
    self.cfg = {
       'Bounds': [7., 36., 19., 48.],
       'FigSize': [6., 6.],
       'Background': ['esri','World_Terrain_Base',1500],
       'Grid': [5., 5.]}

    self.zo = 1

    '''
    Map boundary edges order:
    [LeftLowerLon,LeftLowerLat,UpperRightLon,UpperRightLat]

    Background sources:
    ESRI_Imagery_World_2D (MapServer)
    ESRI_StreetMap_World_2D (MapServer)
    I3_Imagery_Prime_World (GlobeServer)
    NASA_CloudCover_World (GlobeServer)
    NatGeo_World_Map (MapServer)
    NGS_Topo_US_2D (MapServer)
    Ocean_Basemap (MapServer)
    USA_Topo_Maps (MapServer)
    World_Imagery (MapServer)
    World_Physical_Map (MapServer)
    World_Shaded_Relief (MapServer)
    World_Street_Map (MapServer)
    World_Terrain_Base (MapServer)
    World_Topo_Map (MapServer)
    '''

  def baseplot(self):

    plt.figure(figsize = (self.cfg['FigSize'][0],
                          self.cfg['FigSize'][1]))

    # Basemap
    self.map = Basemap(self.cfg['Bounds'][0],
                       self.cfg['Bounds'][1],
                       self.cfg['Bounds'][2],
                       self.cfg['Bounds'][3],
                       resolution = 'h',
                       projection = 'cyl')

    # Background image
    if self.cfg['Background'][0] == 'etopo':
      self.map.etopo(zorder = self.zo)

    if self.cfg['Background'][0] == 'esri':
      self.map.arcgisimage(service = self.cfg['Background'][1],
                           xpixels = self.cfg['Background'][2],
                           zorder = self.zo)

    # Boundaries and lines
    self.map.drawcoastlines(linewidth = 0.5, zorder = self.zo+1)
    self.map.drawstates(linewidth = 0.5, zorder = self.zo+2)
    self.map.drawcountries(linewidth = 0.5, zorder = self.zo+3)
    self.map.drawrivers(linewidth = 0.1, color='b', zorder = self.zo+4)
    self.map.drawmapboundary(linewidth = 2, color='k', zorder = self.zo+5)

    # Parallels and meridians
    parallels = np.arange(-90, 90, self.cfg['Grid'][0])
    meridians = np.arange(0, 360., self.cfg['Grid'][1])
    self.map.drawparallels(parallels, labels = [1,0,0,0],
                           fontsize = 12, weight = 'normal',
                           zorder = self.zo+6)
    self.map.drawmeridians(meridians, labels = [0,0,0,1],
                           fontsize = 12, weight = 'normal',
                           zorder = self.zo+7)

    self.zo += 7

  def pointplot(self, lon, lat, makeup = ['o','y',5]):

    self.zo += 1

    x,y = self.map(lon,lat)
    self.map.plot(x, y, makeup[0],
                        color = makeup[1],
                        markersize = makeup[2],
                        zorder = self.zo)

  def show(self):

    plt.show(block = False)
    
  def savefig(self,pic_file):

    plt.savefig(pic_file, bbox_inches = 'tight', dpi = 300)