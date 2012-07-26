	PRO PLATE_ABS,t,w,phi,tth,ab
;
; Plots the absorption (abs)for a flat plate sample of  thickness (t in mm), 
; width (w in mm) and angle with respect to the incident beam (phi in deg) 
; as a function of the scattering angle (twoth).  
;
	lambda=1.
	mu=.0368+.0367*lambda/1.798
	print,mu
;
; Angles of the tube centers
;
	ntth=240
	tth=FLTARR(ntth)
	tth[0:111]=10.35+0.4*findgen(112)
	tth[112:223]=56.+0.4*findgen(112)
	tth[224:239]=101.75+0.4*findgen(16)
	tthr=tth*!pi/180.
;
	ab=FLTARR(ntth)
	phir=phi*!pi/180.
;
; Integration over the plate done on a mesh of 0.1mm x 0.1 mm
;
	ntpts=FIX(t/0.1)-1
	nwpts=FIX(w/0.5)-1
;
; Integrate over plate in 2D (Assume height contribution negligible for 
; perfectly collimated incident beam and all sample dimensions << distance
; to detector)
;
; Note, t defined from 0 to t, w defined from -w/2 to w/2

	FOR k=0,ntth-1 DO BEGIN	
	   FOR i=0,ntpts DO BEGIN
	      y=0.1*FLOAT(i)+0.05
	      li=y/sin(phir)
	      FOR j=0,nwpts DO BEGIN
	        x=-0.5*w+0.5*FLOAT(j)+0.25
	        a=atan((t-y)/(0.5*w-x))
	        b=atan(y/(0.5*w-x))
	        th1=!pi-a-phir
	        th2=!pi-b-phir
;
		IF (tthr[k] LE th1) THEN lf=ABS((t-y)/sin(tthr[k]+phir))
		IF (tthr[k] LE th2 AND tthr[k] GT th1) THEN 		$
			lf=ABS((0.5*w+x)/cos(tthr[k]+phir))
		IF (tthr[k] GT th2) THEN lf=ABS(y/sin(tthr[k]+phir))
		IF (lf LT 0) THEN PRINT,x,y,li,lf
;
		ab[k]=ab[k]+exp(-mu*(li+lf))
	      ENDFOR
	   ENDFOR
	ENDFOR
	ab=ab/(ntpts+1)/(nwpts+1)
;
	END

		
