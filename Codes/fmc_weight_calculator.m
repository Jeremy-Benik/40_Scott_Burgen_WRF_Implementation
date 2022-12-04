function [fuel_weight_1hr, fuel_weight_10hr, fuel_weight_100hr, ...
    fuel_weight_herb, fuel_weight_woody] = fmc_weight_calculator(fuel, percent_dead)

%Enter number in as whole number, not decimal

% Reading in the file and assigning variables
% Reading in the file
dynamic = fuel.isdynamic;
%Getting the fuel name (not necessary)
fuel_name = fuel.fuel_name;
% Getting the fuel load for dead 1hr fuels
fgi_1hr = fuel.fgi_1hr;
% Getting the fuel load for dead 10hr fuels
fgi_10hr = fuel.fgi_10hr;
% Getting the fuel load for dead 100hr fuels
fgi_100hr = fuel.fgi_100hr;
% Getting the fuel load for live herb fuels
fgi_live_herb = fuel.fgi_live_herb;
% Getting the fuel load for live woody fuels
fgi_live_woody = fuel.fgi_live_woody;
% Getting the fuel model type (may be used later)
%fuel_model_type = fuel.fuel_model_type;
% Getting the SAVR for dead 1hr fuels
savr_1hr = fuel.savr_dead_1hr;
% Getting the SAVR for dead 10hr fuels
savr_10hr = fuel.savr_dead_10hr;
% Getting the SAVR for dead 100hr fuels
savr_100hr = fuel.savr_dead_100hr;
% Getting the SAVR for live herb fuels
savr_live_herb = fuel.savr_live_herb;
% Getting the SAVR for live woody fuels
savr_live_woody = fuel.savr_live_woody;
% Setting the x value. This will become an input later on
x = percent_dead/100;
% Calculating the dead FPSA
FPSA_total_dead = (((fgi_live_herb .* x) ./ 513) .* savr_live_herb) + ...
    ((fgi_1hr ./ 513) .* savr_1hr) + ((fgi_10hr ./ 513) .* savr_10hr) + ...
    ((fgi_100hr ./ 513) .* savr_100hr);

% Calculating the live FPSA
FPSA_total_live = (((fgi_live_herb .* x) ./ 513) .* savr_live_herb) + ...
    ((fgi_live_woody ./ 513) .* savr_live_woody);

% Calculating the individual fuel weighting parameters
% Woody fuels
fuel_weight_woody = (fgi_live_woody / 513) .* ...
    savr_live_woody ./ FPSA_total_live;
% herb
fuel_weight_herb = ((fgi_live_herb .* x) / 513) .* ...
    savr_live_herb ./ FPSA_total_dead;
%1 hour fules
fuel_weight_1hr = (fgi_1hr ./ 513) .* savr_1hr ./ FPSA_total_dead;
%10 hour fuels
fuel_weight_10hr = (fgi_10hr ./ 513) .* savr_10hr ./ FPSA_total_dead;
%100 hour fuels
fuel_weight_100hr = (fgi_100hr ./ 513) .* savr_100hr ./ FPSA_total_dead;







