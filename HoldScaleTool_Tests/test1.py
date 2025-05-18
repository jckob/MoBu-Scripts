#change model to wireframe
#cube.ShadingMode = FBModelShadingMode.kFBModelShadingAll
#cube.ShadingMode = FBModelShadingMode.kFBModelShadingWire
#cube.Show = True

from pyfbsdk import FBFindModelByLabelName, FBVector3d, FBMatrix, FBVectorMatrixMult, FBMatrixToRotation
import math


# -------------------
# Helper Functions
# -------------------
def to_vector(a, b):
    return [b[i] - a[i] for i in range(3)]

def normalize(vec):
    length = math.sqrt(sum(v*v for v in vec))
    return [v / length for v in vec] if length != 0 else [0, 0, 0]

def cross_product(v1, v2):
    return [
        v1[1]*v2[2] - v1[2]*v2[1],
        v1[2]*v2[0] - v1[0]*v2[2],
        v1[0]*v2[1] - v1[1]*v2[0]
    ]

def dot_product(v1, v2):
    return sum(v1[i]*v2[i] for i in range(3))

def vector_angle(v1, v2):
    dot = dot_product(normalize(v1), normalize(v2))
    dot = max(-1.0, min(1.0, dot))  # Clamp
    return math.acos(dot)

# -------------------
# Fetch Models
# -------------------
wrist1 = FBFindModelByLabelName("RightFingerBase")
prop1 = FBFindModelByLabelName("Mocap_Prop")

wrist2 = FBFindModelByLabelName("Aragor:RightHand")
prop2 = FBFindModelByLabelName("Test_Offset")

# -------------------
# Step 1: Vectors
# -------------------
v_ref = to_vector(prop1.Translation, wrist1.Translation)
v_test = to_vector(prop2.Translation, wrist2.Translation)

v_ref_n = normalize(v_ref)
v_test_n = normalize(v_test)

# -------------------
# Step 2: Compute Rotation Axis & Angle
# -------------------
angle = vector_angle(v_test_n, v_ref_n)  # radians
axis = normalize(cross_product(v_test_n, v_ref_n))

if angle < 1e-4 or math.isnan(angle):
    print("Vectors already aligned or angle too small.")
else:
    print("Rotating Offset by", math.degrees(angle), "degrees")

    # -------------------
    # Step 3: Apply Rotation (FBRotation matrix)
    # -------------------
    

    # Build rotation matrix from axis + angle
    def axis_angle_to_matrix(axis, angle):
        x, y, z = axis
        c = math.cos(angle)
        s = math.sin(angle)
        t = 1 - c
        rot = FBMatrix()
        rot[0] = t*x*x + c
        rot[1] = t*x*y - s*z
        rot[2] = t*x*z + s*y
        rot[3] = 0
        rot[4] = t*x*y + s*z
        rot[5] = t*y*y + c
        rot[6] = t*y*z - s*x
        rot[7] = 0
        rot[8] = t*x*z - s*y
        rot[9] = t*y*z + s*x
        rot[10] = t*z*z + c
        rot[11] = 0
        rot[12] = 0
        rot[13] = 0
        rot[14] = 0
        rot[15] = 1
        return rot

    rot_matrix = axis_angle_to_matrix(axis, angle)

    # Get original prop2 rotation as matrix
    original_matrix = FBMatrix()
    prop2.GetMatrix(original_matrix)

    # Multiply: rot_matrix * original_matrix
    final_matrix = FBMatrix()
    for row in range(4):
        for col in range(4):
            final_matrix[row*4 + col] = sum(
                rot_matrix[row*4 + k] * original_matrix[k*4 + col] for k in range(4)
            )

    # Apply new rotation
    
    new_rot = FBVector3d()
    FBMatrixToRotation(new_rot, final_matrix)
    prop2.Rotation = new_rot
