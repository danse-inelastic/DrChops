PRO todos,ar1,ar2,e,qbin

FOR i=0,49 DO BEGIN
  FOR j=0,159 DO BEGIN
    ar2[i,j]=ar1[i,j]*e[j]/(qbin[i]*qbin[i])
  ENDFOR
ENDFOR

END
