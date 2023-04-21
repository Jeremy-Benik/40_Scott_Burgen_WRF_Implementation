% This is the original WFA (Wild Fire Analyst model) Rothermel model. It
% was originally written in c++, however Dr. Angel Farguell Caus converted
% it to a matlab file for testing purposes so we can see how this code is
% different from the WRF-SFIRE fire_ros.m code since the values we have
% noticed are different from each other. Please checkout this paper for a
% more in depth explanation on the differences between each ROS model. 
% https://github.com/Jeremy-Benik/40_Scott_Burgen_WRF_Implementation/blob/main/Papers/Comparison_between_models.pdf


function ros=fire_ros_tslv(fuel,speed,tanphi,fmc_1,fmc_10,fmc_100,fmc_herba,fmc_woody)
% ros=fire_ros_tslv(fuel,speed,tanphi,fmc_1,fmc_10,fmc_100,fmc_herba,fmc_woody)
% in
%       fuel       fuel description structure
%       speed      wind speed
%       tanphi     slope
%       fmc_1      dead 1-hour fuel moisture
%       fmc_10     dead 10-hour fuel moisture
%       fmc_100    dead 100-hour fuel moisture
%       fmc_herba  live herbaceous fuel moisture
%       fmc_woody  live woody fuel moisture
% out
%       ros       rate of spread

% given fuel params
windrf=fuel.windrf;                       % WIND REDUCTION FACTOR (1)
fgi=fuel.fgi;                             % INITIAL TOTAL MASS OF SURFACE FUEL (KG/M**2)
fueldepthm=fuel.fueldepthm;               % FUEL DEPTH (M)
savr=fuel.savr;                           % FUEL PARTICLE SURFACE-AREA-TO-VOLUME RATIO (1/FT)
fuelmce=fuel.fuelmce;                     % MOISTURE CONTENT OF EXTINCTION (1)
fueldens=fuel.fueldens;                   % OVENDRY PARTICLE DENSITY (LB/FT^3)
st=fuel.st;                               % FUEL PARTICLE TOTAL MINERAL CONTENT (1)
se=fuel.se;                               % FUEL PARTICLE EFFECTIVE MINERAL CONTENT (1)
weight=fuel.weight;                       % WEIGHTING PARAMETER THAT DETERMINES THE SLOPE OF THE MASS LOSS CURVE (1)
fci_d=fuel.fci_d;                         % INITIAL DRY MASS OF CANOPY FUEL
fct=fuel.fct;                             % BURN OUT TIME FOR CANOPY FUEL, AFTER DRY (S)
ichap=fuel.ichap;                         % 1 if chaparral, 0 if not
fci=fuel.fci;                             % INITIAL TOTAL MASS OF CANOPY FUEL (KG/M**2)
fcbr=fuel.fcbr;                           % FUEL CANOPY BURN RATE (KG/M^2/S)
hfgl=fuel.hfgl;                           % SURFACE FIRE HEAT FLUX THRESHOLD TO IGNITE CANOPY (W/M^2)
cmbcnst=fuel.cmbcnst;                     % JOULES PER KG OF DRY FUEL (J/KG)
fuelheat=fuel.fuelheat;                   % FUEL PARTICLE LOW HEAT CONTENT (BTU/LB)
fuelmc_g=fuel.fuelmc_g;                   % FUEL PARTICLE (SURFACE) MOISTURE CONTENT (1)
fuelmc_c=fuel.fuelmc_c;                   % FUEL PARTICLE (CANOPY) MOISTURE CONTENT (1)
fuelmce_live=fuel.fuelmce_live;           % MOISTURE CONTENT OF EXTINCTION FOR LIVE FUEL (1)
fuelload_1=fuel.fuelload_1               % OVEN-DRY FUEL LOAD FROM DEAD 1H FUEL (LB/FT^2)
fuelload_10=fuel.fuelload_10             % OVEN-DRY FUEL LOAD FROM DEAD 10H FUEL (LB/FT^2)
fuelload_100=fuel.fuelload_100;           % OVEN-DRY FUEL LOAD FROM DEAD 100H FUEL (LB/FT^2)
fuelload_herba=fuel.fuelload_herba;       % OVEN-DRY FUEL LOAD FROM LIVE HERBACEOUS FUEL (LB/FT^2)
fuelload_woody=fuel.fuelload_woody;       % OVEN-DRY FUEL LOAD FROM LIVE WOODY FUEL (LB/FT^2)
savr_1=fuel.savr_1;                       % FUEL PARTICLE SURFACE-AREA-TO-VOLUME RATIO FROM DEAD 1H FUEL (1/FT)
savr_10=fuel.savr_10;                     % FUEL PARTICLE SURFACE-AREA-TO-VOLUME RATIO FROM DEAD 10H FUEL (1/FT)
savr_100=fuel.savr_100;                   % FUEL PARTICLE SURFACE-AREA-TO-VOLUME RATIO FROM DEAD 100H FUEL (1/FT)
savr_herba=fuel.savr_herba;               % FUEL PARTICLE SURFACE-AREA-TO-VOLUME RATIO FROM LIVE HERBACEOUS FUEL (1/FT)
savr_woody=fuel.savr_woody;               % FUEL PARTICLE SURFACE-AREA-TO-VOLUME RATIO FROM LIVE WOODY FUEL (1/FT)
idynamic=fuel.idynamic;                   % 1 if dynamic fuel, 0 if not
% translating units
fueldepth= fueldepthm/0.3048;              % to ft
% dynamic load transfer from live to dead
fuelload_herba_dead = 0;
savr_herba_dead = savr_herba;
fmc_herba_dead = fmc_1;
if idynamic
    if fmc_herba < 0.3
        fuelload_herba_dead = fuelload_herba_dead + fuelload_herba;
        fuelload_herba = 0;
    elseif fmc_herba < 1.2
        fuelload_herba_dead = fuelload_herba_dead * (1.333 - 1.11 * fmc_herba);
		fuelload_herba = fuelload_herba - fuelload_herba_dead;          
    end
