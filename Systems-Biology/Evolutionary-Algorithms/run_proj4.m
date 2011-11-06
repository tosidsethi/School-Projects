%% Run simulation with the Nominal parameters for Goldbeter's fly clock.

vs = 0.76;
vm = 0.65;
Km = 0.5;
ks = 0.38;
vd = 0.95;
k1 = 1.9;
k2 = 1.3;
KI = 1;
Kd = 0.2;
n = 4;
K1 = 2;
K2 = 2;
K3 = 2;
K4 = 2;
V1 = 3.2;
V2 = 1.58;
V3 = 5;
V4 = 2.5;

params = [vs, vm, Km, ks, vd, k1, k2, KI, Kd, n, ...
    K1, K2, K3, K4, V1, V2, V3, V4];
% yinit = [1,1,1,1,1];
% [t,y] = ode15s(@gol95,0:0.1:100,yinit,[],params);
% figure;
% plot(t,y);
% title('Published Parameters');

% [per, sdper] = getPeriod(t,y);
% disp(['Period is ', num2str(per), ' +/- ', num2str(sdper)]);

%% Test the cost function on the nominal params
vs = 0.76;
vm = 0.65;
Km = 0.5;
ks = 0.38;
vd = 0.95;
k1 = 1.9;
k2 = 1.3;
KI = 1;
Kd = 0.2;
n = 4;
K1 = 2;
K2 = 2;
K3 = 2;
K4 = 2;
V1 = 3.2;
V2 = 1.58;
V3 = 5;
V4 = 2.5;

params = [vs, vm, Km, ks, vd, k1, k2, KI, Kd, n, ...
    K1, K2, K3, K4, V1, V2, V3, V4];

drawFigure = true;
cost = gol95CostFunction2(params,drawFigure);
disp(['Cost of published parameters is ', num2str(cost)]);

%% Optimize for parameters using an ES
% NOTE: THIS IS NEW CODE!
lb = zeros();
ub = zeros();
lb(1) = 0;   ub(1) = 1;% vs = 0.76;
lb(2) = 0;   ub(2) = 1;% vm = 0.65;
lb(3) = .1;  ub(3) = 1;% Km = 0.5;
lb(4) = 0;   ub(4) = 1;% ks = 0.38;
lb(5) = 0;   ub(5) = 1;% vd = 0.95;
lb(6) = 0;   ub(6) = 2;% k1 = 1.9;
lb(7) = 0;   ub(7) = 2;% k2 = 1.3;
lb(8) = 1;   ub(8) = 1;% KI = 1;
lb(9) = 0.1; ub(9) = 1;% Kd = 0.2;
lb(10) = 4;  ub(10) = 4;% n = 4;
lb(11) = 0.5;  ub(11) = 2.5;% K1 = 2;
lb(12) = 0.5;  ub(12) = 2.5;% K2 = 2;
lb(13) = 0.5;  ub(13) = 2.5;% K3 = 2;
lb(14) = 0.5;  ub(14) = 2.5;% K4 = 2;
lb(15) = 0;  ub(15) = 5;% V1 = 3.2;
lb(16) = 0;  ub(16) = 5;% V2 = 1.58;
lb(17) = 0;  ub(17) = 5;% V3 = 5;
lb(18) = 0;  ub(18) = 5;% V4 = 2.5;


filenum = 1001;
cost_fcn = @gol95CostFunction2;
settings = gaset(filenum,'numParents',8,'numChildren',40,...
     'selection','truncation','eliteCount',0);
[params, cost] = proj4GA(cost_fcn, lb, ub, settings);
disp(['Lowest cost from this run is ', num2str(cost)]);
cost_fcn(params,true)

% Plot the cost function as it improves
% 
figure;
cm = jet(settings.numGenerations); % blue to red
for g = 1 : settings.numGenerations,
    fn = ['ga' int2str(settings.filenum) 'generation' int2str(g) '.mat'];
    f  = load(fn);
    plot(1:length(f.Gcost),f.Gcost,'*','Color',cm(g,:));
    hold on;
end;
xlabel('Child');
ylabel('Cost');

