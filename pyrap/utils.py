'''
Created on Nov 10, 2015

@author: nyga
'''
from collections import defaultdict
import traceback
import sys
import os


def currentframe():
    """Return the frame object for the caller's stack frame."""
    try:
        raise Exception()
    except:
        traceback.print_exc()
        return sys.exc_info()[2].tb_frame

if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(2)


def caller(tb=1):
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.
    """
    f = currentframe()
    #On some versions of IronPython, currentframe() returns None if
    #IronPython isn't run with -X:Frames.
    rv = "(unknown file)", 0, "(unknown function)"
    d = 0
    while hasattr(f, "f_code"):
        co = f.f_code
        rv = (co.co_filename, f.f_lineno, co.co_name)
        if d >= tb: break
        d += 1
        f = f.f_back
    return rv


def out(*args, **kwargs):
    rv = caller(kwargs.get('tb', 1))
    print('%s: l.%d: %s' % (os.path.basename(rv[0]), rv[1], ' '.join(map(str, args))))


def stop(*args, **kwargs):
    out(*args, **edict(kwargs) + {'tb': kwargs.get('tb', 1) + 1})
    sys.stdout.write('<press enter to continue>\r')
    eval(input())
    

def trace(*args, **kwargs):
    print('=== STACK TRACE ===')
    sys.stdout.flush()
    traceback.print_stack(file=sys.stdout)
    out(*args, **edict(kwargs) + {'tb': kwargs.get('tb', 1) + 1})
    sys.stdout.flush()
    
    
def stoptrace(*args, **kwargs):
    trace(**edict(kwargs) + {'tb': kwargs.get('tb', 1) + 1})
    stop(*args, **edict(kwargs) + {'tb': kwargs.get('tb', 1) + 1})

def ifnone(if_, else_, transform=None):
    '''
    Returns the condition if_ iff it is not None, or if a transformation is
    specified, transform(if_). Returns else_ if the condition is None.
    '''
    if if_ is None:
        return else_
    else:
        if transform is not None: return transform(if_)
        else: return if_

def ifnot(if_, else_, transform=None):
    '''
    Returns the condition if_ iff it evaluates to False, or if a transformation is
    specified, transform(if_). Returns else_ if the condition is None.
    '''
    if not bool(if_):
        return else_
    else:
        if transform is not None: return transform(if_)
        else: return if_

        
def allnone(it):
    return not ([1 for e in it if e is not None])


class edict(dict):
    '''
    Enhanced dict with some convenience methods such as dict addition and
    subtraction.
    
    :Example:
    
    >>> s = edict({'a':{'b': 1}, 'c': [1,2,3]})
    >>> r = edict({'x': 'z', 'c': 5})
    >>> print s
    {'a': {'b': 1}, 'c': [1, 2, 3]}
    >>> print r
    {'x': 'z', 'c': 5}
    >>> print s + r
    {'a': {'b': 1}, 'x': 'z', 'c': 5}
    >>> print s - r
    {'a': {'b': 1}}
    >>> print r
    {'x': 'z', 'c': 5}
    '''
    
    def __iadd__(self, d):
        self.update(d)
        return self
    
    def __isub__(self, d):
        for k in d: 
            if k in self: del self[k]
        return self
    
    def __add__(self, d):
        return type(self)({k: v for k, v in (self.items() + d.items())})
    
    def __sub__(self, d):
        return type(self)({k: v for k, v in self.items() if k not in d})
    
    
class RStorage(edict):
    '''
    Recursive extension of web.util.Storage that applies the Storage constructor
    recursively to all value elements that are dicts.
    '''
    __slots__ = []

    def __init__(self, d=None):
        if d is not None:
            for k, v in d.items(): self[k] = v
    
    def __setattr__(self, key, value):
        if key in self.__slots__:
            self.__dict__[key] = value
        else: 
            self[key] = value
            
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, rstorify(value))
            
    def __getattr__(self, key):
        if key in type(self).__slots__: 
            return self.__dict__[key]
        else:
            try:
                return self[key]
            except KeyError as k:
                raise AttributeError(k)
            
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)
            
    def __repr__(self):     
        return ('<%s ' % type(self).__name__) + dict.__repr__(self) + '>'
        
        
def rstorify(e):
    if type(e) is dict:
        return RStorage(d=e)
    elif type(e) in (list, tuple):
        return [rstorify(i) for i in e]
    else: return e
        
def jsonify(o):
    if hasattr(o, 'json'): 
        return o.json
    elif isinstance(o, dict):
        return {str(k): jsonify(v) for k, v in o.items()}
    elif type(o) in (list, tuple):
        return [jsonify(e) for e in o]
    elif isinstance(o, (int, float, bool, str, type(None))):
        return o
    else:
        raise TypeError('object of type "%s" is not jsonifiable: %s' % (type(o), repr(o)))
    
        
class BiMap:
    '''
    Bi-directional mapping.
    '''
    
    def __init__(self, values=None):
        self._fwd = {}
        self._bwd = {}
        self += values
        self.__iter__ = self._fwd.__iter__
        self.items = self._fwd.items
        self.keys = self._fwd.keys
        self.values = self._fwd.values
        
    def __iadd__(self, values):
        if type(values) in (list, tuple):
            for f, b in values: self[f:b]
        elif isinstance(values, (dict, BiMap)):
            for f, b in values.items():
                self[f:b]
        return self
    
    def __add__(self, values):
        newmap = BiMap(self)
        newmap += values
        return newmap
     
    def __getitem__(self, s):
        if type(s) is slice:
            if not s.start and s.stop: return self._bwd[s.stop]
            if s.start and not s.stop: return self._fwd[s.start]
            if s.start and s.stop:
                self._fwd[s.start] = s.stop
                self._bwd[s.stop] = s.start
            else: raise AttributeError('Slice argument for BiMap cannot be empty')
        else: return self._fwd[s]

    def __contains__(self, e):
        return e in self._fwd or e in self._bwd

    def __str__(self):
        return ';'.join([str(e) for e in list(self._fwd.items())])


class BitMask(BiMap):
    def __init__(self, *values):
        BiMap.__init__(self)
        self._count = 0
        for v in values:
            numval = 1 << self._count
            setattr(self, v, numval)
            self._count += 1
            self[numval:v]


def pparti(number, proportions):
    '''
    Partition a number into a sum of n integers, proportionally to the ratios given in 
    proportions. 
    
    The result is guaranteed to sun up to ``number``, so it is cleaned wrt.
    to numerical instabilities.
    '''
    Z = sum(proportions)
    percents = [float(p) / Z for p in proportions]
    result = [max(0, int(round(p * number))) for p in percents[:-1]]
    return result + [number - sum(result)]
    

def bind(**kwargs):
    def wrap_f(function):
        def probeFunc(frame, event, arg):
            if event == 'call':
                frame.f_locals.update(kwargs)
                frame.f_globals.update(kwargs)
            elif event == 'return':
                for key in kwargs:
                    kwargs[key] = frame.f_locals[key]
                sys.settrace(None)
            return probeFunc
        def traced(*args, **kwargs):
            sys.settrace(probeFunc)
            function(*args, **kwargs)
        return traced
    return wrap_f

if __name__ == '__main__':
    print(pparti(10, [.2, .2, .1, .5]))
