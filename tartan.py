from xml.dom.minidom import getDOMImplementation
import re

def uniqnum():
    count=0
    while True:
        count+=1
        yield count
        
uniq=uniqnum()
class Tartan:
    
    def stripeGradient(self, ident, color, width=None, prime=False):
        if width is None:
            width=self.unit
        elt=self.dom.createElement("linearGradient")
        elt.setAttribute("id", ident)
        stop=self.dom.createElement("stop")
        stop.setAttribute("id","stop%04d"%uniq.next())
        stop.setAttribute("offset", "0")
        stop.setAttribute("stop-color",color)
        stop.setAttribute("stop-opacity", "0")
        elt.appendChild(stop)
        
        stop=self.dom.createElement("stop")
        stop.setAttribute("id","stop%04d"%uniq.next())
        stop.setAttribute("offset","50%")
        stop.setAttribute("stop-color",color)
        stop.setAttribute("stop-opacity","0")
        elt.appendChild(stop)
        
        stop=self.dom.createElement("stop")
        stop.setAttribute("id","stop%04d"%uniq.next())
        stop.setAttribute("offset","50%")
        stop.setAttribute("stop-color",color)
        stop.setAttribute("stop-opacity","1")
        elt.appendChild(stop)
        
        stop=self.dom.createElement("stop")
        stop.setAttribute("id","stop%04d"%uniq.next())
        stop.setAttribute("offset","100%")
        stop.setAttribute("stop-color",color)
        stop.setAttribute("stop-opacity","1")
        elt.appendChild(stop)
        
        elt.setAttribute("x1","0")
        elt.setAttribute("y1","0")
        elt.setAttribute("x2",str(width))
        elt.setAttribute("y2",str(width))
        elt.setAttribute("gradientUnits","userSpaceOnUse")
        elt.setAttribute("spreadMethod","repeat")
        if prime:
            elt.setAttribute("gradientTransform","translate(-%f,0)"%width)
            
        return elt

    @staticmethod
    def str2color(s):
        standards={
            'B' : '#0000cd',    # blue
            'DB' : '#000080',   # dark blue (navy)
            'R' : 'red',
            'G' : '#228b22',    # green (forestgreen)
            'Y' : 'yellow',
            #'BK' : 'black',
            'BK' : '#101010',
            'W' : 'white',
            'AZ' : '#87ceeb',   # sky blue
            'BR' : '#a52a2a',   # brown
            'CR' : '#b22222',   # crimson (firebrick)
            'GY' : '#bebebe',   # grey
            'LG' : '#98fb98',   # light green
            'PU' : '#dda0dd',   # plum
            'Lil' : '#da70d6',  # lilac (orchid)
            'Lv' : '#e6e6fa',   # lavender
            'Ma' : '#ff00ff',   # magenta
            'Mn' : '#b03060',   # maroon
            'Or' : '#ffa500',   # orange
            'Cy' : '#00ffff',   # cyan
            'Cor' : '#ff7f50',  # coral
            'SlB' : '#6a5acd',  # slate blue
            'Mar' : '#b03060',  # maroon
            'Trq' : '#40e0d0',  # turquoise
            'Glr' : '#daa520',  # goldenrod
            'Wh' : '#f5deb3'    # wheat
            }
        return standards.get(s,'white')
    
    def makeHorizStripe(self, spec):
        m=self.re.match(spec)
        if not m:
            return None         # ??
        r=self.dom.createElement('rect')
        # x & y should be set elsewhere?
        # y should anyway.
        r.setAttribute("x","0")
        r.setAttribute("width","100%")
        r.setAttribute("height",m.group(2))
        gID=self.gradID(self.str2color(m.group(1)),prime=False)
        r.setAttribute("fill","url(#%s)"%gID)
        return r

    # Maybe I should assemble an array of stripes and throw them into
    # the svg at the last minute?

    def makeVertStripe(self, spec):
        m=self.re.match(spec)
        if not m:
            return None
        r=self.dom.createElement('rect')
        r.setAttribute('y','0')
        r.setAttribute('height','100%')
        r.setAttribute('width',m.group(2))
        gID=self.gradID(self.str2color(m.group(1)),prime=True)
        r.setAttribute('fill','url(#%s)'%gID)
        return r
        
    def gradID(self, color, prime=False):
        if self.gradientCache.has_key((color,bool(prime))):
            return self.gradientCache[(color,bool(prime))]
        else:
            g=self.stripeGradient(color=color, ident='grad%04d'%uniq.next(), 
                                  prime=prime)
            self.defs.appendChild(g)
            self.gradientCache[(color,bool(prime))]=g.getAttribute('id')
            return g.getAttribute('id')

    def __init__(self, width=100, height=100, unit=2):
        impl=getDOMImplementation()
        self.dom=impl.createDocument(None,'svg',None)
        d=self.dom.documentElement
        self.width=width
        self.height=height
        self.unit=unit
        self.gradientCache={}
        self.svg=self.dom.documentElement
        d.setAttribute("xmlns","http://www.w3.org/2000/svg")
        d.setAttribute("xmlns:xlink","http://www.w3.org/1999/xlink")
        d.setAttribute("height","10cm") # ??
        d.setAttribute("width", "10cm")
        d.setAttribute("viewBox", "0 0 %d %d"%(width, height))
        d.setAttribute("x","0")
        d.setAttribute("y","0")
        self.re=re.compile(r'([a-zA-Z]+)(\d+)')
        self.defs=self.dom.createElement("defs")
        d.appendChild(self.defs)
        self.horiz=[]
        self.vert=[]

    def addHorizStripe(self, spec):
        # just collect the stripes, mkay?
        self.horiz.append(spec)

    def addVertStripe(self, spec):
        self.vert.append(spec)

    def assembleAll(self):
        h=0
        i=0
        dr= +1
        while h<self.height:
            strip=self.horiz[i]
            r=self.makeHorizStripe(strip)
            r.setAttribute('y',str(h))
            h+=int(r.getAttribute('height'))
            self.svg.appendChild(r)
            if i+dr >= len(self.horiz) or i+dr < 0:
                # I just hit the end.
                dr *= -1
            i+=dr
        i=0
        w=0
        dr= +1
        while w<self.width:
            strip=self.vert[i]
            r=self.makeVertStripe(strip)
            r.setAttribute('x',str(w))
            w+=int(r.getAttribute('width'))
            self.svg.appendChild(r)
            if i+dr >= len(self.vert) or i+dr < 0:
                dr *= -1
            i+=dr

    def xml(self):
        return self.svg.toprettyxml()

    def symStripes(self, stripes):
        for s in stripes.split():
            self.addHorizStripe(s)
            self.addVertStripe(s)

t=Tartan(width=300, height=300, unit=1)
#t.symStripes("B6 W2 BK2 W2 G10")
t.symStripes("R96 W8 B8 BK8 R24 B8 R2 Y8")
t.assembleAll()

print t.xml()
