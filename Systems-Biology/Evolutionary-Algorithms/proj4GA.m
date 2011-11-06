function [params, cost] = proj4GA(cost_fcn, lb, ub, settings)

% Seed the random number generator so that it will generate
% a new pseudo-random number sequence each time the algorithm
% is run.
rand('state',sum(100*clock));

% -------
% NEW CODE (lines l1:l5)
% adds support for file i/o. these lines won't recreate
% a file that already exists.
% -------
% Create the parents
fn = ['ga' int2str(settings.filenum) 'generation' int2str(0) '.mat']; %l1
if ~exist(fn),%l2
    P = zeros(settings.numParents,length(lb));
    Pcost = zeros(settings.numParents,1);
    for i = 1 : settings.numParents,
        [P(i,:) Pcost(i)] = generateParent(cost_fcn, lb, ub);
    end;
    save(fn,'P','Pcost','lb','ub','settings'); % l3
end; %l4
f = load(fn); %l5
P = f.P;
Pcost = f.Pcost;

% ---------
% REMOVED PLOTTING ODE
% ---------

% Loop over the generations
for g = 1 : settings.numGenerations,
    % -------
    % NEW CODE (lines l6:l10)
    % adds support for file i/o. these lines won't recreate
    % a file that already exists.
    % -------
    fn = ['ga' int2str(settings.filenum) 'generation' int2str(g) '.mat']; % l6
    if ~exist(fn,'file') % l7
        G     = zeros(settings.numChildren, length(lb));
        Gcost = zeros(settings.numChildren,1);
        G(1:settings.eliteCount,:) = P(1:settings.eliteCount,:);
        Gcost(1:settings.eliteCount) = Pcost(1:settings.eliteCount);
        for c = settings.eliteCount+1 : settings.numChildren
            % Create a child from the previous generation
            [G(c,:) Gcost(c)] = generateChild(cost_fcn, P, Pcost, lb, ub, settings);
        end;
        % Sort the children by cost from least to greatest
        [Gcost idx] = sort(Gcost);
        G           = G(idx,:);

        % Determine the parents of the next generation
        P     = G(1:settings.numParents,:);
        Pcost = Gcost(1:settings.numParents);
        save(fn,'G','Gcost');
    end; % l9
    load(fn); % l10
end;
% best params
params = G(1,:);
cost   = Gcost(1);

% Randomly generate a parent (params) and report its cost
function [params, cost] = generateParent(cost_fcn, lb, ub)
params = lb;
cost   = inf;
for i = 1 : 1000,
    params = lb + rand(size(lb)) .* (ub-lb);
    cost   = cost_fcn(params);
    if isfinite(cost)
        return;
    end;
end;

% Generate a child from two of the list of Parents P where
% P is numParents by numParams
function [params, cost] = generateChild(cost_fcn, P, Pcost, lb, ub, settings)
params = lb;
cost   = inf;
for i = 1 : 1000,
    % Select two parents P1 and P2
    if strcmp(settings.selection,'truncation')
        idx1 = round(0.5 + rand*(settings.numParents-0.5));
        idx2 = round(0.5 + rand*(settings.numParents-0.5));
        P1   = P(idx1,:);
        P2   = P(idx2,:);
    elseif strcmp(settings.selection,'linearRanking')
        N = settings.numParents;
        % 2/N is probability of best parent being chosen
        % 0/N is the probability of the worst parent being chosen
        % rank = N for best
        % rank = 1 for worst
        ranks = N:-1:1;
        % probability of each parent being chosen
        probs = 1/N .* (2*(ranks-1)./(N-1));
        % Store the accumulated probilities
        cprobs = cumsum(probs);
        % For each parent, randomly choose a number between 0 and 1 and 
        % find where it falls on the accumulated ranking list.
        idx1 = find(cprobs > rand, 1, 'first');
        idx2 = find(cprobs > rand, 1, 'first');
        P1   = P(idx1,:);
        P2   = P(idx2,:);            
    elseif strcmp(settings.selection,'exponentialRanking')
        N = settings.numParents;
        c = settings.exponentialRankingBase;
        % rank = N for best
        % rank = 1 for worst
        ranks = N:-1:1;
        % probability of each parent being chosen
        probs = (c-1)/(c^N-1) .* c.^(N-ranks);
        % Store the accumulated probilities
        cprobs = cumsum(probs);
        % For each parent, randomly choose a number between 0 and 1 and 
        % find where it falls on the accumulated ranking list.
        idx1 = find(cprobs > rand, 1, 'first');
        idx2 = find(cprobs > rand, 1, 'first');
        P1   = P(idx1,:);
        P2   = P(idx2,:);            
    elseif strcmp(settings.selection,'proportional')
        ratios = max(Pcost) ./ Pcost;
        % probability of each parent being chosen
        probs = ratios ./ sum(ratios);
        % Store the accumulated probilities
        cprobs = cumsum(probs);
        % For each parent, randomly choose a number between 0 and 1 and 
        % find where it falls on the accumulated ranking list.
        idx1 = find(cprobs > rand, 1, 'first');
        idx2 = find(cprobs > rand, 1, 'first');
        P1   = P(idx1,:);
        P2   = P(idx2,:);       
    elseif strcmp(settings.selection,'tournament')
        N = settings.numParents;     
        % this only works for P1 and P2 right now
        % (because we are only returning P1 and P2 everywhere else)        
        for j = 1 : settings.tournamentSize,            
            % choose two potential parents randomly
            idx1 = round(0.5 + rand*(N-0.5));
            idx2 = round(0.5 + rand*(N-0.5));

            % find out their costs
            Pc1   = Pcost(idx1,:);
            Pc2   = Pcost(idx2,:);  

            % whoever has the lowest cost gets to be a parent!
            if (Pc1 < Pc2)
                if (j == 1)
                    P1 = P(idx1,:);            
                else
                    P2 = P(idx1,:);
                end;
            else
                if (j == 1)
                    P1 = P(idx2,:);
                else
                    P2 = P(idx2,:);
                end;
            end;
        end;
        % end tournament selection
    else
        disp(['Unknown selection operator : ',settings.selection]);
        return;
    end;
    % Create child using crossover
    if strcmp(settings.crossover,'uniform')
        for j = 1 : length(params),
            if rand < 0.5
                params(j) = P1(j);
            else
                params(j) = P2(j);
            end;
        end;
    else
        disp(['Unknown crossover operator : ',settings.crossover]);
        return;
    end;
    % Mutate
    params = params + randn(size(params)).*settings.mutation.*params;
    % Make sure child is in bounds
    params = max(params,lb);
    params = min(params,ub);
    % evaluate cost
    cost   = cost_fcn(params);
    if isfinite(cost)
        return;
    end;
end;
