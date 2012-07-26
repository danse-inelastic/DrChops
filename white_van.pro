	PRO WHITE_VAN,ei,phi,eff,ab,vfile=vfile,strv=strv
; Program calculates the efficiency of each tube from a white beam vanadium
; run.  Program requires the incident energy (in meV) where the efficiency
; correction is to be made (i.e. the incident energy of the monochromatic
; run that needs to be corrected). vfile is the filename of the white
; beam vanadium file. Program outputs eff array containing the efficiency
; correction for each tube.
;
;	ei = incident energy
;	phi = dark angle of plate in degrees
;	eff = detector efficiency
;	ab = plate absorption correction function
;	vfile = name of vanadium run file (optional)
;	strv = name of vanadium structure (optional)
;
; Right now the program assumes a flat plate V sample of a certain thickness
; and width.  Will soon generalize to a cylinder
;---------------------------------------------------------------------------
;
; Read vanadium data. If vanadium data is not already in memory (in
; the data structure strv), then enter filename of V data.  If no filename
; is entered, then open dialog box. 
;
	IF (N_ELEMENTS(strv) EQ 0) THEN BEGIN
	   IF (N_ELEMENTS(vfile) EQ 0) THEN 				$
		vfile=DIALOG_PICKFILE(PATH='/home/pharos/data',	$
		TITLE='Pick a white bean vanadium file')
	   read_data,strv,file=vfile
	ENDIF
;
; Vanadium cross-sections and plate sample information
;
	s_scat=5.10e-24		; in cm^2
	s_abs=5.08e-24		; at Ei=25.3 meV (lambda=1.798 Ang-1)
	t=0.2			; thickness of plate in cm
	w=6.3			; width of plate in cm
	phir=phi*!pi/180.
;
	rho=6.11		; density of vanadium g/cm3
	mass=50.942		; molar mass of vanadium in g/mol
	av=6.022e23		; Avogadro's number
;
	lambda=SQRT(81.81/ei)
;
; Inverse penetration depth in mm^-1
;
	mu_scat=s_scat*rho*av/mass
	mu_abs=s_abs*rho*av/mass*lambda/1.798
	mu=mu_scat+mu_abs
;	print,mu
;
; Angles of the tube centers
;
	ntth=376
	tth=FLTARR(ntth)
	tth[0:23]=-10.+0.4*findgen(24)
	tth[24:39]=1.5+0.4*findgen(16)
	tth[40:151]=0.4011*(41+findgen(112))-6.1665
	tth[152:263]=0.4029*(153+findgen(112))-5.6868
	tth[264:375]=0.412*(265+findgen(112))-7.4276
	tthr=tth*!pi/180.
;
	eff=FLTARR(ntth)
	ab=FLTARR(ntth)
;
; Correction for plate absorption
; Integration over the plate done on a mesh of dw x dt cm^2
;
	dt=0.01
	dw=0.05
	ntpts=FIX(t/dt)-1
	nwpts=FIX(w/dw)-1
;	print,ntpts,nwpts
;
; Integrate over plate in 2D (Assume height contribution negligible for
; perfectly collimated incident beam and all sample dimensions << distance
; to detector)
;
; Note, t defined from 0 to t, w defined from 0 to w

	li=0.
	FOR k=0,ntth-1 DO BEGIN
	   FOR i=0,ntpts DO BEGIN
	      y=dt*FLOAT(i)+0.5*dt
	      FOR j=0,nwpts DO BEGIN
	        x=dw*FLOAT(j)+0.5*dw
	        IF (x LT y/tan(!pi-phir)) THEN li=x/cos(!pi-phir)
		IF (x GT y/tan(!pi-phir)) THEN li=y/sin(!pi-phir)
		li=y/sin(!pi-phir)
	        a=atan(y/x)
	        b=atan((t-y)/x)
	        th1=phir-b
	        th2=phir+a
;
		IF (tthr[k] LE th1) THEN 				$
			lf=ABS((t-y)/cos(0.5*!pi+tthr[k]-phir))
		IF (tthr[k] LE th2 AND tthr[k] GT th1) THEN 		$
			lf=x/cos(tthr[k]-phir)
		IF (tthr[k] GT th2) THEN lf=ABS(y/cos(0.5*!pi-tthr[k]+phir))
		IF (lf LT 0) THEN PRINT,x,y,li,lf
;
		ab[k]=ab[k]+exp(-mu*(li+lf))
	      ENDFOR
	   ENDFOR
	ENDFOR
	ab=ab/(ntpts+1)/(nwpts+1)
;
; Read in white beam vanadium data from data structure strv for
; the appropriate time range corresponding to chosen ei.
;
	tof=strv.tof_time
	dt=tof[1]-tof[0]
	tof_min=MIN(tof)
	time=252.8*24.*lambda
	iarr=FIX((time-dt/2.-tof_min)/dt)
	print,'TOF channel range: ',iarr-50,iarr+50
;
; Calculate the difference in efficiency for 6 and 10 atm tubes.
; Note that tubes 0:111 are 6 atm, 112:375 are 10 atm.
; Note: white beam efficiency must be corrected for different fill pressures
; to avoid double correcting (this is also done in ef efficiency correction).
	ef_efficiency,ei,eff6,eff10
;
; Efficiency for each detector tube
;
;	eff[0:111]=strv.tof[iarr,0:111]/ab[0:111]/eff6[0]
;	eff[112:375]=strv.tof[iarr,112:375]/ab[112:375]/eff10[0]
	eff[0:111]=TOTAL(strv.tof[iarr-50:iarr+50,0:111],1)/ab[0:111]/eff6[0]
	eff[112:375]=TOTAL(strv.tof[iarr-50:iarr+50,112:375],1)/ab[112:375]/eff10[0]
	eff=eff/TOTAL(eff)*376
	index=WHERE(eff EQ 0, count)
	IF (count NE 0) THEN eff(index)=1.
;
	END



