PRO oplterr, xval, yval, err, detmin, detmax, scalef=scalef, color=color

IF N_ELEMENTS(scalef) EQ 0 THEN scalef = 1.0
IF N_ELEMENTS(color) EQ 0 THEN color=0

npnts = N_ELEMENTS(xval)
ndets = detmax - detmin + 1

yn = TOTAL(yval[*,detmin:detmax],2) * scalef

yerr = FLTARR(npnts)

FOR index0=0, npnts-1 DO BEGIN
  yerr[index0] = 0.0
  FOR index1=detmin, detmax DO BEGIN
    yerr[index0] = yerr[index0] + err[index0, index1] * err[index0, index1]
  ENDFOR
ENDFOR

yerr = SQRT(yerr) * scalef

IF (!D.NAME EQ 'x' OR !D.NAME EQ 'X') THEN !P.COLOR=color

OPLOT, xval, yn

ERRPLOT, xval, yn-yerr, yn+yerr

!P.COLOR=0

END
