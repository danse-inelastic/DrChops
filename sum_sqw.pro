PRO sum_sqw,sqw,esqw,xin,yin,sumtype,minval,maxval,xval,yval,eval,mon

; sqw is 2-D array containing sqw data
; esqw is error of sqw
; xin is the array of xvalues for sqw
; yin is the array of y values for sqw
; sumtype = 1 for summation over x
; minval is the lower cutoff for summation
; maxval is the upper cutoff for summation
; xval, yval and eval are new arrays created with the summed data
; mon is proportional to the numbner of protons
; e.g. sum_sqw,sqe_11,qbin11,e11,2,5,10,xout,yout,mon
; sums over energy from 5-10 meV

IF (sumtype EQ 1) THEN tmpval = xin ELSE tmpval = yin
rng = size(tmpval)

FOR i=0,rng[1] DO BEGIN
  IF (minval LT tmpval[i]) THEN BEGIN
    minindx = i
    BREAK
  ENDIF
ENDFOR

FOR i=0,rng[1] DO BEGIN
  IF (maxval LT tmpval[i]) THEN BEGIN
    maxindx = i
    BREAK
  ENDIF
ENDFOR

PRINT,minindx,maxindx


IF (sumtype EQ 1) THEN BEGIN
 rng = size(yin)
 yval = FLTARR(rng[1])
 eval = FLTARR(rng[1])
 numval = FLTARR(rng[1])
 FOR i=0,rng[1]-1 DO BEGIN
  FOR j=minindx,maxindx DO BEGIN
    IF (sqw[j,i] GT -999) THEN BEGIN
      yval[i] = yval[i] + sqw[j,i]
      eval[i] = eval[i] + esqw[j,i]*esqw[j,i]
      numval[i] = numval[i]+1
    ENDIF
  ENDFOR
 ENDFOR
 xval = yin
ENDIF ELSE BEGIN
 rng = size(xin)
 yval = FLTARR(rng[1])
 eval = FLTARR(rng[1])
 numval = FLTARR(rng[1])
 FOR i=0,rng[1]-1 DO BEGIN
  FOR j=minindx,maxindx DO BEGIN
    IF (sqw[i,j] GT -999) THEN BEGIN
      yval[i] = yval[i] + sqw[i,j]
      eval[i] = eval[i] + esqw[i,j] * esqw[i,j]
      numval[i] = numval[i]+1
    ENDIF
  ENDFOR
 ENDFOR
 xval = xin
ENDELSE

FOR i=0,rng[1]-1 DO BEGIN
   IF (numval[i] GT 0) THEN BEGIN
       yval[i] = yval[i] / numval[i] / mon
       eval[i] = SQRT(eval[i])/ numval[i] / mon
   ENDIF
ENDFOR
ploterr,xval,yval,eval

END