% Plot the normalized parameter values of the last generation
% The normalized will be 1 if the parameter is at the upper bound
% and it will be 0 if it is as its lower bound.
% For parameters with the same lower and upper bounds, just use
% the value 1.
% The fittest (lowest cost) child will be red and the 
% least fit (highest cost) child will be blue
g  = settings.numGenerations;
fn = ['ga' int2str(settings.filenum) 'generation' int2str(g) '.mat'];
f  = load(fn);
figure;
cm = flipud(jet(settings.numChildren)); % red to blue
for i = 1 : settings.numChildren
    % normalize it, one parameter at a time
    % (this means I handle parameter j for all kids in one
    % fell swoop)
    normG = f.G;
    for j = 1 : size(f.G, 2), % j is the param num
        if ub(j)-lb(j) > 1e-16
            normG(:,j) = (f.G(:,j)-lb(j))./(ub(j)-lb(j));
        else
            normG(:,j) = ones(size(f.G(:,j)));
        end;
    end;
    plot(1:size(normG,2),normG(i,:),'.-','Color',cm(i,:));
    hold on;
end;
xlabel('Parameter');
ylabel('Normalized Value');

%% Optimize using a GA with linear ranking selection

lb = zeros();
ub = zeros();
lb(1) = 0;     ub(1) = 1;% vs = 0.76;
lb(2) = 0;     ub(2) = 1;% vm = 0.65;
lb(3) = .1;    ub(3) = 1;% Km = 0.5;
lb(4) = 0;     ub(4) = 1;% ks = 0.38;
lb(5) = 0;     ub(5) = 1;% vd = 0.95;
lb(6) = 0;     ub(6) = 2;% k1 = 1.9;
lb(7) = 0;     ub(7) = 2;% k2 = 1.3;
lb(8) = 1;     ub(8) = 1;% KI = 1;
lb(9) = 0.1;   ub(9) = 1;% Kd = 0.2;
lb(10) = 4;    ub(10) = 4;% n = 4;
lb(11) = 0.5;  ub(11) = 2.5;% K1 = 2;
lb(12) = 0.5;  ub(12) = 2.5;% K2 = 2;
lb(13) = 0.5;  ub(13) = 2.5;% K3 = 2;
lb(14) = 0.5;  ub(14) = 2.5;% K4 = 2;
lb(15) = 0;    ub(15) = 5;% V1 = 3.2;
lb(16) = 0;    ub(16) = 5;% V2 = 1.58;
lb(17) = 0;    ub(17) = 5;% V3 = 5;
lb(18) = 0;    ub(18) = 5;% V4 = 2.5;

filenum = 4001;
cost_fcn = @gol95CostFunction2;
settings = gaset(filenum,'numParents',40,'numChildren',40,...
    'selection','tournament','eliteCount',1);
[params, cost] = proj4GA(cost_fcn, lb, ub, settings);
disp(['Lowest cost from this run is ', num2str(cost)]);
cost_fcn(params,true)

% Plot the cost function as it improves
% 
figure;
cm = jet(settings.numGenerations); % blue to red
for g = 1 : settings.numGenerations,
    fn = ['ga' int2str(settings.filenum) 'generation' int2str(g) '.mat'];
    f  = load(fn);
    plot(1:length(f.Gcost),f.Gcost,'*','Color',cm(g,:));
    hold on;
end;
xlabel('Child');
ylabel('Cost');

% Plot the normalized parameter values of the last generation
% The normalized will be 1 if the parameter is at the upper bound
% and it will be 0 if it is as its lower bound.
% For parameters with the same lower and upper bounds, just use
% the value 1.
% The fittest (lowest cost) child will be red and the 
% least fit (highest cost) child will be blue
g  = settings.numGenerations;
fn = ['ga' int2str(settings.filenum) 'generation' int2str(g) '.mat'];
f  = load(fn);
figure;
cm = flipud(jet(settings.numChildren)); % red to blue
for i = 1 : settings.numChildren
    % normalize it, one parameter at a time
    % (this means I handle parameter j for all kids in one
    % fell swoop)
    normG = f.G;
    for j = 1 : size(f.G, 2), % j is the param num
        if ub(j)-lb(j) > 1e-16
            normG(:,j) = (f.G(:,j)-lb(j))./(ub(j)-lb(j));
        else
            normG(:,j) = ones(size(f.G(:,j)));
        end;
    end;
    plot(1:size(normG,2),normG(i,:),'.-','Color',cm(i,:));
    hold on;
end;
xlabel('Parameter');
ylabel('Normalized Value');


