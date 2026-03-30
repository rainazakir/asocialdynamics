%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% We study the Cross Inhibition (T1) model with generic asocial behaviour
%
% We consider the best-of-n case
%
% We vary eta and we plot the difference between the asymptotic fraction of
% best option and second best option for a given eta with respect to the
% case best-of-2
%
% This is the case best-of-5
%
% This file realizes the same computation than XrossInhibBOfn_000.m but for
% several initial conditions
%
% We determine the equilibira by root finding methods
% This is similar to XrossInhibBOfn_FindEq_002a.m but the roots are
% computed by using a symbolic solver. In this way we solve some numerical
% problems that induce some "spurious" roots
%
% It computes the stability of the equilibrium solution by computing the
% eigenvalues of the Jacobian matrix
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clearvars; close all;

%
% maximal number of possible roots
nmax = 35;
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
% eta : probability to get (generic) asocial information
% hence
% 1-eta : probability to get social information
eta_min = 0.01;
eta_max = 0.7;
eta_stp = 151;
eta_vec = linspace(eta_min,eta_max,eta_stp);

%
% A1bofn-A1bof2
% A2bofn-A2bof2
DeltaA1 = zeros(nmax,eta_stp);
DeltaA2 = zeros(nmax,eta_stp);

%
% A1bof2-A2bof2
% A1bofn-A2bofn
deltaA12_bof2 = zeros(nmax,eta_stp);
deltaA12_bofn = zeros(nmax,eta_stp);

%
% final value of A1 and A2 for a given eta best-of-2
A1tbof2 = zeros(nmax,eta_stp);
A2tbof2 = zeros(nmax,eta_stp);

%
% final value of A1 and A2 for a given eta best-of-n
A1tbofn = zeros(nmax,eta_stp);
A2tbofn = zeros(nmax,eta_stp);

%
%
bofn = 5;
%
% This is the quality of the opinion of the remaining agents, the larger
% the better, it is measure as percentage of QA2, ie, the second best
% option
pQ = 1.00;
QA3 = pQ*QA2;
QA4 = pQ*QA2;
QA5 = pQ*QA2;
QAi = [QAibof2;QA3;QA4;QA5];

%
% etaAi : bias toward option Ai once the asocial information is transmitted
etaAi = ones(bofn,1)/bofn;

%
% there will not be more than nmax roots/equilibria
stability_bof2 = nan(nmax,eta_stp);
stability_bofn = nan(nmax,eta_stp);

