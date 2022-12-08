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
ros_very_low = ros_rothermel(x, wind_speed, 0, very_low);

% ROS for low fuels
ros_low = ros_rothermel(x, wind_speed, 0, low);

% ROS for moderate fuels
ros_moderate = ros_rothermel(x, wind_speed, 0, moderate);

% ROS for high FMC
ros_high = ros_rothermel(x, wind_speed, 0, high);




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

