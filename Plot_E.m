function E_fig=Plot_E(P,point,itp)

if ischar(point)
    E=P.Efield(point);
    n=1;
else
    E=P.Efield(int32(point-1));
    n=length(point)
end

X=double(E{1})*1e6;
Y=double(E{2})*1e6;
Wlidx=double(E{4})*1e6
X_in=linspace(X(1),X(end),itp*length(X));
Y_in=linspace(Y(1),Y(end),itp*length(Y));
[X0,Y0] = meshgrid(X,Y);
[X1,Y1] = meshgrid(X_in,Y_in);
for i=1:n
    E_f=double(E{3});

    if n==1
        E_f=E_f';
    else
        E_f=E_f(:,:,i)';
    end

    E_in=interp2(X0,Y0,E_f,X1,Y1);

    %%%%%%%%%%%%%%%%%%  plot origin data  %%%%%%%%%%%%%%%
    % figure()
    % image(X,Y,E_f,'CDataMapping','scaled')
    % xlabel('x(um)','FontName','Times New Roman','FontSize',20);
    % ylabel('y(um)','FontName','Times New Roman','FontSize',20);
    % zlabel('z(um)','FontName','Times New Roman','FontSize',20);
    % set(gca,'FontName','Times New Roman','FontSize',15,'LineWidth',1);
    % set(gca,'XDir','normal','YDir','normal');
    % shading interp
    % colorbar
    % colormap jet
    % set(gca,'FontName','Times New Roman','FontSize',15,'LineWidth',1);



    %%%%%%%%%%%%%%%%%%  plot interp data  %%%%%%%%%%%%%%%
    figure()
    image(X_in,Y_in,E_in,'CDataMapping','scaled')
    xlabel('x(um)','FontName','Times New Roman','FontSize',20);
    ylabel('y(um)','FontName','Times New Roman','FontSize',20);
    zlabel('z(um)','FontName','Times New Roman','FontSize',20);
    set(gca,'FontName','Times New Roman','FontSize',15,'LineWidth',1);
    set(gca,'XDir','normal','YDir','normal');
    shading interp
    colorbar
    colormap jet
    tt=strcat('wavelength = ',num2str(Wlidx(i)),'μm')
    title(tt,'FontWeight','bold','FontSize',20,'FontName','Times New Roman');
end
end