tic
for ii = 1:eta_stp
    eta = eta_vec(ii);

    syms x y
    eq1 = x*(1-eta)*(QAibof2(1)*(1-x-y)-QAibof2(2)*y)+eta*((1-x-y)*etaAibof2(1)-x*etaAibof2(2)) == 0;
    eq2 = y*(1-eta)*(QAibof2(2)*(1-x-y)-QAibof2(1)*x)+eta*((1-x-y)*etaAibof2(2)-y*etaAibof2(1)) == 0;
    eq3 = x > 0;
    eq4 = x < 1;
    eq5 = y > 0;
    eq6 = y < 1;
    eqns = [eq1,eq2,eq3,eq4,eq5,eq6];
    S = solve(eqns,[x,y]);

    % Jacobian
    J_bof2 = @(x,y) [(1-eta)*(QAibof2(1)*(1-x-y)-QAibof2(2)*y)-x*(1-eta)*QAibof2(1)-eta*(etaAibof2(1)+etaAibof2(2)),-x*(1-eta)*(QAibof2(1)+QAibof2(2))-eta*etaAibof2(1);-y*(1-eta)*(QAibof2(2)+QAibof2(1))-eta*etaAibof2(2),(1-eta)*(QAibof2(2)*(1-x-y)-QAibof2(1)*x)-y*(1-eta)*QAibof2(2)-eta*(etaAibof2(2)+etaAibof2(1))];
    %
    %
    ns = length(S.x);

    A1tbof2(:,ii) = [S.x;nan(nmax-ns,1)];
    A2tbof2(:,ii) = [S.y;nan(nmax-ns,1)];
    %
    deltaA12_bof2(:,ii) = A1tbof2(:,ii)-A2tbof2(:,ii);
    %
    % determine the stability of the solution
    for jj = 1:ns
        J_bof2_val = J_bof2(A1tbof2(jj,ii),A2tbof2(jj,ii));
        lambda_bof2 = eig(J_bof2_val);
        if (max(real(lambda_bof2))>0)
            stability_bof2(jj,ii) = 1;
        else
            stability_bof2(jj,ii) = 0;
        end
    end
    %
    % now the best-of-n case
    syms x1 x2 x3 x4 x5
    eq1_bofn = x1*(1-eta)*(QAi(1)*(1-x1-x2-x3-x4-x5)-QAi(2)*x2-QAi(3)*x3-QAi(4)*x4-QAi(5)*x5)+...
        eta*((1-x1-x2-x3-x4-x5)*etaAi(1)-x1*(etaAi(2)+etaAi(3)+etaAi(4)+etaAi(5))) == 0;
    eq2_bofn = x2*(1-eta)*(QAi(2)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(3)*x3-QAi(4)*x4-QAi(5)*x5)+...
        eta*((1-x1-x2-x3-x4-x5)*etaAi(2)-x2*(etaAi(1)+etaAi(3)+etaAi(4)+etaAi(5))) == 0;
    eq3_bofn = x3*(1-eta)*(QAi(3)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(2)*x2-QAi(4)*x4-QAi(5)*x5)+...
        eta*((1-x1-x2-x3-x4-x5)*etaAi(3)-x3*(etaAi(1)+etaAi(2)+etaAi(4)+etaAi(5))) == 0;
    eq4_bofn = x4*(1-eta)*(QAi(4)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(2)*x2-QAi(3)*x3-QAi(5)*x5)+...
        eta*((1-x1-x2-x3-x4-x5)*etaAi(4)-x4*(etaAi(1)+etaAi(2)+etaAi(3)+etaAi(5))) == 0;
    eq5_bofn = x5*(1-eta)*(QAi(5)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(2)*x2-QAi(3)*x3-QAi(4)*x4)+...
        eta*((1-x1-x2-x3-x4-x5)*etaAi(5)-x5*(etaAi(1)+etaAi(2)+etaAi(3)+etaAi(4))) == 0;
    eq6_bofn = x1 > 0;
    eq7_bofn = x1 < 1;
    eq8_bofn = x2 > 0;
    eq9_bofn = x2 < 1;
    eq10_bofn = x3 > 0;
    eq11_bofn = x3 < 1;
    eq12_bofn = x4 > 0;
    eq13_bofn = x4 < 1;
    eq14_bofn = x5 > 0;
    eq15_bofn = x5 < 1;
    
    eqns_bofn = [eq1_bofn,eq2_bofn,eq3_bofn,eq4_bofn,eq5_bofn,eq6_bofn,eq7_bofn,eq8_bofn,eq9_bofn,eq10_bofn,eq11_bofn,eq12_bofn,eq13_bofn,eq14_bofn,eq15_bofn];
    S_bofn = solve(eqns_bofn,[x1,x2,x3,x4,x5]);
    %
    % Jacobian
    J_bofn = @(x1,x2,x3,x4,x5) ...
    [(1-eta)*(QAi(1)*(1-x1-x2-x3-x4-x5)-QAi(2)*x2-QAi(3)*x3-QAi(4)*x4-QAi(5)*x5)-x1*(1-eta)*QAi(1)-eta*sum(etaAi),...
    -x1*(1-eta)*(QAi(1)+QAi(2))-eta*etaAi(1),...
    -x1*(1-eta)*(QAi(1)+QAi(3))-eta*etaAi(1),...
    -x1*(1-eta)*(QAi(1)+QAi(4))-eta*etaAi(1),...
    -x1*(1-eta)*(QAi(1)+QAi(5))-eta*etaAi(1);...
    -x2*(1-eta)*(QAi(2)+QAi(1))-eta*etaAi(2),...
    (1-eta)*(QAi(2)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(3)*x3-QAi(4)*x4-QAi(5)*x5)-x2*(1-eta)*QAi(2)-eta*sum(etaAi),...
    -x2*(1-eta)*(QAi(2)+QAi(3))-eta*etaAi(2),...
    -x2*(1-eta)*(QAi(2)+QAi(4))-eta*etaAi(2),...
    -x2*(1-eta)*(QAi(2)+QAi(5))-eta*etaAi(2);...
    -x3*(1-eta)*(QAi(3)+QAi(1))-eta*etaAi(3),...
    -x3*(1-eta)*(QAi(3)+QAi(2))-eta*etaAi(3),...
    (1-eta)*(QAi(3)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(2)*x2-QAi(4)*x4-QAi(5)*x5)-x3*(1-eta)*QAi(3)-eta*sum(etaAi),...
    -x3*(1-eta)*(QAi(3)+QAi(4))-eta*etaAi(3),...
    -x3*(1-eta)*(QAi(3)+QAi(5))-eta*etaAi(3);...
    -x4*(1-eta)*(QAi(4)+QAi(1))-eta*etaAi(4),...
    -x4*(1-eta)*(QAi(4)+QAi(2))-eta*etaAi(4),...
    -x4*(1-eta)*(QAi(4)+QAi(3))-eta*etaAi(4),...
    (1-eta)*(QAi(4)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(2)*x2-QAi(3)*x3-QAi(5)*x5)-x4*(1-eta)*QAi(4)-eta*sum(etaAi),...
    -x4*(1-eta)*(QAi(4)+QAi(5))-eta*etaAi(4);...
    -x5*(1-eta)*(QAi(5)+QAi(1))-eta*etaAi(5),...
    -x5*(1-eta)*(QAi(5)+QAi(2))-eta*etaAi(5),...
    -x5*(1-eta)*(QAi(5)+QAi(3))-eta*etaAi(5),...
    -x5*(1-eta)*(QAi(5)+QAi(4))-eta*etaAi(5),...
    (1-eta)*(QAi(5)*(1-x1-x2-x3-x4-x5)-QAi(1)*x1-QAi(2)*x2-QAi(3)*x3-QAi(4)*x4)-x5*(1-eta)*QAi(5)-eta*sum(etaAi)];

    ns_bofn = length(S_bofn.x1);
    A1tbofn(:,ii) = [S_bofn.x1;nan(nmax-ns_bofn,1)];
    A2tbofn(:,ii) = [S_bofn.x2;nan(nmax-ns_bofn,1)];
    %
    deltaA12_bofn(:,ii) = A1tbofn(:,ii)-A2tbofn(:,ii);
    %
    % determine the stability of the solution
    for jj = 1:ns_bofn
        J_bofn_val = vpa(J_bofn(S_bofn.x1(jj),S_bofn.x2(jj),S_bofn.x3(jj),S_bofn.x4(jj),S_bofn.x5(jj)));
        lambda_bofn_tmp = eig(J_bofn_val);
        if (max(real(lambda_bofn_tmp))>0)
            stability_bofn(jj,ii) = 1;
        else
            stability_bofn(jj,ii) = 0;
        end
    end
