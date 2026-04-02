%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% We study the Direct Switch model with generic asocial behaviour
%
% We consider the best-of-n case
%
% We vary eta and we plot the difference between the asymptotic fraction of
% best option and second best option for a given eta with respect to the
% case best-of-2
%
% This is the case best-of-3
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clearvars; close all;

%
% Let us first study the case best-of-2
%
% This is the quality of the opinion, the larger the better
QA1 = 1;   
QA2 = 0.92;
QAibof2 = [QA1;QA2];

%
% etaAi : bias toward option Ai once the asocial information is transmitted
etaA1 = 1/2;%QA1;
etaA2 = 1/2;%QA2;
etaAibof2 = [etaA1;etaA2];

%
% initial conditions
Ai0bof2 = ones(2,1)/2;

% Time
t_ini = 0.0;
t_step = 0.01;
t_final = 50;
nt_every=floor(1);

%
% eta : probability to get (generic) asocial information
% hence
% 1-eta : probability to get social information
eta_min = 0;
eta_max = 0.7;
eta_stp = 81;
eta_vec = linspace(eta_min,eta_max,eta_stp);

%
% A1bofn-A1bof2
% A2bofn-A2bof2
DeltaA1 = zeros(1,eta_stp);
DeltaA2 = zeros(1,eta_stp);

%
% final value of A1 and A2 for a given eta best-of-2
A1tbof2 = zeros(1,eta_stp);
A2tbof2 = zeros(1,eta_stp);

%
% final value of A1 and A2 for a given eta best-of-n
A1tbofn = zeros(1,eta_stp);
A2tbofn = zeros(1,eta_stp);

%
%
bofn = 3;
%
% This is the quality of the opinion of the remaining agents, the larger
% the better, it is measure as percentage of QA2, ie, the second best
% option
pQ = 0.1;
QA3 = pQ*QA2;
QAi = [QAibof2;QA3];

%
% etaAi : bias toward option Ai once the asocial information is transmitted
%etaA3 = QA3;
etaAi = ones(bofn,1)/bofn;%[etaAibof2;etaA3];

%
% initial conditions
Ai0 = ones(bofn,1)/bofn;


for ii = 1:eta_stp
    eta = eta_vec(ii);
    tic
    [Aitbof2,ttoutbof2] = DSBOfnRK4(Ai0bof2,t_ini,t_final,t_step,QAibof2,etaAibof2,eta,nt_every);
    A1tbof2(ii) = Aitbof2(1,end);
    A2tbof2(ii) = Aitbof2(2,end);
    %
    [Ait,ttout] = DSBOfnRK4(Ai0,t_ini,t_final,t_step,QAi,etaAi,eta,nt_every);
    A1tbofn(ii) = Ait(1,end);
    A2tbofn(ii) = Ait(2,end);
    tCPU = toc;
    DeltaA1(ii) = A1tbof2(ii)-A1tbofn(ii);
    DeltaA2(ii) = A2tbof2(ii)-A2tbofn(ii);
end

% figure
% plot(eta_vec,DeltaA1,'b-','LineWidth',2)
% hold on
% plot(eta_vec,DeltaA2,'g-','LineWidth',2)
% xlabel('$\eta$','Interpreter','latex')
% legend('$\Delta_1$','$\Delta_2$','Interpreter','latex','Location','best')
% set(gca,'FontAngle','italic')
% set(gca,'FontName','Times')
% set(gca,'FontSize',24)
% title(['$Q_3=Q_4= $',num2str(pQ),'$Q_2$'],'Interpreter','latex')

figure
plot(eta_vec,A1tbof2-A2tbof2,'b-','LineWidth',2)
hold on
plot(eta_vec,A1tbofn-A2tbofn,'b--','LineWidth',2)
xlabel('$\eta$','Interpreter','latex')
legend('$\delta_{12}^{(2)}$','$\delta_{12}^{(n)}$','Interpreter','latex','Location','best')
set(gca,'FontAngle','italic')
set(gca,'FontName','Times')
set(gca,'FontSize',24)
title(['$Q_3=Q_4= $',num2str(pQ),'$Q_2$'],'Interpreter','latex')

% figure
% plot(eta_vec,A1tbof2,'b--','LineWidth',2)
% hold on
% plot(eta_vec,A1tbofn,'b-','LineWidth',2)
% plot(eta_vec,A2tbof2,'g--','LineWidth',2)
% plot(eta_vec,A2tbofn,'g-','LineWidth',2)
% xlabel('$\eta$','Interpreter','latex')
% ylabel('$A^{bof2}_j(t_{fin})$ and $A_j^{bofn}(t_{fin})$','Interpreter','latex')
% set(gca,'FontAngle','italic')
% set(gca,'FontName','Times')
% set(gca,'FontSize',24)

