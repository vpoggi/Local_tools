import numpy as np
import datetime as dt
import shapely.geometry as shp

#---------------------------------------
# Base class for the synthetic catalogue
# generation and manipulation

class catalogue():

  def __init__(self, cfg = []):

    if not cfg:
      # Initialise default values
      self.cfg = {'aValue' : 100.,
                  'bValue' : 1.,
                  'MinMag' : 4.,
                  'MaxMag' : 8.,
                  'Years' : 1.,
                  'Source' : [1., 1.],
                  'Depth': [0, 50],
                  'Date' : [1900,01,01,00,00,00]}

      print '>> Using default values'

    else:
      self.cfg = cfg

  #-------------------------------------
  # Synthetic catalogue generator

  def generate(self):

    # Initialise local variables

    a = self.cfg['aValue']
    b = self.cfg['bValue']
    mmin = self.cfg['MinMag']
    mmax = self.cfg['MaxMag']
    time = self.cfg['Years']
    date = self.cfg['Date']

    slen = len(self.cfg['Source'])

    if slen < 3:
      poly = self.cfg['Source']
      self.area = 0
      self.catlen = int(a*time)
    else:
      # poly = self.cfg['Area']+[self.cfg['Area'][0]]
      poly = shp.Polygon(self.cfg['Source'])
      self.area = poly.area
      self.catlen = int(a*time*self.area)

    zmin = np.min(self.cfg['Depth'])
    zmax = np.max(self.cfg['Depth'])

    #-----------------------------------
    # Magnitude distribution:
    # Derived as the inverse of the 
    # double-truncated cumulative GR

    Um = np.random.rand(self.catlen)

    C = 1.-(10.**(-b*(mmax-mmin)))

    # To check!
    self.magnitude = mmin-np.log10(1.-(Um*C))/b

    #-----------------------------------
    # Average interval time obtained
    # from the inverse of the cumulative
    # of the exponential distribution
    # (Poisson assumption)

    Ut = np.random.rand(self.catlen)

    dT = -np.log(1-Ut)/self.catlen

    T = np.cumsum(dT)

    # Seconds per year
    # (Not counting leap second years)
    secyear = time*365.*24.*60.*60.

    timeinsec = T*secyear

    #-----------------------------------
    # Conversion to calendar format.
    # eventtime is structured as:
    # [year,month,day,hour,minute,second]

    d0 = dt.datetime(int(date[0]),
                     int(date[1]),
                     int(date[2]),
                     int(date[3]),
                     int(date[4]),
                     int(date[5]))

    self.year = np.zeros(self.catlen)
    self.month = np.zeros(self.catlen)
    self.day = np.zeros(self.catlen)
    self.hour = np.zeros(self.catlen)
    self.minute = np.zeros(self.catlen)
    self.second = np.zeros(self.catlen)

    for i, s in enumerate(timeinsec):

      d1 = d0 + dt.timedelta(seconds=int(s))

      self.year[i] = np.array(d1.year)
      self.month[i] = np.array(d1.month)
      self.day[i] = np.array(d1.day)
      self.hour[i] = np.array(d1.hour)
      self.minute[i] = np.array(d1.minute)
      self.second[i] = np.array(d1.second)

    #-----------------------------------
    # Spatial distribution.
    # Three options available:
    # 1) single location
    # 2) Linear fault
    # 3) Source area
    # Note that the source area randomisation
    # is at the moment highly inefficient
    # and it has to be improved

    if slen == 1:
      ones = np.ones(self.catlen)
      self.longitude = poly[0][0]*ones
      self.latitude = poly[0][1]*ones

    elif slen == 2:
      x1 = poly[0][0]
      y1 = poly[0][1]
      x2 = poly[1][0]
      y2 = poly[1][1]

      dx = x2-x1
      dy = y2-y1

      R = np.random.rand(self.catlen)
      
      self.longitude = x1+dx*R
      self.latitude = y1+dy*R

    else:
      xmin, ymin, xmax, ymax = poly.bounds

      pnt_num = 0
      self.latitude = np.zeros(self.catlen)
      self.longitude = np.zeros(self.catlen)

      while pnt_num != self.catlen:

        X = np.random.uniform(xmin, xmax)
        Y = np.random.uniform(ymin, ymax)

        point = shp.Point(X, Y)

        if poly.contains(point):
          self.longitude[pnt_num] = X
          self.latitude[pnt_num] = Y
          pnt_num += 1

    #-----------------------------------
    # Depth distribution.
    # Non uniform distribution is pending,
    # but a workaround is to merge several
    # catalogue with different depths

    self.depth = np.random.uniform(zmin, zmax, self.catlen)

  #-------------------------------------
  # Completeness filter

  def completeness(self, comp_win):

    j = np.zeros(self.catlen, dtype=bool)

    for cw in comp_win:

      i = (self.magnitude >= cw[0]) & (self.magnitude < cw[1]) & \
          (self.year >= cw[2]) & (self.year < cw[3])

      j = j|i

    self.year = self.year[j]
    self.month = self.month[j]
    self.day = self.day[j]
    self.hour = self.hour[j]
    self.minute = self.minute[j]
    self.second = self.second[j]
    self.latitude = self.latitude[j]
    self.longitude = self.longitude[j]
    self.depth = self.depth[j]
    self.magnitude = self.magnitude[j]

    self.catlen = len(self.magnitude)

  #-------------------------------------
  # Merging catalogues

  def append(self, cat2):

    # Cleaning the configuration variable
    # to avoid misuse of the parameters
    self.cfg = {}

    # Appending the catalogue item
    self.year = np.append(self.year,cat2.year)
    self.month = np.append(self.month,cat2.month)
    self.day = np.append(self.day,cat2.day)
    self.hour = np.append(self.hour,cat2.hour)
    self.minute = np.append(self.minute,cat2.minute)
    self.second = np.append(self.second,cat2.second)
    self.latitude = np.append(self.latitude,cat2.latitude)
    self.longitude = np.append(self.longitude,cat2.longitude)
    self.depth = np.append(self.depth,cat2.depth)
    self.magnitude = np.append(self.magnitude,cat2.magnitude)

    self.catlen = self.catlen + cat2.catlen
    self.area = self.area + cat2.area

  #-------------------------------------
  # I/O methods

  def loadcfg(self):

    print 'WORK IN PROGRESS'


  def export(self, csv_file, write_header='yes',separator=','):

    header = ['Year',
              'Month',
              'Day',
              'Hour',
              'Minute',
              'Second',
              'Latitude',
              'Longitude',
              'Depth',
              'Magnitude',
              'Sigma']

    f = open(csv_file, 'w')

    # Write header
    if write_header == 'yes':

      header = separator.join(header)
      f.write(header + '\n')

    # Write data
    for i in range(self.catlen):

      data = separator.join(['{:.0f}'.format(self.year[i]),
                             '{:.0f}'.format(self.month[i]),
                             '{:.0f}'.format(self.day[i]),
                             '{:.0f}'.format(self.hour[i]),
                             '{:.0f}'.format(self.minute[i]),
                             '{:.0f}'.format(self.second[i]),
                             '{:.4f}'.format(self.latitude[i]),
                             '{:.4f}'.format(self.longitude[i]),
                             '{:.2f}'.format(self.depth[i]),
                             '{:.2f}'.format(self.magnitude[i]),
                             '1.00'])

      if i < (self.catlen-1):
        f.write(data + '\n')
      else:
        f.write(data)

    f.close()
