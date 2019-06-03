from pyasn1.type import univ, namedtype

class Person(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('height', univ.Integer()),
        namedtype.NamedType('width', univ.Integer()),
        namedtype.NamedType('name', univ.OctetString()),
        )
    
    
