function plot_PSA(returndata)
returndata=cell(returndata);
Gbest=double(returndata{1});
Gbestpop=cell(returndata{2});
wl=double(returndata{3})*1e6;
R=cell(returndata{4});
n=[length(R),length(R{1})];
figure()
for i=1:length(R)
    Gbestpop{i}=double(Gbestpop{i});
    R{i}=cell(R{i});
    for j=1:length(R{1})
        R{i}{j}=double(R{i}{j});
        subplot(n(1),n(2),(i-1)*n(2)+j)
        plot(wl,R{i}{j},'LineWidth',2,'color',[i/length(R) 0.2 1-i/length(R)])
        title(strcat('iteration=',num2str(i-1),',pop=',num2str(j)),'FontWeight','bold','FontSize',15,...
            'FontName','Times New Roman')
        xlabel('Wavelength(μm)','FontWeight','bold','FontSize',10,...
            'FontName','Times New Roman');
        ylabel('R','FontWeight','bold','FontSize',10,...
            'FontName','Times New Roman');
        set(gca,'FontName','Times New Roman','FontSize',12,'LineWidth',1.5);
    end
end
figure()
plot(0:length(Gbest)-1,Gbest,'LineWidth',2)
title('iteration-FOM','FontWeight','bold','FontSize',20,...
    'FontName','Times New Roman')
xlabel('iteration times','FontWeight','bold','FontSize',20,...
    'FontName','Times New Roman');
ylabel('FOM','FontWeight','bold','FontSize',20,...
    'FontName','Times New Roman');
set(gca,'FontName','Times New Roman','FontSize',15,'LineWidth',1.5);
