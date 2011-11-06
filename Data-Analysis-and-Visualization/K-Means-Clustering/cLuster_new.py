'''HW6: Clustering Algorithms'''

import Tkinter, tkFileDialog, tkSimpleDialog, tkMessageBox, numpy, random, ViewRef, math

# create a shorthand object for Tkinter
tk = Tkinter

class cLuster:
    def __init__(self, width, height):
        # create a tk object, which is the root window
        self.root = tk.Tk()

        # width and height of the window
        self.initDx = width
        self.initDy = height

        # set up the geometry for the window
        self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

        # set the title of the window
        self.root.title("K-Means Cluster Visualization")
		
        # set the maximum size of the window for resizing
        self.root.maxsize( 1920, 1080 )

        # bring the window to the front
        self.root.lift()

        # setup the menus
        self.buildMenus()

        # build the objects on the Canvas
        self.buildCanvas()

        # set up the key bindings
        self.setBindings()

        # set up other variables
        self.shape = "oval"
        
        # this list holds graphics objects
        self.graphics = []
        
        # create view reference object
        self.vRef = ViewRef.ViewRef()
        
        # set up VTM
        self.buildAxes()
        
        # start off with no data
        self.dataM = False
        
        # We're not in histomode
        self.histoMode = False
        
        # turn off rotationMode
        self.rotationMode = True

    def scaledEucl(self, a, b, sigma):
        ''' Returns scaled Euclidean distance between value 'a' and 'b' given a
            standard deviation of value 'sigma'.'''
        return ((a - b) **2 ) / (sigma ** 2)

    def runCluster(self):
		''' Run k-means clusters w/ 'K' number of clusters.'''
		# Ask user for how many clusters to use
		Ktotal = tkSimpleDialog.askinteger("K-means Clustering Algorithm", "Initial Cluster Count:")
		numIter = tkSimpleDialog.askinteger("K-means Clustering Algorithm","Number of Iterations:") 
	
		#Given: N feature vectors and the number of clusters K
		N = self.dataM.shape[0]
		
		# Keep track of representation errors
		reprErrs = []
		
		#create a copy of points
		list = self.dataM
		
		# calculate sigmas
		xSD = list[:,0].std()
		ySD = list[:,1].std()
		
		for K in range(Ktotal, Ktotal+numIter):
		
			print "Current K:", K
		
			'''Initialization Phase'''
			#Initialize K cluster means C by randomly selecting K points and
			#assigning their values to the cluster means.
			C = []
			
			# Get a random number in the range of data points
			rand = random.randint(0, len(self.dataM.getA())-1)
			
			# Pick one random data point
			rDP = self.dataM[rand]
			
			# Add its value to C & prev
			C.append(rDP)
			
			#delete rDP from list
			numpy.delete(list, rand) 
						
			for currentCluster in range(1, K):
				
				farthestPtDist = -1
				
				#find pt furthest from all previous selections
				for newPt in list:
					
					dist=0
					#//Euclidean dist: sqrt[(ax - bx)^2 + (ay-by)^2]//
					for prevClust in C:
						dist += self.scaledEucl(prevClust[0,0],newPt[0,0], xSD) + \
								self.scaledEucl(prevClust[0,1], newPt[0,1], ySD)
					  
					if dist > farthestPtDist:
						farthestPt = newPt 
						farthestPtDist = dist
				
				#print "Furthest pt: ", farthestPt, "  Dist: ", farthestPtDist 
				
				# add its value to C; delete from list
				C.append(farthestPt)
				numpy.delete(list, currentCluster)    
			
			#print "C Init:", C, "\n" 
			
			#Initialize K cluster means C_old to zeros
			C_old = []
			for index in range(K):
				C_old.append(0)
				
			#Initialize a vector Csize of size K to zeros
			Csize = []
			for index  in range(K):
				Csize.append(0)
			
			#Initialize a Marker array of length N to -1 (I think he means make all #s -1?)    
			Marker = numpy.ones(N) * -1  
			#for i in range(N):
			#    Marker[i] = -1
			
			#Threshold - a fairly small value
			thresh = 0.0001
			
			#Change = a large value
			change = thresh + 1
			
			#while change is bigger than threshold
			while change > thresh: 
				'''Classify the data points using the current clusters'''
				
				#for each data point x_i
				for i in range(self.dataM.shape[0]):
					x_i = self.dataM[i]
					oldDist = False
					
					#compare x_i to each cluster
					for j, c_i in enumerate(C):
						newDist = self.scaledEucl(x_i[0,0], c_i[0,0], xSD) + self.scaledEucl(x_i[0,1], c_i[0,1], ySD)
						 
						if not oldDist or newDist < oldDist:
							closest = j
							oldDist = newDist
							
					#set Marker[i] to the id of the closest cluster
					Marker[i] = closest
					
				# calculate the average cluster means
				C_old = C
				
				#set C to all zeros
				C = numpy.zeros_like(C)
				
				#set Csize to all zeros
				Csize = numpy.zeros_like(Csize)
	
				#for each data point x_i
				for i in range(self.dataM.shape[0]):
					x_i = self.dataM[i]
					C[ Marker[i] ] += x_i
					Csize[ Marker[i] ] +=1
			
				#for each cluster c_i
				for i, c_i in enumerate(C):
					c_i /= Csize[i]
			
				'''Calculate the change'''
				#Change = sum over i of the Euclidean distance of C[i] - C_old[i]
				d = C - C_old
				change = numpy.sqrt(numpy.sum(d*d))
			
			# Find the SCALED EUCLIDEAN distance between every point and the cluster mean it was assigned to
			dist = 0
			for i in range(self.dataM.shape[0]):
				curMark = int(Marker[i])
				x_i = self.dataM[i, 0]
				y_i = self.dataM[i, 1]
				#print C[0].shape, C[0], curMark
				x_c = C[curMark, :, 0][0]
				y_c = C[curMark, :, 1][0]
				#print x_c, y_c, x_i, y_i
				dist += self.scaledEucl(x_i, x_c, xSD) + self.scaledEucl(y_i, y_c, ySD)
			
			reprErrs.append([dist, K, Marker, C])
				
		
		# Sort in order from min -> max
		reprErrs.sort()
		print "Best K: ", reprErrs[0][1], "  Next Best:", reprErrs[1][1]
		bestMarker = reprErrs[0][2]
		bestC = reprErrs[0][3]
		return bestMarker, bestC 
        
    def updateData(self):
        if type(self.dataM) is not bool and self.histoMode == False:
            print "Updating data"
            self.vRef.build()
        
            pts = (self.vRef.vtm * self.dataM.getT()).getT()[:,:2].getA()
        
            for i,point in enumerate(self.dataGfx):
                curCoords = self.canvas.coords(point)
                
                dX = pts[i][0] - curCoords[0]
                dY = pts[i][1] - curCoords[1]
                self.canvas.move(point, dX, dY)
    
    def buildMenus(self):
        # create a new menu
        self.menu = tk.Menu(self.root)

        # set the root menu to our new menu
        self.root.config(menu = self.menu)

        # create a variable to hold the individual menus
        self.menulist = []

        # create a file menu
        filemenu = tk.Menu( self.menu )
        self.menu.add_cascade( label = "File", menu = filemenu )
        self.menulist.append(filemenu)
        
        # create another menu for kicks
        viewmenu = tk.Menu( self.menu )
        self.menu.add_cascade( label = "View", menu = viewmenu )
        self.menulist.append(viewmenu)

        # create another menu for kicks
        cmdmenu = tk.Menu( self.menu )
        self.menu.add_cascade( label = "Analysis", menu = cmdmenu )
        self.menulist.append(cmdmenu)

        # menu text for the elements
        menutext = [ [ 'Open... \xE2\x8C\x98-O', '-', 'Clear \xE2\x8C\x98-W', '-', 'Quit \xE2\x8C\x98-Q' ],
                     [ 'Restore Default View','Controls'], 
                     ['Run K-means Clustering Algorithm'] ]

        # menu callback functions
        menucmd = [ [self.handleOpen, None, self.handleClose, None, self.handleQuit],
                    [self.handleCmd0, self.handleCmd1],
                    [self.handleCmd2] ]
    
        
        # build the menu elements and callbacks
        for i in range( len( self.menulist ) ):
            for j in range( len( menutext[i]) ):
                if menutext[i][j] != '-':
                    self.menulist[i].add_command( label = menutext[i][j],
                                                  command=menucmd[i][j] )
                else:
                    self.menulist[i].add_separator()
                            
    # binds user actions to functions
    def setBindings(self):
        self.root.bind( '<Button-1>', self.handleButton1 )
        self.root.bind( '<Button-2>', self.handleButton2 )
        self.root.bind( '<Button-3>', self.handleButton3 )
        self.root.bind( '<B1-Motion>', self.handleButton1Motion )
        self.root.bind( '<B2-Motion>', self.handleButton2Motion )
        self.root.bind( '<B3-Motion>', self.handleButton3Motion )
        self.root.bind( '<Command-o>', self.handleOpenEvent )
        self.root.bind( '<Control-o>', self.handleOpenEvent )
        self.root.bind( '<Command-w>', self.handleCloseEvent )
        self.root.bind( '<Control-w>', self.handleCloseEvent )
        self.root.bind( '<Control-q>', self.handleQuit )   #cmd-q happens automatically
    
    #handles cmd-w event
    def handleCloseEvent(self, event):
        self.handleClose()
    
    # handles cmd-o event
    def handleOpenEvent(self, event):
        self.handleOpen()
        
    # handles Open.. in the File menu
    def handleOpen(self):
        print 'handleOpen'
        fobj = tkFileDialog.askopenfile( parent=self.root, mode='rb', 
                                         title='Choose a data file' )
        if fobj == None:
            print 'User did not select a file'
            return
        
        self.dataGfx = []
        self.dataTemp = []
        dx = 4
        dy = 4
        for line in fobj:
            xyz = line.split()
            x = float(xyz[0])
            y = float(xyz[1])
            if (len(xyz) < 2):
                z = float(xyz[2])
            
            # Make z a random float from 0-1
            else:
                z = random.random()
            
            self.dataTemp.append([x,y,z,1])
            shape = self.canvas.create_oval(x - dx,y - dy,x + dx,y + dy)
            self.dataGfx.append(shape)
        
        self.dataTemp = numpy.matrix(self.dataTemp)
        
        # Normalize to 0-1
        normMax = 1.0
        allX = self.dataTemp[:, 0]
        allY = self.dataTemp[:, 1]
        allZ = self.dataTemp[:, 2]
        
        xMin =  allX.min()
        xRange = allX.max() - xMin
        xNorm = (normMax / xRange) * (allX - xMin)

        yMin =  allY.min()
        yRange = allY.max() - yMin
        yNorm = (normMax / yRange) * (allY - yMin)

        zMin =  allZ.min()
        zRange = allZ.max() - zMin
        zNorm = (normMax / zRange) * (allZ - zMin)
        
        self.dataTemp[:, 0] = xNorm
        self.dataTemp[:, 1] = yNorm
        self.dataTemp[:, 2] = zNorm
        
        self.dataM = self.dataTemp
        
        print self.dataM, self.dataM.shape
        
        self.updateData()

    # handles Close in the File menu
    def handleClose(self):
        if type(self.dataM) is not bool:
                    for dataPoint in self.dataGfx:
                        self.canvas.delete(dataPoint)
        # reset
        self.dataSet = False
        self.dataM = False
        self.bins = False  

    # handles Quit in the File menu
    # cmd-q automatically quits the program
    def handleQuit(self):
        yonrose = tkMessageBox.askquestion('Quit program?', 'Really quit?')
        if yonrose != 'no':
            self.root.destroy()
            print 'Quitting application.'
        print 'Resuming session.'

    # the next four functions handle menu item selections        
    def handleCmd0(self):
        yonrose = tkMessageBox.askquestion('Confirm Action', 
                                           'Restore default view?')
        if yonrose != 'no':
            self.vRef.reset(self.vRef.view, self.vRef.viewOffset)
            self.updateAxes()
            self.updateData()
            print 'View restored.'
        else: print 'View not restored.'

    def handleCmd1(self):       
        str =  ('Left Mouse Button:      Translate\n')
        str += ('Middle Mouse Button:  Rotate\n')
        str += ('Right Mouse Button:    Zoom\n')
       #str += ('Ctrl + H:                      Show/Hide Axes \n')
        
        tkMessageBox.showinfo(title='Controls', message=str)

    def handleCmd2(self):
		if type(self.dataM) is not bool:
			print 'Running k-means clustering...'
			Marker, C = self.runCluster()
			#colors = ["22ff22", "ff3300", "0000ff", "ff00bb"]
			
			# Generate random colors
			colors = []
			for i in range(len(C)):
				rcolor = '#' + "".join(["%02x"%random.randrange(256) for x in range(3)])
				colors.append(rcolor)
			
			print Marker.shape, len(self.dataGfx)
			
			# Loop through and color data points according to their cluster
			for i, ptGraphic in enumerate(self.dataGfx):
				curMarker = int(Marker[i])
				self.canvas.itemconfigure(ptGraphic, outline=colors[curMarker])
        
		else:  
			tkMessageBox.showinfo(title='Analysis Failed!', message="No data loaded.") 
        
    # builds a canvas for drawing that expands to fill the window
    def buildCanvas(self):
        self.canvas = tk.Canvas( self.root, width=self.initDx, 
                                 height=self.initDy )
        self.canvas.pack( expand=tk.YES, fill=tk.BOTH )

    # build the view transformation matrix [VTM], multiplies the axis endpoints
    # by the VTM, then creates three new line objects, one for each axis. Store
    # the three line objects.
    def buildAxes(self):
        
        # six endpoints. the length of each axis is 1
        self.axes = numpy.matrix([[0,0,0,1],
                                  [1,0,0,1],
                                  [0,0,0,1],
                                  [0,1,0,1],                                  
                                  [0,0,0,1],
                                  [0,0,1,1]])
        
        # build the view transformation matrix [VTM]
        self.vRef.build()
        
        # multiply the axis endpoints by the VTM
        pts = (self.vRef.vtm * self.axes.getT()).getT()[:,:2]
        
        xAxis = pts[:2].getA()
        yAxis = pts[2:4].getA()
        zAxis = pts[4:6].getA()
        
        # You'll also want a list to hold the actual graphics objects 
        # (the lines) that instantiate them on the screen.
        xObj = self.canvas.create_line(xAxis[0][0], xAxis[0][1],
                                       xAxis[1][0], xAxis[1][1], arrow=tk.LAST)
        yObj = self.canvas.create_line(yAxis[0][0], yAxis[0][1],
                                       yAxis[1][0], yAxis[1][1], arrow=tk.LAST)
        zObj = self.canvas.create_line(zAxis[0][0], zAxis[0][1],
                                       zAxis[1][0], zAxis[1][1], arrow=tk.LAST)
        self.axesGfx =  [xObj, yObj, zObj]
    
    def updateAxes(self):
        
        # build the view transformation matrix [VTM]
        self.vRef.build()
        
        # multiply the axis endpoints by the VTM
        pts = (self.vRef.vtm * self.axes.getT()).getT()[:,:2].getA()
        
        # for each line object
        i = 0
        for line in self.axesGfx:
            
            # update the coordinates of the object
            self.canvas.coords(line, pts[i][0], pts[i][1],
                                     pts[i+1][0], pts[i+1][1])
            i+= 2
            
    # handles clicks from button 1
    def handleButton1(self, event):
        print 'handle button 1: %d %d' % (event.x, event.y)
        self.baseClick = [event.x, event.y]

    # handles clicks from button 2
    def handleButton2(self, event):
        print 'handle button 2: %d %d' % (event.x, event.y)
        self.baseClick2 = [event.x, event.y]
        #self.drawShape(event.x,event.y)

    # handles clicks from button 3
    def handleButton3(self, event):
        print 'handle button 3: %d %d' % (event.x, event.y)
        self.baseClick3 = [event.x, event.y]
    # handles motion while button 1 held down
    def handleButton1Motion(self, event):
        
        if not self.histoMode:
            ########## Errors here if baseClick doesn't exist
            ########## DisplayApp instance has no attribute 'baseClick'
            diff = [ event.x - self.baseClick[0], event.y - self.baseClick[1] ]
            print 'handle button1  motion %d %d' % (diff[0], diff[1])
            self.baseClick = [ event.x, event.y ]
    
            #Divide the differential motion (dx, dy) by the screen size 
            #(view X, view Y) & multiply by the extents
            delta0 = 1.0 * diff[0]*self.vRef.extent[0] / self.vRef.view[0]
            delta1 = 1.0 * diff[1]*self.vRef.extent[1] / self.vRef.view[1]
            
            # Update the VRP
            dvrpx = delta0 * self.vRef.u.item(0) + delta1 * self.vRef.vup.item(0)
            
            # for some reason, it thinks vup and u only have one element...
            dvrpy = delta0 * self.vRef.u.item(1) + delta1 * self.vRef.vup.item(1)
            
            theVRP = self.vRef.vrp.getA()
            theVRP[0][0] = self.vRef.vrp.item(0) + dvrpx
            theVRP[0][1] = self.vRef.vrp.item(1) + dvrpy
            
            #Call updateAxes()
            self.updateAxes()
            self.updateData()
    
    # handles motion while button 2 held down
    def handleButton2Motion(self,event):
        if self.rotationMode:
            diff = [ event.x - self.baseClick2[0], event.y - self.baseClick2[1] ]
            #self.baseClick2 = [ event.x, event.y ]
            
            #constant (200) is arbitrary (use half extent)
            delta0 = 1.0*diff[0]*math.pi / 10000
            delta1 = -1.0*diff[1]*math.pi / 10000
            
            self.vRef.rotateVRP(delta0, delta1)
            self.updateAxes()
            self.updateData()

    # handles motion while button 3 held down
    def handleButton3Motion(self,event):
        
        if not self.histoMode:
            diff = event.y - self.baseClick3[1]
            print 'handle button3  motion %d' % diff
            
            # Keep the scale factor between 0.1 and 3.0
            if diff < 0:
                if diff < -3:
                    diff = -3
                elif diff > -0.1:
                    diff = -0.1
            else:
                if diff > 3:
                    diff = 3
                elif diff < 0.1:
                    diff = 0.1
                    
            k = 0.01
            f = 1.0 + k*diff
            
            #Update the extent.
            self.vRef.extent[0] *= f
            self.vRef.extent[1] *= f
            self.vRef.extent[2] *= f
            
            self.updateAxes()
            self.updateData()
            
    # main TK loop
    def main(self):
        print 'Entering main loop'
        self.root.mainloop()
        
# execute the program if called from the command line
if __name__ == "__main__":
    dapp = cLuster(500, 500)
    dapp.main()