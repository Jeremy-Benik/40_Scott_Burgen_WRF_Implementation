#ifndef WFA_ROTHERMEL_H
#define WFA_ROTHERMEL_H

#include<math.h>
#include<cmath>
#include "WFA_Fuels.h"
#include "WFA_Helper.h"

const double PI = 3.1415926535;
const double RAD2DEG = 180.0 / PI;
const double DEG2RAD = PI / 180.0;


class ReturnRothBase
{
public:
	double xiDivHeatSink, sigma, beta, iR, c, b, e, betaOp_, _temp, resTime;
	ReturnRothBase() { }
	ReturnRothBase(double _xiDivHeatSink, double _sigma, double _beta, double _iR)
	{
		xiDivHeatSink = _xiDivHeatSink;
		sigma = _sigma;
		beta = _beta;
		iR = _iR;
		c = 7.47 * exp(-0.133 * pow(sigma, 0.55));
		b = 0.02526 * pow(sigma, 0.54);
		e = 0.715 * exp(-0.000359 * sigma);
		betaOp_ = 3.348 * pow(sigma, -0.8189);
		_temp = pow(beta / betaOp_, e);
		resTime = (384.0 / sigma);

	}
};


class RothFinalVal
{
public:
	double I_B, Rkmph, length_to_width, pathDir;
	double Flength;
	RothFinalVal() { }
	RothFinalVal(double _I_B, double _Rkmph, double _length_to_width, double _pathDir,double _flength)
	{
		I_B = _I_B; Rkmph = _Rkmph; pathDir = _pathDir; length_to_width = _length_to_width; Flength = _flength;
	}
};



