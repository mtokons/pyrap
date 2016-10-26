'''
Created on Oct 18, 2015

@author: nyga
'''
import random
import string
from colorsys import hsv_to_rgb, rgb_to_hsv
from PIL import Image as PILImage
import os
from _pyio import StringIO, BytesIO
from web.utils import storify, Storage
import threading
from pyrap.utils import BiMap, out, BitMask, stop
from pyrap.constants import FONT


class Event(object):
    
    def __init__(self):
        self._listeners = []
        self._wait = threading.Condition()
        
    def __iadd__(self, l):
        if l not in self._listeners:
            self._listeners.append(l)
        return self

    def __isub__(self, l):
        self._listeners.remove(l)
        return self

    def __contains__(self, l):
        return l in self._listeners

    def addall(self, listeners):
        if listeners is None: return self
        if type(listeners) is not list: listeners = [listeners]
        for l in listeners: self += l
        return self
            
    def notify(self, *args, **kwargs):
        with self._wait: self._wait.notify_all()
        for listener in self._listeners: self._notify(listener, *args, **kwargs)
        
    def _notify(self, listener, *args, **kwargs):
        raise Exception('Not implemented.')
    
    def wait(self):
        with self._wait: self._wait.wait()
    
    def __iter__(self):
        for l in self._listeners: yield l


    
class ValueChanged(Event):
    
    def _notify(self, listener, var, caller):
        listener(var, caller)


class DirtyState(Event):
    
    def _notify(self, listener, var, caller):
        listener(var, var.dirty, caller)


class VarCompound(object):
    
    def __init__(self, *vars):
        self.vars = vars
        
    @property
    def dirty(self):
        for v in self.vars:
            if v.dirty: return True
        return False
    
    def clean(self):
        for v in self.vars: v.clean()
        
    def all_defined(self):
        for v in self.vars:
            if v.value is None: return False
        return True
    
    def all_none(self):
        for v in self.vars:
            if v.value is not None: return False
        return True
        

class Var(object):
    '''
    Represents an abstract variable with a listen/notification interface,
    dirty flags, history, undo and redo functionality, and more.
    '''
    
    def __init__(self, value=None, track=False, typ=None, on_change=None, on_dirty=None):
        self.type = typ
        self._history = track
        self._values = [self._getval(value)]
        self._pointer = 0
        self.on_change = ValueChanged().addall(on_change)
        self.on_dirty = DirtyState().addall(on_dirty)
        self._init = self.value

    def __nonzero__(self):
        return bool(self.value)
    
    
    def _getval(self, other):
        return other.value if type(other) == type(self) else other
        
    @property
    def value(self):
        return self.get()
    
    @value.setter
    def value(self, v):
        self.set(v)
        
    @property
    def prev(self):
        if not self.hasprev:
            raise Exception('Variable has no previous value.')
        return self._values[self._pointer-1]
    
    @property
    def succ(self):
        if not self.hassucc:
            raise Exception('Variable has no succeeding value.') 
        return self._values[self._pointer+1]
    
    @property
    def hasprev(self):
        return self._pointer > 0

    @property
    def hassucc(self):
        return len(self._values) <= self._pointer

    def get(self):
        return self._values[self._pointer]

    def set(self, v, caller=None):
        v = self._getval(v)
        if v != self.value:
            dirty = self.dirty
            if self._history:
                self._pointer += 1
                self._values = self._values[:self._pointer] + [v]
            else:
                self._values[self._pointer] = v
            dirty = dirty != self.dirty
            self.on_change.notify(self, caller)
            if dirty: self.on_dirty.notify(self, caller)

    @property
    def dirty(self):
        return self._init != self.value
    
    @property
    def canundo(self):
        return self._pointer > 0
    
    @property
    def canredo(self):
        return self._pointer < len(self._values) - 1
            
    def undo(self, caller=None):
        if not self.canundo:
            raise Exception('There are no operations to undo.')
        dirty = self.dirty
        self._pointer -= 1
        dirty = dirty != self.dirty
        self.on_change.notify(self, caller)
        if dirty: self.on_dirty.notify(self, caller)
        return self
    
    def redo(self, caller=None):
        if not self.canredo:
            raise Exception('There are no operations to redo')
        dirty = self.dirty
        self._pointer += 1
        dirty = dirty != self.dirty
        self.on_change.notify(self, caller)
        if dirty: self.on_dirty.notify(self, caller)
        return self
    
    def __call__(self):
        return self.value
    
    def bind(self, var):
        if not type(var) is type(self):
            raise Exception('Can only bind variables of the same type')
        def set_mine(other, c):
            if c is self: return
            self.set(other.value, self)
        def set_other(me, c):
            if c is var: return
            var.set(me.value, var)
        var.on_change += set_mine
        self.on_change += set_other
        self.set(var.value, self)
    
    def clean(self):
        self._init = self.value
        
    def reset(self):
        self._values = [self.value]
        self._pointer = 0
        
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return '<%s[%s] at %s : %s>' % (self.__class__.__name__, type(self.value).__name__, hex(hash(self)), str(self.value))
    

