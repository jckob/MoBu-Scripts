from pyfbsdk import *
import math

def distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0])**2 +
        (p1[1] - p2[1])**2 +
        (p1[2] - p2[2])**2
    )

bones_to_measure = [
    "Small1",
    "Big1",
]

# Zakładamy: Small1 -> child -> child
bone1 = FBFindModelByLabelName("Big1")
if bone1 is None or len(bone1.Children) == 0:
    print("Brak kości Small1 lub jej potomków.")
else:
    print(bone1.Children)
  