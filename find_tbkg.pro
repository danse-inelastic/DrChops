	PRO find_tbkg,str,tmin,tmax,tbkg,MASK=mask,dmin=dmin,dmax=dmax,	$
		hmin=hmin,hmax=hmax
;
; Finds the average time independent background per pixel (tbkg) from 
; data in the structure str given a time window defined by tmin and 
; tmax (in microseconds)
; Optionally enter a detector mask file and detector channel maxima and minima
; for background estimation
; Optionally enter minimum and maximum height indices for background estimation

	IF (N_ELEMENTS(dmin) EQ 0) THEN dmin=0
	IF (N_ELEMENTS(dmax) EQ 0) THEN dmax=375
;
	IF (N_ELEMENTS(hmin) EQ 0) THEN hmin=0
	IF (N_ELEMENTS(hmax) EQ 0) THEN hmax=39

	tbkg=0.
	tof=str.big_time		;in microseconds
	tof_min=MIN(tof)
	sz=SIZE(str.big,/DIMENSIONS)
	dt=tof[1]-tof[0]
	imin=FIX((tmin-dt/2.-tof_min)/dt)
	imax=FIX((tmax-dt/2.-tof_min)/dt)
	tbkg=TOTAL(str.big[imin:imax,hmin:hmax,dmin:dmax])/	$
			(imax-imin+1)/(hmax-hmin+1)
;
; Remove bad detectors from sum
;
	IF (N_ELEMENTS(mask) EQ 0) THEN sznewmask=0
	IF (N_ELEMENTS(mask) NE 0) THEN BEGIN
	   sz_mask=N_ELEMENTS(mask)
	   sznewmask=0
	   newmask=INTARR(sz_mask[0])
	   FOR i=0, sz_mask[0]-1 DO BEGIN
	      IF (mask[i] GE dmin AND mask[i] LE dmax) THEN BEGIN
	         newmask[sznewmask]=mask[i]
	         sznewmask=sznewmask+1
	      ENDIF
	   ENDFOR
;
	   FOR i=0,sznewmask-1 DO BEGIN
	      iarr=newmask[i]
	      tbkg=tbkg-TOTAL(str.big[imin:imax,hmin:hmax,iarr])/	$
			(imax-imin+1)/(hmax-hmin+1)
	   ENDFOR
	ENDIF
;
	tbkg=tbkg/(dmax-dmin+1-sznewmask)
	print,'Time independent background per pixel (',tmin,' - ',tmax,' us): ',tbkg
	END