class BitField(Var):
    '''
    A variable representing a field of bit flags.
    '''
    
    class _iterator():
        def __init__(self, v):
            self._v = v
        
        def next(self):
            if not self._v: raise StopIteration()
            b = self._v & (~self._v+1)
            self._v ^= b
            return b
        
        def __iter__(self): return self
    
    def setbit(self, bit, setorunset):
        if setorunset: self |= bit
        else: del self[bit]
        return self
    
    def __ior__(self, bits):
        self.value |= self._getval(bits)
        return self 
    
    def __or__(self, o):
        return self.value | self._getval(o)
    
    def __ror__(self, o):
        return self | o

    def __invert__(self):
        return ~self.value

    def __iand__(self, o):
        self.value = self.value & self._getval(o)
        return self
    
    def __and__(self, o):
        return self.value & self._getval(o)
    
    def __rand__(self, o):
        return self & o
    
    def __contains__(self, bits):
        if type(bits) in (list, tuple):
            return all([self._getval(b) in self for b in bits])
        else:
            return bool(self.value & self._getval(bits))
        
    def __delitem__(self, bits):
        if type(bits) in (list, tuple):
            newval = self.value
            for b in bits:
                newval &= ~self._getval(b)
            self.value = newval
        else:
            self.value = self.value & ~self._getval(bits) 
            
    def __iter__(self):
        return self._iterator(self.value)
         
    def __eq__(self, o):
        return self.value == self._getval(o)
    
    def __ne__(self, o):
        return not self == o
         
    def __str__(self):
        return bin(self.value)
    
    def readable(self, bitmask):
        return ' | '.join([bitmask[b] for b in self])
    
    
class BoolVar(Var):
    '''
    Represents a boolean variable.
    '''
    
    def __iand__(self, o):
        self.value = bool(self) and o
        return self
    
    def __ior__(self, o):
        self.value = bool(self) or o
        return self
    
    
    
class NumVar(Var):
    '''
    A variable representing a numeric value.
    '''    


    def __add__(self, o):
        return self.value + self._getval(o)
    
    def __radd__(self, o):
        return self + o
     
    def __sub__(self, o):
        return self.value - self._getval(o)
    
    def __rsub__(self, o):
        return self - o
     
    def __div__(self, o):
        return float(self.value) / self._getval(o)
    
    def __floordiv__(self, o):
        return self.value / self._getval(o)
    
    def __rdiv__(self, o):
        return o / self.value
     
    def __mul__(self, o):
        return self.value * self._getval(o)
    
    def __rmul__(self, o):
        return self * o
     
    def __iadd__(self, o):
        self.set(self + o)
        return self
         
    def __isub__(self, o):
        self.set(self.value - o)
        return self
     
    def __idiv__(self, o):
        self.set(self.value / o)
        return self
     
    def __imul__(self, o):
        self.set(self.value * o)
        return self
    
    def __eq__(self, o):
        return self.value == self._getval(o)
    
    def __ne__(self, o):
        return not self == o
    
    def round(self):
        return int(round(self.value))
    

class StringVar(Var):
    '''
    A variable representing a string.
    '''
    
    def __add__(self, o):
        return self.value + self._getval(o)
    
    def __radd__(self, o):
        return self._getval(o) + self.value
    
    def __iadd__(self, o):
        self.set(self + o)
        return self
    
    def __eq__(self, o):
        return self.value == self._getval(o)
    
    def __ne__(self, o):
        return not self == o
    
    
class BoundedDim(object):
    
    def __init__(self, _min, _max, value=None):
        self._min = Var(_min)
        self._max = Var(_max)
        self._value = Var(value)
        self.clean()
        
    def __call__(self):
        return self.value
        
    @property
    def min(self):
        return self._min()
    
    @min.setter
    def min(self, m):
        if m is not None and self.min is not None:
            m = max(m, self.min)
        self._min.set(m)
        if m == self.max:
            self._value.set(m)
        
    @property
    def max(self):
        return self._max()  
    
    @max.setter
    def max(self, m):
        if m is not None and self.max is not None:
            m = min(m, self.max)
        self._max.set(m)
        if m == self.min:
            self._value.set(m)
        
    @property
    def value(self):
        if self.min == self.max: return self.min
        return self._value()
        
    @value.setter
    def value(self, v):
        if v is not None:
            v = min(self.max, max(self.min, v))
