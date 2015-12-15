

class FloatOption:

    def __init__(self,name):
        self.name = name
        self.float = []
    def add(self, listOfObj):
        self.float.append(listOfObj)
    def getName(self):
        return self.name
    def get(self,i):
        return self.float[i]
    def getNIter(self):
        return len(self.float)
    def toString(self):
        s = self.name + ':\n'
        i=0
        s += '%10s  %s\n' % ('Iteration', 'Floating')
        for v in self.float:
            s += '%10d  %s\n' % (i,v)
            i=i+1
        return s


class FloatOptions:
    
    def __init__(self):
        self.list = self.initlist()
    
    def printlist(self):
        print len( self.list ), ' options:\n'
        i = 0
        for opt in self.list:
            print 'Option ', i, ': ', opt.toString()
            i += 1
    
    def getoption(self,switch):
        if switch >= len( self.list ):
            print 'This switch ', switch, ' is not defined'
            print self.printlist()
            sys.exit(1)
        else:
            return self.list[ switch ]

    def initlist(self):
        l = []
        opt = FloatOption('L0_L01_L12_L23_L01_L12_L34_L45_L01_tu')
        opt.add('L0b_tu L0t_tu')
        opt.add('L0b_tu L0t_tu L1b_tu L1t_tu')
        opt.add('L1b_tu L1t_tu L2b_tu L2t_tu')
        opt.add('L2b_tu L2t_tu L3b_tu L3t_tu')
        opt.add('L0b_tu L0t_tu L1b_tu L1t_tu')
        opt.add('L1b_tu L1t_tu L2b_tu L2t_tu')
        opt.add('L3b_tu L3t_tu L4b_tu L4t_tu')
        opt.add('L4b_tu L4t_tu L5b_tu L5t_tu')
        opt.add('L0b_tu L0t_tu L1b_tu L1t_tu')
        l.append(opt)

        opt = FloatOption('L01_L12_L23_L01_L12_L34_L45_L01_L12_tu')
        opt.add('L0b_tu L0t_tu L1b_tu L1t_tu')
        opt.add('L1b_tu L1t_tu L2b_tu L2t_tu')
        opt.add('L2b_tu L2t_tu L3b_tu L3t_tu')
        opt.add('L0b_tu L0t_tu L1b_tu L1t_tu')
        opt.add('L1b_tu L1t_tu L2b_tu L2t_tu')
        opt.add('L3b_tu L3t_tu L4b_tu L4t_tu')
        opt.add('L4b_tu L4t_tu L5b_tu L5t_tu')
        opt.add('L0b_tu L0t_tu L1b_tu L1t_tu')
        opt.add('L1b_tu L1t_tu L2b_tu L2t_tu')
        l.append(opt)

        opt = FloatOption('L2345_tu_singleLayerIter')
        opt.add('L2b_tu L2t_tu')
        opt.add('L3b_tu L3t_tu')
        opt.add('L4b_tu L4t_tu')
        opt.add('L5b_tu L5t_tu')
        l.append(opt)

        opt = FloatOption('L2345_rw_singleLayerIter')
        opt.add('L2b_rw L2t_rw')
        opt.add('L3b_rw L3t_rw')
        opt.add('L4b_rw L4t_rw')
        opt.add('L5b_rw L5t_rw')
        l.append(opt)

        opt = FloatOption('L2345_tu_rw_singleLayerIter_L234_L345_tu_rw')
        opt.add('L2b_tu L2t_tu L2b_rw L2t_rw')
        opt.add('L3b_tu L3t_tu L3b_rw L3t_rw')
        opt.add('L4b_tu L4t_tu L4b_rw L4t_rw')
        opt.add('L5b_tu L5t_tu L5b_rw L5t_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        opt.add('L3t_tu L3b_tu L3t_rw L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw')
        l.append(opt)

        opt = FloatOption('L2345_tu_rw_singleLayerIter_L2345_tu_singleLayerIter')
        opt.add('L2b_tu L2t_tu L2b_rw L2t_rw')
        opt.add('L3b_tu L3t_tu L3b_rw L3t_rw')
        opt.add('L4b_tu L4t_tu L4b_rw L4t_rw')
        opt.add('L5b_tu L5t_tu L5b_rw L5t_rw')
        opt.add('L2b_tu L2t_tu')
        opt.add('L3b_tu L3t_tu')
        opt.add('L4b_tu L4t_tu')
        opt.add('L5b_tu L5t_tu')
        l.append(opt)

        opt = FloatOption('L5u_L2u_2iterseach')
        opt.add('L5b_u L5t_u')
        opt.add('L2b_u L2t_u')
        opt.add('L5b_u L5t_u')
        opt.add('L2b_u L2t_u')
        l.append(opt)

        opt = FloatOption('htu')
        opt.add('L4hb_tu L5hb_tu L4ht_tu L5ht_tu ')
        opt.add('L3b_tu L4hb_tu L3t_tu L4ht_tu ')
        opt.add('L4hb_tu L4hb_tu L5ht_tu L5ht_tu ')
        opt.add('L2b_tu L3b_tu L2t_tu L3t_tu ')
        l.append(opt)    

        opt = FloatOption('L2-5-HOLE_tu')
        opt.add('L2b_tu L3b_tu L4hb_tu L5hb_tu L2t_tu L3t_tu L4ht_tu L5ht_tu')
        l.append(opt)    

        opt = FloatOption('L2-5-HOLE_tu_rw')
        opt.add('L2b_tu L3b_tu L4hb_tu L5hb_tu L2t_tu L3t_tu L4ht_tu L5ht_tu L2b_rw L3b_rw L4hb_rw L5hb_rw L2t_rw L3t_rw L4ht_rw L5ht_rw')
        l.append(opt)    

        opt = FloatOption('L234_tu_rw')
        opt.add('L2b_tu L3b_tu L4b_tu L5b_tu L2t_tu L3t_tu L4t_tu L5t_tu')
        l.append(opt)    

        opt = FloatOption('L5_tu')
        opt.add('L5t_tu L5b_tu')
        l.append(opt)    

        opt = FloatOption('L5_tuw')
        opt.add('L5t_tu L5b_tu L5t_tw L5b_tw')
        l.append(opt)    

        opt = FloatOption('L5_tuw_ruw')
        opt.add('L5t_tu L5b_tu L5t_tw L5b_tw L5t_ru L5b_ru L5t_rw L5b_rw')
        l.append(opt)    

        opt = FloatOption('L5_tu_ruw')
        opt.add('L5t_tu L5b_tu L5t_ru L5b_ru L5t_rw L5b_rw')
        l.append(opt)    

        opt = FloatOption('L1-3_tu_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        l.append(opt)    

        opt = FloatOption('L4-6_tu_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        l.append(opt)    

        opt = FloatOption('L123_L456_L235_L345_L123_L456_tu_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        opt.add('L3t_tu L3b_tu L3t_rw L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        l.append(opt)    

        opt = FloatOption('L123_L234_L345_L123_L456_L123_tu_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        opt.add('L3t_tu L3b_tu L3t_rw L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        l.append(opt)    

        opt = FloatOption('L56_L4_L56_L4_L56_L4_tu_rw')
        opt.add('L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw')
        opt.add('L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw')
        opt.add('L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw')
        l.append(opt)    

        opt = FloatOption('L456_L123_tu_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        l.append(opt)    

        opt = FloatOption('L123_L456_tu_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        l.append(opt)    

        opt = FloatOption('L123_L456_L234_tu_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        l.append(opt)    

        opt = FloatOption('L456_L123_L234_tu_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        l.append(opt)    

        opt = FloatOption('L123_L456_L234_L345_tu_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        opt.add('L3t_tu L3b_tu L3t_rw L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw')
        l.append(opt)    

        opt = FloatOption('L456_L123_L234_L345_tu_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        opt.add('L3t_tu L3b_tu L3t_rw L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw')
        l.append(opt)    

        opt = FloatOption('L123_L456_L234_L345_L123_L456_tu_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        opt.add('L3t_tu L3b_tu L3t_rw L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        l.append(opt)    

        opt = FloatOption('L456_L123_L234_L345_L123_L456_tu_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L2t_tu L2b_tu L2t_rw L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw')
        opt.add('L3t_tu L3b_tu L3t_rw L3b_rw L4t_tu L4t_rw L4b_tu L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw')
        opt.add('L1t_tu L1b_tu L1t_rw L1b_rw L2t_tu L2t_rw L2b_tu L2b_rw L3t_tu L3t_rw L3b_tu L3b_rw')
        opt.add('L4t_tu L4b_tu L4t_rw L4b_rw L5t_tu L5t_rw L5b_tu L5b_rw L6t_tu L6t_rw L6b_tu L6b_rw')
        l.append(opt)    

        return l





