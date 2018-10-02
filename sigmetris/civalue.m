
for i=1:22
 bsm1=csm(:,1);
 
in=find(bsm1==0);
in1=find(bsm1~=0);
cm=data(:,i);
bsm=cm(in);
ndsm=cm(in1);
[ CInbs ] = civaluem( bsm );
[ CIbs ] = civaluem( ndsm );
x=[CIbs;CInbs];
boxplot(x');
set(gca, 'XTick',1:2, 'XTickLabel',{'Code smell','No smell'});
fename=strcat('box',num2str(i));
figname=strcat(fename,'.png');
saveas(gcf,figname);
 close(gcf);
 
p(i) = ranksum(bsm,ndsm);
end