#             if self.min is not None and self.min > v:
#                 raise ValueError('Value must not be smaller than minimum value: min: %s, value: %s' % (self.min, v))
#             if self.max is not None and self.max < v:
#                 raise ValueError('Value must not be larger than maximum value.')
        self._value.set(v)
        return self.value
        
    @property
    def dirty(self):
        return self._min.dirty or self._max.dirty or self._value.dirty
    
    def clean(self):
        self._min.clean()
        self._max.clean()
        self._value.clean()
    
    def __str__(self):
        return '<Dim[%s < %s < %s]>' % (self.min, self.value, self.max)
        

class Dim(object):
    '''
    Represents an abstract dimension value.
    '''
    
    def __init__(self, value):
        if value is None or type(value) not in (float, int):
            raise Exception('Illegal value for a dimension: %s' % repr(value))
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, v):
        self._value = v
        return self.value
        
    def __gt__(self, o):
        o = parse_value(o)
        return self._value > (o.value if isinstance(o, Dim) else o)
    
    def __lt__(self, o):
        o = parse_value(o)
        return self._value < (o.value if isinstance(o, Dim) else o)
    
    def __le__(self, o):
        o = parse_value(o)
        return self._value <= (o.value if isinstance(o, Dim) else o)
    
    def __ge__(self, o):
        o = parse_value(o)
        return self._value >= (o.value if isinstance(o, Dim) else o)
    
    def __eq__(self, o):
        o = parse_value(o)
        return self._value == (o.value if isinstance(o, Dim) else o)
    
    def __ne__(self, o):
        return not self == o
    
    def __add__(self, s):
        s = parse_value(s)
        if isinstance(s, Percent):
            return self + s.of(self.value)
        elif isinstance(s, type(self)):
            return self + s.value
        else:
            return type(self)(self.value + s)
        
    def __radd__(self, s):
        return self + s
    
    def __rsub__(self, s):
        return s - self.value
        
    def __sub__(self, s):
        s = parse_value(s)
        if isinstance(s, Percent):
            return self - s.of(self.value)
        elif isinstance(s, type(self)):
            return self - s.value
        else:
            return type(self)(self.value - s)
        
    def __mul__(self, t):
        t = parse_value(t)
        if isinstance(t, type(self)):
            return self * t.value
        else:
            return type(self)(self.value * t)
    
    def __rmul__(self, t):
        return self * t
        
    def __str__(self):
        return str(self._value)
        
    def __repr__(self):
        return '<%s[%s] at 0x%x>' % (type(self).__name__, str(self), hash(self))

            
    
class Pixels(Dim):
    '''
    Represents a dimension of pixel units.
    '''
    
    def __init__(self, v):
        if isinstance(v, basestring):
            v = v.strip()
            if v.endswith('px'):
                Dim.__init__(self, int(v[:-2]))
            else:
                raise Exception('Illegal number format: %s' % v)
        elif isinstance(v, Dim):
            Dim.__init__(self, v.value)
        else:
            Dim.__init__(self, v)

    def __div__(self, d):
        s = parse_value(d)
        return px(int(round(self.value / (s.value if type(d) == Pixels else d))))
    
    def __add__(self, o):
        return px(int(round(Dim.__add__(self, o).value)))
    
    def __sub__(self, o):
        return px(int(round(Dim.__sub__(self, o).value)))

    def __mul__(self, o):
        return px(int(round(Dim.__mul__(self, o).value)))
    
    def __str__(self):
        return '%spx' % self._value

    def __call__(self):
        return self.value

    def num(self):
        return self._num
    
#     @property
#     def json(self):
#         return self.value
    
    
def px(v):
    ''' Creates a new pixel dimension with the value v.'''
    if type(v) is Pixels: v = v.value
    return Pixels(v)


class Percent(Dim):
    '''Represents an abstract percentage value.'''
    
    def __init__(self, v):
        if isinstance(v, basestring):
            v = v.strip()
            if v.endswith('%'):
                Dim.__init__(self, float(v[:-1]))
            else:
                raise Exception('Illegal number format: %s' % v)
        else:
            Dim.__init__(self, v)
            
    def of(self, v):
        if type(v) is float:
            return self.value * v / 100.
        if type(v) is int:
            return int(round(self.value * v / 100.))
        if isinstance(v, basestring):
            v = parse_value(v)
        if isinstance(v, Pixels):
            return Pixels(int(round((v.value * self._value / 100.))))
        return type(v)((v.value if isinstance(v, Dim) else v) * self._value / 100.)
            
    def __str__(self):
        return '%f%%' % self._value
    
    @property
    def float(self):
        return self.value / 100.
    

