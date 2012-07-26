PRO show_qe, Einc, MinDet, MaxDet, Detang

Const = 2 * !PI / sqrt(81.787)

numDet = MaxDet - minDet + 1

; go to 90% Einc

deltaE = 0.009 * Einc

E = FLTARR(100)
FOR i=0,99 DO E[i] = Einc - deltaE * i

Q = FLTARR(100)
FOR j = 0,99 DO Q[j] = Const * sqrt(Einc + E[j] -    $
    2*sqrt(Einc * E[j]) * cos(detang[MinDet]/180*!PI) )
PLOT, E, Q, xrange=[80,100], yrange=[0,1]

FOR i = MinDet+1,MaxDet DO BEGIN
  FOR j = 0,99 DO Q[j] = Const * sqrt(Einc + E[j] -   $
    2*sqrt(Einc * E[j]) * cos(detang[i]/180*!PI) )
  OPLOT, E, Q
ENDFOR

END  
