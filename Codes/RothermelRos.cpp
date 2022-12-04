#include <iostream>
#include "WFA_Fuels.h"
#include "WFA_Rothermel.h"

int main()
{

	double windSpeed = 10; //km/h at midflame
	double windAspect = 0; //degrees, start North, increase clockwise
	double slopeAspect = 90; //degrees, start North, increase clockwise
	double slopeMod = 30; //degrees
	double m1h = 0.08; 
	double m10h = 0.08;
	double m100h = 0.08;
	double mwoody = 0.9;
	double mherb = 0.6;
	

	Fuels fuelList;
	//fuelList.GetBurgan();
	fuelList.GetClasic();

	int fuelName = 4;


	FuelFamilyItem myfuel = fuelList.list[fuelList.dic_ToPos[fuelName]];

	//We have the model divided into two independent steps. One for the moisture and the other one for the wind
	ReturnRothBase rob = RothBase(myfuel, m1h, m10h,m100h, mwoody, mherb);
	RothFinalVal result= RotherAddWindSlope(rob, windSpeed, windAspect, slopeMod, slopeAspect);

	std::cout << "Fuel" << myfuel.FuelNum << std::endl; 
	std::cout << "ROS(km/h): " << result.Rkmph << std::endl;
	std::cout << "IB(kW/m): " << result.I_B << std::endl;
	std::cout << "Flame length (m): " << result.Flength << std::endl;
	std::cout << "LW " << result.length_to_width << std::endl;
	std::cout << "Direction Maximum Spread " << result.pathDir;



}