def pc(v):
    ''' Creates a new percentage dimension with the value v.'''
    return Percent(v)
            
        
def color(c):
    if isinstance(c, Color): return c
    return Color(c)
    
class Color(object):
    
    names = {'red': '#5c6bc0', 
             'green': '#0f9d58', 
             'blue': '#4285f4',
             'gray': '#CCC', 
             'grey': '#CCC', 
             'white': '#FFF', 
             'yellow': '#f4b400', 
             'transp': '#FFFFFF00',
             'cyan': '#00acc1',
             'purple': '#ab47bc',
             'orange': '#ff7043'}
    
    
    def __init__(self, html=None, rgb=None, hsv=None, fct=None, alpha=None):
        if sum([1 for e in (html, rgb, hsv) if e is not None]) != 1:
            raise Exception('Need precisely one color value argument')
        if fct is not None:
            if fct.name == 'rgb': rgb = fct.args
            elif fct.name == 'hsv': hsv = fct.args
            else: raise Exception('Unknown color value function: %s' % str(fct))
        if html is not None:
            if html in Color.names: html = Color.names[html]
            if html.startswith('#'):
                if len(html) < 5: html += html[1:] # for short notations like #ccc
                self._r, self._g, self._b = int(html[1:3], base=16) / 255., int(html[3:5], base=16) / 255., int(html[5:7], base=16) / 255.
                self._a = float(html[7:9]) / 255. if len(html) > 7 else 1.
            else: raise Exception('Illegal color value: %s' % html)
        elif rgb is not None:
            self._r, self._g, self._b = rgb[:3]
            self._a = rgb[3] if len(rgb) > 3 else 1.
        elif hsv is not None:
            self._r, self._g, self._b = hsv_to_rgb(*hsv[:3])
            self._a = hsv[3] if len(hsv) > 3 else 1.
        else: raise Exception('Illegal color value: %s' % ' '.join(map(str, (html, rgb, hsv, fct, alpha))))
        if alpha is not None: self._a = alpha
    
    @property
    def red(self):
        return self._r
    
    @property
    def green(self):
        return self._g
    
    @property
    def blue(self):
        return self._b

    @property
    def hue(self):
        return rgb_to_hsv(*self.rgb)[0]
    
    @property
    def saturation(self):
        return rgb_to_hsv(*self.rgb)[1]
    
    @property
    def value(self):
        return rgb_to_hsv(*self.rgb)[2]
        
    @property
    def alpha(self):
        return self._a
        
    @property
    def rgb(self):
        return (self._r, self._g, self._b)
    
    @property
    def rgba(self):
        return (self._r, self._g, self._b, self._a)
    
    @property
    def hsv(self):
        return rgb_to_hsv(self._r, self._g, self._b)
        
    @property
    def html(self):
        return '#%.2x%.2x%.2x' % tuple([int(round(255 * x)) for x in self.rgb])
    
    @property
    def htmla(self):
        return self.html + '%.2x' % int(round((self._a * 255.)))
        
    def __str__(self):
        return self.htmla
    
    def __repr__(self):
        return '<Color[%s] at 0x%x>' % (str(self), hash(self))
    
    def __eq__(self, o):
        if isinstance(o, basestring):
            o = Color(html=o)
        return self.htmla == o.htmla
        
    def __ne__(self, o):
        return not self == o
    
    def darker(self, scale=.1):
        hsv = self.hsv
        return Color(hsv=(hsv[0], hsv[1] + (1 - hsv[1]) * scale, hsv[2] - hsv[2] * scale), alpha=self.alpha)
    
    def brighter(self, scale=.1):
        hsv = self.hsv
        return Color(hsv=(hsv[0], hsv[1] - hsv[1] * scale, hsv[2] + (1 - hsv[2]) * scale), alpha=self.alpha)
    
def parse_value(v, default=None):
    if isinstance(v, basestring):
        if v.endswith('px'): return Pixels(v)
        elif v.endswith('%'): return Percent(v)
        elif v.startswith('#'): return Color(v)
    else: 
        return v if (default is None or v is None or type(v) is default) else default(v)
    
        
