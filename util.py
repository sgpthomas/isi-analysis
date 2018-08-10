from functools import wraps
import errno
import os
import signal
import numpy as np
from pmlb import fetch_data
import warnings

# from progressbar import ProgressBar, Percentage, Bar, ETA
import itertools
from random import randint
import traceback

class TimeoutError(Exception):
    pass

class timeout(object):
    def __init__(self, seconds):
        self.seconds = seconds

    def __call__(self, f):
        def _handle_timeout(signum, fname):
            raise TimeoutError()

        def wrapped_f(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(self.seconds)
            try:
                result = f(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wrapped_f

def make_progressbar(val):
    return ProgressBar(widgets=[Percentage(),
                                Bar(left=" |", right="| "),
                                ETA()],
                       maxval=val)

def list_to_idx_dict(lst):
    res = {}
    for i, x in enumerate(lst):
        res[i] = x
    return res

def dict_mean(d):
    lst = []
    for key in d:
        lst.append(d[key])
    return np.mean(lst)

def filter_dict(f, d):
    return { k: v for k, v in d.items() if f(k, v) }

def map_dict(f, d):
    return { k: f(v) for k, v in d.items() }

def map2_dict(f, d):
    res = {}
    for k, v in d.items():
        tup = f(k, v)
        res[tup[0]] = tup[1]
    return res

def flatten(l):
    return [item for sublist in l for item in sublist]

def filter_dataframe_by_column(f, data):
    return data[[col for col in data.columns if
                 len(list(filter(lambda x: f(x), data[col].values))) == 0]]

def merge_dicts(d1, d2):
    if d1 == {}:
        return d2
    if d1.keys() != d2.keys():
        raise Exception("Keys must match: {} != {}".format(d1.keys(), d2.keys()))
    for k in d1:
        d1[k] += d2[k]
    return d1

def product_dict(d):
    keys = d.keys()
    vals = d.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))

def average(f, n_times):
    res = []
    for n in range(n_times):
        res.append(f())
    return np.mean(res)

def unique_values(l):
    unique = []
    for item in l:
        if item not in unique:
            unique.append(item)
    unique.sort()
    return unique

def fold_list(f, acc, l):
    if l == []:
        return acc
    else:
        acc = f(acc, l[0])
        return fold_list(f, acc, l[1:])

def randomize_labels(y):
    unique = unique_values(y)
    res = [unique[randint(0, len(unique)-1)] for _ in y]
    return np.array(res)

def vectorize(x):
    return list(map(lambda v: [v], x))

def fetch_data_Xy(name):
    return fetch_data(name, return_X_y=True, local_cache_dir="~/Isi/pmlb-cache")

def progress_loop_wrapper(f, things, warn=False, show_error=False):
    results = {}
    for i, th in enumerate(things):
        print("{}/{} -> ".format(i+1, len(things)), end='', flush=True)
        try:
            with warnings.catch_warnings():
                if not warn: warnings.simplefilter("ignore")
                f(th, results)
        except Exception as e:
            if show_error:
                traceback.print_exc(e)
                return None
            else:
                print("Failed!")
    return results

def list_diff(l1, l2):
    return [x for x in l1 if x not in l2]

def dictToString(d):
    d = dict(sorted(d.items()))
    res = []
    for k, v in d.items():
        res.append("{}={}".format(k, v))
    return ",".join(res)

def stringToDict(pString):
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

def frequency(l):
    freq = {}
    for item in l:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return dict(sorted(freq.items(), key=lambda t: t[1], reverse=True))
