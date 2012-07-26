	PRO FIT_ENERGY,str,tmin,tmax,store=store,print=print
;
; Fits multiple chopper transmission spectra to a gaussian in energy space
;	tof=time-of-flight array (in microseconds)
;	spec=TOF spectrum array
;	tmin=lower time bound for fitting (in microseconds)
;	tmax=upper time bound for fitting (in microseconds)
;
	tof=str.tof_time
	spec=str.tof
	runno=str.runno
	tof_min=MIN(tof)
	dt=tof[1]-tof[0]
	imin=FIX((tmin-dt/2.-tof_min)/dt)
	imax=FIX((tmax-dt/2.-tof_min)/dt)
	print,tof_min,dt,imin,imax
	spec_tot=total(spec[imin:imax,40:375],2)
;	plot,tof[imin:imax],spec_tot
	gfit=gaussfit(tof[imin:imax],spec_tot,a,nterms=3)
;
; Various quantities of interest
;
	l1=18.
	l2=2.1
	l3=4.0
	lambda=a[1]/252.8/(l1+l2+l3)    ;in Angstrom
	ei=81.81/lambda^2	   ;in meV
	vi=SQRT(ei/5.227e6)	   ;in m/us
	area=a[0]*a[2]*sqrt(2*!pi)
;
; Print quantities
;
	print,'Apparent wavelength (Ang): ',lambda
	print,'Apparent energy (meV): ',ei
	print,'Peak area (counts): ',area
;
; Rebin spec array into energy space
;
	hw=fltarr(imax-imin+1)
	d_hw=fltarr(imax-imin+1)
	cts_mev=fltarr(imax-imin+1)
	hw=ei*(1.-(l3/(vi*(tof[imin:imax]-0.5)-l1-l2))^2)
	for i=0,imax-imin-1 do d_hw[i]=hw[i+1]-hw[i]
	d_hw[imax-imin]=d_hw[imax-imin-1]
	for i=0,imax-imin do cts_mev[i]=spec_tot[i]/d_hw[i]
	efit=gaussfit(hw,cts_mev,b)
;
; Plot
;
	!p.multi=[0,0,2,0,0]
	plot,tof[imin:imax],spec_tot,			$
	   xra=[tmin,tmax],xsty=1,psym=10,		$
	   xtitle='Time-of-flight (microseconds)',	$
	   ytitle='Counts/microsecond',			$
	   title=string(runno)+string(a[0])+string(a[1])+string(a[2])
	oplot,tof[imin:imax],gfit
;
	plot,hw,cts_mev,				$
	   xsty=1,psym=10,				$
	   xtitle='Energy Transfer  (meV)',		$
	   ytitle='Counts/meV',				$
	   title=string(runno)+string(b[0])+string(b[1])+string(b[2])
	oplot,hw,efit
;
	IF (N_ELEMENTS(print) NE 0) THEN BEGIN
	   SET_PLOT,'PS'
	   DEVICE,SCALE=0.65
	!p.multi=[0,0,2,0,0]
	plot,tof[imin:imax],spec_tot,			$
	   xra=[tmin,tmax],xsty=1,psym=10,		$
	   xtitle='Time-of-flight (microseconds)',	$
	   ytitle='Counts/microsecond',			$
	   title=string(runno)+string(a[0])+string(a[1])+string(a[2])
	oplot,tof[imin:imax],gfit
;
	PLOT,hw,cts_mev,				$
	   xsty=1,psym=10,				$
	   xtitle='Energy Transfer  (meV)',		$
	   ytitle='Counts/meV',				$
	   title=string(runno)+string(b[0])+string(b[1])+string(b[2])
	OPLOT,hw,efit
	   DEVICE,/CLOSE
	   SPAWN,'lp -dzippy idl.ps'
	   SET_PLOT,'X'
	ENDIF
;
; Append output to file
;
	IF (N_ELEMENTS(store) NE 0) THEN BEGIN
	   openw,1,'/home/mcqueene/data/chopper_data.dat',/APPEND
	   printf,1,							$
	format='(i3,2x,f7.2,2x,f5.3,2x,f7.2,2x,f5.2,2x,f8.2,2x,f5.2)',	$
		runno,a[1],lambda,ei,a[2],area,100.*b[2]/ei
	   close,1
	ENDIF
;
	!p.multi=0
	END