class Font(object):
    
    def __init__(self, family='Arial', size='12px', style=FONT.NONE):
        family = [family] if type(family) is not list else family
        self._family = [f.strip('"\'') for f in family] 
        self._size = parse_value(size, Pixels)
        self._style = BitField(style, track=False)
        
    @property
    def bf(self):
        return FONT.BF in self._style
    
    @property
    def it(self):
        return FONT.IT in self._style
    
    @property
    def style(self):
        return self._style
    
    @property
    def family(self):
        return self._family
     
    @property
    def size(self):
        return self._size    

    def __str__(self):
        s = []
        s.append(str(self.size))
        if self.bf: s.append('bold')
        if self.it: s.append('italic')
        s.append(reduce(str.__add__, ', '.join([(('"%s"' % f) if ' ' in f else f) for f in self._family])))
        return ' '.join(s)

    def __repr__(self):
        return '<Font[%s] at 0x%x>' % (str(self), hash(self))


class Image(object):
    
    def __init__(self, filepath):
        self._img = None
        self._filepath = filepath
        self.load()
        with open(filepath) as f: self._content = f.read()
        self.close() 
        
    def load(self):
        self._img = PILImage.open(self._filepath)
        return self
        
    def close(self):
        if self._img is not None:
            self._img.close()
            
    @property
    def content(self):
        return str(self._content)
        
    @property
    def filename(self):
        return os.path.basename(self._filepath)
        
    @property
    def fileext(self):
        return self._filepath.split('.')[-1]
        
    @property
    def width(self):
        return px(self._img.size[0])
    
    @width.setter
    def width(self, w):
        self.resize(width=w)
    
    @property
    def height(self):
        return px(self._img.size[1])
    
    @height.setter
    def height(self, h):
        self.resize(height=h)
    
    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, s):
        w, h = s
        self.resize(width=w, height=h)
    
    def __repr__(self):
        return '<Image[%sx%s] "%s" at 0x%x>' % (self.width, self.height, self.filename, hash(self))
    
    def __str__(self):
        return '<Image[%sx%s] "%s">' % (self.width, self.height, self.filename)

    def resize(self, width=None, height=None):
        '''
        Scales this image according to the given parameters.
        
        If both ``width`` and ``height`` are given, the image is scaled accordingly.
        If only one of them is specified, the other one is computed proportionally.
        
        Both ``width`` and ``height`` can be either ``str``, ``int``, :class:`pyrap.Pixels`,
        or :class:`pyrap.Percent` values. If ``int``, they will be treated as pixel values
        
        :return:     this image instance.
        '''
        w = self.width
        h = self.height
        ratio = float(h.value) / float(w.value)
        # if either of them is int, convert to pixels by default
        if type(width) is int:
            width = px(width)
        if type(height) is int:
            height = px(height)
        # if either of them is string, parse the value
        if isinstance(width, basestring):
            width = parse_value(width)
        if isinstance(height, basestring):
            height = parse_value(height)
        if isinstance(width, Percent):
            w = width.of(w)
        else: w = width
        if isinstance(height, Percent):
            h = height.of(h)
        else:
            h = height
        if height is None:
            h = w * ratio
        elif width is None:
            w = h / ratio
        self._img = PILImage.open(self._filepath)
        self._img = self._img.resize((w.value, h.value), PILImage.LANCZOS)
        stream = BytesIO()
        self._img.save(stream, format=self.fileext)
        self._content = str(stream.getvalue())
        stream.close()
        return self

        
        

if __name__ == '__main__':
    
    print Color('#0000ff')
    
    exit(0)
    
    v1 = NumVar()
    v2 = NumVar()
    v3 = NumVar()
    v1.bind(v2)
    v3.bind(v2)
    v3.bind(v2)
    print v1, v2, v3
    v1.set(5)
    print v1, v2, v3
    v2.set(10)
    print v1, v2, v3
    b = BoolVar(False)
    b2 = BoolVar(True)
    print not b 
    
    FONT = BitMask('IT', 'BF', "STRIKETHROUGH")

    bits = BitField(FONT.IT | FONT.BF)
    for b in bits: 
        out(FONT[b]) 
    print '|'.join([FONT[b] for b in bits])
    
    print bits.readable(FONT)
    exit(0)
    
    print Font(style=FONT.IT | FONT.BF, family=['Arial', 'Nimbus Sans', 'sans-serif'], size=13)
    
    def getdirty(v, d, c):
        print repr(v), 'is now', {True:'dirty', False:'clean'}[d], 'by', c
    
    s = StringVar('hello', on_change=lambda v, c: out(repr(v), 'was modified by', c))
    s += ', world!'
    print s
    
    
    n1 = NumVar(1, history=True, on_dirty=getdirty)
    n2 = NumVar(7)
    print n1 + 2 * n2
    n1 += 5.
    n1 /= 10
    print n1
    print n1.undo()
    print n1
    print n1.redo()
    print n1
    print n1._values
    
    
    
    