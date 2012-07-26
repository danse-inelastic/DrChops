PRO bin_plot_save,str,omega,yn,ei=ei,vmin,vmax,hmin,hmax, $
			emin=emin,emax=emax,detang

L1=20.1
L2=4.

yn=total(total(str.big[*,vmin:vmax,hmin:hmax],3),2)

t1=sqrt(5227600/ei)*L1
tmin=t1+sqrt(5227600/(ei-emin))*L2
tmax=t1+sqrt(5227600/(ei-emax))*L2
nmin=fix((tmin-3000)/2.5)
nmax=fix((tmax-3000)/2.5)
t2=str.big_time - t1
tof2=t2/L2
ef=5227600/(tof2*tof2)
omega=ei-ef

plot,omega,yn,xrange=[emin,emax]

hcenter=(hmin+hmax)/2
det=detang[hcenter]

filename=''

read,filename,prompt='Enter filename to be saved without extension: '
openw,1,filename+'.txt'

printf,1,'horizontal:', hmin,hmax
printf,1,'vertical:', vmin,vmax
printf,1,'detang = ', det
printf,1,'' 

; printf,1,'Energy','Intensity'
for i = nmin,nmax do begin
   printf,1,format='(8f10.3)',omega[i],yn[i]
endfor
close,1
END
