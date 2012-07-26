PRO pltsum,xval,yval,err,detmin,detmax,     $
           xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax

npnts = N_ELEMENTS(xval)
ndets = detmax - detmin + 1

yn = TOTAL(yval[*,detmin:detmax],2)

IF N_ELEMENTS(xmin) EQ 0 THEN xmin = xval[0]
IF N_ELEMENTS(xmax) EQ 0 THEN xmax = xval[npnts]
IF N_ELEMENTS(ymin) EQ 0 THEN ymin = yval[0]
IF N_ELEMENTS(ymax) EQ 0 THEN ymax = MAX(yval)

yerr = FLTARR(npnts)

FOR index0=0, npnts-1 DO BEGIN
  yerr[index0] = 0.0
  FOR index1=detmin, detmax DO BEGIN
    yerr[index0] = yerr[index0] + err[index0, index1] * err[index0, index1]
  ENDFOR
ENDFOR

yerr = SQRT(yerr)

!P.BACKGROUND=255
!P.COLOR=0
PLOT, xval, yn, xrange = [xmin,xmax], yrange=[ymin,ymax], $
      xtitle='Neutron Energy Loss (meV)',ytitle='S(Q,E) (arbitrary units)',psym=-6


;ERRPLOT, xval, yn-yerr, yn+yerr
END
