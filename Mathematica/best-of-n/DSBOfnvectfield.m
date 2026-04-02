function [dA] = DSBOfnvectfield(A,ni,QAi,etaAi,eta)
%
    dA = zeros(ni,1);
    for ii = 1:ni
        T1 = A.*(QAi(ii)-QAi);
        T2 = (A*etaAi(ii)-A(ii)*etaAi);

        dA(ii) = A(ii)*(1-eta)*sum(T1)+eta*sum(T2);
    end
end

