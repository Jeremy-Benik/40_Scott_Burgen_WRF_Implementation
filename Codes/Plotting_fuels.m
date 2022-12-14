% Reading in the fuels code
%fuels;
x = fuel(3);
% Finding the wind reduction factor for calculating the midflame height
windrf = x.windrf;

% Setting the wind speed from
wind_speed = linspace(0,22,500);

% Calculating the wind speed at the mid flame height
ws_mid_flame = wind_speed .* windrf;

% Converting the mid flame wind speed to m/s wind to mph to match the graphs 
wind_mph = ws_mid_flame .* 2.2369362920544;

% Assigning the values for the FMC (can be found in table 3 in paper)
very_low = 0.03;
low = 0.06;
moderate = 0.09;
high  = 0.12;

% Calculating the rate of spread from the rothermel model
% ROS for very low fuel
ros_very_low = fire_ros(x, wind_speed, 0, very_low);

% ROS for low fuels
ros_low = fire_ros(x, wind_speed, 0, low);

% ROS for moderate fuels
ros_moderate = fire_ros(x, wind_speed, 0, moderate);

% ROS for high FMC
ros_high = fire_ros(x, wind_speed, 0, high);


convert = 178.91; %converting m/s to ch/h
very_low_ros = ros_very_low .* convert;
low_ros = ros_low .* convert;
moderate_ros = ros_moderate .* convert;
high_ros = ros_high .* convert;

plot(wind_mph, very_low_ros, 'red', 'LineWidth', 2);
hold on;
plot(wind_mph, low_ros, 'yellow', 'LineWidth', 2);
hold on;
plot(wind_mph, moderate_ros, 'green', 'LineWidth', 2);
hold on;
plot(wind_mph, high_ros, 'blue', 'LineWidth', 2);
leg = legend('very low', 'low', 'moderate', 'high');
xlabel('Midflame Wind Speed (mph)', fontsize = 12, fontweight = 'bold');
ylabel('ROS (ch/h)', fontsize = 12, fontweight = 'bold');
title('Fuel 3');
grid on;
set(leg,'location','best')
%%
x = fuel(17);
wind_speed = 1;
midflame = wind_speed * x.windrf;
midflame_2 = midflame * 3.6;
disp('Midflame height km/hr')
disp(midflame_2);


ros = ros_rothermel(fuel(17), 0, 1, 0.03);
disp('The ROS is');
disp(ros);



%%
wind_speed = linspace(0, 15, 100);

[ir, qig, phiw, phis, gamma, xifr, etam, rtemp1, ros_1] = ros_rothermel(fuel(3), wind_speed, 0, 0.04);
[ir, qig, phiw, phis, gamma, xifr, etam, rtemp1, ros_2] = ros_rothermel(fuel(3), wind_speed, 0, 0.07);
plot(wind_speed, ros_1, 'red', 'LineWidth', 2);
hold on;
plot(wind_speed, ros_2, 'blue', 'LineWidth', 2);
grid on;
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold');
ylabel('ROS (m/s)', fontsize = 12, fontweight = 'bold');
legend('Fuel cat 3, FM = 4%', 'Fuel cat 3, FM = 7%');
%%
wind_speed = linspace(0, 15, 100);

ros_3 = fire_ros(fuel(3), wind_speed, 0, 0.04);
ros_4 = fire_ros(fuel(3), wind_speed, 0, 0.07);
plot(wind_speed, ros_3, 'red', 'LineWidth', 2);
hold on;
plot(wind_speed, ros_4, 'blue', 'LineWidth', 2);
grid on;
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold');
ylabel('ROS (m/s)', fontsize = 12, fontweight = 'bold');
legend('Fuel cat 3, FM = 4%', 'Fuel cat 3, FM = 7%');


%%
% lets make a code that does everything I need with one change
disp('------------------------------------------------')
wind_speed = 3;
x = fuel(12);
disp('the wind speed is');
disp(wind_speed);
windrf = x.windrf;
fmc = 0.10;
slope = 0;
disp('the midflame wind speed in km/hr is');
wind = (wind_speed * windrf) * 3.6

disp('The windrf adjustment factor is:');
disp(windrf);

disp('FMC');
disp(fmc);
disp('ROS')
ros = fire_ros(x, wind_speed, slope, fmc)
%%
wind_speed = linspace(0, 5, 5);
x = fuel(12);

ros = fire_ros(x, wind_speed, 0, 0.09);
disp(ros)



















