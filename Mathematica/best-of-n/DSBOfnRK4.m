function [Atout,ttout] = DSBOfnRK4(Ai0,t_ini,t_final,t_step,QAi,etaAi,eta,ntout)
%

nt = floor((t_final-t_ini)/t_step);
ni = length(Ai0);
Ait = zeros(ni,nt);
ttime = zeros(1,nt);

% initialization
tt = t_ini;
Ai_old = Ai0;

jj = 1;

Ait(:,jj) = Ai_old;

ttime(jj) = tt;

while (tt<=t_final)
    % Runge Kutta 4
    [Ai_K1] = DSBOfnvectfield(Ai_old,ni,QAi,etaAi,eta);
    [Ai_K2] = DSBOfnvectfield(Ai_old+(t_step/2).*Ai_K1,ni,QAi,etaAi,eta);
    [Ai_K3] = DSBOfnvectfield(Ai_old+(t_step/2).*Ai_K2,ni,QAi,etaAi,eta);
    [Ai_K4] = DSBOfnvectfield(Ai_old+t_step.*Ai_K3,ni,QAi,etaAi,eta);

    Ai_new = Ai_old + (t_step/6).*(Ai_K1+2.*Ai_K2+2.*Ai_K3+Ai_K4);
    %
    tt = tt + t_step;

    Ai_old = Ai_new;
    
    jj = jj+1;
    Ait(:,jj) = Ai_old;
    ttime(jj) = tt;

end

idx = 1:ntout:size(ttime,2);
ttout = ttime(idx);
Atout = Ait(:,idx);

end
