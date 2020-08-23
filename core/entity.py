from pyrsistent import field

from base.data import PayloadData


class Entity(PayloadData):
    data = field()
