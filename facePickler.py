import pickle

faceList = ['A.jpg']


facePK = 'facePK.pk'

# with open(facePK, 'wb') as f:
#     pickle.dump(faceList, f)

with open(facePK, 'rb') as f:
    regFaces = pickle.load(f)

print(regFaces)