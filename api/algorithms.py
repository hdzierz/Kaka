# -*- coding: utf-8 -*-


class traverse:
    last = None

    def __call__(self, lst, op):
        for item in lst:
            item = op(item, self.last)
            self.last = item
        return lst


class count:
    ct = 0

    def __call__(self, lst, comp, op=None):
        for item in lst:
            if(op):
                if(op(item, comp)):
                    self.ct += 1
            else:
                if(item == comp):
                    self.ct += 1
        return self.ct


def find(lst, comp, op=None):
    for item in lst:
        if(op):
            if(op(item, comp)):
                return item
        else:
            if(item == comp):
                return item
    return None


def for_each(lst, op):
    for item in lst:
        item = op(item)
    return lst


def accumulate(lst, op, tgt):
    for item in lst:
        tgt = op(item, tgt)
    return tgt


def propagate(lst, op, tgt1, tgt2):
    for item in lst:
        tgt1, tgt2 = op(item, tgt1, tgt2)
    return tgt1, tgt2