ReturnRothBase RothBase(FuelFamilyItem& f, double moisture1, double moisture10, double moisture100, double moisture_live, double moisture_herbacious)
{
	if (moisture1 >= f.MoistExtReal)
	{
		return ReturnRothBase(99999, 0.0, 0.0, 0.0);
	}

	double sigma_ij[2][4] = {
		f.Sarv1h,  109,    30,		 f.SarvHerb,  
		f.SarvWoody,9999, 9999,		 f.SarvHerb }; 


	double w_0_ij[2][4] = {
		f.Load1h,	f.Load10h,	f.Load100h,                     0,
		f.LoadWoody,                 0,                       0, f.LoadHerb };

	double M_f_ij[2][4] = {
		moisture1,          moisture10,  moisture100,        moisture1,
		moisture_live,             0,         0,           moisture_herbacious };


	if (f.Dynamic == 1)
	{
		if (moisture_herbacious < 0.3)
		{
			w_0_ij[0][3] += w_0_ij[1][3];
			w_0_ij[1][3] = 0;
		}
		else if (moisture_herbacious < 1.2)
		{
			w_0_ij[0][3] += w_0_ij[1][3] * (1.333 - 1.11 * moisture_herbacious);
			w_0_ij[1][3] -= w_0_ij[0][3];
		}
	}

	double depth = f.Depth;
	double S_t_ij = 0.0555;
	double S_e_ij = 0.01;
	double h_ij[2] = { f.Heat,f.Heat };
	double rho_p_ij = 32.0;


	double A_ij[2][4];
	for (int ii = 0; ii < 2; ii++)
	{
		for (int jj = 0; jj < 4; jj++)
		{
			A_ij[ii][jj] = sigma_ij[ii][jj] * w_0_ij[ii][jj] / rho_p_ij;
		}
	};

	double A_i[2] = { A_ij[0][0] + A_ij[0][1] + A_ij[0][2] + A_ij[0][3],A_ij[1][0] + A_ij[1][3] };
	double AT = A_i[0] + A_i[1];

	double w_n_ij[2][4];
	double f_i[2];
	double f_ij[2][4];

	for (int ii = 0; ii < 2; ii++)
	{
		f_i[ii] = A_i[ii] / AT;
		for (int jj = 0; jj < 4; jj++)
		{
			f_ij[ii][jj] = div_(A_ij[ii][jj], A_i[ii]);
			w_n_ij[ii][jj] = w_0_ij[ii][jj] * (1 - S_t_ij);
		}
	};

	double sigma_i[2] = {
		sigma_ij[0][0] * f_ij[0][0] + sigma_ij[0][1] * f_ij[0][1] + sigma_ij[0][2] * f_ij[0][2] + sigma_ij[0][3] * f_ij[0][3],
		sigma_ij[1][0] * f_ij[1][0] + sigma_ij[1][3] * f_ij[1][3]
	};
	double sigma = sigma_i[0] * f_i[0] + sigma_i[1] * f_i[1];
	double A = 133 * power_(sigma, (-0.7913));


	double M_x_i[2] = { f.MoistExtReal,109 };

	double exp00 = w_0_ij[0][0] * exp(-138.0 / sigma_ij[0][0]);
	double exp01 = w_0_ij[0][1] * exp(-138.0 / sigma_ij[0][1]);
	double exp02 = w_0_ij[0][2] * exp(-138.0 / sigma_ij[0][2]);
	double exp03 = w_0_ij[0][3] * exp(-138.0 / sigma_ij[0][3]);

	double W_prima = div_(exp00 + exp01 + exp02 + exp03, (w_0_ij[1][0] * exp(-500 / sigma_ij[1][0]) + w_0_ij[1][3] * exp(-500 / sigma_ij[1][3])));
	double M_prima_f = (moisture1 * exp00 + moisture10 * exp01 + moisture100 * exp02 + moisture1 * exp03) / (exp00 + exp01 + exp02 + exp03);

	M_x_i[1] = 2.9 * W_prima * (1 - M_prima_f / M_x_i[0]) - 0.226;

	if (M_x_i[1] < M_x_i[0]) { M_x_i[1] = M_x_i[0]; }

	double h_i[2] = { 0,0 };
	double S_e_i[2] = { 0,0 };
	double w_n_i[2] = { 0,0 };
	double M_f_i[2] = { 0,0 };

	for (int ii = 0; ii < 2; ii++)
	{
		for (int jj = 0; jj < 4; jj++)
		{
			h_i[ii] = h_i[ii] + h_ij[ii] * f_ij[ii][jj];
			S_e_i[ii] = S_e_ij * f_ij[ii][jj] + S_e_i[ii];
			M_f_i[ii] = M_f_i[ii] + M_f_ij[ii][jj] * f_ij[ii][jj];
		}
	}

	//Getting the same as farsite, but it is wrong (!?)
	//for (int ii = 0; ii < 2; ii++){for (int jj = 0; jj < 4; jj++){w_n_i[ii] = w_n_ij[ii][jj] * f_ij[ii][jj] + w_n_i[ii];}}

	/////RIGHT IMPLEMENTATION THE SUM SHOUDL BE DONE BY CLASS SIZE AND [0,0] AND [0,3] HAVE THE SAME SIZE
	w_n_i[0] = (f_ij[0][0] + f_ij[0][3]) * (w_n_ij[0][0] + w_n_ij[0][3]) + f_ij[0][1] * w_n_ij[0][1] + f_ij[0][2] * w_n_ij[0][2];
	w_n_i[1] = (f_ij[1][0] + f_ij[1][3]) * (w_n_ij[1][0] + w_n_ij[1][3]);
	//////////////////////////////////////////

	double r_m_i[2] = { M_f_i[0] / M_x_i[0],M_f_i[1] / M_x_i[1] };
	if (r_m_i[1] > 1) { r_m_i[1] = 1; }
	if (r_m_i[0] > 1) { r_m_i[0] = 1; }


	double eta_m_i[2] = {
		1 - 2.59 * r_m_i[0] + 5.11 * r_m_i[0] * r_m_i[0] - 3.52 * r_m_i[0] * r_m_i[0] * r_m_i[0],
		1 - 2.59 * r_m_i[1] + 5.11 * r_m_i[1] * r_m_i[1] - 3.52 * r_m_i[1] * r_m_i[1] * r_m_i[1]
	};
	double eta_s_i[2] = {
		0.174 * power_(S_e_i[0],(-0.19)),
		0.174 * power_(S_e_i[1],(-0.19))
	};


	double rho_b = (1 / depth) * (w_0_ij[0][0] + w_0_ij[0][1] + w_0_ij[0][2] + w_0_ij[0][3] + w_0_ij[1][0] + w_0_ij[1][1] + w_0_ij[1][2] + w_0_ij[1][3]);

	double beta = rho_b / rho_p_ij;
	double beta_op = 3.348 * power_(sigma, (-0.8189));
	double gamma_max = power_(sigma, (1.5)) / (495 + 0.0594 * power_(sigma, 1.5));
	double gamma = (gamma_max * power_(beta / beta_op, A)) * exp(A * (1 - beta / beta_op));

	double xi = 1 / (192 + 0.2595 * sigma) * exp((0.792 + 0.681 * power_(sigma, 0.5)) * (beta + 0.1));
	double I_R = gamma * (w_n_i[0] * h_i[0] * eta_m_i[0] * eta_s_i[0] + w_n_i[1] * h_i[1] * eta_m_i[1] * eta_s_i[1]); //changed by Albini
	double Q_ij[2][4];

	double denominador_aux[2] = { 0,0 };
	for (int ii = 0; ii < 2; ii++)
	{
		for (int jj = 0; jj < 4; jj++)
		{
			Q_ij[ii][jj] = 250 + 1116 * M_f_ij[ii][jj];
			denominador_aux[ii] = denominador_aux[ii] + f_ij[ii][jj] * exp(div_(-138, sigma_ij[ii][jj])) * Q_ij[ii][jj];
		}
	}

	double heatSink = rho_b * (f_i[0] * denominador_aux[0] + f_i[1] * denominador_aux[1]);
	double xiDivHeatSink = div_(xi, heatSink);
	return  ReturnRothBase(xiDivHeatSink, sigma, beta, I_R);


}

