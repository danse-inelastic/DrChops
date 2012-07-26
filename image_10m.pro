PRO image_10m, str, res

str_size = SIZE(str.big,/DIMENSIONS)
res = fltarr(str_size[0],str_size[1],56)

FOR k=0,39 DO BEGIN
  FOR j=0,str_size[1]-1 DO BEGIN
    FOR i=0,str_size[0]-1 DO BEGIN
      IF (k LT 24) THEN res[i,j,k] = str.big[i,j,k] $
         ELSE res[i,j,k+16] = str.big[i,j,k]
    ENDFOR
  ENDFOR
ENDFOR

END
      
