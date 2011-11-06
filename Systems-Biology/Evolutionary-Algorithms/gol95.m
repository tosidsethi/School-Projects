function dydt = gol95(t,y,params)

vs = params(1);
vm = params(2);
Km = params(3);
ks = params(4);
vd = params(5);
k1 = params(6);
k2 = params(7);
KI = params(8);
Kd = params(9);
n  = params(10);
K1 = params(11);
K2 = params(12);
K3 = params(13);
K4 = params(14);
V1 = params(15);
V2 = params(16);
V3 = params(17);
V4 = params(18);

M = y(1);
P0 = y(2);
P1 = y(3);
P2 = y(4);
PN = y(5);
      
dydt(1,1) = vs*KI^n/(KI^n+PN^n) - vm*M/(Km + M);
dydt(2,1) = ks*M - V1*P0/(K1+P0) + V2*P1/(K3+P1);
dydt(3,1) = V1*P0/(K1+P0) - V2*P1/(K2+P1) - V3*P1/(K3+P1) + V4*P2/(K4+P2);
dydt(4,1) = V3*P1/(K3+P1) - V4*P2/(K4+P2) - k1*P2 + k2*PN - vd*P2/(Kd+P2);
dydt(5,1) = k1*P2 - k2*PN;