end
tCPU = toc;


figure
plot(eta_vec,A1tbof2,'bo','MarkerFaceColor','b')
hold on
plot(eta_vec,A2tbof2,'bo')
xlabel('$\eta$','Interpreter','latex')
ylabel('$A^2_{1}$, $A^2_{2}$','Interpreter','latex')
set(gca,'FontAngle','italic')
set(gca,'FontName','Times')
set(gca,'FontSize',24)

% figure
% plot(eta_vec,A1tbofn,'go','MarkerFaceColor','g')
% hold on
% plot(eta_vec,A2tbofn,'go')
% xlabel('$\eta$','Interpreter','latex')
% ylabel('$A^n_{1}$, $A^n_{2}$','Interpreter','latex')
% set(gca,'FontAngle','italic')
% set(gca,'FontName','Times')
% set(gca,'FontSize',24)
% title(['$Q_3=Q_4=Q_5= $',num2str(pQ),'$Q_2$'],'Interpreter','latex')


figure
plot(eta_vec,deltaA12_bof2,'bo','MarkerFaceColor','b')
hold on
plot(eta_vec,deltaA12_bofn,'go','MarkerFaceColor','g')
xlabel('$\eta$','Interpreter','latex')
ylabel('$\delta_{12}^{(2)}\;\delta_{12}^{(n)}$','Interpreter','latex')
set(gca,'FontAngle','italic')
set(gca,'FontName','Times')
set(gca,'FontSize',24)
title(['$Q_3=Q_4=Q_5= $',num2str(pQ),'$Q_2$'],'Interpreter','latex')
%legend('$\delta_{12}^{(2)}$','$\delta_{12}^{(n)}$','Interpreter','latex')

figure
hold on
for ii = 1:eta_stp
    for jj = 1:nmax
        if (stability_bof2(jj,ii) == 1)
            color_bof2 = 'r';
        elseif (stability_bof2(jj,ii) == 0)
            color_bof2 = 'g';
        else
            color_bof2 = 'k';
        end
        plot(eta_vec(ii),deltaA12_bof2(jj,ii),'o','MarkerEdgeColor',color_bof2,'MarkerFaceColor',color_bof2)
        if (stability_bofn(jj,ii) == 1)
            color_bofn = 'r';
        elseif (stability_bofn(jj,ii) == 0)
            color_bofn = 'g';
        else
            color_bofn = 'k';
        end
        plot(eta_vec(ii),deltaA12_bofn(jj,ii),'o','MarkerEdgeColor',color_bofn)        
    end
end
xlabel('$\eta$','Interpreter','latex')
ylabel('$\delta_{12}^{(2)}$, $\delta_{12}^{(n)}$','Interpreter','latex')
set(gca,'FontAngle','italic')
set(gca,'FontName','Times')
set(gca,'FontSize',24)
title(['$Q_3=Q_4=Q_5= $',num2str(pQ),'$Q_2$'],'Interpreter','latex')

figure
plot(eta_vec,deltaA12_bof2,'bo','MarkerFaceColor','b')
xlabel('$\eta$','Interpreter','latex')
ylabel('$\delta_{12}^{(2)}$','Interpreter','latex')
set(gca,'FontAngle','italic')
set(gca,'FontName','Times')
set(gca,'FontSize',24)


figure
plot(eta_vec,deltaA12_bofn,'go','MarkerFaceColor','g')
xlabel('$\eta$','Interpreter','latex')
ylabel('$\delta_{12}^{(n)}$','Interpreter','latex')
set(gca,'FontAngle','italic')
set(gca,'FontName','Times')
set(gca,'FontSize',24)
title(['$Q_3=Q_4=Q_5= $',num2str(pQ),'$Q_2$'],'Interpreter','latex')


save('XrossInhibBOfn_FindEq_002a_bisp1_00.mat','-mat')
