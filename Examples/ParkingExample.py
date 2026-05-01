from AIGamePyLibrary import *

player = InitializeParking(
    "AIA",                          # name
    "United States of America",     # country
    "White",                        # skin color
    0,                              # body style
    3,                              # hair style
    "Black",                        # hair color
    1,                              # facial hair style
    "Green",                        # car color
    ""                              # custom outfit URL
)

#Is the car near the parking stall?
selfTransform = ParkingGetTransform("Self")
selfPosition = RelativePosition(selfTransform, "Self")

stallTransform = ParkingGetTransform("Target Parking Stall")
stallPosition = RelativePosition(stallTransform, "Self")

distanceToStall = Distance(selfPosition, stallPosition)

isNearStall = CompareFloats(distanceToStall, 1.5, "<")

#Is the car aligned with the parking stall?
selfRight = RelativePosition(selfTransform, "Self + Right")
selfRightNormalized = Normalize(selfRight)

directionToStall = selfPosition - stallPosition
directionToStallNormalized = Normalize(directionToStall)

dotProductToStall = DotProduct(selfRightNormalized, directionToStallNormalized)
dotProductToStall = Abs(dotProductToStall)
isAligned = CompareFloats(dotProductToStall, 0.9, ">")


#Throttle: Forward collision check
forwardRayCheckLength = ConditionalSetFloat(isNearStall, 5, 6.5)

isAlignedAndNearStall = CompareBool(isAligned, isNearStall, "and")
forwardRayCheckLength = ConditionalSetFloat(isNearStall, 5, 6.5, "True")
sideRayCheckLength = 6


spherecast = Spherecast(1.25, 10)
carRaycasts = CarRaycasts(spherecast)

leftHitInfo = HitInfo(carRaycasts.RaycastHit1)
forwardHitInfo = HitInfo(carRaycasts.RaycastHit2)
rightHitInfo = HitInfo(carRaycasts.RaycastHit3)

checkLeftRaycast = CompareFloats(sideRayCheckLength, leftHitInfo.Distance, ">")
checkForwardRaycast = CompareFloats(forwardRayCheckLength, forwardHitInfo.Distance)
checkRightRaycast = CompareFloats(sideRayCheckLength, rightHitInfo.Distance, ">")

anyRaycastBlocked = CompareBool(checkLeftRaycast, checkForwardRaycast, "or")
anyRaycastBlocked = CompareBool(anyRaycastBlocked, checkRightRaycast, "or")    

targetThrottle = ConditionalSetFloat(anyRaycastBlocked, -1, 0.15, "True")

#throttle
throttle = ConditionalSetFloat(isNearStall, -0.15, targetThrottle)

#steering
initialSteering = Autosteer(stallPosition)

signedSpeed = ParkingGetFloat("Signed Speed (forward +, reverse −)")
signedSpeed = Operation(signedSpeed, "sign")

steering = initialSteering * signedSpeed

#braking
carWantsStop = CompareFloats(targetThrottle, 0, "<")
isMovingForward = CompareFloats(signedSpeed, 0, ">")

carWantsBrake = CompareBool(carWantsStop, isMovingForward, "and")
needsToBrake = CompareBool(carWantsBrake, isNearStall, "or")

brake = ConditionalSetFloat(needsToBrake, 1, 0, "True")

ModularUniformController(throttle, steering, brake)

SaveData("ParkingExample3.txt", "grid")
