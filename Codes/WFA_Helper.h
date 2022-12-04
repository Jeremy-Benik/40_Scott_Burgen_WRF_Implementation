#ifndef WFA_HELPER_H
#define WFA_HELPER_H

#include<iostream>
#include<fstream>
#include<math.h>
#include <ctime>
#include <vector>
#include <string>
#include <algorithm>   
#include <sstream>



inline static double div_(double a, double b) { return b == 0 ? 0 : a / b; }
inline static double power_(double a, double b) { return a == 0 ? 0 : pow(a, b); }


inline static int AngleDistance(int a, int b)
{
	double diff = (b - a + 180) % 360 - 180;
	return diff < -180 ? diff + 360 : diff;
}



std::vector<std::vector < std::string >> Read_CSV(std::string path)
{

	std::ifstream inFile(path, std::ios::in);
	std::string lineStr;
	std::vector<std::vector<std::string>> strArray;
	while (getline(inFile, lineStr))
	{
		std::stringstream ss(lineStr);
		std::string str;
		std::vector<std::string> lineArray;
		// separated by comma
		while (std::getline(ss, str, ','))
			lineArray.push_back(str);
		strArray.push_back(lineArray);
	}
	return strArray;
}



#endif

