function cost = gol95CostFunction2(params,drawFigure)
cost = inf;

if nargin < 2
    drawFigure = false;
end;

dt = 0.1;
days = 10;

% First, run it for 10 days to get it to the limit cycle (if it is
% periodic)
[t1,y1] = ode15s(@gol95,0:dt:days*24,zeros(5,1),[],params);
if abs(t1(end)-dt) > days*24,
    % The simulation didn't run.
    return;
end;

% Now, run it on the limit cycle
[t2, y2] = ode15s(@gol95,0:dt:days*24,y1(end,:),[],params);

% Determine the period
[per, sdper] = getPeriod(t2,y2);

% Determine the amp (peak to trough difference) of each state
amp = max(y2,[],1) - min(y2,[],1);


if drawFigure;
    figure;
    plot(t2,y2);
    xlabel('Time (h)');
    ylabel('Concentration (nM)');
end;
disp([amp per sdper]);

% The period should be 23.6, there should be very little
% period-to-period variation, and the amplitudes should be
% between 0.1 and 10.
ideal_per = 23.6;
log10amp = log(amp)./log(10);
idxTooSmall = find(log10amp < -1);
costTooSmall = 0;
for i = 1 : length(idxTooSmall)
    costTooSmall = costTooSmall+abs(-1-log10amp(idxTooSmall(i)))^2;
end;
idxTooBig   = find(log10amp > 2);
costTooBig  = 0;
for i = 1 : length(idxTooBig)
    costTooBig = costTooBig+abs(1-log10amp(idxTooBig(i)))^2;
end;
cost = sqrt( ((per-ideal_per)/ideal_per)^2 + ...
             sdper + costTooSmall + costTooBig);
