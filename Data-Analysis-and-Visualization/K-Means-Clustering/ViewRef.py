import numpy
import math
'''
Class for visualizing CS (and Communications?) log data.
'''
class ViewRef:
    
    def __init__(self, view=[400,400], viewOffset=[20,20],debugMode=False):
        ''' Params:
                debugMode <bool> - whether or not to display debug messages
        ''' 
        self.dbg = debugMode
        self.reset(view,viewOffset)
        self.build()
        
    def debug(self,str):
        ''' Prints debug messages '''
        if self.dbg:
            print str
    
    def reset(self,view,viewOffset):
        self.debug("Restoring default view...")
        self.vrp = numpy.matrix([0.5, 0.5, 0])
        self.vpn = numpy.matrix([0, 0, 1])
        self.vup = numpy.matrix([0, 1, 0])
        self.u = numpy.matrix([1, 0, 0])
        self.extent = [1.0, 1.0, 1.0]
        self.view = view
        self.viewOffset = viewOffset
        self.debug("Default view restored.")
        
    def build(self):
        self.debug("Computing view matrix...")
        ''' Generate 4 x 4 identity matrix: the basis of the view matrix. '''
        m = numpy.identity( 4, float )
        
        ''' Generate a translation matrix to move the VRP to the origin,
        and premultiply m by the translation. '''
        m = self.T(-self.vrp[0, 0], -self.vrp[0, 1], -self.vrp[0, 2]) * m
        
        ''' Calculate the view reference axes. '''
        tu = numpy.cross(self.vpn, self.vup)
        tvup = numpy.cross(tu, self.vpn)
        tvpn = self.vpn
        
        ''' Normalize the view reference axes. '''
        tu = self.normalize(tu)
        tvup = self.normalize(tvup)
        tvpn = self.normalize(tvpn)
        
        ''' Copy the orthonormal axes back to self.u, self.vup and self.vpn.'''
        self.u = tu
        self.vup = tvup
        self.vpn = tvpn
        
        ''' Generate the rotation matrix to align the view reference axes. '''
        m = self.R(tu, tvup, tvpn) * m

        ''' Translate the lower left corner of the view space to the origin,
        and premultiply m by the translation. '''
        m = self.T( 0.5*self.extent[0], 0.5*self.extent[1], 0 ) * m
        
        ''' Scale to the screen. '''
        m = self.S( -self.view[0] / self.extent[0], -self.view[1] / \
                    self.extent[1], 1.0 / self.extent[2] ) * m
        
        ''' Move to screen coordinates. '''
        m = self.T( self.view[0] + self.viewOffset[0], self.view[1] + \
                    self.viewOffset[1], 0 ) * m
        
        self.debug("View matrix constructed successfully.")
        self.vtm = m
        
    def normalize(self, v):
        ''' Returns the Euclidean norm of view axes 'v'. '''
        norm = numpy.linalg.norm(v)
        #norm = numpy.sqrt(numpy.square(v).sum())
        v = v / norm
        return v
    
    def T(self, dx, dy, dz):
        ''' Returns a translation matrix '''
        return numpy.matrix(  [[1, 0, 0, dx],
                               [0, 1, 0, dy],
                               [0, 0, 1, dz],
                               [0, 0, 0,  1]])
    
    def R(self, dx, dy, dz):
        ''' Returns a rotation matrix '''
        return numpy.matrix(  [[ dx[0,0], dx[0,1], dx[0,2], 0.0 ],
                               [ dy[0,0], dy[0,1], dy[0,2], 0.0 ],
                               [ dz[0,0], dz[0,1], dz[0,2], 0.0 ],
                               [     0.0,     0.0,     0.0, 1.0 ]])

    def S(self, dx, dy, dz):
        ''' Returns a scaled matrix '''
        return numpy.matrix(  [[dx,  0,  0, 0],
                               [ 0, dy,  0, 0],
                               [ 0,  0, dz, 0],
                               [ 0,  0,  0, 1]])
        
    def rotateVRP(self, angleVUP, angleU):
       
        #Step 1: Translation Matrix
        # Make a translation matrix to move the point ( VRP + VPN * extent[Z] * 0.5 ) to the origin. Put it in t1.
        t1 = self.T(-self.vrp[0,0] - self.vpn[0,0] * self.extent[2] * 0.5,
                    -self.vrp[0,1] - self.vpn[0,1] * self.extent[2] * 0.5,
                    -self.vrp[0,2] - self.vpn[0,2] * self.extent[2] * 0.5)
        
        # Step 1.5: Calculate VUP' = VPN*u
        #vupPrime = numpy.cross(self.vpn,self.u)
        
        #Step 2: Axis Alignment matrix Rxyz
        # Make an axis alignment matrix Rxyz using u, vup and vpn.
        Rxyz = numpy.matrix([ [  self.u.item(0),  self. u.item(1),   self.u.item(2), 0],
                 [                self.vup[0,0],    self.vup[0,1],    self.vup[0,2], 0],
                 [             self.vpn.item(0), self.vpn.item(1), self.vpn.item(2), 0],
                 [                            0,                0,                0, 1] ])
        
        #print "Rxyz",Rxyz
        #Step 3: Rotation Matrix (Y axis)
        # Make a rotation matrix about the Y axis by the VUP angle, put it in r1.
        r1 = [ [  math.cos(angleVUP), 0, math.sin(angleVUP), 0 ],
               [                   0, 1,                  0, 0 ],
               [ -math.sin(angleVUP), 0, math.cos(angleVUP), 0 ],
               [                   0, 0,                  0, 1 ] ]
        
        #Step 4: Rotation Matrix (X axis)
        r2 = [ [  1,                0,                 0, 0 ],
               [  0, math.cos(angleU), -math.sin(angleU), 0 ],
               [  0, math.sin(angleU),  math.cos(angleU), 0 ],
               [  0,                0,                 0, 1 ] ]
        
        
        #Step 5: 2nd Translation Matrix (opp)
        t2 = self.T(+self.vrp[0,0] + self.vpn[0,0] * self.extent[2] * 0.5,
                    +self.vrp[0,1] + self.vpn[0,1] * self.extent[2] * 0.5,
                    +self.vrp[0,2] + self.vpn[0,2] * self.extent[2] * 0.5)
        
        #Step 6: NumPy matrix!
        tvrc = numpy.matrix([ [self.vrp[0,0], self.vrp[0,1], self.vrp[0,2], 1],
                            [    self.u[0,0],   self.u[0,1],   self.u[0,2], 0],
                            [  self.vup[0,0], self.vup[0,1], self.vup[0,2], 0],
                            [  self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0],
                          ])
        
        #print "tvrc before",tvrc
        
        #Step 7
        tvrc = (t2*Rxyz.getT()*r2*r1*Rxyz*t1*tvrc.getT()).getT()
        
        #print "tvrc after",tvrc
        
        #Copy the values from tvrc back into the VRP, U, VUP,
        #and VPN fields
        self.vrp =  numpy.matrix([tvrc[0,0], tvrc[0,1], tvrc[0,2]])
        self.u =    numpy.matrix([tvrc.item(1,0), tvrc.item(1,1), tvrc.item(1,2)])
        self.vup =  numpy.matrix([tvrc.item(2,0), tvrc.item(2,1), tvrc.item(2,2)])
        self.vpn =  numpy.matrix([tvrc.item(3,0), tvrc.item(3,1), tvrc.item(3,2)])
                                
        #Normalize U, VUP, and VPN.
        self.u = self.normalize(self.u)
        self.vup = self.normalize(self.vup)
        self.vpn = self.normalize(self.vpn) 
        
# execute the program if called from the command line
if __name__ == "__main__":
    vr = ViewRef()
