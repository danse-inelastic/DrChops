	PRO PH_PLOT,str,MON1=mon1,MON2=mon2,MON3=mon3,CHOP1=chop1,CHOP2=chop2,DET=det,	$
		XRA=xra,YRA=yra,FIT=fit,ylog=ylog
;
; Plots various arrays from a Pharos data structure
; This line is just to check CVS.. 
;
	length=24.
	pos='DET'
	IF (N_ELEMENTS(MON1) NE 0) THEN BEGIN
		tof=str.mon1_time
		sz=N_ELEMENTS(tof)
		dt=tof[1]-tof[0]
		tofc=str.mon1_time[0:sz-1]+0.5*dt
		data=str.mon1
		ytitle='Intensity@MON1'
	ENDIF
;
	IF (N_ELEMENTS(MON2) NE 0) THEN BEGIN
		tof=str.mon2_time
		sz=N_ELEMENTS(tof)
		dt=tof[1]-tof[0]
		tofc=str.mon2_time[0:sz-1]+0.5*dt
		data=str.mon2
		ytitle='Intensity@MON2'
	ENDIF
	;
	IF (N_ELEMENTS(MON3) NE 0) THEN BEGIN
		tof=str.mon3_time
		sz=N_ELEMENTS(tof)
		dt=tof[1]-tof[0]
		tofc=str.mon3_time[0:sz-1]+0.5*dt
		data=str.mon3
		ytitle='Intensity@MON3'
	ENDIF
;
	IF (N_ELEMENTS(CHOP1) NE 0) THEN BEGIN
		tof=str.chop1_time
		sz=N_ELEMENTS(tof)
		dt=tof[1]-tof[0]
		tofc=str.chop1_time[0:sz-1]+0.5*dt
		data=str.chop1
		ytitle='Intensity@CHOP1(T0)'
	ENDIF
;
	IF (N_ELEMENTS(CHOP2) NE 0) THEN BEGIN
		tof=str.chop2_time
		sz=N_ELEMENTS(tof)
		dt=tof[1]-tof[0]
		tofc=str.chop2_time[0:sz-1]+0.5*dt
		data=str.chop2
		ytitle='Intensity@CHOP2(FC)'
	ENDIF
;
	IF (N_ELEMENTS(DET) NE 0) THEN BEGIN
		tof=str.big_time
		sz=N_ELEMENTS(big)
		dt=tof[1]-tof[0]
		tofc=str.big_time[0:sz-1]+0.5*dt
		data=TOTAL(TOTAL(str.big,2),2)
		ytitle='Counts/time'
	ENDIF
;
	plot,tofc,data,xra=xra,yra=yra,xtitle='Flight Time (us)',ytitle=ytitle,psym=10,ylog=ylog
;
	IF (N_ELEMENTS(FIT) NE 0) THEN BEGIN
		tof_min=MIN(tof)
		tmin=MAX([MIN(tof),xra[0]])
		tmax=MIN([MAX(tof),xra[1]])
		imin=FIX((tmin-dt/2.-tof_min)/dt)
		imax=FIX((tmax-dt/2.-tof_min)/dt)
		print,dt,tmin,tmax,imin,imax
		ipeak=WHERE(data[imin:imax] EQ MAX(data[imin:imax]))
		result=GAUSSFIT(tofc[imin:imax],data[imin:imax],a,			$
			estimates=[data[imin+ipeak],tofc[imin+ipeak],10.,0.,0.,0.])
		oplot,tofc[imin:imax],result
		print,a
	ENDIF
	END
