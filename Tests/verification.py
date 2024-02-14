from deepface import DeepFace
result  = DeepFace.verify("attemptingFace.jpg", "registeredFace.jpg", "OpenFace")
print("Is verified: ", result["verified"])