PRO bin_plot,str,xn,yn,ei=ei,vmin,vmax,hmin,hmax, $
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
xn=ei-ef
hcenter=(hmin+hmax)/2
det=detang[hcenter]

plot,xn,yn,xrange=[emin,emax], $
	title='vertical'+string(vmin)+'-'+string(vmax) $
	+' horizontal'+string(hmin)+'-'+string(hmax) $
	+'detector = '+string(det)+'deg.'
END
