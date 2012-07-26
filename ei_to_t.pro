	PRO EI_TO_T,ei,MON1=mon1,MON2=mon2,MON3=mon3,CHOP=chop,DET=det
;
; Converts flight time (t) in microseconds to incident energy for monitor 1 position
; If not detector is specifically chosen, program defaults to detector bank position
;
	length=24.
	pos='DET'
	IF (N_ELEMENTS(MON1) NE 0) THEN BEGIN
		length=17.887
		pos='MON1'
	ENDIF
	IF (N_ELEMENTS(CHOP) NE 0) THEN BEGIN
		length=18.0
		pos='CHOP'
	ENDIF
	IF (N_ELEMENTS(MON2) NE 0) THEN BEGIN
		length=18.193
		pos='MON2'
	ENDIF
	IF (N_ELEMENTS(MON3) NE 0) THEN BEGIN
		length=31.4626
		pos='MON3'
	ENDIF
	IF (N_ELEMENTS(DET) NE 0) THEN BEGIN
		length=24.
		pos='DET'
	ENDIF
;
	v=SQRT(ei/5.227e-6)
	t=length/v*1.e6
;
	print,'Flight time at ', pos, ' is: ',t,' microsecs'
;
	END