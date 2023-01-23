% This code will be used to test every fuel parameter for both models
% I am testing it from 0 to 15m/s since in the BehavePlus model, the
% strongest wind you can have is 17m/s
%% Reading in the fuels code for the technosylvia model
fuels_tslv;

% Since the model starts to behave (pun not intended) different with fuel
% type 4, I will stop this at 3, then continue to 4 but with different fuel
% moistures

% Fuel type 1
x = linspace(0, 15, 500);
fuel_1 = zeros(500);
fuel_1 = fire_ros_tslv(fuel(1), x, 0, 0.03, 0., 0.03, 0.03, 0.03);
plot(x, fuel_1, 'red', 'LineWidth',2)
hold on;

% Fuel type 2
x = linspace(0, 15, 500);
fuel_2 = zeros(500);
fuel_2 = fire_ros_tslv(fuel(2), x, 0, 0.03, 0.03, 0.03, 0.03, 0.03);
plot(x, fuel_2, 'blue', 'LineWidth',2)
hold on;

% Fuel type 3
x = linspace(0, 15, 500);
fuel_3 = zeros(500);
fuel_3 = fire_ros_tslv(fuel(3), x, 0, 0.03, 0.03, 0.03, 0.03, 0.03);
plot(x, fuel_3, 'green', 'LineWidth',2)
hold off;
legend('fuel 1', 'fuel 2', 'fuel 3', 'Location','northwest')
grid on;
ylim([0, 30])
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
title('WFA ROS Model with all 13 Albini Fuel Categories (3% FMC)', fontsize = 15, ...
    fontweight = 'bold')
%% Reading in the fuels code from WRF-SFIRE
fuels;
% Fuel type 1
x = linspace(0, 15, 500);
fuel_1 = zeros(500);
fuel_1 = fire_ros(fuel(1), x, 0, 0.03);
plot(x, fuel_1, 'red', 'LineWidth',2)
hold on;

% Fuel type 2
x = linspace(0, 15, 500);
fuel_2 = zeros(500);
fuel_2 = fire_ros(fuel(2), x, 0, 0.03);
plot(x, fuel_2, 'blue', 'LineWidth',2)
hold on;

% Fuel type 3
x = linspace(0, 15, 500);
fuel_3 = zeros(500);
fuel_3 = fire_ros(fuel(3), x, 0, 0.03);
plot(x, fuel_3, 'green', 'LineWidth',2)
hold off;
legend('fuel 1', 'fuel 2', 'fuel 3', 'Location','northwest')

grid on;
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
ylim([0, 30])
title('WRF-SFIRE ROS Model with all 13 Albini Fuel Categories', fontsize = 15, ...
    fontweight = 'bold')
%% Showing fuel category 4 since that has been really sensitive
fuels_tslv;
% Fuel type 4 WFA
x = linspace(0, 15, 500)
fuel_4_WFA = zeros(500);
fuel_4_WFA = fire_ros_tslv(fuel(4), x, 0, 0.1, 0.1, 0.1, 0.1, 0.1);
plot(x, fuel_4_WFA, 'red', 'LineWidth',2)
grid on;
ylim([0, 20])
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
title('WFA ROS Model with Fuel Cateogory 4', fontsize = 15, ...
    fontweight = 'bold')
%%
fuels;
% Fuel type 4 WRF
x = linspace(0, 15, 500)
fuel_4_WRF = zeros(500);
fuel_4_WRF = fire_ros(fuel(4), x, 0, 0.1);
plot(x, fuel_4_WRF, 'blue', 'LineWidth',2)
grid on;
ylim([0, 20])
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
title('WRF ROS Model with Fuel Cateogory 4', fontsize = 15, ...
    fontweight = 'bold')


%% Showing all other fuel categories
% WFA 
% Fuel type 5
x = linspace(0, 15, 500);
fuel_5_WFA = zeros(500);
fuel_5_WFA = fire_ros_tslv(fuel(5), x, 0, 0.15, 0.15, 0.15, 0.15, 0.15);
plot(x, fuel_5_WFA, 'red', 'LineWidth',2)
hold on;

% Fuel type 6
x = linspace(0, 15, 500);
fuel_6_WFA = zeros(500);
fuel_6_WFA = fire_ros_tslv(fuel(6), x, 0, 0.15, 0.15, 0.15, 0.15, 0.15);
plot(x, fuel_6_WFA, 'blue', 'LineWidth',2)
hold on;

% Fuel type 7
x = linspace(0, 15, 500);
fuel_7_WFA = zeros(500);
fuel_7_WFA = fire_ros_tslv(fuel(7), x, 0, 0.15, 0.15, 0.15, 0.15, 0.15);
plot(x, fuel_7_WFA, 'green', 'LineWidth',2)
hold on;

% Fuel type 8
x = linspace(0, 15, 500);
fuel_8_WFA = zeros(500);
fuel_8_WFA = fire_ros_tslv(fuel(8), x, 0, 0.15, 0.15, 0.15, 0.15, 0.15);
plot(x, fuel_8_WFA, 'magenta', 'LineWidth',2)
hold on;

