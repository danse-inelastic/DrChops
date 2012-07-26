	PRO ef_efficiency,ef,eff6,eff10
;
; program calculates the detector efficiency correction dependence on
; the final neutron energy for the 6 atm and 10 atm Pharos detectors.
;
;	ef: final energy array (in meV)
;	eff6: efficiency for 6 atm tube
;	eff10=efficiency for 10 atm tube 
;
;
; Helium three cross-section and detector information
;
	s_abs=5333.0e-24	; at Ei=25.3 meV (lambda=1.798 Ang^-1)
	l0=1.798		; reference wavelength for s_abs in Ang^-1
	r=1.27			; tube radius in cm
	n6=1.468e20		; number density of 6 atm fill  at/cm3
	n10=2.447e20		; number density of 10 atm fill  at/cm3
;
; Loop over ef values
;
	sz=N_ELEMENTS(ef)
	eff6=FLTARR(sz)
	eff10=FLTARR(sz)
;
; Integrate over circular cross_section of detector tube
;
	npts=500
	FOR i=0,sz-1 DO BEGIN
	lf=SQRT(81.81/ef[i])
	sig=s_abs*lf/l0
	      FOR j=0,npts-1 DO BEGIN
		u=FLOAT(j)/(npts-1)
		eff6[i]=eff6[i]+exp(-2*n6*sig*r*SQRT(1-u*u))
		eff10[i]=eff10[i]+exp(-2*n10*sig*r*SQRT(1-u*u))
	      ENDFOR
	ENDFOR
	eff6=1-eff6/(npts-1)
	eff10=1-eff10/(npts-1)
;
	END

