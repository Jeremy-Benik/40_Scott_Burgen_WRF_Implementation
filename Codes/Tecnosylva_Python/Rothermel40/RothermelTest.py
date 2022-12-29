import os
import math
import sys
import bindpython as rothermel

def AngleDistance( a,  b):
    diff = (b - a + 180) % 360 - 180;
    if diff<-180:diff+360
    return diff

def rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood, spreadDir ):

    '''
    Returns the ros, Ib and flength in the desired spread direction
    '''
    
    fire = rothermel.Roth_py()
    surface = fire.Rothermel(  fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood  )
   
    maxRos = surface["ROS"] #km/h
    maxIb = surface["I_B"] 
    maxFlength = surface['Flength'] #meters
    maxSpreadDir = surface['pathDir'] #degrees (N=0, increasing clockwise)
    LW = surface['length_to_width'] #elliptical shape

    angleDistace = abs( AngleDistance(maxSpreadDir,spreadDir ))
    epsi_elip = math.sqrt(1 - 1 / (LW*LW));
    elipseWeight = (1 - epsi_elip) / (1 - epsi_elip * math.cos(angleDistace * math.pi/180))    
    ros = maxRos * elipseWeight;
    Ib= maxIb * elipseWeight
    flength =(0.07752 * math.pow(Ib, 0.46));
    
    return {"ros": ros, "Ib":Ib , "flength": flength}                         
                        
def main():
    spreadDir=0
    wind=25  #midflame km/h
    windAspect=0  #towards where the wind is blowing to 
    slope=(180.0/ math.pi)* math.atan( 35/100.0)  #degrees
    slopeAspect=0  #towards uphill
    m1h=0.04
    m10h=0.04
    m100h=0.05
    herb=0.6
    wood=0.6

    print("40 S&B")
    for fuel in range(101,110):
        res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
        ros = res["ros"] #km/h
        ib = res["Ib"] 
        flength = res['flength'] #meters
        print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')
    for fuel in range(121,125):
        res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
        ros = res["ros"] #km/h
        ib = res["Ib"] 
        flength = res['flength'] #meters
        print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')
    for fuel in range(141,149):
        res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
        ros = res["ros"] #km/h
        ib = res["Ib"] 
        flength = res['flength'] #meters
        print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')
    for fuel in range(161,166):
        res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
        ros = res["ros"] #km/h
        ib = res["Ib"] 
        flength = res['flength'] #meters
        print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')
    for fuel in range(181,190):
        res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
        ros = res["ros"] #km/h
        ib = res["Ib"] 
        flength = res['flength'] #meters
        print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')
    for fuel in range(201,205):
        res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
        ros = res["ros"] #km/h
        ib = res["Ib"] 
        flength = res['flength'] #meters
        print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')

    print("Custom")
    fuel = 4
    res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
    ros = res["ros"] #km/h
    ib = res["Ib"] 
    flength = res['flength'] #meters
    print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')
    fuel = 10
    res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
    ros = res["ros"] #km/h
    ib = res["Ib"] 
    flength = res['flength'] #meters
    print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')
    fuel = 99
    res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , spreadDir)
    ros = res["ros"] #km/h
    ib = res["Ib"] 
    flength = res['flength'] #meters
    print(f'{fuel}: {spreadDir} {ros} km/h {ib} {flength} m')

if __name__ == "__main__":
    main()
