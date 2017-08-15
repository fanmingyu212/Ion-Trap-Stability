from Ions.PointCharge import PointCharge

class Sr88Ion(PointCharge):
    def __init__(self):
        q = 1.60217662e-19
        m = 1.4549642e-25
        super(Sr88Ion, self).__init__(q, m)
