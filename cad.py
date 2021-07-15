# -*- coding: utf-8 -*-
import Part
import FreeCAD as App
from FreeCAD import Base
import FreeCADGui as Gui
import math
from math import pi
import csv




#Function to clear Window
def clearAll():
    doc = App.ActiveDocument
    for obj in doc.Objects:
        doc.removeObject(obj.Label)



def make_parts(self, csv_filename):						#Plot Part
    #Definition of Values
    csvdatei = open(csv_filename,"r")
    csv_reader = csv.reader(csvdatei, delimiter=';')
    zeilennummer = 0
    for row in csv_reader:
        if zeilennummer == 0:
            print(f'Spaltennamen sind: {", ".join(row)}')
        else:
            Width=float(row[0])
            Height=float(row[1])
            DL=float(row[2])
            Thickness=float(row[3])
            LHD=float(row[4])
            RodLength=int(row[5])
            LensBin= int(row[6])
            LL=float(row[7])
            DLL= float(row[8])
            Mount = int(row[11])


        zeilennummer += 1
    
    csvdatei.close()

    clearAll()
    ###Part-Code###############################################################
    ###DOE-Holder1###############################################################
    ##BasePart
    #make sketch
    x1=15
    y1=-30
    x2=15
    y2=30
    x3=18
    y3=30
    x4=18
    y4=21
    x5=23
    y5=16
    x6=23
    y6=6.5
    x7=20
    y7=6.5
    x8=20
    y8=15.25
    x9=17
    y9=15.25
    x10=17
    y10=-15.25
    x11=20
    y11=-15.25
    x12=20
    y12=-6.5
    x13=23
    y13=-6.5
    x14=23
    y14=-16
    x15=18
    y15=-21
    x16=18
    y16=-30
    x17=15
    y17=-30

    #Extrude
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0), Base.Vector(x10, y10, 0), Base.Vector(x11, y11, 0), Base.Vector(x12, y12, 0), Base.Vector(x13, y13, 0), Base.Vector(x14, y14, 0), Base.Vector(x15, y15, 0), Base.Vector(x16, y16, 0), Base.Vector(x17, y17, 0)])
    L=Part.Face(lshape_wire)
    BasePart=  L.extrude(Base.Vector(0, 0, 60))

    #Part.show(BasePart)


    #SquareHole
    SquareHole=Part.makeBox(15,15,2)
    SquareHole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
    TranslationSquareHole=(15,-15/2,30+15/2)
    SquareHole.translate(TranslationSquareHole)
    #Part.show(SquareHole)


    fused1=BasePart.cut(SquareHole)
    #Part.show(fused1)

    #Cylinders for threads
    Cylinder=Part.makeCylinder(8/2,3)
    Cylinder.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
    TranslationCylinder=(23,11,30)
    Cylinder.translate(TranslationCylinder)
    fused2=fused1.fuse(Cylinder)
    #Part.show(Cylinder)


    TranslationCylinder=(0,-2*11,0)
    Cylinder.translate(TranslationCylinder)
    fused3=fused2.fuse(Cylinder)
    #Part.show(Cylinder)


    #Part.show(fused3)

    #Drilling
    Drilling=Part.makeCylinder(3.9/2,6)
    Drilling.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
    DrillingTranslation=(20,11,30)
    Drilling.translate(DrillingTranslation)
    fused4=fused3.cut(Drilling)
    TranslationDrilling=(0,-2*11,0)
    Drilling.translate(TranslationDrilling)
    fused5=fused4.cut(Drilling)

    #Part.show(fused5)

    #threads
    #Screw
    x1=0
    y1=0
    x2=0.1
    y2=0
    x3=0.1
    y3=0.05
    x4=1.0392/2+0.1
    y4=0.35
    x5=0.1
    y5=0.65
    x6=0.1
    y6=0.7
    x7=0
    y7=0.7
    x8=0
    y8=0
    
    shape1=Part.makeHelix(0.8,8,4.134/2)
    shape2= Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0)])
    shape2.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
    TranslationShape2=(4.134/2-0.1,0,0)
    shape2.translate(TranslationShape2)

    traj = Part.Wire([shape1])
    section = Part.Wire([shape2])

    makeSolid = True #1
    isFrenet = True #1

    # create a 3D shape and assigh it to the current document
    Sweep = Part.Wire(traj).makePipeShell([section],makeSolid,isFrenet)
    inner=Part.makeCylinder(4.132/2,10)
    
    Thread=inner.fuse(Sweep)
    Thread.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)

    TranslationThread=(18.5,11,30)
    Thread.translate(TranslationThread)

    fused6=fused5.cut(Thread)

    TranslationThread=(0,-2*11,0)
    Thread.translate(TranslationThread)
    BasePart=fused6.cut(Thread)

    #Part.show(fused7)

    ################################################################
    ##LaserHolder Part
    #Definition
    HoleTolerance=0
    RectangleTolerance=0
    ToleranceNubble=0


	        
    #OuterRing
    BossExtrude1=Part.makeCylinder(40/2,15)
    CutExtrude1=Part.makeCylinder(33/2,15)
    PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        

    #OuterRingSquares
    Square=Part.makeBox(5.13,15,15)
    TranslationSquare=(17.37,-15/2,0)
    Square.translate(TranslationSquare)
    #Part.show(Square)

	
    #CutoutsOuterRingSquares1
    Hole=Part.makeCylinder(2.2+HoleTolerance,15)
    TranslationHole=(20.3,0,0)
    Hole.translate(TranslationHole)
    PartCutout=Square.cut(Hole)
    fused6=PartBossExtrude1.cut(Hole)

    Rectangle=Part.makeBox(0.69+0.5,3.2+RectangleTolerance,15)
    TranslationRectangle=(21.81-0.25,-3.2/2-RectangleTolerance/2,0)
    Rectangle.translate(TranslationRectangle)
    PartCut=PartCutout.cut(Rectangle)
    fused7= fused6.fuse(PartCut)

    #CutoutsOuterRingSquares2
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    fused8=fused7.fuse(PartCut)
    fused9=fused8.cut(Hole)

	
    #CutoutsOuterRingSquares3
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    fused10=fused9.fuse(PartCut)
    fused11=fused10.cut(Hole)
    
	
    #CutoutsOuterRingSquares4
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    fused12=fused11.fuse(PartCut)
    fused13=fused12.cut(Hole)
    #Part.show(fused13)

	
	

    #Outer Polygon
    x1=18+2.75/(math.tan((30)*2*pi/360))
    y1=-4.25
    x2=18+2.75/(math.tan((30)*2*pi/360))
    y2=4.25
    x3=18
    y3=4.25
    x4=18
    y4=-4.25
    x5=18+2.75/(math.tan((30)*2*pi/360))
    y5=-4.25


    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
    L=Part.Face(lshape_wire)
    K1 = L.extrude(Base.Vector(0, 0, 15))
    K2 = L.extrude(Base.Vector(0, 0, 15))
    K3 = L.extrude(Base.Vector(0, 0, 15))
    K4 = L.extrude(Base.Vector(0, 0, 15))
    K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
    K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
    K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

    fused14=fused13.fuse(K1)
    fused15=fused14.fuse(K2)
    fused16=fused15.fuse(K3)
    fused17=fused16.fuse(K4)
   
    fused17.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)	
    TranslationHolder4=(0,0,30)
    fused17.translate(TranslationHolder4)

    fused18=fused17.fuse(BasePart)
    #Part.show(fused18)

    #clampings
    #make sketch
    x1=0
    y1=0
    x2=0
    y2=3.25
    x3=2
    y3=3.25
    x4=15
    y4=0.25
    x5=15
    y5=0
    x6=0
    y6=0
    
    #Extrude
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
    L=Part.Face(lshape_wire)
    Clamping=  L.extrude(Base.Vector(0, 0, 1.5))
    Clamping.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180)
    Clamping.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), -90)
    TranslationClamping=(15,-4.25,7.75)
    Clamping.translate(TranslationClamping)
    #Part.show(Clamping)
    fused19=fused18.fuse(Clamping)
    Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
    #Part.show(Clamping)
    fused20=fused19.fuse(Clamping)
    Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
    #Part.show(Clamping)
    fused21=fused20.fuse(Clamping)
    Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
    #Part.show(Clamping)
    fused22=fused21.fuse(Clamping)
    
    TranslationClamping=(0,0,10)
    Clamping.translate(TranslationClamping)
    #Part.show(Clamping)
    fused23=fused22.fuse(Clamping)
    Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
    #Part.show(Clamping)
    fused24=fused23.fuse(Clamping)
    Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
    #Part.show(Clamping)
    fused25=fused24.fuse(Clamping)
    Clamping.rotate(Base.Vector(0, 0, 30),Base.Vector(1, 0, 0), -90)
    #Part.show(Clamping)
    fused26=fused25.fuse(Clamping)
    fused26.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
    AssemblyTranslation=(-30,0,0)
    fused26.translate(AssemblyTranslation)
    
    #chamferinnerring
    Holder4=App.ActiveDocument.addObject("Part::Feature", "myHolder4")
    Holder4.Shape=fused26
    Holder4.Shape=Holder4.Shape.removeSplitter()
    
    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "DOE_Holder1")
    chmfr.Base = App.ActiveDocument.myHolder4
    myEdges = []
    

    myEdges.append((2, 1.74, 1.74))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((144, 1.74, 1.74))
    myEdges.append((170, 1.74, 1.74))
    myEdges.append((184, 1.74, 1.74))
    myEdges.append((209, 1.74, 1.74))
    myEdges.append((223, 1.74, 1.74))
    myEdges.append((248, 1.74, 1.74))
    myEdges.append((270, 1.74, 1.74))
    

    myEdges.append((21, 1.5, 1.5))
    myEdges.append((156, 1.5, 1.5))
    myEdges.append((158, 1.5, 1.5))
    myEdges.append((195, 1.5, 1.5))
    myEdges.append((197, 1.5, 1.5))
    myEdges.append((234, 1.5, 1.5))
    myEdges.append((236, 1.5, 1.5))
    myEdges.append((258, 1.5, 1.5))
    myEdges.append((394, 1.5, 1.5))
    myEdges.append((395, 1.5, 1.5))
    myEdges.append((396, 1.5, 1.5))
    myEdges.append((397, 1.5, 1.5))
    myEdges.append((398, 1.5, 1.5))
    myEdges.append((399, 1.5, 1.5))
    myEdges.append((400, 1.5, 1.5))
    myEdges.append((401, 1.5, 1.5))
    myEdges.append((402, 1.5, 1.5))
    myEdges.append((403, 1.5, 1.5))
    myEdges.append((404, 1.5, 1.5))
    myEdges.append((405, 1.5, 1.5))
    myEdges.append((112, 7.0, 7.0))
    myEdges.append((113, 7.0, 7.0))
    myEdges.append((114, 7.0, 7.0))
    myEdges.append((128, 7.0, 7.0))


    chmfr.Edges = myEdges

    Gui.ActiveDocument.myHolder4.Visibility = False


    App.ActiveDocument.recompute()
   
    chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)
    ###DOE-Holder1_End############################################################
    ###DOE-Holder3##############################################################
    #Base
    BossExtrude1=Part.makeBox(40,30,2.5)

    #Square Hole
    CutExtrude1=Part.makeBox(Height,Width,2.5)
    TranslationCutExtrude1=(20-Height/2,15-Width/2,0)
    #TranslationCutExtrude1=(17,12,0)
    CutExtrude1.translate(TranslationCutExtrude1)
    PartCutExtrude1=BossExtrude1.cut(CutExtrude1)
    DOEHolder3Translation=(-20,-15,-19.5)
    PartCutExtrude1.translate(DOEHolder3Translation)

    #chamfer
    DOE_Holder_3=App.ActiveDocument.addObject("Part::Feature", "DOE_Holder_3")
    DOE_Holder_3.Shape=PartCutExtrude1
    DOE_Holder_3.Shape=DOE_Holder_3.Shape.removeSplitter()

    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "DOE_Holder3")
    chmfr.Base = App.ActiveDocument.DOE_Holder_3
    myEdges = []

    myEdges.append((1, 2.0, 2.0))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((3, 2.0, 2.0))
    myEdges.append((6, 2.0, 2.0))
    myEdges.append((15, 2.0, 2.0))


    chmfr.Edges = myEdges
    Gui.ActiveDocument.DOE_Holder_3.Visibility = False

    App.ActiveDocument.recompute()
    
    chmfr.ViewObject.ShapeColor = (232/255,113/225,8/225)
    ###DOE-Holder3_End###########################################################
    ###Rod1##################################################################
    #BossExtrude1
    BossExtrude1=Part.makeCylinder(4/2,RodLength)
    #Part.show(BossExtrude1)
    TranslationRod1=(20.5,0,-15)
    BossExtrude1.translate(TranslationRod1)
    
    #Fillets
    Rod1=App.ActiveDocument.addObject("Part::Feature", "Rod1")
    Rod1.Shape=BossExtrude1



    App.ActiveDocument.addObject("Part::Fillet","MetalRod1")
    App.ActiveDocument.MetalRod1.Base = App.ActiveDocument.Rod1
    __fillets__ = []
    __fillets__.append((1,0.50,0.50))
    __fillets__.append((3,0.50,0.50))
    App.ActiveDocument.MetalRod1.Edges = __fillets__
    del __fillets__

    Rod1.ViewObject.ShapeColor = (0.3,0.3,0.3)
    Gui.ActiveDocument.Rod1.Visibility = False
    App.ActiveDocument.recompute()
    ###Rod1_End###############################################################
    ###Rod2##################################################################
    #BossExtrude1
    BossExtrude1=Part.makeCylinder(4/2,RodLength)
    #Part.show(BossExtrude1)
    TranslationRod2=(-20.5,0,-15)
    BossExtrude1.translate(TranslationRod2)

    #Fillets
    Rod2=App.ActiveDocument.addObject("Part::Feature", "Rod2")
    Rod2.Shape=BossExtrude1



    App.ActiveDocument.addObject("Part::Fillet","MetalRod2")
    App.ActiveDocument.MetalRod2.Base = App.ActiveDocument.Rod2
    __fillets__ = []
    __fillets__.append((1,0.50,0.50))
    __fillets__.append((3,0.50,0.50))
    App.ActiveDocument.MetalRod2.Edges = __fillets__
    del __fillets__

    Rod2.ViewObject.ShapeColor = (0.3,0.3,0.3)
    Gui.ActiveDocument.Rod2.Visibility = False
    App.ActiveDocument.recompute()
    ###Rod2_End###############################################################
    ###Rod3##################################################################
    #BossExtrude1
    BossExtrude1=Part.makeCylinder(4/2,RodLength)
    #Part.show(BossExtrude1)
    TranslationRod3=(0,20.5,-15)
    BossExtrude1.translate(TranslationRod3)

    #Fillets
    Rod3=App.ActiveDocument.addObject("Part::Feature", "Rod3")
    Rod3.Shape=BossExtrude1

    

    App.ActiveDocument.addObject("Part::Fillet","MetalRod3")
    App.ActiveDocument.MetalRod3.Base = App.ActiveDocument.Rod3
    __fillets__ = []
    __fillets__.append((1,0.50,0.50))
    __fillets__.append((3,0.50,0.50))
    App.ActiveDocument.MetalRod3.Edges = __fillets__
    del __fillets__

    Rod3.ViewObject.ShapeColor = (0.3,0.3,0.3)
    Gui.ActiveDocument.Rod3.Visibility = False
    App.ActiveDocument.recompute()
    ###Rod3_End###############################################################
    ###Rod4##################################################################
    #BossExtrude1
    BossExtrude1=Part.makeCylinder(4/2,RodLength)
    #Part.show(BossExtrude1)
    TranslationRod4=(0,-20.5,-15)
    BossExtrude1.translate(TranslationRod4)

    #Fillets
    Rod4=App.ActiveDocument.addObject("Part::Feature", "Rod4")
    Rod4.Shape=BossExtrude1



    App.ActiveDocument.addObject("Part::Fillet","MetalRod4")
    App.ActiveDocument.MetalRod4.Base = App.ActiveDocument.Rod4
    __fillets__ = []
    __fillets__.append((1,0.50,0.50))
    __fillets__.append((3,0.50,0.50))
    App.ActiveDocument.MetalRod4.Edges = __fillets__
    del __fillets__

    Rod4.ViewObject.ShapeColor = (0.3,0.3,0.3)
    Gui.ActiveDocument.Rod4.Visibility = False
    App.ActiveDocument.recompute()
    ###Rod4_End###############################################################
    ###Lens-Holder#############################################################
    if LensBin==1:
        #Definition
        #DL=16.2
        ##DL=8.9*2
        #DSA=106/15*DL-431/5
        #DSA=106/15*LHD-431/5+1+14+4+(LHD-16.2)*2
        #DSA=106/15*LHD-431/5
        #DSA=47.28+(LHD-16.2)*8
        DSA=6.1*DL-58.6
        DSI=DSA-5
        #MM=4*DL-42
        #MM=4*LHD-42+7+2+(LHD-16.2)/2*2
        #MM=4*LHD-42
        #MM=31.8+(LHD-16.2)*4.25
        MM=3.5*DL-27.8
        ##Thickness=8
        #HoleTolerance=0
        #RectangleTolerance=0
        #ToleranceNubble=0


	        
        #OuterRing
        BossExtrude1=Part.makeCylinder(40/2,Thickness)
        CutExtrude1=Part.makeCylinder(33/2,Thickness)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        
	        
        #InnerRing
        #BossExtrude2=Part.makeCylinder((DL+5)/2,Thickness)
        #CutExtrude2=Part.makeCylinder(DL/2,Thickness)
        #PartBossExtrude2=BossExtrude2.cut(CutExtrude2)

        #InnerRing
        if DL>=14:
            BossExtrude2=Part.makeCylinder((DL+5)/2,Thickness)
            CutExtrude2=Part.makeCylinder(DL/2,Thickness)
            PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
        elif DL<14:
            BossExtrude2=Part.makeCylinder((DL+5+14-DL)/2,Thickness)
            CutExtrude2=Part.makeCylinder(DL/2,Thickness)
            PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
    	        
    	
        #CutsInnerRing
        x1=0
        y1=0
        x2=(DL+4)*math.sin((20)*2*pi/360)
        y2=DL+4
        x3=-(DL+4)*math.sin((20)*2*pi/360)
        y3=DL+4
        x4=0
        y4=0
	        
	        
        #lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
        L=Part.Face(lshape_wire)
        K1 = L.extrude(Base.Vector(0, 0, Thickness))
        K2 = L.extrude(Base.Vector(0, 0, Thickness))
        K3 = L.extrude(Base.Vector(0, 0, Thickness))
        K4 = L.extrude(Base.Vector(0, 0, Thickness))
        K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
        K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
        K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)
        C1=PartBossExtrude2.cut(K1)
        C2=C1.cut(K2)
        C3=C2.cut(K3)
        C4=C3.cut(K4)
    	        
	
        #SpringElements
        #BossExtrude3=Part.makeCylinder(DSA/2,Thickness)
        #CutExtrude3=Part.makeCylinder(DSI/2,Thickness)
        #PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
        #TranslationPartBossExtrude3=(MM,0,0)
        #PartBossExtrude3.translate(TranslationPartBossExtrude3)
        #BossExtrude4=Part.makeCylinder(DSA*2,Thickness)
        #CutExtrude4=Part.makeCylinder(36/2,Thickness)
        #PartBossExtrude4=BossExtrude4.cut(CutExtrude4)




        if DL>=14:
            #SpringElements
            BossExtrude3=Part.makeCylinder(DSA/2,Thickness)
            CutExtrude3=Part.makeCylinder(DSI/2,Thickness)
            PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
            TranslationPartBossExtrude3=(MM,0,0)
            PartBossExtrude3.translate(TranslationPartBossExtrude3)
            BossExtrude4=Part.makeCylinder(DSA*2,Thickness)
            CutExtrude4=Part.makeCylinder(36/2,Thickness)
            PartBossExtrude4=BossExtrude4.cut(CutExtrude4)

        elif DL<14:
            #SpringElements
            BossExtrude3=Part.makeCylinder(26.8/2,Thickness)
            CutExtrude3=Part.makeCylinder(21.8/2,Thickness)
            PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
            TranslationPartBossExtrude3=(21.2,0,0)
            PartBossExtrude3.translate(TranslationPartBossExtrude3)
            BossExtrude4=Part.makeCylinder(26.8*2,Thickness)
            CutExtrude4=Part.makeCylinder(36/2,Thickness)
            PartBossExtrude4=BossExtrude4.cut(CutExtrude4)




	        
	
        #UnionParts
        fused1 = PartBossExtrude1.fuse(C4)
        

        PartBossExtrude5=PartBossExtrude3.cut(PartBossExtrude4)
        #Part.show(PartBossExtrude5)
        fused2= fused1.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        #Part.show(PartBossExtrude5)
        fused3= fused2.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        #Part.show(PartBossExtrude5)
        fused4= fused3.fuse(PartBossExtrude5)
        PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        #Part.show(PartBossExtrude5)
        fused5= fused4.fuse(PartBossExtrude5)
    

        #OuterRingSquares
        Square=Part.makeBox(5.13,15,Thickness)
        TranslationSquare=(17.37,-15/2,0)
        Square.translate(TranslationSquare)
        #Part.show(Square)
        
    	
        #CutoutsOuterRingSquares1
        Hole=Part.makeCylinder(2.1,Thickness)
        TranslationHole=(20.5,0,0)
        Hole.translate(TranslationHole)
        PartCutout=Square.cut(Hole)
        fused6=fused5.cut(Hole)

        Rectangle=Part.makeBox(0.69+0.5,3.2,Thickness)
        TranslationRectangle=(21.81-0.25,-3.2/2,0)
        Rectangle.translate(TranslationRectangle)
        PartCut=PartCutout.cut(Rectangle)
        fused7= fused6.fuse(PartCut)
        
        #CutoutsOuterRingSquares2
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        fused8=fused7.fuse(PartCut)
        fused9=fused8.cut(Hole)

    	
        #CutoutsOuterRingSquares3
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
        fused10=fused9.fuse(PartCut)
        fused11=fused10.cut(Hole)
        
	
        #CutoutsOuterRingSquares4
        PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
        fused12=fused11.fuse(PartCut)
        fused13=fused12.cut(Hole)
        #Part.show(fused13)

	
	

        #Outer Polygon
        #x1=18+2.75/(math.tan((30)*2*pi/360))
        x1=22.7
        y1=-5
        #x2=18+2.75/(math.tan((30)*2*pi/360))
        x2=22.7
        y2=5
        x3=18
        y3=5
        x4=18
        y4=-5
        #x5=18+2.75/(math.tan((30)*2*pi/360))
        x5=22.7
        y5=-5


        lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
        L=Part.Face(lshape_wire)
        K1 = L.extrude(Base.Vector(0, 0, Thickness))
        K2 = L.extrude(Base.Vector(0, 0, Thickness))
        K3 = L.extrude(Base.Vector(0, 0, Thickness))
        K4 = L.extrude(Base.Vector(0, 0, Thickness))
        K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
        K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
        K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
        K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

        fused14=fused13.fuse(K1)
        fused15=fused14.fuse(K2)
        fused16=fused15.fuse(K3)
        fused17=fused16.fuse(K4)
        #Part.show(fused17)
   
        #TranslationLensHolder=(0,0,69	
        TranslationLensHolder=(0,0,83-DLL)
        fused17.translate(TranslationLensHolder)
        #Part.show(fused17)



  
        #chamferinnerring
        Holder1=App.ActiveDocument.addObject("Part::Feature", "myHolder1")
        Holder1.Shape=fused17
        Holder1.Shape=Holder1.Shape.removeSplitter()
      

        App.ActiveDocument.addObject("Part::Fillet","LensHolder1")
        App.ActiveDocument.LensHolder1.Base = App.ActiveDocument.myHolder1
        __fillets__ = []
        __fillets__.append((184,0.50,0.50))
        __fillets__.append((185,0.50,0.50))
        __fillets__.append((197,0.50,0.50))
        __fillets__.append((198,0.50,0.50))
        __fillets__.append((221,0.50,0.50))
        __fillets__.append((222,0.50,0.50))
        __fillets__.append((209,0.50,0.50))
        __fillets__.append((210,0.50,0.50))
        App.ActiveDocument.LensHolder1.Edges = __fillets__
        del __fillets__
        Gui.ActiveDocument.myHolder1.Visibility = False



        chmfr = App.ActiveDocument.addObject("Part::Chamfer", "LensHolder")
        #chmfr.Base = App.ActiveDocument.myHolder4
        chmfr.Base = App.ActiveDocument.LensHolder1
        myEdges = []


        myEdges.append((9, 1.0, 1.0))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((10, 1.0, 1.0))
        myEdges.append((25, 1.0, 1.0))
        myEdges.append((26, 1.0, 1.0))
        myEdges.append((115, 1.0, 1.0))
        myEdges.append((116, 1.0, 1.0))
        myEdges.append((118, 1.0, 1.0))
        myEdges.append((147, 1.0, 1.0))
        myEdges.append((150, 1.0, 1.0))
        myEdges.append((38, 1.0, 1.0))
        myEdges.append((39, 1.0, 1.0))
        myEdges.append((40, 1.0, 1.0))
        myEdges.append((41, 1.0, 1.0))
        myEdges.append((42, 1.0, 1.0))
        myEdges.append((52, 1.0, 1.0))
        myEdges.append((53, 1.0, 1.0))
        myEdges.append((54, 1.0, 1.0))
        myEdges.append((55, 1.0, 1.0))
        myEdges.append((56, 1.0, 1.0))
        myEdges.append((66, 1.0, 1.0))
        myEdges.append((67, 1.0, 1.0))
        myEdges.append((68, 1.0, 1.0))
        myEdges.append((69, 1.0, 1.0))
        myEdges.append((70, 1.0, 1.0))
        myEdges.append((80, 1.0, 1.0))
        myEdges.append((81, 1.0, 1.0))
        myEdges.append((82, 1.0, 1.0))
        myEdges.append((83, 1.0, 1.0))
        myEdges.append((84, 1.0, 1.0))
        myEdges.append((173, 1.0, 1.0))
        myEdges.append((176, 1.0, 1.0))
        myEdges.append((177, 1.0, 1.0))
        myEdges.append((178, 1.0, 1.0))
        myEdges.append((180, 1.0, 1.0))
        myEdges.append((199, 1.0, 1.0))
        myEdges.append((202, 1.0, 1.0))
        myEdges.append((203, 1.0, 1.0))
        myEdges.append((204, 1.0, 1.0))
        myEdges.append((206, 1.0, 1.0))
        myEdges.append((225, 1.0, 1.0))
        myEdges.append((228, 1.0, 1.0))
        myEdges.append((229, 1.0, 1.0))
        myEdges.append((230, 1.0, 1.0))
        myEdges.append((232, 1.0, 1.0))
        myEdges.append((251, 1.0, 1.0))
        myEdges.append((254, 1.0, 1.0))
        myEdges.append((255, 1.0, 1.0))
        myEdges.append((256, 1.0, 1.0))
        myEdges.append((258, 1.0, 1.0))
        myEdges.append((169, 2.0, 2.0))
        myEdges.append((182, 2.0, 2.0))
        myEdges.append((195, 2.0, 2.0))
        myEdges.append((208, 2.0, 2.0))
        myEdges.append((221, 2.0, 2.0))
        myEdges.append((234, 2.0, 2.0))
        myEdges.append((247, 2.0, 2.0))
        myEdges.append((260, 2.0, 2.0))

        chmfr.Edges = myEdges
    
        Gui.ActiveDocument.LensHolder1.Visibility = False
    
    
        App.ActiveDocument.recompute()
            
        #Holder4.ViewObject.ShapeColor = (103/204,125/204,204/204)
        chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)
    
    else:
        print("no Lens")
    ###Lens-Holder_End##########################################################
    ###Lens#################################################################
    if LensBin==1:
        #init
        #d=2*8.0
        R=2*DL/2
    
        sphere = Part.makeSphere(R)
        cube = Part.makeBox(2*R,2*R,2*R)
        x=math.cos(math.asin((DL/2)/(R)))*R
        translation = (-x,-R,-R)
        cube.translate(translation)
        PartCutExtrude1=sphere.cut(cube)
        #Part.show(PartCutExtrude1)

        Cylinder=Part.makeCylinder(DL/2,DL/10)
        Cylinder.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
        translationCylinder = (-x,0,0)
        Cylinder.translate(translationCylinder)
        #Part.show(Cylinder)


        sphere2 = Part.makeSphere(R)
        cube2 = Part.makeBox(2*R,2*R,2*R)
        x2=math.cos(math.asin((DL/2)/(R)))*R
        translation2 = (-2*R+x2,-R,-R)
        cube2.translate(translation2)
        PartCutExtrude2=sphere2.cut(cube2)
        translation3=(-2*x+DL/10,0,0)
        PartCutExtrude2.translate(translation3)
        #Part.show(PartCutExtrude2)

        fused1=PartCutExtrude1.fuse(Cylinder)
        fused2=fused1.fuse(PartCutExtrude2)
        #Part.show(fused2)
        fused2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), -90)
        #TranslationLens=(0,0,84.75+DL-16)
        #TranslationLens=(0,0,84.75+DL-2-DLL)
        TranslationLens=(0,0,84.75+DL-1-0.1*DL-DLL)
        fused2.translate(TranslationLens)

        #Display
        Lens = App.ActiveDocument.addObject("Part::Feature", "Lens")
        Lens.Shape=fused2
        Lens.Shape=Lens.Shape.removeSplitter()
        Lens.ViewObject.ShapeColor = (152/255,245/255,255/255)
        Lens.ViewObject.Transparency=50

    else:
        print("no Lens")
    ###Lens_End##############################################################
    ###Laser-Holder1############################################################
    #Definition
    #DL=16.2
    ##LHD=7.9*2
    #DSA=106/15*DL-431/5
    #DSA=106/15*LHD-431/5+1+14+4+(LHD-16.2)*2
    #DSA=106/15*LHD-431/5
    #DSA=47.28+(LHD-16.2)*8
    DSA=6.1*LHD-58.6
    DSI=DSA-5
    #MM=4*DL-42
    #MM=4*LHD-42+7+2+(LHD-16.2)/2*2
    #MM=4*LHD-42
    #MM=31.8+(LHD-16.2)*4.25
    MM=3.5*LHD-27.8
    #HoleTolerance=0
    #RectangleTolerance=0
    #ToleranceNubble=0
    

	        
    #OuterRing
    BossExtrude1=Part.makeCylinder(40/2,15)
    CutExtrude1=Part.makeCylinder(33/2,15)
    PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        
	        
    #InnerRing

    if LHD >=14:
        BossExtrude2=Part.makeCylinder((LHD+5)/2,15)
        CutExtrude2=Part.makeCylinder(LHD/2,15)
        PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
    elif LHD<14:
        BossExtrude2=Part.makeCylinder((LHD+5+14-LHD)/2,15)
        CutExtrude2=Part.makeCylinder(LHD/2,15)
        PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
	        
	
    #CutsInnerRing
    x1=0
    y1=0
    x2=(LHD+4)*math.sin((20)*2*pi/360)
    y2=LHD+4
    x3=-(LHD+4)*math.sin((20)*2*pi/360)
    y3=LHD+4
    x4=0
    y4=0
	        
	        
    #lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
    L=Part.Face(lshape_wire)
    K1 = L.extrude(Base.Vector(0, 0, 15))
    K2 = L.extrude(Base.Vector(0, 0, 15))
    K3 = L.extrude(Base.Vector(0, 0, 15))
    K4 = L.extrude(Base.Vector(0, 0, 15))
    K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
    K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
    K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)
    C1=PartBossExtrude2.cut(K1)
    C2=C1.cut(K2)
    C3=C2.cut(K3)
    C4=C3.cut(K4)
	        
	
    if LHD>=14:
        #SpringElements
        BossExtrude3=Part.makeCylinder(DSA/2,15)
        CutExtrude3=Part.makeCylinder(DSI/2,15)
        PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
        TranslationPartBossExtrude3=(MM,0,0)
        PartBossExtrude3.translate(TranslationPartBossExtrude3)
        BossExtrude4=Part.makeCylinder(DSA*2,15)
        CutExtrude4=Part.makeCylinder(36/2,15)
        PartBossExtrude4=BossExtrude4.cut(CutExtrude4)

    elif LHD<14:
        #SpringElements
        BossExtrude3=Part.makeCylinder(26.8/2,15)
        CutExtrude3=Part.makeCylinder(21.8/2,15)
        PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
        TranslationPartBossExtrude3=(21.2,0,0)
        PartBossExtrude3.translate(TranslationPartBossExtrude3)
        BossExtrude4=Part.makeCylinder(26.8*2,15)
        CutExtrude4=Part.makeCylinder(36/2,15)
        PartBossExtrude4=BossExtrude4.cut(CutExtrude4)
	        
	
    #UnionParts
    fused1 = PartBossExtrude1.fuse(C4)
    

    PartBossExtrude5=PartBossExtrude3.cut(PartBossExtrude4)
    #Part.show(PartBossExtrude5)
    fused2= fused1.fuse(PartBossExtrude5)
    PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    #Part.show(PartBossExtrude5)
    fused3= fused2.fuse(PartBossExtrude5)
    PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    #Part.show(PartBossExtrude5)
    fused4= fused3.fuse(PartBossExtrude5)
    PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    #Part.show(PartBossExtrude5)
    fused5= fused4.fuse(PartBossExtrude5)


    #OuterRingSquares
    Square=Part.makeBox(5.13,15,15)
    TranslationSquare=(17.37,-15/2,0)
    Square.translate(TranslationSquare)
    #Part.show(Square)

	
    #CutoutsOuterRingSquares1
    Hole=Part.makeCylinder(2.1,15)
    TranslationHole=(20.5,0,0)
    Hole.translate(TranslationHole)
    PartCutout=Square.cut(Hole)
    fused6=fused5.cut(Hole)

    Rectangle=Part.makeBox(0.69+0.5,3.2,15)
    TranslationRectangle=(21.81-0.25,-3.2/2,0)
    Rectangle.translate(TranslationRectangle)
    PartCut=PartCutout.cut(Rectangle)
    fused7= fused6.fuse(PartCut)

    #CutoutsOuterRingSquares2
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    fused8=fused7.fuse(PartCut)
    fused9=fused8.cut(Hole)

    	
    #CutoutsOuterRingSquares3
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    fused10=fused9.fuse(PartCut)
    fused11=fused10.cut(Hole)
    
	
    #CutoutsOuterRingSquares4
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    fused12=fused11.fuse(PartCut)
    fused13=fused12.cut(Hole)
    #Part.show(fused13)

	
	

    #Outer Polygon
    #x1=18+2.75/(math.tan((30)*2*pi/360))
    x1=22.7
    y1=-5
    #x2=18+2.75/(math.tan((30)*2*pi/360))
    x2=22.7
    y2=5
    x3=18
    y3=5
    x4=18
    y4=-5
    #x5=18+2.75/(math.tan((30)*2*pi/360))
    x5=22.7
    y5=-5


    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
    L=Part.Face(lshape_wire)
    K1 = L.extrude(Base.Vector(0, 0, 15))
    K2 = L.extrude(Base.Vector(0, 0, 15))
    K3 = L.extrude(Base.Vector(0, 0, 15))
    K4 = L.extrude(Base.Vector(0, 0, 15))
    K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
    K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
    K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

    fused14=fused13.fuse(K1)
    fused15=fused14.fuse(K2)
    fused16=fused15.fuse(K3)
    fused17=fused16.fuse(K4)
    #Part.show(fused17)
   
	
    #TranslationHolder2=(0,0,102.5)
    #TranslationHolder2=(0,0,192.5-LL)
    #TranslationHolder2=(0,0,RodLength-7.5-LL)
    TranslationHolder2=(0,0,RodLength-31-LL)
    fused17.translate(TranslationHolder2)
    #Part.show(fused17)



  
    #chamferinnerring
    Holder2=App.ActiveDocument.addObject("Part::Feature", "myHolder2")
    Holder2.Shape=fused17
    Holder2.Shape=Holder2.Shape.removeSplitter()
  

    App.ActiveDocument.addObject("Part::Fillet","LaserHolder_1")
    App.ActiveDocument.LaserHolder_1.Base = App.ActiveDocument.myHolder2
    __fillets__ = []
    __fillets__.append((184,0.50,0.50))
    __fillets__.append((185,0.50,0.50))
    __fillets__.append((197,0.50,0.50))
    __fillets__.append((198,0.50,0.50))
    __fillets__.append((221,0.50,0.50))
    __fillets__.append((222,0.50,0.50))
    __fillets__.append((209,0.50,0.50))
    __fillets__.append((210,0.50,0.50))
    App.ActiveDocument.LaserHolder_1.Edges = __fillets__
    del __fillets__
    Gui.ActiveDocument.myHolder2.Visibility = False


    
    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "LaserHolder1")
    #chmfr.Base = App.ActiveDocument.myHolder4
    chmfr.Base = App.ActiveDocument.LaserHolder_1
    myEdges = []
    

    myEdges.append((9, 1.0, 1.0))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((10, 1.0, 1.0))
    myEdges.append((25, 1.0, 1.0))
    myEdges.append((26, 1.0, 1.0))
    myEdges.append((115, 1.0, 1.0))
    myEdges.append((116, 1.0, 1.0))
    myEdges.append((118, 1.0, 1.0))
    myEdges.append((147, 1.0, 1.0))
    myEdges.append((150, 1.0, 1.0))
    myEdges.append((38, 1.0, 1.0))
    myEdges.append((39, 1.0, 1.0))
    myEdges.append((40, 1.0, 1.0))
    myEdges.append((41, 1.0, 1.0))
    myEdges.append((42, 1.0, 1.0))
    myEdges.append((52, 1.0, 1.0))
    myEdges.append((53, 1.0, 1.0))
    myEdges.append((54, 1.0, 1.0))
    myEdges.append((55, 1.0, 1.0))
    myEdges.append((56, 1.0, 1.0))
    myEdges.append((66, 1.0, 1.0))
    myEdges.append((67, 1.0, 1.0))
    myEdges.append((68, 1.0, 1.0))
    myEdges.append((69, 1.0, 1.0))
    myEdges.append((70, 1.0, 1.0))
    myEdges.append((80, 1.0, 1.0))
    myEdges.append((81, 1.0, 1.0))
    myEdges.append((82, 1.0, 1.0))
    myEdges.append((83, 1.0, 1.0))
    myEdges.append((84, 1.0, 1.0))
    myEdges.append((173, 1.0, 1.0))
    myEdges.append((176, 1.0, 1.0))
    myEdges.append((177, 1.0, 1.0))
    myEdges.append((178, 1.0, 1.0))
    myEdges.append((180, 1.0, 1.0))
    myEdges.append((199, 1.0, 1.0))
    myEdges.append((202, 1.0, 1.0))
    myEdges.append((203, 1.0, 1.0))
    myEdges.append((204, 1.0, 1.0))
    myEdges.append((206, 1.0, 1.0))
    myEdges.append((225, 1.0, 1.0))
    myEdges.append((228, 1.0, 1.0))
    myEdges.append((229, 1.0, 1.0))
    myEdges.append((230, 1.0, 1.0))
    myEdges.append((232, 1.0, 1.0))
    myEdges.append((251, 1.0, 1.0))
    myEdges.append((254, 1.0, 1.0))
    myEdges.append((255, 1.0, 1.0))
    myEdges.append((256, 1.0, 1.0))
    myEdges.append((258, 1.0, 1.0))
    myEdges.append((169, 2.0, 2.0))
    myEdges.append((182, 2.0, 2.0))
    myEdges.append((195, 2.0, 2.0))
    myEdges.append((208, 2.0, 2.0))
    myEdges.append((221, 2.0, 2.0))
    myEdges.append((234, 2.0, 2.0))
    myEdges.append((247, 2.0, 2.0))
    myEdges.append((260, 2.0, 2.0))

    chmfr.Edges = myEdges

    Gui.ActiveDocument.LaserHolder_1.Visibility = False


    App.ActiveDocument.recompute()
    
    #Holder4.ViewObject.ShapeColor = (103/204,125/204,204/204)
    chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)

    ###Laser-Holder1_End#########################################################
    
    ###Laser-Holder2############################################################
    #Definition
    #DL=16.2
    ##LHD=7.9*2
    #DSA=106/15*DL-431/5
    #DSA=106/15*LHD-431/5+1+14+4+(LHD-16.2)*2
    #DSA=106/15*LHD-431/5
    #DSA=47.28+(LHD-16.2)*8
    DSA=6.1*LHD-58.6
    DSI=DSA-5
    #MM=4*DL-42
    #MM=4*LHD-42+7+2+(LHD-16.2)/2*2
    #MM=4*LHD-42
    #MM=31.8+(LHD-16.2)*4.25
    MM=3.5*LHD-27.8
    #HoleTolerance=0
    #RectangleTolerance=0
    #ToleranceNubble=0


	        
    #OuterRing
    BossExtrude1=Part.makeCylinder(40/2,15)
    CutExtrude1=Part.makeCylinder(33/2,15)
    PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
	        
	        

    #InnerRing
    if LHD >=14:
        BossExtrude2=Part.makeCylinder((LHD+5)/2,15)
        CutExtrude2=Part.makeCylinder(LHD/2,15)
        PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
    elif LHD<14:
        BossExtrude2=Part.makeCylinder((LHD+5+14-LHD)/2,15)
        CutExtrude2=Part.makeCylinder(LHD/2,15)
        PartBossExtrude2=BossExtrude2.cut(CutExtrude2)
	        
	
    #CutsInnerRing
    x1=0
    y1=0
    x2=(LHD+4)*math.sin((20)*2*pi/360)
    y2=LHD+4
    x3=-(LHD+4)*math.sin((20)*2*pi/360)
    y3=LHD+4
    x4=0
    y4=0
	        
	        
    #lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0)])
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
    L=Part.Face(lshape_wire)
    K1 = L.extrude(Base.Vector(0, 0, 15))
    K2 = L.extrude(Base.Vector(0, 0, 15))
    K3 = L.extrude(Base.Vector(0, 0, 15))
    K4 = L.extrude(Base.Vector(0, 0, 15))
    K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
    K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
    K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)
    C1=PartBossExtrude2.cut(K1)
    C2=C1.cut(K2)
    C3=C2.cut(K3)
    C4=C3.cut(K4)
	        

    if LHD>=14:
        #SpringElements
        BossExtrude3=Part.makeCylinder(DSA/2,15)
        CutExtrude3=Part.makeCylinder(DSI/2,15)
        PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
        TranslationPartBossExtrude3=(MM,0,0)
        PartBossExtrude3.translate(TranslationPartBossExtrude3)
        BossExtrude4=Part.makeCylinder(DSA*2,15)
        CutExtrude4=Part.makeCylinder(36/2,15)
        PartBossExtrude4=BossExtrude4.cut(CutExtrude4)

    elif LHD<14:
        #SpringElements
        BossExtrude3=Part.makeCylinder(26.8/2,15)
        CutExtrude3=Part.makeCylinder(21.8/2,15)
        PartBossExtrude3=BossExtrude3.cut(CutExtrude3)
        TranslationPartBossExtrude3=(21.2,0,0)
        PartBossExtrude3.translate(TranslationPartBossExtrude3)
        BossExtrude4=Part.makeCylinder(26.8*2,15)
        CutExtrude4=Part.makeCylinder(36/2,15)
        PartBossExtrude4=BossExtrude4.cut(CutExtrude4)
	
	
    #UnionParts
    fused1 = PartBossExtrude1.fuse(C4)
            

    PartBossExtrude5=PartBossExtrude3.cut(PartBossExtrude4)
    #Part.show(PartBossExtrude5)
    fused2= fused1.fuse(PartBossExtrude5)
    PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    #Part.show(PartBossExtrude5)
    fused3= fused2.fuse(PartBossExtrude5)
    PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    #Part.show(PartBossExtrude5)
    fused4= fused3.fuse(PartBossExtrude5)
    PartBossExtrude5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    #Part.show(PartBossExtrude5)
    fused5= fused4.fuse(PartBossExtrude5)


    #OuterRingSquares
    Square=Part.makeBox(5.13,15,15)
    TranslationSquare=(17.37,-15/2,0)
    Square.translate(TranslationSquare)
    #Part.show(Square)

	
    #CutoutsOuterRingSquares1
    Hole=Part.makeCylinder(2.1,15)
    TranslationHole=(20.5,0,0)
    Hole.translate(TranslationHole)
    PartCutout=Square.cut(Hole)
    fused6=fused5.cut(Hole)

    Rectangle=Part.makeBox(0.69+0.5,3.2,15)
    TranslationRectangle=(21.81-0.25,-3.2/2,0)
    Rectangle.translate(TranslationRectangle)
    PartCut=PartCutout.cut(Rectangle)
    fused7= fused6.fuse(PartCut)

    #CutoutsOuterRingSquares2
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    fused8=fused7.fuse(PartCut)
    fused9=fused8.cut(Hole)

	
    #CutoutsOuterRingSquares3
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 180)
    fused10=fused9.fuse(PartCut)
    fused11=fused10.cut(Hole)
    
	
    #CutoutsOuterRingSquares4
    PartCut.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    Hole.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 270)
    fused12=fused11.fuse(PartCut)
    fused13=fused12.cut(Hole)
    #Part.show(fused13)

	
	

    #Outer Polygon
    #x1=18+2.75/(math.tan((30)*2*pi/360))
    x1=22.7
    y1=-5
    #x2=18+2.75/(math.tan((30)*2*pi/360))
    x2=22.7
    y2=5
    x3=18
    y3=5
    x4=18
    y4=-5
    x5=22.7
    #x5=18+2.75/(math.tan((30)*2*pi/360))
    y5=-5


    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
    L=Part.Face(lshape_wire)
    K1 = L.extrude(Base.Vector(0, 0, 15))
    K2 = L.extrude(Base.Vector(0, 0, 15))
    K3 = L.extrude(Base.Vector(0, 0, 15))
    K4 = L.extrude(Base.Vector(0, 0, 15))
    K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
    K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
    K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

    fused14=fused13.fuse(K1)
    fused15=fused14.fuse(K2)
    fused16=fused15.fuse(K3)
    fused17=fused16.fuse(K4)
    #Part.show(fused17)
   
	
    TranslationHolder3=(0,0,RodLength-37.5)
    fused17.translate(TranslationHolder3)
    #Part.show(fused17)
    


  
    #chamferinnerring
    Holder3=App.ActiveDocument.addObject("Part::Feature", "myHolder3")
    Holder3.Shape=fused17
    Holder3.Shape=Holder3.Shape.removeSplitter()
  

    App.ActiveDocument.addObject("Part::Fillet","LaserHolder_2")
    App.ActiveDocument.LaserHolder_2.Base = App.ActiveDocument.myHolder3
    __fillets__ = []
    __fillets__.append((184,0.50,0.50))
    __fillets__.append((185,0.50,0.50))
    __fillets__.append((197,0.50,0.50))
    __fillets__.append((198,0.50,0.50))
    __fillets__.append((221,0.50,0.50))
    __fillets__.append((222,0.50,0.50))
    __fillets__.append((209,0.50,0.50))
    __fillets__.append((210,0.50,0.50))
    App.ActiveDocument.LaserHolder_2.Edges = __fillets__
    del __fillets__
    Gui.ActiveDocument.myHolder3.Visibility = False



    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "LaserHolder2")
    #chmfr.Base = App.ActiveDocument.myHolder4
    chmfr.Base = App.ActiveDocument.LaserHolder_2
    myEdges = []


    myEdges.append((9, 1.0, 1.0))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((10, 1.0, 1.0))
    myEdges.append((25, 1.0, 1.0))
    myEdges.append((26, 1.0, 1.0))
    myEdges.append((115, 1.0, 1.0))
    myEdges.append((116, 1.0, 1.0))
    myEdges.append((118, 1.0, 1.0))
    myEdges.append((147, 1.0, 1.0))
    myEdges.append((150, 1.0, 1.0))
    myEdges.append((38, 1.0, 1.0))
    myEdges.append((39, 1.0, 1.0))
    myEdges.append((40, 1.0, 1.0))
    myEdges.append((41, 1.0, 1.0))
    myEdges.append((42, 1.0, 1.0))
    myEdges.append((52, 1.0, 1.0))
    myEdges.append((53, 1.0, 1.0))
    myEdges.append((54, 1.0, 1.0))
    myEdges.append((55, 1.0, 1.0))
    myEdges.append((56, 1.0, 1.0))
    myEdges.append((66, 1.0, 1.0))
    myEdges.append((67, 1.0, 1.0))
    myEdges.append((68, 1.0, 1.0))
    myEdges.append((69, 1.0, 1.0))
    myEdges.append((70, 1.0, 1.0))
    myEdges.append((80, 1.0, 1.0))
    myEdges.append((81, 1.0, 1.0))
    myEdges.append((82, 1.0, 1.0))
    myEdges.append((83, 1.0, 1.0))
    myEdges.append((84, 1.0, 1.0))
    myEdges.append((173, 1.0, 1.0))
    myEdges.append((176, 1.0, 1.0))
    myEdges.append((177, 1.0, 1.0))
    myEdges.append((178, 1.0, 1.0))
    myEdges.append((180, 1.0, 1.0))
    myEdges.append((199, 1.0, 1.0))
    myEdges.append((202, 1.0, 1.0))
    myEdges.append((203, 1.0, 1.0))
    myEdges.append((204, 1.0, 1.0))
    myEdges.append((206, 1.0, 1.0))
    myEdges.append((225, 1.0, 1.0))
    myEdges.append((228, 1.0, 1.0))
    myEdges.append((229, 1.0, 1.0))
    myEdges.append((230, 1.0, 1.0))
    myEdges.append((232, 1.0, 1.0))
    myEdges.append((251, 1.0, 1.0))
    myEdges.append((254, 1.0, 1.0))
    myEdges.append((255, 1.0, 1.0))
    myEdges.append((256, 1.0, 1.0))
    myEdges.append((258, 1.0, 1.0))
    myEdges.append((169, 2.0, 2.0))
    myEdges.append((182, 2.0, 2.0))
    myEdges.append((195, 2.0, 2.0))
    myEdges.append((208, 2.0, 2.0))
    myEdges.append((221, 2.0, 2.0))
    myEdges.append((234, 2.0, 2.0))
    myEdges.append((247, 2.0, 2.0))
    myEdges.append((260, 2.0, 2.0))
    
    chmfr.Edges = myEdges

    Gui.ActiveDocument.LaserHolder_2.Visibility = False


    App.ActiveDocument.recompute()
    
    #Holder4.ViewObject.ShapeColor = (103/204,125/204,204/204)
    chmfr.ViewObject.ShapeColor = (103/204,125/204,0.0)
    ###Laser-Holder2_End##########################################################
    
    ###Laser##################################################################
    #Cylinder
    BossExtrude1=Part.makeCylinder(LHD/2,LL)


    #Cutouts
    BossExtrude2=Part.makeCylinder((LHD+1)/2,1.84)
    CutExtrude1=Part.makeCylinder((LHD-2)/2,1.84)
    PartBossExtrude1=BossExtrude2.cut(CutExtrude1)
    TranslationPartBossExtrude1=(0,0,LL-14.7)
    PartBossExtrude1.translate(TranslationPartBossExtrude1)
    BossExtrude2=BossExtrude1.cut(PartBossExtrude1)

    TranslationPartBossExtrude2=(0,0,1.84*2)
    PartBossExtrude1.translate(TranslationPartBossExtrude2)
    BossExtrude3=BossExtrude2.cut(PartBossExtrude1)

    PartBossExtrude1.translate(TranslationPartBossExtrude2)
    BossExtrude4=BossExtrude3.cut(PartBossExtrude1)

    PartBossExtrude1.translate(TranslationPartBossExtrude2)
    BossExtrude5=BossExtrude4.cut(PartBossExtrude1)

    #Part.show(BossExtrude5)

    #Drillings
    Drilling1=Part.makeCylinder(3/2,3)
    TranslationDrilling1=(0,0,LL-3)
    Drilling1.translate(TranslationDrilling1)
    #Part.show(Drilling1)
    BossExtrude6=BossExtrude5.cut(Drilling1)

    Drilling2=Part.makeCylinder(1.6/2,5)
    TranslationDrilling2=(1.6,0,0)
    Drilling2.translate(TranslationDrilling2)
    #Part.show(Drilling2)
    BossExtrude7=BossExtrude6.cut(Drilling2)

    TranslationDrilling2=(-3.2,0,0)
    Drilling2.translate(TranslationDrilling2)
    #Part.show(Drilling2)
    BossExtrude8=BossExtrude7.cut(Drilling2)

    BossExtrude8.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180)
    TranslationLaser=(0,0,RodLength-22.5)
    BossExtrude8.translate(TranslationLaser)



    #chamfer
    laser=App.ActiveDocument.addObject("Part::Feature", "laser")
    laser.Shape=BossExtrude8
    laser.Shape=laser.Shape.removeSplitter()

    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "Laser")
    chmfr.Base = App.ActiveDocument.laser
    myEdges = []
    
    myEdges.append((13, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((33, 0.5, 0.5))


    chmfr.Edges = myEdges
    Gui.ActiveDocument.laser.Visibility = False

    App.ActiveDocument.recompute()
    
    chmfr.ViewObject.ShapeColor = (0.3,0.3,0.3)
    ###Laser_End###############################################################
    ###Cap###################################################################

    #make sketch
    x1=-23
    y1=-30
    x2=23
    y2=-30
    x3=30
    y3=-23
    x4=30
    y4=23
    x5=23
    y5=30
    x6=-23
    y6=30
    x7=-30
    y7=23
    x8=-30
    y8=-23
    x9=-23
    y9=-30

    #Extrude
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0)])
    L=Part.Face(lshape_wire)
    BasePart=  L.extrude(Base.Vector(0, 0, 3))

    #Part.show(BasePart)
    
    #Drillings
    CentralDrilling = Part.makeCylinder(16/2,3)
    BossExtrude=BasePart.cut(CentralDrilling)

    SmallDrilling = Part.makeCylinder(5/2,3)
    TranslationSmallDrilling1 = (0,-20.5,0)
    SmallDrilling.translate(TranslationSmallDrilling1)
    BossExtrude1=BossExtrude.cut(SmallDrilling)

    TranslationSmallDrilling2 = (0,20.5*2,0)
    SmallDrilling.translate(TranslationSmallDrilling2)
    BossExtrude2=BossExtrude1.cut(SmallDrilling)

    TranslationSmallDrilling3 = (-20.5,-20.5,0)
    SmallDrilling.translate(TranslationSmallDrilling3)
    BossExtrude3=BossExtrude2.cut(SmallDrilling)

    TranslationSmallDrilling4 = (20.5*2,0,0)
    SmallDrilling.translate(TranslationSmallDrilling4)
    BossExtrude4=BossExtrude3.cut(SmallDrilling)

    #Plug
    Basepart1=Part.makeCone(4.18,2.3,7)
    TranslationBasepart1=(0,0,3)
    Basepart1.translate(TranslationBasepart1)
    #Part.show(Basepart1)
    Basepart2=Part.makeCylinder(4.18,3)
    #Part.show(Basepart2)

    fused=Basepart1.fuse(Basepart2)
    #Part.show(fused)


    #make sketch
    x1=0
    y1=0
    x2=-1
    y2=5
    x3=1
    y3=5
    x4=0
    y4=0
    
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0)])
    L=Part.Face(lshape_wire)
    CutPart=  L.extrude(Base.Vector(0, 0, 10))
    #Part.show(CutPart)
    Extrude1=fused.cut(CutPart)

    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    #Part.show(CutPart)
    Extrude2=Extrude1.cut(CutPart)

    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    #Part.show(CutPart)
    Extrude3=Extrude2.cut(CutPart)

    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    #Part.show(CutPart)
    Extrude4=Extrude3.cut(CutPart)

    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    #Part.show(CutPart)
    Extrude5=Extrude4.cut(CutPart)

    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    #Part.show(CutPart)
    Extrude6=Extrude5.cut(CutPart)

    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    #Part.show(CutPart)
    Extrude7=Extrude6.cut(CutPart)

    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    #Part.show(CutPart)
    Extrude8=Extrude7.cut(CutPart)
    #Part.show(Extrude8)


    Central=Part.makeCylinder(2.3,10)
    fused1=Central.fuse(Extrude8)
    #Part.show(fused1)

    Translationfused1=(21.12,21.12,3)
    fused1.translate(Translationfused1)
    fused2=BossExtrude4.fuse(fused1)

    Translationfused2=(-21.12*2,0,0)
    fused1.translate(Translationfused2)
    fused3=fused2.fuse(fused1)
    Translationfused3=(0,-21.12*2,0)
    fused1.translate(Translationfused3)
    fused4=fused3.fuse(fused1)
    Translationfused4=(21.12*2,0,0)
    fused1.translate(Translationfused4)
    fused5=fused4.fuse(fused1)
    
    fused5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180)
    Translationcap=(0,0,RodLength-19.5)
    fused5.translate(Translationcap)

    
    #Display
    cap = App.ActiveDocument.addObject("Part::Feature", "cap")
    cap.Shape=fused5
    cap.Shape=cap.Shape.removeSplitter()
    cap.ViewObject.ShapeColor = (1.0,1.0,192/255)

    ###Cap_End################################################################
    ###Clamping_Holder1##########################################################
    if LensBin==1:
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)
    
    
        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        #clampingholderTranslation=(20.5,0,64)
        clampingholderTranslation=(20.5,0,78-DLL)
        PartBossExtrude4.translate(clampingholderTranslation)


        #chamfer
        clamping_holder1=App.ActiveDocument.addObject("Part::Feature", "clamping_holder1")
        clamping_holder1.Shape=PartBossExtrude4
        clamping_holder1.Shape=clamping_holder1.Shape.removeSplitter()

        chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder1")
        chmfr.Base = App.ActiveDocument.clamping_holder1
        myEdges = []
    
        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))
        
        chmfr.Edges = myEdges
        Gui.ActiveDocument.clamping_holder1.Visibility = False

        App.ActiveDocument.recompute()
        
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    else:
        print("no Lens")
    ###Clamping_Holder1_End#######################################################
    ###Clamping_Holder2##########################################################
    if LensBin==1:
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)


        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        clampingholderTranslation=(-20.5,0,78-DLL)
        PartBossExtrude4.translate(clampingholderTranslation)
        
    
        #chamfer
        clamping_holder2=App.ActiveDocument.addObject("Part::Feature", "clamping_holder2")
        clamping_holder2.Shape=PartBossExtrude4
        clamping_holder2.Shape=clamping_holder2.Shape.removeSplitter()
        
        chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder2")
        chmfr.Base = App.ActiveDocument.clamping_holder2
        myEdges = []

        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))
        
        chmfr.Edges = myEdges
        Gui.ActiveDocument.clamping_holder2.Visibility = False

        App.ActiveDocument.recompute()
    
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    
    else:
        print("no Lens")
    ###Clamping_Holder2_End#######################################################
    ###Clamping_Holder3##########################################################
    if LensBin==1:
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)
    

        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        clampingholderTranslation=(0,20.5,78-DLL)
        PartBossExtrude4.translate(clampingholderTranslation)
        

        #chamfer
        clamping_holder3=App.ActiveDocument.addObject("Part::Feature", "clamping_holder3")
        clamping_holder3.Shape=PartBossExtrude4
        clamping_holder3.Shape=clamping_holder3.Shape.removeSplitter()

        chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder3")
        chmfr.Base = App.ActiveDocument.clamping_holder3
        myEdges = []

        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))
        
        chmfr.Edges = myEdges
        Gui.ActiveDocument.clamping_holder3.Visibility = False

        App.ActiveDocument.recompute()
    
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    else:
        print("no Lens")
    ###Clamping_Holder3_End#######################################################
    ###Clamping_Holder4##########################################################
    if LensBin==1:
        #Cylinder
        BossExtrude1=Part.makeCylinder(8/2,5)
        CutExtrude1=Part.makeCylinder(4/2,5)
        PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
        #Part.show(PartBossExtrude1)
    
    
        #Cutouts
        CutExtrude2=Part.makeBox(3,1,1)
        CutExtrude3=Part.makeBox(1,0.5,5)
        CutExtrude4=Part.makeBox(3.4,3,5)
        TranslationCutExtrude2=(1,-0.5,4)
        TranslationCutExtrude3=(1.5,-0.25,0)
        TranslationCutExtrude4=(-4,-1.7,0)
        CutExtrude2.translate(TranslationCutExtrude2)
        CutExtrude3.translate(TranslationCutExtrude3)
        CutExtrude4.translate(TranslationCutExtrude4)
        #Part.show(CutExtrude2)
        #Part.show(CutExtrude3)
        PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
        PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
        PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
        #Part.show(PartBossExtrude3)
        clampingholderTranslation=(0,-20.5,78-DLL)
        PartBossExtrude4.translate(clampingholderTranslation)
    
    
        #chamfer
        clamping_holder4=App.ActiveDocument.addObject("Part::Feature", "clamping_holder4")
        clamping_holder4.Shape=PartBossExtrude4
        clamping_holder4.Shape=clamping_holder4.Shape.removeSplitter()
        
        chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder4")
        chmfr.Base = App.ActiveDocument.clamping_holder4
        myEdges = []
        
        myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
        myEdges.append((18, 0.5, 0.5))
        myEdges.append((19, 0.5, 0.5))
        myEdges.append((26, 0.5, 0.5))
        myEdges.append((30, 0.5, 0.5))
        myEdges.append((37, 0.5, 0.5))

        chmfr.Edges = myEdges
        Gui.ActiveDocument.clamping_holder4.Visibility = False

        App.ActiveDocument.recompute()
            
        chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    else:
        print("no Lens")
    ###Clamping_Holder4_End#######################################################
    ###Clamping_Holder5##########################################################
    #Cylinder
    BossExtrude1=Part.makeCylinder(8/2,5)
    CutExtrude1=Part.makeCylinder(4/2,5)
    PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
    #Part.show(PartBossExtrude1)
    
    
    #Cutouts
    CutExtrude2=Part.makeBox(3,1,1)
    CutExtrude3=Part.makeBox(1,0.5,5)
    CutExtrude4=Part.makeBox(3.4,3,5)
    TranslationCutExtrude2=(1,-0.5,4)
    TranslationCutExtrude3=(1.5,-0.25,0)
    TranslationCutExtrude4=(-4,-1.7,0)
    CutExtrude2.translate(TranslationCutExtrude2)
    CutExtrude3.translate(TranslationCutExtrude3)
    CutExtrude4.translate(TranslationCutExtrude4)
    #Part.show(CutExtrude2)
    #Part.show(CutExtrude3)
    PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
    PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
    PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
    #Part.show(PartBossExtrude3)
    clampingholderTranslation=(20.5,0,RodLength-19.5)
    PartBossExtrude4.translate(clampingholderTranslation)


    #chamfer
    clamping_holder5=App.ActiveDocument.addObject("Part::Feature", "clamping_holder5")
    clamping_holder5.Shape=PartBossExtrude4
    clamping_holder5.Shape=clamping_holder5.Shape.removeSplitter()
    
    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder5")
    chmfr.Base = App.ActiveDocument.clamping_holder5
    myEdges = []

    myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((18, 0.5, 0.5))
    myEdges.append((19, 0.5, 0.5))
    myEdges.append((26, 0.5, 0.5))
    myEdges.append((30, 0.5, 0.5))
    myEdges.append((37, 0.5, 0.5))

    chmfr.Edges = myEdges
    Gui.ActiveDocument.clamping_holder5.Visibility = False

    App.ActiveDocument.recompute()
    
    chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    ###Clamping_Holder5_End#######################################################
    ###Clamping_Holder6##########################################################
    #Cylinder
    BossExtrude1=Part.makeCylinder(8/2,5)
    CutExtrude1=Part.makeCylinder(4/2,5)
    PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
    #Part.show(PartBossExtrude1)


    #Cutouts
    CutExtrude2=Part.makeBox(3,1,1)
    CutExtrude3=Part.makeBox(1,0.5,5)
    CutExtrude4=Part.makeBox(3.4,3,5)
    TranslationCutExtrude2=(1,-0.5,4)
    TranslationCutExtrude3=(1.5,-0.25,0)
    TranslationCutExtrude4=(-4,-1.7,0)
    CutExtrude2.translate(TranslationCutExtrude2)
    CutExtrude3.translate(TranslationCutExtrude3)
    CutExtrude4.translate(TranslationCutExtrude4)
    #Part.show(CutExtrude2)
    #Part.show(CutExtrude3)
    PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
    PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
    PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
    #Part.show(PartBossExtrude3)
    clampingholderTranslation=(-20.5,0,RodLength-19.5)
    PartBossExtrude4.translate(clampingholderTranslation)
    

    #chamfer
    clamping_holder6=App.ActiveDocument.addObject("Part::Feature", "clamping_holder6")
    clamping_holder6.Shape=PartBossExtrude4
    clamping_holder6.Shape=clamping_holder6.Shape.removeSplitter()
    
    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder6")
    chmfr.Base = App.ActiveDocument.clamping_holder6
    myEdges = []
    
    myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((18, 0.5, 0.5))
    myEdges.append((19, 0.5, 0.5))
    myEdges.append((26, 0.5, 0.5))
    myEdges.append((30, 0.5, 0.5))
    myEdges.append((37, 0.5, 0.5))
    
    chmfr.Edges = myEdges
    Gui.ActiveDocument.clamping_holder6.Visibility = False
    
    App.ActiveDocument.recompute()
            
    chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    ###Clamping_Holder6_End#######################################################
    ###Clamping_Holder7##########################################################
    #Cylinder
    BossExtrude1=Part.makeCylinder(8/2,5)
    CutExtrude1=Part.makeCylinder(4/2,5)
    PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
    #Part.show(PartBossExtrude1)
    

    #Cutouts
    CutExtrude2=Part.makeBox(3,1,1)
    CutExtrude3=Part.makeBox(1,0.5,5)
    CutExtrude4=Part.makeBox(3.4,3,5)
    TranslationCutExtrude2=(1,-0.5,4)
    TranslationCutExtrude3=(1.5,-0.25,0)
    TranslationCutExtrude4=(-4,-1.7,0)
    CutExtrude2.translate(TranslationCutExtrude2)
    CutExtrude3.translate(TranslationCutExtrude3)
    CutExtrude4.translate(TranslationCutExtrude4)
    #Part.show(CutExtrude2)
    #Part.show(CutExtrude3)
    PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
    PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
    PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
    #Part.show(PartBossExtrude3)
    clampingholderTranslation=(0,20.5,RodLength-19.5)
    PartBossExtrude4.translate(clampingholderTranslation)


    #chamfer
    clamping_holder7=App.ActiveDocument.addObject("Part::Feature", "clamping_holder7")
    clamping_holder7.Shape=PartBossExtrude4
    clamping_holder7.Shape=clamping_holder7.Shape.removeSplitter()

    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder7")
    chmfr.Base = App.ActiveDocument.clamping_holder7
    myEdges = []

    myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((18, 0.5, 0.5))
    myEdges.append((19, 0.5, 0.5))
    myEdges.append((26, 0.5, 0.5))
    myEdges.append((30, 0.5, 0.5))
    myEdges.append((37, 0.5, 0.5))
    
    chmfr.Edges = myEdges
    Gui.ActiveDocument.clamping_holder7.Visibility = False
    
    App.ActiveDocument.recompute()
            
    chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    ###Clamping_Holder7_End#######################################################
    ###Clamping_Holder8##########################################################
    #Cylinder
    BossExtrude1=Part.makeCylinder(8/2,5)
    CutExtrude1=Part.makeCylinder(4/2,5)
    PartBossExtrude1=BossExtrude1.cut(CutExtrude1)
    #Part.show(PartBossExtrude1)
    

    #Cutouts
    CutExtrude2=Part.makeBox(3,1,1)
    CutExtrude3=Part.makeBox(1,0.5,5)
    CutExtrude4=Part.makeBox(3.4,3,5)
    TranslationCutExtrude2=(1,-0.5,4)
    TranslationCutExtrude3=(1.5,-0.25,0)
    TranslationCutExtrude4=(-4,-1.7,0)
    CutExtrude2.translate(TranslationCutExtrude2)
    CutExtrude3.translate(TranslationCutExtrude3)
    CutExtrude4.translate(TranslationCutExtrude4)
    #Part.show(CutExtrude2)
    #Part.show(CutExtrude3)
    PartBossExtrude2=PartBossExtrude1.cut(CutExtrude2)
    PartBossExtrude3=PartBossExtrude2.cut(CutExtrude3)
    PartBossExtrude4=PartBossExtrude3.cut(CutExtrude4)
    #Part.show(PartBossExtrude3)
    #clampingholderTranslation=(0,-20.5,180.5)
    clampingholderTranslation=(0,-20.5,RodLength-19.5)
    PartBossExtrude4.translate(clampingholderTranslation)


    #chamfer
    clamping_holder8=App.ActiveDocument.addObject("Part::Feature", "clamping_holder8")
    clamping_holder8.Shape=PartBossExtrude4
    clamping_holder8.Shape=clamping_holder8.Shape.removeSplitter()

    chmfr = App.ActiveDocument.addObject("Part::Chamfer", "clamping_Holder8")
    chmfr.Base = App.ActiveDocument.clamping_holder8
    myEdges = []

    myEdges.append((15, 0.5, 0.5))# (edge number, chamfer start length, chamfer end length)
    myEdges.append((18, 0.5, 0.5))
    myEdges.append((19, 0.5, 0.5))
    myEdges.append((26, 0.5, 0.5))
    myEdges.append((30, 0.5, 0.5))
    myEdges.append((37, 0.5, 0.5))
    
    chmfr.Edges = myEdges
    Gui.ActiveDocument.clamping_holder8.Visibility = False

    App.ActiveDocument.recompute()
            
    chmfr.ViewObject.ShapeColor = (1.0,0.0,0.0)
    ###Clamping_Holder8_End#######################################################
    ###Shroud-Mount############################################################
    ##Base
    #make sketch
    x1=-30
    y1=-23
    x2=-23
    y2=-30
    x3=23
    y3=-30
    x4=30
    y4=-23
    x5=30
    y5=23
    x6=23
    y6=30
    x7=-23
    y7=30
    x8=-30
    y8=23
    x9=-30
    y9=-23
    

    #Extrude
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0)])
    L=Part.Face(lshape_wire)
    BasePart=  L.extrude(Base.Vector(0, 0, RodLength-7.5))
    #BasePart=  L.extrude(Base.Vector(0, 0, 192.5))
    #Part.show(BasePart)
    
    ##Cutouts
    #make sketch
    x1=-25.5
    y1=-10.56
    x2=-25.5
    y2=-23.96
    x3=-23.96
    y3=-25.5
    x4=-10.56
    y4=-25.5
    x5=-25.5
    y5=-10.56

    #Extrude
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0)])
    L=Part.Face(lshape_wire)
    #CutPart=  L.extrude(Base.Vector(0, 0, 192.5))
    CutPart=  L.extrude(Base.Vector(0, 0, RodLength-7.5))
    BossExtrude1=BasePart.cut(CutPart)
    
    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    BossExtrude2=BossExtrude1.cut(CutPart)
    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    BossExtrude3=BossExtrude2.cut(CutPart)
    CutPart.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
    BossExtrude4=BossExtrude3.cut(CutPart)
    #Part.show(BossExtrude4)

    #make sketch
    x1=-7.03
    y1=-25.5
    x2=7.03
    y2=-25.5
    x3=25.5
    y3=-7.03
    x4=25.5
    y4=7.03
    x5=7.03
    y5=25.5
    x6=-7.03
    y6=25.5
    x7=-25.5
    y7=7.03
    x8=-25.5
    y8=-7.03
    x9=-7.03
    y9=-25.5
    

    #Extrude
    lshape_wire = Part.makePolygon([Base.Vector(x1, y1, 0), Base.Vector(x2, y2, 0), Base.Vector(x3, y3, 0), Base.Vector(x4, y4, 0), Base.Vector(x5, y5, 0), Base.Vector(x6, y6, 0), Base.Vector(x7, y7, 0), Base.Vector(x8, y8, 0), Base.Vector(x9, y9, 0)])
    L=Part.Face(lshape_wire)
    #CutPart2=  L.extrude(Base.Vector(0, 0, 192.5))
    CutPart2=  L.extrude(Base.Vector(0, 0, RodLength-7.5))

    Shroud=BossExtrude4.cut(CutPart2)
    #Part.show(BossExtrude5)
    
    ######################################################################################################################################################

    #BasePart
    BasePart=Part.makeBox(90,45,15)
    #Part.show(BasePart)
    
    ##Drillings
    #BigDrillings
    BigDrilling=Part.makeCylinder(9/2,15)
    TranslationBigDrilling=(15,22.5,0)
    BigDrilling.translate(TranslationBigDrilling)
    BossExtrude1=BasePart.cut(BigDrilling)
    #Part.show(BigDrilling)
    TranslationBigDrilling=(30,0,0)
    BigDrilling.translate(TranslationBigDrilling)
    BossExtrude2=BossExtrude1.cut(BigDrilling)
    #Part.show(BigDrilling)
    TranslationBigDrilling=(30,0,0)
    BigDrilling.translate(TranslationBigDrilling)
    BossExtrude3=BossExtrude2.cut(BigDrilling)
    #Part.show(BigDrilling)

    #middleDrillings
    middleDrilling=Part.makeCylinder(5/2,15)
    TranslationmiddleDrilling=(29,22.5,0)
    middleDrilling.translate(TranslationmiddleDrilling)
    BossExtrude4=BossExtrude3.cut(middleDrilling)
    #Part.show(middleDrilling)
    TranslationmiddleDrilling=(8,8,0)
    middleDrilling.translate(TranslationmiddleDrilling)
    BossExtrude5=BossExtrude4.cut(middleDrilling)
    #Part.show(middleDrilling)
    TranslationmiddleDrilling=(16,0,0)
    middleDrilling.translate(TranslationmiddleDrilling)
    BossExtrude6=BossExtrude5.cut(middleDrilling)
    #Part.show(middleDrilling)
    TranslationmiddleDrilling=(8,-8,0)
    middleDrilling.translate(TranslationmiddleDrilling)
    BossExtrude7=BossExtrude6.cut(middleDrilling)
    #Part.show(middleDrilling)
    TranslationmiddleDrilling=(-8,-8,0)
    middleDrilling.translate(TranslationmiddleDrilling)
    BossExtrude8=BossExtrude7.cut(middleDrilling)
    #Part.show(middleDrilling)
    TranslationmiddleDrilling=(-16,0,0)
    middleDrilling.translate(TranslationmiddleDrilling)
    BossExtrude9=BossExtrude8.cut(middleDrilling)
    #Part.show(middleDrilling)

    #recessmiddleDrillings
    recess=Part.makeCylinder(6.4/2,0.8)
    Translationrecess=(29,22.5,15-0.8)
    recess.translate(Translationrecess)
    BossExtrude10=BossExtrude9.cut(recess)
    #Part.show(recess)
    Translationrecess=(8,8,0)
    recess.translate(Translationrecess)
    BossExtrude11=BossExtrude10.cut(recess)
    #Part.show(recess)
    Translationrecess=(16,0,0)
    recess.translate(Translationrecess)
    BossExtrude12=BossExtrude11.cut(recess)
    #Part.show(recess)
    Translationrecess=(8,-8,0)
    recess.translate(Translationrecess)
    BossExtrude13=BossExtrude12.cut(recess)
    #Part.show(recess)
    Translationrecess=(-8,-8,0)
    recess.translate(Translationrecess)
    BossExtrude14=BossExtrude13.cut(recess)
    #Part.show(recess)
    Translationrecess=(-16,0,0)
    recess.translate(Translationrecess)
    BossExtrude15=BossExtrude14.cut(recess)
    #Part.show(recess)

    #smallDrillings
    smallDrilling=Part.makeCylinder(4.2/2,15)
    TranslationsmallDrilling=(2,15,0)
    smallDrilling.translate(TranslationsmallDrilling)
    insert=Part.makeBox(1,3.2,15)
    Translationinsert=(0,15-3.2/2,0)
    insert.translate(Translationinsert)
    BossExtrude16=BossExtrude15.cut(smallDrilling)
    BossExtrude17=BossExtrude16.cut(insert)
    #Part.show(smallDrilling)
    #Part.show(insert)

    TranslationsmallDrilling=(0,15,0)
    smallDrilling.translate(TranslationsmallDrilling)
    Translationinsert=(0,15,0)
    insert.translate(Translationinsert)
    BossExtrude18=BossExtrude17.cut(smallDrilling)
    BossExtrude19=BossExtrude18.cut(insert)
    #Part.show(smallDrilling)
    #Part.show(insert)
    
    TranslationsmallDrilling=(86,0,0)
    smallDrilling.translate(TranslationsmallDrilling)
    Translationinsert=(89,0,0)
    insert.translate(Translationinsert)
    BossExtrude20=BossExtrude19.cut(smallDrilling)
    BossExtrude21=BossExtrude20.cut(insert)
    #Part.show(smallDrilling)
    #Part.show(insert)

    TranslationsmallDrilling=(0,-15,0)
    smallDrilling.translate(TranslationsmallDrilling)
    Translationinsert=(0,-15,0)
    insert.translate(Translationinsert)
    BossExtrude22=BossExtrude21.cut(smallDrilling)
    BossExtrude23=BossExtrude22.cut(insert)
    #Part.show(smallDrilling)
    #Part.show(insert)

    
    #Stab
    stabholder=Part.makeBox(5.5,8.5,4.1)
    Translationstabholder=(15,3.25,15-4.1)
    stabholder.translate(Translationstabholder)
    BossExtrude24=BossExtrude23.cut(stabholder)
    #Part.show(stabholder)
    Translationstabholder=(0,30,0)
    stabholder.translate(Translationstabholder)
    BossExtrude25=BossExtrude24.cut(stabholder)
    #Part.show(stabholder)
    Translationstabholder=(54.5,0,0)
    stabholder.translate(Translationstabholder)
    BossExtrude26=BossExtrude25.cut(stabholder)
    #Part.show(stabholder)
    Translationstabholder=(0,-30,0)
    stabholder.translate(Translationstabholder)
    BossExtrude27=BossExtrude26.cut(stabholder)
    #Part.show(stabholder)
    
    stabdrilling=Part.makeCylinder(4.2/2,90)
    stabdrilling.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
    Translationstabdrilling=(0,7.5,13)
    stabdrilling.translate(Translationstabdrilling)
    BossExtrude28=BossExtrude27.cut(stabdrilling)
    #Part.show(stabdrilling)

    Translationstabdrilling=(0,30,0)
    stabdrilling.translate(Translationstabdrilling)
    BossExtrude29=BossExtrude28.cut(stabdrilling)
    #Part.show(stabdrilling)
    
    stabrecess=Part.makeBox(90,3.2,1)
    Translationstabrecess=(0,7.5-3.2/2,15-1)
    stabrecess.translate(Translationstabrecess)
    BossExtrude30=BossExtrude29.cut(stabrecess)
    Translationstabrecess=(0,30,0)
    stabrecess.translate(Translationstabrecess)
    BossExtrude31=BossExtrude30.cut(stabrecess)

    #Fillets
    Cut1=Part.makeBox(4,4,15)
    Cut2=Part.makeCylinder(4,15)
    Cut3=Cut1.cut(Cut2)
    filletTranslation=(90-4,45-4,0)
    Cut3.translate(filletTranslation)
    BossExtrude32=BossExtrude31.cut(Cut3)
    #Part.show(Cut3)

    Cut3.rotate(Base.Vector(90-4, 45-4, 0),Base.Vector(0, 0, 1), -90)
    filletTranslation=(0,-45+8,0)
    Cut3.translate(filletTranslation)
    #Part.show(Cut3)
    BossExtrude33=BossExtrude32.cut(Cut3)

    Cut3.rotate(Base.Vector(90-4, 0, 0),Base.Vector(0, 0, 1), -90)
    filletTranslation=(-90+4,4,0)
    Cut3.translate(filletTranslation)
    #Part.show(Cut3)
    BossExtrude34=BossExtrude33.cut(Cut3)
    
    Cut3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -90)
    filletTranslation=(0,45,0)
    Cut3.translate(filletTranslation)
    #Part.show(Cut3)
    BossExtrude35=BossExtrude34.cut(Cut3)
    

    
    
    BossExtrude35.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
    #MountTranslation=(30,-22.5,90+42.5)
    MountTranslation=(30,-22.5,90+42.5+(-200+RodLength)/2)
    BossExtrude35.translate(MountTranslation)
    #Part.show(BossExtrude35)
    fuse1=Shroud.fuse(BossExtrude35)

    if Mount == 0:
        BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 1, 0), 180)
        #MountTranslation=(0,0,42.5*2+90)
        #MountTranslation=(0,0,42.5*2+90+(-200+RodLength)/2)
        MountTranslation=(0,0,0)
        BossExtrude35.translate(MountTranslation)
        #Part.show(BossExtrude31)
        fuse2=fuse1.fuse(BossExtrude35)

    elif Mount == 1:
        fuse2=fuse1

    elif Mount == 2:
        BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
        fuse2=fuse1.fuse(BossExtrude35)
    elif Mount == 3:
        BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
        fuse3=fuse1.fuse(BossExtrude35)         
        BossExtrude36=BossExtrude35   
        BossExtrude36.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
        fuse2=fuse3.fuse(BossExtrude36)  
    elif Mount == 4:
        BossExtrude35.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
        fuse3=fuse1.fuse(BossExtrude35)         
        BossExtrude36=BossExtrude35   
        BossExtrude36.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
        fuse4=fuse3.fuse(BossExtrude36)  
        BossExtrude37=BossExtrude36
        BossExtrude37.rotate(Base.Vector(0, 0, 90+42.5+(-200+RodLength)/2-90/2),Base.Vector(0, 0, 1), 90)
        fuse2=fuse4.fuse(BossExtrude37)  




    
    Translationshroud=(0,0,-15)
    fuse2.translate(Translationshroud)
    
    #Part.show(fuse2)
      
    
    #Fillets
    mount=App.ActiveDocument.addObject("Part::Feature", "Mount_Shroud")
    mount.Shape=fuse2
    mount.ViewObject.ShapeColor = (0.69,0.72,0.72)
    mount.ViewObject.Transparency=90
    ###Shroud_Mount_End########################################################
    #Show parts in a nice View
    App.activeDocument().recompute()
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")

########################################################################

