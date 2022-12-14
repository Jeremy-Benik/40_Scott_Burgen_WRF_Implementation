import os
import math
import sys
import bindpython as rothermel

fire = rothermel.Roth_py()

def AngleDistance( a,  b):
    diff = (b - a + 180) % 360 - 180;
    if diff<-180:diff+360
    return diff

def rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood, spreadDir ):

    '''
    Returns the ros, Ib and flength in the desired spread direction
    '''
    
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
    
    return {"ros": ros, "Ib":Ib, "flength": flength}
                     
def main():
    spreadDir=0
    wind=18  #midflame km/h
    windAspect=0  #towards where the wind is blowing to 
    slope=10 #(180.0/ math.pi)* math.atan( 35/100.0)  #degrees
    slopeAspect=0  #towards uphill
    m1h=0.05
    m10h=0.05
    m100h=0.05
    herb=0.05
    wood=0.05
    
    for fuel in range(1,14):
        res = rothermel_test(fuel, wind, windAspect, slope,  slopeAspect,  m1h,  m10h, m100h, herb, wood , 0)
        ros = res["ros"] #km/h
        ib = res["Ib"] 
        flength = res['flength'] #meters
        ros /= 3.6 #to m/s
        print(f'{spreadDir} {ros} m/s {ib} {flength} m')
    
if __name__ == "__main__":
    main()
