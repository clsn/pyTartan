#!/usr/bin/env python

from xml.dom.minidom import getDOMImplementation
import re

def uniqnum():
    count=0
    while True:
        count+=1
        yield count

def setAtts(self, attribs):
    for k in attribs:
        self.setAttribute(k, attribs[k])
        
uniq=uniqnum()
class Tartan:

    herring=False

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
        # see http://www.tartanregister.gov.uk/guidance.aspx
        standards={
            'B' : '#0000cd',    # blue
            'DB' : '#000080',   # dark blue (navy)
            'R' : 'red',
            'G' : '#228b22',    # green (forestgreen)
            'Y' : '#fee600',
            #'BK' : 'black',
            'BK' : '#101010',
            'K' : '#101010',
            'W' : 'white',
            'AZ' : '#87ceeb',   # sky blue
            'BR' : '#a52a2a',   # brown
            'CR' : '#b22222',   # crimson (firebrick)
            # 'GY' : '#bebebe',   # grey
            'GY' : '#666666',   # grey
            'N'  : '#666666',
            'T' : '#603311',
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
        try:
            return standards[s]
        except KeyError:
            if s.startswith("("):
                return s[1:-1]  # trim parens
            return s

    def convertWidth(self, wid):
        # Convert the width of a stripe.
        if hasattr(self, 'divisor'):
            wid /= self.divisor
        wid *= self.unit
        return wid
    
    def makeHorizStripe(self, spec):
        r=self.dom.createElement('rect')
        # x & y should be set elsewhere?
        # y should anyway.
        r.setAttribute("x","0")
        r.setAttribute("width","100%")
        h=self.convertWidth(int(spec[1]))
        r.setAttribute("height",str(h))
        r.setAttribute("fill","%s"%self.str2color(spec[0]))
        return r

    # Maybe I should assemble an array of stripes and throw them into
    # the svg at the last minute?

    def makeVertStripe(self, spec):
        r=self.dom.createElement('rect')
        r.setAttribute('y','0')
        r.setAttribute('height','100%')
        w=self.convertWidth(int(spec[1]))
        r.setAttribute('width',str(w))
        r.setAttribute('fill','%s'%self.str2color(spec[0]))
        return r
        
    def __init__(self, width=100, height=100, unit=2, asymmetrical=False):
        impl=getDOMImplementation()
        self.dom=impl.createDocument(None,'svg',None)
        d=self.dom.documentElement
        self.width=width
        self.height=height
        self.unit=unit
        self.svg=self.dom.documentElement
        self.asymmetrical=asymmetrical
        d.setAttribute("xmlns","http://www.w3.org/2000/svg")
        d.setAttribute("xmlns:xlink","http://www.w3.org/1999/xlink")
        d.setAttribute("height","%dpx"%height) # ??
        d.setAttribute("width", "%dpx"%width)
        d.setAttribute("viewBox", "0 0 %d %d"%(width, height))
        d.setAttribute("x","0")
        d.setAttribute("y","0")
        self.re=re.compile(r'([a-zA-Z]+|\(.*?\))/?(\d+)')
        self.defs=self.dom.createElement("defs")
        self.defs.__class__.setAtts=setAtts
        d.appendChild(self.defs)
        self.horelt=self.dom.createElement("g")
        self.horelt.setAttribute("id","horizStripes")
        d.appendChild(self.horelt)
        self.vertelt=self.dom.createElement("g")
        self.vertelt.setAttribute("id","vertStripes")
        d.appendChild(self.vertelt)
        grating=self.stripeGradient("grategrad", "white", self.unit)
        self.defs.appendChild(grating)
        gmask=self.dom.createElement("mask")
        gmask.setAttribute("id","grating")
        gmaskr=self.dom.createElement("rect")
        gmaskr.setAtts({"width":"100%", "height":"100%", "x":"0", "y":"0", "fill":"url(#grategrad)"})
        self.defs.appendChild(gmask)
        gmask.appendChild(gmaskr)
        self.horiz=[]
        self.vert=[]

        
    def setdims(self, width, height):
        # I can reset the viewbox, right?
        self.width=width
        self.height=height
        self.svg.setAttribute('viewBox','0 0 %d %d'%(width, height))
        self.svg.setAttribute('width','%dpx'%width)
        self.svg.setAttribute('height','%dpx'%height)
    
    def addHorizStripe(self, spec):
        # just collect the stripes, mkay?
        # Handle either parsed stripes (tuples) or unparsed (strings)
        if isinstance(spec,str):
            self.horiz.append(self.re.match(spec).groups())
        else:
            self.horiz.append(spec)

    def addVertStripe(self, spec):
        if isinstance(spec,str):
            self.vert.append(self.re.match(spec).groups())
        else:
            self.vert.append(spec)

    def assembleAll(self):
        for align in ('h', 'w'):
            if align=='h':
                maker=self.makeHorizStripe
                setattrib='y'
                getattrib='height'
                array=self.horiz
                #array.reverse() # We build these stripes the wrong way!
                # the y axis is upside-down or something.
                lim=self.height
                place=self.horelt
            else:
                maker=self.makeVertStripe
                setattrib='x'
                getattrib='width'
                array=self.vert
                place=self.vertelt
                lim=self.width
            i=0
            a=0
            dr= +1
            while a<lim:
                strip=array[i]
                r=maker(strip)
                r.setAttribute(setattrib,str(a))
                a+=int(r.getAttribute(getattrib))
                place.appendChild(r)
                if i+dr >= len(array) or i+dr < 0:
                    # I just hit the end.
                    if self.asymmetrical:
                        i=0
                        continue
                    dr *= -1
                i+=dr
        self.vertelt.setAttribute("mask", "url(#grating)")
        if self.herring:
            h=self.dom.createElement("rect")
            h.setAttribute("x","0")
            h.setAttribute("y","0")
            h.setAttribute("width","100%")
            h.setAttribute("height","100%")
            h.setAttribute("fill","url(herringbone.svg#herringbone)")
            self.svg.appendChild(h)

    def xml(self):
        return self.svg.toprettyxml()

    def symStripes(self, stripes):
        for s in self.re.findall(stripes):
            self.addHorizStripe(s)
            self.addVertStripe(s)

    def horizStripes(self, stripes):
        for s in self.re.findall(stripes):
            self.addHorizStripe(s)

    def vertStripes(self, stripes):
        for s in self.re.findall(stripes):
            self.addVertStripe(s)

    def computeDims(self, reps=2):
        w=0
        h=0
        for strip in self.horiz:
            h+=int(strip[1])
        for strip in self.vert:
            w+=int(strip[1])
	if not self.asymmetrical:
	    h -= int(self.horiz[0][1])/2
	    h -= int(self.horiz[-1][1])/2
	    w -= int(self.vert[0][1])/2
	    w -= int(self.vert[-1][1])/2
        if hasattr(self, 'divisor'):
            h/=self.divisor
            w/=self.divisor
        h*=self.unit
        w*=self.unit
        return (w*reps, h*reps)


def readThreadCountInfo(tar):
    # Read in and work directly from a tartanregister.gov.uk threadcount
    # response
    # Sigh... whose format they keep changing...
    cols={}
    lines=sys.stdin.readlines() # I'm going to want them all at once...
    i=0
    while i<len(lines):
        line=lines[i]
        if line.startswith('Threadcount:'):
            l=line.split(':')
            # Take second field--if there is one!
            threads=len(l)>1 and l[1].strip()
            if not threads:     # new style: line-break after colon
                # Take the next line
                threads=lines[i+1]
        elif line.startswith('Pallet:'):
            l=line.split(':')
            pal=len(l)>1 and l[1].strip()
            if not pal:
                # Take next line
                pal=lines[i+1]
            l=pal.split(';')
            for col in l:
                col=col.strip()
                m=re.match(r'([A-Za-z]+)=#?([0-9a-fA-F]{6})',col)
                if m:
                    cols[m.group(1)]='#%s'%m.group(2)
        elif line.startswith("Threadcount given over the full sett."):
            # New style responses contain information about symmettry
            # in auxiliary line.  Passed-in true asym overrides.
            tar.asymmetrical=True
        # No need to check for this, it's the default
        # elif line.startswith("Threadcount given over a half sett with full count at the pivots."):
        #    pass                # asym=False, default
        # Do they have a syntax for half-sett, half-count at pivots?
        # Sigh.  Why couldn't they and I have just stuck with slashes
        # like W/24 for pivots?
        i+=1

    # tar=Tartan(width=300, height=300, asymmetrical=asym, unit=unit)
    if divisor:
        tar.divisor=divisor
    # Horiz/vert stripes are delimited in tartanregister files with a period.
    vh=threads.split('.')
    # The first part might be the only part.
    # Do them individually; replacing on the whole string might get caught
    # in some of the hex strings
    if len(vh) < 2:
        vh.append('')
    allstripes=[[],[]]
    for i in [0, 1]:
        thr=re.findall(r'[a-zA-Z]+/?\d+',vh[i])
        for t in thr:
            m=re.match(r'[a-zA-Z]+',t)
            out=t.replace(m.group(0),'(%s)'%cols[m.group(0)])
            allstripes[i].append(out)
    if not vh[1]:
        allstripes[1]=allstripes[0]
    for out in allstripes[0]:
        tar.addVertStripe(out)
    for out in allstripes[1]:
        tar.addHorizStripe(out)
    return tar


if __name__=='__main__':
    
    import sys
    from getopt import getopt

    (opts, args)=getopt(sys.argv[1:],'d:r:u:aR',
                        ["herringbone", "transparent"])
    divisor=None
    reps=2
    unit=2
    asym=False
    herring=False
    t=None
    readinput=False
    transparent=False
    # print str(opts)
    for (k,v) in opts:
        if k.endswith('d'):
            divisor=int(v)
        elif k.endswith('r'):
            reps=int(v)
        elif k.endswith('u'):
            unit=int(v)
        elif k.endswith('a'):
            asym=True
        elif k.endswith('herringbone'):
            herring=True
            unit=4
        elif k.endswith('transparent'):
            transparent=True
        elif k.endswith('R'):
            readinput=True
    t=Tartan(width=300, height=300, unit=unit, asymmetrical=asym)
    if readinput:
        readThreadCountInfo(t)
    else:
        s=" ".join(args)
        if not s:
            s="R96 W8 B8 BK8 R24 B8 R2 Y8"
        hv=s.split('|',1)
        if len(hv)>1:
            t.horizStripes(hv[0])
            t.vertStripes(hv[1])
        else:
            t.symStripes(s)
    if divisor:
        t.divisor=divisor
    dim=t.computeDims(reps)
    t.setdims(*dim)
    t.herring=herring
    t.assembleAll()
    if transparent:
        t.vertelt.removeAttribute("mask")
        t.vertelt.setAttribute("opacity", "0.5")
    
    print t.xml()
