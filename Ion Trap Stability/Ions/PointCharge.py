class PointCharge(object):

    def __init__(self, q, m):
        self.q = q
        self.m = m

    @property
    def charge(self):
        return self.q

    @property
    def mass(self):
        return self.m
