% PLOT_DATA
%   Plots the z-scored fluorescence raster ordered by detected
%   assemblies, the sample correlation matrix, sample fluorescence 
%   traces for each assembly, and spatial organisation of each assembly.
%
%   Code by Marcus Triplett (2018).

%% Load data
% load('zf_20151104-f1/zf_20151104-f1.mat');
load('zf_20170215-f3/zf_20170215-f3.mat');

[N, duration] = size(activity_matrix);
num_assemblies = numel(detected_assemblies);

% Reorder neurons by detected assembly
order = [];
for ii = 1:num_assemblies
    order = [order detected_assemblies{ii}];   
end

% z-score activities
activities_zs = zeros(size(activity_matrix));
for ii = 1:N
    activities_zs(ii, :) = zscore(activity_matrix(ii, :));
end

%% Plot fluorescence raster
imrate = 2.2; % Hz
xtick = 600 * imrate; % 10 min xticks
figure(1);
imagesc(activities_zs(order, :))
colormap(flipud(gray)); box on;
cb = colorbar; ylabel(cb, 'z-scored \Delta F/F');
set(gcf, 'color', 'white', 'position', [534, 603, 776, 238])
set(gca, 'linewidth', 3, 'YTick', [], 'fontsize', 20, ...
    'XTick', [1, xtick * [1:3]], 'XTickLabel', [0, 10*[1:3]])
ylabel('Neuron'); xlabel('Time (min)');

%% Plot correlation matrix
figure(2); %hold on;
corr_mat = corr(activity_matrix(order, :)')';
imagesc(corr_mat);
box on; axis square;
xlabel('Neuron'); ylabel('Neuron');
set(gca, 'fontsize', 20, 'linewidth', 3);%, 'xtick', [], 'ytick', []);
set(gcf, 'color', 'white')

%% Plot spontaneous activity samples for each assembly
st = 1480; stp = st + 400;
for ii = 1:num_assemblies
    figure(ii + 2); hold on;
    if ii == 1; cols = get(gca, 'colororder'); end;
    assembly = detected_assemblies{ii};
    for j = 1:numel(assembly)
        y = activity_matrix(assembly(j), st:stp);        
        plot(y, 'Color', cols(ii, :), 'linewidth', 1);
    end
    ylabel('\Delta F/F');
    axis tight; box off;    
    set(gca, 'linewidth', 2);
    set(gcf, 'color', 'white', 'position', [678 495 734 182])
end

%% Plot spatial layout of assemblies
fig_start = ii + 2;
for ii = 1:num_assemblies
    figure(fig_start + ii); hold on;
    assembly = detected_assemblies{ii};
    for jj = 1:N
        if ismember(jj, assembly)
            cl = cols(ii, :);
        else
            cl = 'None';
        end
        plot(cell_coordinates(jj, 1), cell_coordinates(jj, 2), 'o', ...
            'markersize', 20, 'markerfacecolor', cl, 'markeredgecolor', 'black')        
    end
end
