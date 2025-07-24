from pyfbsdk import *
from pyfbsdk_additions import * 

take = FBSystem().CurrentTake

print(take.Comments)
take.Comments = "lol"

print(take.Comments)
FBSystem().CurrentTake = take
FBSystem().Scene
