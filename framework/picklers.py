import pickle, os, ROOT

class diclist( list ):
    '''list with an internal dictionary for indexing, 
    allowing to keep dictionary elements ordered. 
    keys can be everything except an integer.
    '''

    def __init__(self):
        super( diclist, self).__init__()
        # internal dictionary, will contain key -> index in list
        self.dico = {}

    def add( self, key, value ):
        if isinstance(key, (int, long)):
            raise ValueError("key cannot be an integer")
        if key in self.dico:
            raise ValueError("key '{key}' already exists".format(key=key) )
        self.dico[key] = len(self)
        self.append(value)

    def __getitem__(self, index):
        '''index can be a dictionary key, or an integer specifying
        the rank of the value to be accessed
        '''
        try:
            # if index is an integer (the rank), use the list.
            return super(diclist, self).__getitem__(index)
        except (TypeError, ValueError):
            # else it's the dictionary key.
            # use the internal dictionary to get the index,
            # and return the corresponding value from the list
            return super(diclist, self).__getitem__( self.dico[index] )

    def __setitem__(self, index, value):
        '''These functions are quite risky...'''
        try:
            return super(diclist, self).__setitem__(index, value)
        except TypeError as ValueError:
            return super(diclist, self).__setitem__( self.dico[index], value )



class Counter(diclist):
    def __init__(self, name):
        self.name = name
        super(Counter, self).__init__()

    def register(self, level):
        self.add( level, [level, 0] )
    
    def inc(self, level, nentries=1):
        '''increment an existing level
        '''
        if level not in self.dico:
            raise ValueError('level', level, 'has not been registered')
        else:
            self[level][1] += nentries

    def __add__(self, other):
        '''Add two counters (+).'''
        size = max( len(self), len(other))
        for i in range(0, size):
            if i>=len(other):
                # this line exists only in this counter, leave it as is
                continue
            elif i>=len(self):
                self.register( other[i][0])
                self.inc( other[i][0], other[i][1] )
            else:
                if self[i][0] != other[i][0]:  
                    err = ['cannot add these counters:', str(self), str(other)]
                    raise ValueError('\n'.join(err))
                else:
                    self.inc( other[i][0], other[i][1] )
        return self

    def __iadd__(self, other):
        '''Add two counters (+=).'''
        return self.__add__(other)

    def write(self, dirname):
        '''Dump the counter to a pickle file and to a text file in dirname.'''
        pckfname = '{d}/{f}.pck'.format(d=dirname, f=self.name)
        pckfname = pckfname.replace('*','STAR')
        pckfile = open( pckfname, 'w' )
        pickle.dump(self, pckfile)
        txtfile = open( pckfname.replace('.pck', '.txt'), 'w')
        txtfile.write( str(self) )
        txtfile.write( '\n' )
        txtfile.close()
        
    def __str__(self):
        retstr = 'Counter %s :\n' % self.name
        prev = None
        init = None
        for level, count in self:
            if prev == None:
                prev = count
                init = count
            if prev == 0:
                eff1 = -1.
            else:
                eff1 = float(count)/prev
            if init == 0:
                eff2 = -1.
            else:
                eff2 = float(count)/init
            retstr += '\t {level:<40} {count:>9} \t {eff1:4.2f} \t {eff2:6.4f}\n'.format(
                level=level,
                count=count,
                eff1=eff1,
                eff2=eff2 )
            prev = count
        return retstr

