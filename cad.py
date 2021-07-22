# -*- coding: utf-8 -*-
import Part
import FreeCAD as App
from FreeCAD import Base
import FreeCADGui as Gui
import Mesh
import ImportGui
import math
from math import pi
import csv
import shutil
import os.path



from . import __path__, doc_name
source_path = os.path.join(__path__[0], 'step')
source_path = os.path.normpath(source_path)

doe_halter_filename = 'DOE-Halter_01_D25___V05'
deckel_filename = 'Deckel___V03'
mount_filename = 'Mount'
clamping_Holder_filename = 'FT_Klemmbuchse5_37679_dummie___V02'


RotCenter0 = Base.Vector(0, 0, 0)
RotAxisZ = Base.Vector(0, 0, 1)

#Function to clear Window
def clearAll():
    doc = App.ActiveDocument
    for obj in doc.Objects:
        doc.removeObject(obj.Label)

def create_doc():
    # Only create new document if one does not yet exist
    if doc_name not in App.listDocuments():
        App.newDocument(doc_name)

    App.setActiveDocument(doc_name)
    App.ActiveDocument = App.getDocument(doc_name)
    Gui.ActiveDocument = Gui.getDocument(doc_name)

def close_document():
    if doc_name in App.listDocuments():
        App.closeDocument(doc_name)

def save_parts(format_, lens, dest):
    parts_list = ['DOE_Holder3', 'LaserHolder1', 'LaserHolder2', 'Mount_Shroud']
    if lens == 0:
        parts_list.append('LensHolder')

    if format_ == 0:
        print("Format STL")

        source = os.path.join(source_path, doe_halter_filename + '.STL')
        destination = "%s/DOE_Holder1_new.stl" % dest
        shutil.copy(source,destination)

        source = os.path.join(source_path, deckel_filename + '.STL')
        destination = "%s/cap_new.stl" % dest
        shutil.copy(source,destination)

        for p in parts_list:
            objs_to_save = [App.getDocument(doc_name).getObject(p)]
            save_name = '%s.%s' % (p, 'stl')
            save_path = os.path.join(dest , save_name)
            Mesh.export(objs_to_save, save_path)
            print(save_path)

    elif format_ == 1:
        print("Format STEP")

        source = os.path.join(source_path, doe_halter_filename + '.STEP')
        destination = "%s/DOE_Holder1_new.step" % dest
        shutil.copy(source,destination)

        source = os.path.join(source_path, deckel_filename + '.STEP')
        destination = "%s/cap_new.step" % dest
        shutil.copy(source,destination)

        for p in parts_list:
            objs_to_save = [App.getDocument(doc_name).getObject(p)]
            save_name = '%s.%s' % (p, 'step')
            save_path = os.path.join(dest, save_name)
            ImportGui.export(objs_to_save, save_path)
            print(save_path)

    elif format_ == 2:
        print(".FreeCAD")
        save="%s .FCStd" % dest
        #Gui.SendMsgToActiveView("SaveAs")
        App.getDocument(doc_name).saveAs(save)


def make_poly_points(xpoints, ypoints):
    n = len(xpoints)
    assert len(ypoints) == n, 'x and y lengths not equal'
    zpoints = [0.0] * n
    
    return list(map(Base.Vector, xpoints, ypoints, zpoints))


