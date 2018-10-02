function [ CI ] = civaluem( x )
SEM = std(x)/sqrt(length(x));               
ts = tinv([0.05  0.95],length(x)-1);      
CI = mean(x) + ts*SEM;  
end