% Fuel type 9
x = linspace(0, 15, 500);
fuel_9_WFA = zeros(500);
fuel_9_WFA = fire_ros_tslv(fuel(9), x, 0, 0.15, 0.15, 0.15, 0.15, 0.15);
plot(x, fuel_9_WFA, 'black', 'LineWidth',2)
hold off;
legend('fuel 5', 'fuel 6', 'fuel 7', 'fuel 8', 'fuel 9', 'Location','northwest')
grid on;
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylim([0, 6])
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
title('WFA ROS Model with all 13 Albini Fuel Categories (15% FMC)', fontsize = 15, ...
    fontweight = 'bold')

%% WRF-SFIRE
fuels;
% Fuel type 5
x = linspace(0, 15, 500);
fuel_5 = zeros(500);
fuel_5 = fire_ros(fuel(5), x, 0, 0.15);
plot(x, fuel_5, 'red', 'LineWidth',2)
hold on;

% Fuel type 6
x = linspace(0, 15, 500);
fuel_6 = zeros(500);
fuel_6 = fire_ros(fuel(6), x, 0, 0.15);
plot(x, fuel_6, 'blue', 'LineWidth',2)
hold on;

% Fuel type 7
x = linspace(0, 15, 500);
fuel_7 = zeros(500);
fuel_7 = fire_ros(fuel(7), x, 0, 0.15);
plot(x, fuel_7, 'green', 'LineWidth',2)
hold on;

% Fuel type 8
x = linspace(0, 15, 500);
fuel_8 = zeros(500);
fuel_8 = fire_ros(fuel(8), x, 0, 0.15);
plot(x, fuel_8, 'magenta', 'LineWidth',2)
hold on;


% Fuel type 9
x = linspace(0, 15, 500);
fuel_9 = zeros(500);
fuel_9 = fire_ros(fuel(9), x, 0, 0.15);
plot(x, fuel_9, 'black', 'LineWidth',2)
hold off;

legend('fuel 5', 'fuel 6', 'fuel 7', 'fuel 8', 'fuel 9', 'Location','northwest')

grid on;
ylim([0, 6])
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
title('WRF-SFIRE ROS Model with all 13 Albini Fuel Categories (15% FMC)', fontsize = 15, ...
    fontweight = 'bold')

%% Showing all other fuel categories 10, 11, 12, 13
% WFA 
% Fuel type 5
x = linspace(0, 15, 500);
fuel_10_WFA = zeros(500);
fuel_10_WFA = fire_ros_tslv(fuel(10), x, 0, 0.150, 0.150, 0.150, 0.150, 0.150);
plot(x, fuel_10_WFA, 'red', 'LineWidth',2)
hold on;

% Fuel type 6
x = linspace(0, 15, 500);
fuel_11_WFA = zeros(500);
fuel_11_WFA = fire_ros_tslv(fuel(11), x, 0, 0.150, 0.150, 0.150, 0.150, 0.150);
plot(x, fuel_11_WFA, 'blue', 'LineWidth',2)
hold on;

% Fuel type 7
x = linspace(0, 15, 500);
fuel_12_WFA = zeros(500);
fuel_12_WFA = fire_ros_tslv(fuel(12), x, 0, 0.150, 0.150, 0.150, 0.150, 0.150);
plot(x, fuel_12_WFA, 'green', 'LineWidth',2)
hold on;

% Fuel type 8
x = linspace(0, 15, 500);
fuel_13_WFA = zeros(500);
fuel_13_WFA = fire_ros_tslv(fuel(13), x, 0, 0.150, 0.150, 0.150, 0.150, 0.150);
plot(x, fuel_13_WFA, 'magenta', 'LineWidth',2)
hold off;

legend('fuel 10', 'fuel 11', 'fuel 12', 'fuel 13', 'Location','northwest')
grid on;
ylim([0, 2.5])
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
title('WFA ROS Model with all 13 Albini Fuel Categories (15% FMC)', fontsize = 15, ...
    fontweight = 'bold')

%% WRF-SFIRE
fuels;
% Fuel type 5
x = linspace(0, 15, 500);
fuel_10_WRF = zeros(500);
fuel_10_WRF = fire_ros(fuel(10), x, 0, 0.15);
plot(x, fuel_10_WRF, 'red', 'LineWidth',2)
hold on;

% Fuel type 6
x = linspace(0, 15, 500);
fuel_11_WRF = zeros(500);
fuel_11_WRF = fire_ros(fuel(11), x, 0, 0.15);
plot(x, fuel_11_WRF, 'blue', 'LineWidth',2)
hold on;

% Fuel type 7
x = linspace(0, 15, 500);
fuel_12_WRF = zeros(500);
fuel_12_WRF = fire_ros(fuel(12), x, 0, 0.15);
plot(x, fuel_12_WRF, 'green', 'LineWidth',2)
hold on;

% Fuel type 8
x = linspace(0, 15, 500);
fuel_13_WRF = zeros(500);
fuel_13_WRF = fire_ros(fuel(13), x, 0, 0.15);
plot(x, fuel_13_WRF, 'magenta', 'LineWidth',2)
hold off;

legend('fuel 10', 'fuel 11', 'fuel 12', 'fuel 13', 'Location','northwest')

grid on;
ylim([0, 2.5])
xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ylabel('Rate of Spread (m/s)', fontsize = 12, fontweight = 'bold')
title('WRF-SFIRE ROS Model with all 13 Albini Fuel Categories (15% FMC)', fontsize = 15, ...
    fontweight = 'bold')
















