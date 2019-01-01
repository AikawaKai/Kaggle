import pandas as pd
import io, numpy as np


cities = pd.read_csv("./data/cities.csv", sep=",", index_col= ["CityId"])
print(cities.head())
cities1k = cities * 1000
print(cities1k.head())


def write_tsp(cities, filename, name='traveling-santa-2018-prime-paths'):
    with open(filename, 'w') as f:
        f.write('NAME : %s\n' % name)
        f.write('COMMENT : %s\n' % name)
        f.write('TYPE : TSP\n')
        f.write('DIMENSION : %d\n' % len(cities))
        f.write('EDGE_WEIGHT_TYPE : EUC_2D\n')
        f.write('NODE_COORD_SECTION\n')
        for row in cities.itertuples():
            f.write('%d %.11f %.11f\n' % (row.Index+1, row.X, row.Y))
        f.write('EOF\n')

write_tsp(cities1k, './data/cities1k.tsp')

def read_cities(filename='./data/cities.csv'):
    return pd.read_csv(filename, index_col=['CityId'])

class Tour:
    cities = read_cities()
    coords = (cities.X + 1j * cities.Y).values
    # penalized = ~cities.index.isin(sympy.primerange(0, len(cities)))

    def __init__(self, data):
        """Initializes from a list/iterable of indexes or a filename of tour in csv/tsplib/linkern format."""

        if type(data) is str:
            data = self._read(data)
        elif type(data) is not np.ndarray or data.dtype != np.int32:
            data = np.array(data, dtype=np.int32)
        self.data = data

        if (self.data[0] != 0 or self.data[-1] != 0 or len(self.data) != len(self.cities) + 1):
            raise Exception('Invalid tour')

    @classmethod
    def _read(cls, filename):
        data = open(filename, 'r').read()
        if data.startswith('Path'):  # csv
            return pd.read_csv(io.StringIO(data)).Path.values
        offs = data.find('TOUR_SECTION\n')
        if offs != -1:  # TSPLIB/LKH
            data = np.fromstring(data[offs+13:], sep='\n', dtype=np.int32)
            data[-1] = 1
            return data - 1
        else:  # linkern
            data = data.replace('\n', ' ')
            data = np.fromstring(data, sep=' ', dtype=np.int32)
            if len(data) != data[0] + 1:
                raise Exception('Unrecognized format in %s' % filename)
            return np.concatenate((data[1:], [0]))

    def info(self):
        dist = np.abs(np.diff(self.coords[self.data]))
        #penalty = 0.1 * np.sum(dist[9::10] * self.penalized[self.data[9:-1:10]])
        penalty = 0
        dist = np.sum(dist)
        return {'score': dist + penalty, 'dist': dist, 'penalty': penalty }

    def dist(self):
        return self.info()['dist']

    def score(self):
        return self.info()['score']

    def __repr__(self):
        return 'Tour: %s' % str(self.info())

    def to_csv(self, filename):
        pd.DataFrame({'Path': self.data}).to_csv(filename, index=False)


tour = Tour('C:\\Users\\marco\\linkern2.tour')
tour.to_csv("./submission_concorde7.csv")
