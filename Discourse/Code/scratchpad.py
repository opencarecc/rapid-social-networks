import gender_guesser.detector as gender

def simplify(complex_string):
    '''
    (str) => str
    makes complex_string easy to split. This is to separate the first name
    from the last name.
    '''
    ns = complex_string.replace('.', ' ')
    nns = ns.replace('_', ' ')
    nnns = nns.replace('-', ' ')
    firstName = nnns.split(' ')[0]
    return firstName
    
    

d = gender.Detector()
a = d.get_gender('philippe_drouillon')
print (a)
