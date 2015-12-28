#---------------------------------------
# Base class for the csv catalogue.
# It contains an header list and a data
# structure (array of dictionaries) 

class catalogue():

  def __init__(self, header=[]):

    if not header:

      # Default header
      self.header = ['Year',
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
    else:

      # User defined header
      self.header = header

    # Initialise data structure
    self.data = []

  #---------------------------------------
  # Add and empty element to the catalogue
  # with a structure corresponding to
  # header list

  def add_empty_element(self):

    newitem = {}

    for key in self.header:
      newitem[key] = []

    self.data.append(newitem)

  #---------------------------------------
  # Method to inflate a catalogue object 
  # from reading a a CSV file.
  # Line separator and the number
  # of lines to skip can be prescribed

  def csv_import(self, csv_file, skipline=0, separator=','):

    f = open(csv_file, 'r')

    # Read and ignore header lines
    for i in range(0,skipline):
      f.readline()

    # Read data
    for i, line in enumerate(f):

      line = line.strip()
      line = line.split(separator)

      self.add_empty_element()

      for j, label in enumerate(self.header):

        self.data[i][label] = line[j]

    f.close()

  #---------------------------------------
  # Method to export a catalogue object
  # to csv format, with optional header and
  # separator format

  def csv_export(self, csv_file, write_header='yes',separator=','):

    dlen = len(self.data)

    f = open(csv_file, 'w')

    # Write header
    if write_header == 'yes':

      header = separator.join(self.header)
      f.write(header + '\n')

    # Write data
    for i,item in enumerate(self.data):

      data = separator.join([item[j] for j in self.header])

      if i < (dlen-1):
        f.write(data + '\n')
      else:
        f.write(data)

    f.close()

  #---------------------------------------
  # Method to extract a list of values
  # from the catalogue object

  def extract(self, key):

    enum = len(self.data)

    values = [self.data[i][key] for i in range(1,enum)]

    return values

  #---------------------------------------
  # Method to filter the catalogue by key.
  # (Key has to be a numerical value!)
  # Note that a new catalogue is created
  # in output

  def filter(self, key, dmin=[], dmax=[]):

    catsel = catalogue(self.header)

    enum = len(self.data)
    j = 0

    for i in range(1,enum):

      if float(self.data[i][key]) >= dmin and \
         float(self.data[i][key]) <= dmax:

        catsel.add_empty_element()

        for k in self.header:
          catsel.data[j][k] = self.data[i][k]

        j += 1

    return catsel
