from util import *
import itertools

class Data(object):
    def __init__(self, df):
        self.data = df

    def _dictToString(self, d):
        d = dict(sorted(d.items()))
        res = []
        for k, v in d.items():
            res.append("{}={}".format(k, v))
        return ",".join(res)

    def _stringToDict(self, pString):
        if pString == "":
            return {}
        else:
            d = {}
            for s in pString.split(','):
                parts = s.split('=')
                key, value = parts[0], parts[1]
                if value == 'True':
                    value = True
                elif value == 'False':
                    value = False
                elif value == 'None':
                    value = None
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                d[key] = value
            return d

    def sortByParam(self, param):
        def f(df):
            res = []
            for i in df.index:
                res.append(self._stringToDict(df.loc[i, 'parameters'])[param])
            return res
        new = self.data.assign(sort = f(self.data))
        return Data(new.sort_values('sort').drop('sort', axis=1).reset_index(drop=True))

    def allCombos(self):
        paramStrings = list(self.data['parameters'])
        unique = {}
        for pStr in paramStrings:
            d = self._stringToDict(pStr)
            for k, v in d.items():
                if k in unique:
                    unique[k].add(v)
                else:
                    unique[k] = set([v])
        return unique

    def varyAlong(self, key):
        combos = self.allCombos()
        saved = combos[key]
        del combos[key]
        res = []
        for k in combos:
            inte = []
            for v in combos[k]:
                inte.append((k, v))
            res.append(inte)

        allStrings = []
        for c in (itertools.product(*res)):
            starter = dict(c)

            res = []
            for v in saved:
                starter[key] = v
                res.append(self._dictToString(starter))
            allStrings.append(res)
        return allStrings

    def filterAlong(self, key):
        datas = []
        for i, combo in enumerate(self.varyAlong(key)):
            datas.append((Data(self.data[self.filterByP(combo)]).sortByParam(key), i))
        return datas

    def holdConstant(self, key, value):
        params = list(self.data['parameters'])
        res = []
        for p in params:
            d = self._stringToDict(p)
            if key in d:
                if d[key] == str(value):
                    res.append(d)
        return unique_values(list(map(self._dictToString, res)))

    def filterByP(self, p):
        res = []
        for i in self.data.index:
            res.append(self.data.loc[i]['parameters'] in p)
        return res