end
% total fuel load
fuelload      = fuelload_1 + fuelload_10 + fuelload_100 + fuelload_herba_dead + fuelload_herba + fuelload_woody 
% mean total surface area per unit fuel cell of each size class within each category
A_1           = savr_1 * fuelload_1 / fueldens; 
A_10          = savr_10 * fuelload_10 / fueldens;
A_100         = savr_100 * fuelload_100 / fueldens;
A_herba_dead  = savr_herba_dead * fuelload_herba_dead / fueldens;
A_herba       = savr_herba * fuelload_herba / fueldens;
A_woody       = savr_woody * fuelload_woody / fueldens;
% mean total surface area per unit fuel cell of the dead and live categories
A_dead        = A_1 + A_10 + A_100 + A_herba_dead;
A_live        = A_herba + A_woody;
% mean total surface area of the fuel
AT            = A_dead + A_live; 
% weighting factors of each size class within each category
f_1           = div_(A_1, A_dead);
f_10          = div_(A_10, A_dead);
f_100         = div_(A_100, A_dead);
f_herba_dead  = div_(A_herba_dead, A_dead);
f_herba       = div_(A_herba, A_live);
f_woody       = div_(A_woody, A_live);
% weighting factors of the dead and live categories
f_dead        = A_dead / AT;
f_live        = A_live / AT;
% fuel particle surface-to-volume ratio of the dead and live categories
savr_dead     = f_1 * savr_1 + f_10 * savr_10 + f_100 * savr_100 + f_herba_dead * savr_herba_dead;
savr_live     = f_herba * savr_herba + f_woody * savr_woody;
% fuel particle surface-to-volume ratio of the fuel
savr          = f_dead * savr_dead + f_live * savr_live
% net fuel loading of each size class within each category
wn_1          = fuelload_1 * (1 - st);
wn_10         = fuelload_10 * (1 - st);
wn_100        = fuelload_100 * (1 - st);
wn_herba_dead = fuelload_herba_dead * (1 - st);
wn_herba      = fuelload_herba * (1 - st);
wn_woody      = fuelload_woody * (1 - st);
% net fuel loading of the dead and live categories
wn_dead       = (f_1 + f_herba_dead) * (wn_1 + wn_herba_dead) + f_10 * wn_10 + f_100 * wn_100;
wn_live       = f_herba * wn_herba + f_woody * wn_woody;
% live fuel moisture of extinction
exp00         = fuelload_1 * exp(-138.0 / savr_1);
exp01         = fuelload_10 * exp(-138.0 / savr_10);
exp02         = fuelload_100 * exp(-138.0 / savr_100);
exp03         = fuelload_herba_dead * exp(-138.0 / savr_herba_dead);
exp10         = fuelload_herba * exp(-500 / savr_herba);
exp11         = fuelload_woody * exp(-500 / savr_woody);
W_prima       = div_(exp00 + exp01 + exp02 + exp03, exp10 + exp11);
M_prima_f     = (fmc_1 * exp00 + fmc_10 * exp01 + fmc_100 * exp02 + fmc_herba_dead * exp03) / (exp00 + exp01 + exp02 + exp03);
fuelmce_live  = 2.9 * W_prima * (1 - M_prima_f / fuelmce) - 0.226;
if fuelmce_live < fuelmce
    fuelmce_live = fuelmce;
