PRO save_sqe,e,sqe,esqe,minindx,maxindx

arrsize = size(sqe)

yval = FLTARR(arrsize[1])
eval = FLTARR(arrsize[1])
numval = FLTARR(arrsize[1])
FOR i=0,arrsize[1]-1 DO BEGIN
 FOR j=minindx,maxindx DO BEGIN
   IF (sqe[i,j] LT 999) THEN BEGIN
     yval[i] = yval[i] + sqe[i,j]
     eval[i] = eval[i] + esqe[i,j]*esqe[i,j]
     numval[i] = numval[i]+1
   ENDIF
 ENDFOR
ENDFOR

FOR i=0,arrsize[1]-1 DO BEGIN
   IF (numval[i] GT 0) THEN BEGIN
       yval[i] = yval[i] / numval[i]
       eval[i] = SQRT(eval[i])/ numval[i]
   ENDIF
ENDFOR

filename=''
get_lun,lunno

read,filename,prompt='Enter filename to be saved without extension: '
openw,lunno,filename+'.dat'

FOR i = 0,arrsize[1]-1 DO BEGIN
;  printf,lunno,format='(8f10.3)',xdat[i],ydat[i],yedat[i]
  printf,lunno,e[i],yval[i],eval[i]
ENDFOR

close,lunno

END