RothFinalVal RotherAddWindSlope(ReturnRothBase& rBase, double windSpeed, int windAspect, int slopeMod, int slopeAspect)
{

	if (rBase.beta == 0) { return  RothFinalVal(0, 0.00001, 1, 1,0.01); }
	else
	{
		double alfa = DEG2RAD * AngleDistance(windAspect, slopeAspect);
		double u_feet_min = windSpeed * 54.6807; 
		double tanPhi = tan(slopeMod * DEG2RAD);
		double phiW = rBase.c * pow(std::min(u_feet_min, 0.9 * rBase.iR), rBase.b) / rBase._temp;
		double phiS = 5.275 * pow(rBase.beta, (-0.3)) * tanPhi * tanPhi;

		double PhisSinAlfa = phiS * sin(alfa);
		double PhisCosAlfa = phiS * cos(alfa);

		double vectorModule = sqrt(PhisSinAlfa * PhisSinAlfa + pow(PhisCosAlfa + phiW, 2));
		double vectorAngulo = RAD2DEG * atan2(PhisSinAlfa, PhisCosAlfa + phiW);

		double pathDir = (int)(vectorAngulo + windAspect + 360) % 360;
		double virtualWind_feet_min = pow(vectorModule * rBase._temp / rBase.c, 1.0 / rBase.b); //Remove the initial Rothemerl limit of 3*0.9*IR

		double lengthToWidth = std::min(8.0, 1 + 0.0028409 * virtualWind_feet_min); //behave phiW= 1 + 0.25 miles/h
		double r_feetMin = rBase.iR * rBase.xiDivHeatSink * (1 + vectorModule);
		double iB = 0.057735667 * rBase.iR * r_feetMin * rBase.resTime;       //byrams fireline   1 but/ft/s = 3.464 kW/m =kj m-1 s-1 // 0.057735667=3.46414
		double Rkmph = r_feetMin * 0.018288; // kM/H ROS
		double Flength= 0.077499428	* pow(iB, 0.46);
		return  RothFinalVal(iB, Rkmph, lengthToWidth, pathDir,Flength);


	}
}




#endif
