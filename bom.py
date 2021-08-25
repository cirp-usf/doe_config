import csv

from .laser import load_modules

class Component:
    def __init__(self, name, quantity, art_nr='', manufacturer='', is_am=False, am_file=''):
        self.name = name
        self.quantity = int(quantity)
        self.art_nr = str(art_nr)
        self.manufacturer = manufacturer
        self. is_am = int(is_am)
        self.am_file = am_file

Axle_art_nr = {125: 31036, 150: 31030, 170: 35696, 200: 35697, 235: 159590}

FP_Clip = Component('Clip 5',0, art_nr=37679, manufacturer='fischertechnik')





def make_BOM(csv_file, bom_file):
    with open(csv_file, newline='') as f:
        csvreader = csv.reader(f.readlines(), delimiter=';')
    next(csvreader) # ignore first line
    row = next(csvreader)
    RodLength=int(row[5])
    LensBin = int(row[6])
    LaserModule = int(row[10])
    if LaserModule < 0:
        lmodule = Component('Custom laser module', 1)
    else:
        lmodule = Component(load_modules()[LaserModule][0], 1)
    doe_holder1 = Component('DOE holder 1', 1,  is_am=True, am_file='DOE_Holder1')
    doe_holder2 = Component('DOE holder 2', 1, is_am=True, am_file='DOE_Holder3')
    laser_holder = Component('Laser holder', 2, is_am=True, am_file='LaserHolder1')
    laser_holder = Component('Laser holder', 2, is_am=True, am_file='LaserHolder1')
    mount = Component('Mount', 1, is_am=True, am_file='Mount_Shroud')
    cap = Component('Cap', 1, is_am=True, am_file='cap')
    lens_holder = Component('Lens holder', 1, is_am=True, am_file='LensHolder')
    
    bom = [mount, doe_holder1, doe_holder2, laser_holder, cap]
    if LensBin:
        bom.append(lens_holder)
        clip_nr = 8
    else:
        clip_nr = 4
    rod = Component('Metal axle {}mm'.format(RodLength), 4, art_nr=Axle_art_nr[RodLength], manufacturer='fischertechnik')
    bom.append(rod)
    FP_Clip.quantity = clip_nr
    bom.append(FP_Clip)
    bom.append(lmodule)
    with open(bom_file, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=';')
        for comp in bom:
            csv_writer.writerow([comp.name, comp.quantity, comp.art_nr, comp.manufacturer, comp.is_am, comp.am_file])