def make_holder(Diameter, Thickness):
    #Definition
    innerD = Diameter
    Diameter = max(14.0, Diameter)
    
    DSA = 6.1 * Diameter - 58.6
    DSI = DSA - 5
    MM = 3.5 * Diameter - 27.8
    
    chamfer1 = 1.0
    chamfer2 = 2.0
    fillet = 0.5

    #OuterRing
    BossExtrude1 = Part.makeCylinder(40 / 2, Thickness)
    CutExtrude1 = Part.makeCylinder(33 / 2, Thickness)
    PartBossExtrude1 = BossExtrude1.cut(CutExtrude1)

    #InnerRing
    BossExtrude2 = Part.makeCylinder((Diameter + 5.0) / 2,Thickness)
    CutExtrude2 = Part.makeCylinder(innerD / 2,Thickness)
    PartBossExtrude2 = BossExtrude2.cut(CutExtrude2)

    #CutsInnerRing
    sin20 = math.sin(math.radians(20.0))
    cut_length = Diameter / 2 + 7
    xpoints = [0, cut_length * sin20, -cut_length * sin20, 0]
    ypoints = [0, cut_length, cut_length, 0]
    
    lshape_wire = Part.makePolygon(make_poly_points(xpoints, ypoints))
    
    L = Part.Face(lshape_wire)
    K1 = L.extrude(Base.Vector(0, 0, Thickness))
    K2 = K1.copy()
    K3 = K1.copy()
    K4 = K1.copy()
    K1.rotate(RotCenter0, RotAxisZ, -45)
    K2.rotate(RotCenter0, RotAxisZ, 45)
    K3.rotate(RotCenter0, RotAxisZ, 225)
    K4.rotate(RotCenter0, RotAxisZ, 135)
    C1 = PartBossExtrude2.cut(K1)
    C2 = C1.cut(K2)
    C3 = C2.cut(K3)
    C4 = C3.cut(K4)


    #SpringElements
    BossExtrude3 = Part.makeCylinder(DSA/2,Thickness)
    CutExtrude3 = Part.makeCylinder(DSI/2,Thickness)
    PartBossExtrude3 = BossExtrude3.cut(CutExtrude3)
    TranslationPartBossExtrude3 = (MM,0,0)
    PartBossExtrude3.translate(TranslationPartBossExtrude3)
    CutExtrude4=Part.makeCylinder(36/2,Thickness)



	        
	
    #UnionParts
    fused1 = PartBossExtrude1.fuse(C4)
    

    SpringElement = PartBossExtrude3.common(CutExtrude4)
    fused1 = fused1.fuse(SpringElement)
    SpringElement.rotate(RotCenter0, RotAxisZ, 90)
    fused1 = fused1.fuse(SpringElement)
    SpringElement.rotate(RotCenter0, RotAxisZ, 180)
    fused1 = fused1.fuse(SpringElement)
    SpringElement.rotate(RotCenter0, RotAxisZ, 270)
    fused1 = fused1.fuse(SpringElement)


    #OuterRingSquares
    Square = Part.makeBox(5.13,15,Thickness)
    TranslationSquare = (17.37,-15/2,0)
    Square.translate(TranslationSquare)
    #Part.show(Square)
    
	
    #CutoutsOuterRingSquares1
    Hole = Part.makeCylinder(2.1,Thickness)
    TranslationHole = (20.5,0,0)
    Hole.translate(TranslationHole)
    PartCutout = Square.cut(Hole)
    fused1 = fused1.cut(Hole)

    Rectangle = Part.makeBox(0.69 + 0.5, 3.2, Thickness)
    TranslationRectangle = (21.81 - 0.25, -3.2 / 2, 0)
    Rectangle.translate(TranslationRectangle)
    PartCut = PartCutout.cut(Rectangle)
    fused1 = fused1.fuse(PartCut)
    
    #CutoutsOuterRingSquares2
    PartCut.rotate(RotCenter0, RotAxisZ, 90)
    Hole.rotate(RotCenter0, RotAxisZ, 90)
    fused1 = fused1.fuse(PartCut)
    fused1 = fused1.cut(Hole)

    #CutoutsOuterRingSquares3
    PartCut.rotate(RotCenter0, RotAxisZ, 180)
    Hole.rotate(RotCenter0, RotAxisZ, 180)
    fused1 = fused1.fuse(PartCut)
    fused1 = fused1.cut(Hole)

    #CutoutsOuterRingSquares4
    PartCut.rotate(RotCenter0, RotAxisZ, 270)
    Hole.rotate(RotCenter0, RotAxisZ, 270)
    fused1 = fused1.fuse(PartCut)
    fused1 = fused1.cut(Hole)

    #Outer Polygon
    xpoints = [22.7, 22.7, 18.0, 18.0, 22.7]
    ypoints = [-5.0, 5.0, 5.0, -5.0, -5.0]


    lshape_wire = Part.makePolygon(make_poly_points(xpoints, ypoints))
    L = Part.Face(lshape_wire)
    K1 = L.extrude(Base.Vector(0, 0, Thickness))
    K2 = K1.copy()
    K3 = K1.copy()
    K4 = K1.copy()
    K1.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -45)
    K2.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 45)
    K3.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 225)
    K4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 135)

    fused1 = fused1.fuse(K1)
    fused1 = fused1.fuse(K2)
    fused1 = fused1.fuse(K3)
    fused1 = fused1.fuse(K4)
   
    #TranslationLensHolder=(0,0,69	
    #TranslationLensHolder=(0,0,83-DLL)
    #fused17.translate(TranslationLensHolder)
    #Part.show(fused17)
    fused1 = fused1.removeSplitter()
    [17, 20, 118, 130, 141, 149, 164, 172]
    [183, 184, 196, 197, 208, 209, 220, 221]

    eds = [28, 29, 31, 32, 34, 35, 36, 37, 47, 48, 49, 50, 51, 61, 62, 63, 64, 65, 75, 76, 77, 78, 82, 88, 94, 100, 101, 122, 127, 146, 157, 169, 180, 194, 205, 217, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257]
    
    edc1 = [fused1.Edges[x] for x in eds]
    
    eds = [17, 20, 118, 130, 141, 149, 164, 172]
    
    edc2 = [fused1.Edges[x] for x in eds]
    
    eds = [183, 184, 196, 197, 208, 209, 220, 221]
    
    edf = [fused1.Edges[x] for x in eds]
    
    fused1 = fused1.makeChamfer(chamfer1, edc1)
    fused1 = fused1.makeChamfer(chamfer2, edc2)
    fused1 = fused1.makeFillet(fillet, edf)

    return fused1





