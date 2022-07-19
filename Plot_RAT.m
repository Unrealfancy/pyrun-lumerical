function [R,T,A]=plot_RAT(P)
    figure(1)
    RAT=P.RAT();
    Wl=double(RAT{1})*1e6;
    R=double(RAT{2});
    T=double(RAT{3});
    A=double(RAT{4});
    Y_matrix=[R;A;T];
    hold on
%     plot(Wl,R,Wl,T,Wl,A,'LineWidth',2)
    plot(Wl,A,'LineWidth',2)
    xlabel('Wavelength(μm)','FontWeight','bold','FontSize',20,...
    'FontName','Times New Roman');
    set(gca,'FontName','Times New Roman','FontSize',15,'LineWidth',1.5);
    title('R A T','FontWeight','bold','FontSize',20,'FontName','Times New Roman');
%     legend("Reflection","Transmission","Absorption")
end