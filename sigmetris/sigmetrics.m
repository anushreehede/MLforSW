agv=data(:,83);
iagc=find(agv~=0);
ingc=find(agv==0);
for i=1:82
   f=data(:,i);
   fvag=f(iagc);
   fvngc=f(ingc);
   cifvag=civaluem(fvag );
   cifvng=civaluem(fvngc );
   
   p(i)=ranksum(fvag,fvngc);
   
   x=[cifvag;cifvng];
   boxplot(x');
set(gca, 'XTick',1:2, 'XTickLabel',{'Aging','No Aging'});
fename=strcat('box',num2str(i));
figname=strcat(fename,'.png');
saveas(gcf,figname);
 close(gcf);
    
end