end
% heat content of the dead and live categories
fuelheat_dead = (f_1 + f_10 + f_100 + f_herba_dead) * fuelheat;
fuelheat_live = (f_herba + f_woody) * fuelheat;
% fuel particle effective mineral content of the dead and live categories
se_dead       = (f_1 + f_10 + f_100 + f_herba_dead) * se;
se_live       = (f_herba + f_woody) * se;
% fuel moisture content of the dead and live categories
fmc_dead      = f_1 * fmc_1 + f_10 * fmc_10 + f_100 * fmc_100 + f_herba_dead * fmc_herba_dead;
fmc_live      = f_herba * fmc_herba + f_woody * fmc_woody;
% moisture damping coefficient of the dead and live categories
rtemp1_dead   = min(1,fmc_dead/fuelmce);
rtemp1_live   = min(1,fmc_live/fuelmce_live);
etam_dead     = 1. - 2.59*rtemp1_dead + 5.11*rtemp1_dead^2 - 3.52*rtemp1_dead^3;
etam_live     = 1. - 2.59*rtemp1_live + 5.11*rtemp1_live^2 - 3.52*rtemp1_live^3;
% mineral damping coefficient of the dead and live categories
etas_dead     = 0.174* power_(se_dead, -0.19);
etas_live     = 0.174* power_(se_live, -0.19); 
% coef for optimum rxn vel
a             = 133. * power_(savr, -0.7913);
% original computations from fire_ros.m
rhob          = fuelload/fueldepth;             % ovendry bulk density, lb/ft^3
betafl        = fuelload/(fueldepth * fueldens);% packing ratio  jm: lb/ft^2/(ft * lb*ft^3) = 1
betaop        = 3.348 * power_(savr, -0.8189); % optimum packing ratio
rtemp2        = power_(savr, 1.5);
gammax        = rtemp2/(495. + 0.0594*rtemp2);  % maximum rxn vel, 1/min
ratio         = betafl/betaop;
gamma         = gammax*(power_(ratio, a))*exp(a*(1.-ratio)); % optimum rxn vel, 1/min
xifr          = exp( (0.792 + 0.681*power_(savr, 0.5))...
                * (betafl+0.1)) /(192. + 0.2595*savr); % propagating flux ratio
% rxn intensity, btu/ft^2 min
ir            = gamma * (wn_dead * fuelheat_dead * etam_dead * etas_dead + ...
                wn_live * fuelheat_live * etam_live * etas_live);
% heat of preiginition of each size class within each category, btu/lb
qig_1         = 250. + 1116.*fmc_1;
qig_10        = 250. + 1116.*fmc_10;
qig_100       = 250. + 1116.*fmc_100;
qig_herba_dead= 250. + 1116.*fmc_herba_dead;
qig_herba     = 250. + 1116.*fmc_herba;
qig_woody     = 250. + 1116.*fmc_woody;
% effective heating number of each size class within each category
epsilon_1          = exp(div_(-138., savr_1));
epsilon_10         = exp(div_(-138., savr_10));
epsilon_100        = exp(div_(-138., savr_100));
epsilon_herba_dead = exp(div_(-138., savr_herba_dead));
epsilon_herba      = exp(div_(-138., savr_herba));
epsilon_woody      = exp(div_(-138., savr_woody));
% heat sink of the dead and live categories
heat_sink_dead     = rhob * f_dead * ( ...
                     f_1 * epsilon_1 * qig_1 + ...
                     f_10 * epsilon_10 * qig_10 + ...
                     f_100 * epsilon_100 * qig_100 + ...
                     f_herba_dead * epsilon_herba_dead * qig_herba_dead);
heat_sink_live     = rhob * f_live * ( ...
                     f_herba * epsilon_herba * qig_herba + ...
                     f_woody * epsilon_woody * qig_woody);
%        ... r_0 is the spread rate for a fire on flat ground with no wind.
r_0                = div_(ir*xifr, heat_sink_dead + heat_sink_live); % default spread rate in ft/min
% wind speed in ft/min with wind limit
%try without this flag (modify the code a bit)
umid     = min(max(0, speed * 196.850), 0.9 * ir); % m/s to ft/min
% original computations from fire_ros.m
c        = 7.47 * exp(-0.133 * savr^0.55); % const in wind coef
bbb      = 0.02526 * savr^0.54;            % const in wind coef
%c        = c * windrf^bbb;                 % jm: wind reduction from 20ft per Baughman&Albini(1980)
e        = 0.715 * exp( -3.59e-4 * savr);  % const in wind coef
phiwc    = c * (betafl/betaop)^(-e);
phiw     = umid.^bbb * phiwc;                  % wind coef
phis = 5.275 * betafl^(-0.3) *max(0,tanphi)^2;  % slope factor
ros = r_0 * (1. + phiw + phis) * .00508; % spread rate, m/s
end
function r = div_(a,b)
    if b == 0
        r=0;
    else
        r=a/b;
    end
end
function r = power_(a,b)
    if a == 0
        r=0;
    else
        r=a^b;
    end
end
