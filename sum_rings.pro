	PRO SUM_RINGS,tth,ste,este,pixel,tmin,tmax,se,ese
;
; Program will sum the ringed data array over some angle range
;
; Input:
;	tth: scattering angle array (in degrees)
;	ste: ringed data array (2-D)
;	este: associated error array
;	pixel: number of pixels per ring (array same size as tth)
;	tmin: lower angle limit of summation
;	tmax: higher angle
; Output:
;	se: summed data
;	ese: error of summed data
;
; Definitions
;
	sz=SIZE(ste)
	se=FLTARR(sz[1])
	ese=FLTARR(sz[1])
;
; Calculate angle array index values corresponding to (tmin,tmax)
; If angle limit is in the middle of a bin, lower index is chosen
; tthmin is lowest bin boundary, tthmax is highest
;
	dt=tth[1]-tth[0]
	tthmin=MIN(tth)-0.5*dt
	tthmax=MAX(tth)+0.5*dt
	print,tthmin,tthmax,dt
;
	IF (tmin GT tthmin AND tmin LT tthmax) THEN BEGIN
	   imin=FIX((tmin-tthmin)/dt)
	ENDIF
	IF (tmax GT tthmin AND tmax LT tthmax) THEN BEGIN
	   imax=FIX((tmax-tthmin-1.e-6)/dt)
	ENDIF
	IF (tmin LE tthmin) THEN imin=0
	IF (tmax GE tthmax) THEN imax=N_ELEMENTS(tth)-1
	print,imin,imax
;
; Sum over the ringed array after weighting by the # of pixels per ring
;
	FOR i=imin,imax DO se[*]=se[*]+ste[*,i]*pixel[i]
	FOR i=imin,imax DO ese[*]=ese[*]+este[*,i]^2*pixel[i]^2
	ese=SQRT(ese)
;
	END

