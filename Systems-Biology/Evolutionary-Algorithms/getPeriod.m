% Given a set of time steps and the values of y at those timesteps,
% determine the period of oscillation (if there is any oscillation)
% Returns the period and the standard deviation of the period
% (measured using the period of each cycle as an individual data point)
% function [period, sdperiod] = getPeriod(t,y)
function [period, sdperiod] = getPeriod(t,y)

[maxval, maxidx] = max(max(abs(y),[],1));
x = y(:,maxidx);

xmean = mean(x);
index = find(x>xmean);
dindex = diff(index);
dindex = find(dindex>1);
index = index(dindex);
tlist = [];
for k = 1:length(index)
    time = t(index(k):index(k)+1);
    tlist(k) = interp1(x(index(k):index(k)+1),time,xmean,'spline');
end
period = mean(diff(tlist));
sdperiod = sqrt(var(diff(tlist)));



