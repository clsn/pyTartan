from xml.dom.minidom import getDOMImplementation

def uniqnum():
    count=0
    while True:
        count+=1
        yield count
        
uniq=uniqnum()

def stripeGradient(dom, ident, color, width=2, prime=False):
    elt=dom.createElement("linearGradient")
    elt.setAttribute("id", ident)
    stop=dom.createElement("stop")
    stop.setAttribute("id","stop%04d"%uniq.next())
    stop.setAttribute("offset", "0")
    stop.setAttribute("stop-color",color)
    stop.setAttribute("stop-opacity", "0")
    elt.appendChild(stop)

    stop=dom.createElement("stop")
    stop.setAttribute("id","stop%04d"%uniq.next())
    stop.setAttribute("offset","50%")
    stop.setAttribute("stop-color",color)
    stop.setAttribute("stop-opacity","0")
    elt.appendChild(stop)

    stop=dom.createElement("stop")
    stop.setAttribute("id","stop%04d"%uniq.next())
    stop.setAttribute("offset","50%")
    stop.setAttribute("stop-color",color)
    stop.setAttribute("stop-opacity","1")
    elt.appendChild(stop)
    
    stop=dom.createElement("stop")
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

impl=getDOMImplementation()
r=impl.createDocument(None,'svg',None)
d=r.documentElement
d.setAttribute("xmlns","http://www.w3.org/2000/svg")
d.setAttribute("xmlns:xlink","http://www.w3.org/1999/xlink")
d.setAttribute("height","10cm")
d.setAttribute("width", "10cm")
d.setAttribute("viewBox", "0 0 100 100")
d.setAttribute("x","0")
d.setAttribute("y","0")

defs=r.createElement("defs")
d.appendChild(defs)
lg=stripeGradient(r,"grad0001","black")
lgp=stripeGradient(r,"grad0001p","red",prime=True)
defs.appendChild(lg)
defs.appendChild(lgp)

rect=r.createElement("rect")
rect.setAttribute("x","20")
rect.setAttribute("y","20")
rect.setAttribute("width", "60")
rect.setAttribute("height", "30")
rect.setAttribute("fill", "url(#grad0001)")
d.appendChild(rect)

rect=r.createElement("rect")
rect.setAttribute("x","40")
rect.setAttribute("y","10")
rect.setAttribute("width","30")
rect.setAttribute("height","60")
rect.setAttribute("fill","url(#grad0001p)")
d.appendChild(rect)

print d.toprettyxml()
