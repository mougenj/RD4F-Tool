clear all
close all
nfig=0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fort40=load("totaux.txt");
TOTtemps=fort40(:,1);
TOTtemp=fort40(:,2);
TOTtotal=fort40(:,3);

nfig=nfig+1;
figure(nfig)
hold on
plot(TOTtemps,TOTtotal,'b');
hold on
xlabel("Temps (s)");
ylabel("Concentration (D/m2)");
print -dpng totaux.png

max(TOTtotal)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fort50=load("TDS.txt");
TDStemp=fort50(:,1);
TDStotal=fort50(:,2);
TDSP1=fort50(:,3);
TDSP2=fort50(:,4);
TDSP3=fort50(:,5);

nfig=nfig+1;
figure(nfig)
hold on
plot(TDStemp,TDStotal,'b');
hold on
plot(TDStemp,TDSP1,'g');
plot(TDStemp,TDSP2,'r');
plot(TDStemp,TDSP3,'m');
%ylim([0 1.2*max([max(TDStotal),max(TDSP1),max(TDSP2)])])
xlabel("T (K)");
ylabel("Desoprption rate (D/m2/s)");
print -dpng TDS.png

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fprofile=dir("profil*.txt");
for j=1:length(fprofile)

fprofile(j).name

fort60=load(fprofile(j).name);
z=fort60(:,1);
diff=fort60(:,2);
p1=abs(fort60(:,3))+1e-9;
p2=abs(fort60(:,4))+1e-9;
p3=abs(fort60(:,5))+1e-9;
ts=abs(fort60(:,6));

nfig=nfig+1;
figure(nfig)
hold on
loglog(z,diff,'b');
loglog(z,p1,'g');
loglog(z,p2,'r');
loglog(z,p3,'m');
ylim([1e-8 1e-1]);
xlim([1e-9 1e-5])
%semilogx(z,diff,'b');
%semilogx(z,p1,'g');
%semilogx(z,p2,'r');
%semilogx(z,p3,'m');
%ylim([1e-8 1e-2])
xlabel("z (m)");
ylabel("concentration H/m2");
legend("solute","trap1","trap2","trap3")
print([fprofile(j).name,'.png'], '-dpng')

end

nfig=nfig+1;
figure(nfig)
plot(z,ts)
xlim([0 20e-9])
xlabel("Profondeur z (m)");
ylabel("Terme source (At/m3/s)");
print -dpng TS.png


