#include <iostream>
#include "WFA_Fuels.h"
#include "WFA_Rothermel.h"

int main()
{

	double windSpeed = 0; //km/h at midflame
	double windAspect = 0; //degrees, start North, increase clockwise
	double slopeAspect = 0; //degrees, start North, increase clockwise
	double slopeMod = 0; //degrees
	double m1h = 0.03; 
	double m10h = 0.00;
	double m100h = 0.00;
	double mwoody = 0.3;
	double mherb = 0.3;
	

	Fuels fuelList;
	//fuelList.GetBurgan();
	fuelList.GetClasic();

	int fuelName = 13;


	FuelFamilyItem myfuel = fuelList.list[fuelList.dic_ToPos[fuelName]];

	//We have the model divided into two independent steps. One for the moisture and the other one for the wind
	ReturnRothBase rob = RothBase(myfuel, m1h, m10h,m100h, mwoody, mherb);
	RothFinalVal result= RotherAddWindSlope(rob, windSpeed, windAspect, slopeMod, slopeAspect);

	std::cout << "Fuel" << myfuel.FuelNum << std::endl; 
	std::cout << "ROS(m/s): " << result.Rkmph * 0.27 << std::endl;
	std::cout << "IB(kW/m): " << result.I_B << std::endl;
	std::cout << "Flame length (m): " << result.Flength << std::endl;
	std::cout << "LW " << result.length_to_width << std::endl;
	std::cout << "Direction Maximum Spread " << result.pathDir << std::endl;
	// std::cout << "I_r" << result.I_R << std::endl;



}