def make_parts(csv_filename):						#Plot Part
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

    create_doc()
    
    clearAll()
    ###Part-Code###############################################################
    ###DOE-Holder1###############################################################
    
    
    #STEP-Import-DOE-Holder1
    fused26 = Part.Shape()
    source = os.path.join(source_path, doe_halter_filename + '.step')
    fused26.read(source)
    
    fused26.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 90)
    fused26.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), -90)
    fused26.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), -90)
    #AssemblyTranslation=(-30,0,0)
    #fused26.translate(AssemblyTranslation)
    
    
    #Display
    Holder = App.ActiveDocument.addObject("Part::Feature", "DOE_Holder1")
    Holder.Shape=fused26
    Holder.Shape=Holder.Shape.removeSplitter()
    Holder.ViewObject.ShapeColor = (0.0,0.0,192/255)
    
    
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
        '''
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
        '''
        LensHolder = make_holder(DL,Thickness)
        
        TranslationLensHolder=(0,0,83-DLL)
        LensHolder.translate(TranslationLensHolder)
        
        Holder1 = App.ActiveDocument.addObject("Part::Feature", "LensHolder")
        Holder1.Shape=LensHolder
        Holder1.Shape=Holder1.Shape.removeSplitter()
        Holder1.ViewObject.ShapeColor = (103/204,125/204,0.0)
        
        
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
    '''
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
    '''
    LaserHolder1 = make_holder(LHD,15)
        
    TranslationLaserHolder1=(0,0,RodLength-31-LL)
    LaserHolder1.translate(TranslationLaserHolder1)
        
    Holder1 = App.ActiveDocument.addObject("Part::Feature", "LaserHolder1")
    Holder1.Shape=LaserHolder1
    Holder1.Shape=Holder1.Shape.removeSplitter()
    Holder1.ViewObject.ShapeColor = (103/204,125/204,0.0)
   
    
    ###Laser-Holder1_End#########################################################
    
    ###Laser-Holder2############################################################
    '''
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
    '''
    LaserHolder2 = LaserHolder1.copy()
        
    TranslationLaserHolder2=(0,0,31+LL-37.5)
    #TranslationLaserHolder2=(0,0,-(RodLength-31-LL)+RodLength-37.5)
    LaserHolder2.translate(TranslationLaserHolder2)
        
    Holder2 = App.ActiveDocument.addObject("Part::Feature", "LaserHolder2")
    Holder2.Shape=LaserHolder2
    Holder2.Shape=Holder2.Shape.removeSplitter()
    Holder2.ViewObject.ShapeColor = (103/204,125/204,0.0)
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
       
    #STEP-Import-Cap
    fused5 = Part.Shape()
    source = os.path.join(source_path, deckel_filename + '.step')
    fused5.read(source)   
    
    fused5.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 1, 0), 180)
    fused5.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), -90)
    Translationcap=(0,0,RodLength-19.5)
    fused5.translate(Translationcap)
    
    #Display
    cap = App.ActiveDocument.addObject("Part::Feature", "cap")
    cap.Shape=fused5
    cap.Shape=cap.Shape.removeSplitter()
    cap.ViewObject.ShapeColor = (0.0,0.0,192/255)

    

    

    ###Cap_End################################################################
    ###Clamping_Holder1##########################################################
    if LensBin==1:
        
        #STEP-Import-Cap
        PartBossExtrude4 = Part.Shape()
        source = os.path.join(source_path, clamping_Holder_filename + '.step')
        PartBossExtrude4.read(source)   
    
        PartBossExtrude4.rotate(Base.Vector(0, 0, 0),Base.Vector(1, 0, 0), 90)
        PartBossExtrude4.rotate(Base.Vector(0, 0, 0),Base.Vector(0, 0, 1), 90)
        clampingholderTranslation=(20.5,0,78-DLL)
        PartBossExtrude4.translate(clampingholderTranslation)
        
    
        #Display
        clamping_holder1 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder1")
        clamping_holder1.Shape=PartBossExtrude4
        clamping_holder1.Shape=clamping_holder1.Shape.removeSplitter()
        clamping_holder1.ViewObject.ShapeColor = (1.0,0.0,0.0)
        
        
    else:
        print("no Lens")
    ###Clamping_Holder1_End#######################################################
    ###Clamping_Holder2##########################################################
    
    if LensBin==1:
        
        PartBossExtrude5 = PartBossExtrude4.copy()
        clampingholderTranslation=(-20.5*2,0,0)
        PartBossExtrude5.translate(clampingholderTranslation)
        
        #Display
        clamping_holder2 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder2")
        clamping_holder2.Shape=PartBossExtrude5
        clamping_holder2.Shape=clamping_holder2.Shape.removeSplitter()
        clamping_holder2.ViewObject.ShapeColor = (1.0,0.0,0.0)
    
    else:
        print("no Lens")
    ###Clamping_Holder2_End#######################################################
    ###Clamping_Holder3##########################################################
    if LensBin==1:
        
        PartBossExtrude6 = PartBossExtrude4.copy()
        clampingholderTranslation=(-20.5,20.5,0)
        PartBossExtrude6.translate(clampingholderTranslation)
        
        #Display
        clamping_holder3 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder3")
        clamping_holder3.Shape=PartBossExtrude6
        clamping_holder3.Shape=clamping_holder3.Shape.removeSplitter()
        clamping_holder3.ViewObject.ShapeColor = (1.0,0.0,0.0)
        
    else:
        print("no Lens")
    ###Clamping_Holder3_End#######################################################
    ###Clamping_Holder4##########################################################
    if LensBin==1:
        
        PartBossExtrude7 = PartBossExtrude4.copy()
        clampingholderTranslation=(-20.5,-20.5,0)
        PartBossExtrude7.translate(clampingholderTranslation)
        
        #Display
        clamping_holder4 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder4")
        clamping_holder4.Shape=PartBossExtrude7
        clamping_holder4.Shape=clamping_holder4.Shape.removeSplitter()
        clamping_holder4.ViewObject.ShapeColor = (1.0,0.0,0.0)
    else:
        print("no Lens")
    ###Clamping_Holder4_End#######################################################
    ###Clamping_Holder5##########################################################
    
    PartBossExtrude8 = PartBossExtrude4.copy()
    clampingholderTranslation=(0,0,-(78-DLL)+RodLength-19.5)
    PartBossExtrude8.translate(clampingholderTranslation)
        
    #Display
    clamping_holder5 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder5")
    clamping_holder5.Shape=PartBossExtrude8
    clamping_holder5.Shape=clamping_holder5.Shape.removeSplitter()
    clamping_holder5.ViewObject.ShapeColor = (1.0,0.0,0.0)
    ###Clamping_Holder5_End#######################################################
    ###Clamping_Holder6##########################################################
    
    PartBossExtrude9 = PartBossExtrude4.copy()
    clampingholderTranslation=(-2*20.5,0,-(78-DLL)+RodLength-19.5)
    PartBossExtrude9.translate(clampingholderTranslation)
        
    #Display
    clamping_holder6 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder6")
    clamping_holder6.Shape=PartBossExtrude9
    clamping_holder6.Shape=clamping_holder6.Shape.removeSplitter()
    clamping_holder6.ViewObject.ShapeColor = (1.0,0.0,0.0)
    ###Clamping_Holder6_End#######################################################
    ###Clamping_Holder7##########################################################
    
    PartBossExtrude10 = PartBossExtrude4.copy()
    clampingholderTranslation=(-20.5,20.5,-(78-DLL)+RodLength-19.5)
    PartBossExtrude10.translate(clampingholderTranslation)
        
    #Display
    clamping_holder7 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder7")
    clamping_holder7.Shape=PartBossExtrude10
    clamping_holder7.Shape=clamping_holder7.Shape.removeSplitter()
    clamping_holder7.ViewObject.ShapeColor = (1.0,0.0,0.0)
    ###Clamping_Holder7_End#######################################################
    ###Clamping_Holder8##########################################################
    
    PartBossExtrude11 = PartBossExtrude4.copy()
    clampingholderTranslation=(-20.5,-20.5,-(78-DLL)+RodLength-19.5)
    PartBossExtrude11.translate(clampingholderTranslation)
        
    #Display
    clamping_holder8 = App.ActiveDocument.addObject("Part::Feature", "clamping_holder8")
    clamping_holder8.Shape=PartBossExtrude11
    clamping_holder8.Shape=clamping_holder8.Shape.removeSplitter()
    clamping_holder8.ViewObject.ShapeColor = (1.0,0.0,0.0)
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
    
    
    #STEP-Import-Mount
    BossExtrude35 = Part.Shape()
    source = os.path.join(source_path, mount_filename + '.step')
    BossExtrude35.read(source)
    #BossExtrude35.read(u"C:/Users/Steffen/Desktop/Source/Mound.STEP")

    
    
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

