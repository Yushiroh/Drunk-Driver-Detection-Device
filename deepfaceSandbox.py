from deepface import DeepFace

regFaces = ['A.jpg','B.jpg','C.jpg','D.jpg','E.jpg']

i = 0

#  result = DeepFace.find(img_path= 'A.jpg' , db_path= 'faceData')
# print(result)

for elements in regFaces:
    
    result = DeepFace.verify(regFaces[i], 'registeredFace.jpg')
    
    if result["verified"] == True:
        print("MATCHED")
        break
    else:
        print(result["verified"])
        i+=1

# print("no matching faces in the database")

# result = DeepFace.verify('A.jpg', 'A.jpg')

# print(result["verified"])