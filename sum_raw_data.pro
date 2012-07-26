PRO sum_raw_data,counts1,counts2,newdata

arrsize = size(counts1.big)

newdata = counts1

FOR k = 0,arrsize[3]-1 DO BEGIN
  FOR j = 0,arrsize[2]-1 DO BEGIN
    FOR i = 0,arrsize[1]-1 DO BEGIN
      newdata.big[i,j,k] = newdata.big[i,j,k] + counts2.big[i,j,k]
    ENDFOR
  ENDFOR
ENDFOR

END
