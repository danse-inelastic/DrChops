pro save_spe,e,phi_in,sppe,esppe,mask=mask,eff=eff

phi = (phi_in[0:39,*] + phi_in[1:40,*])/2.0

GET_LUN, lun
spename=''
READ,spename,prompt='Enter filename to be saved without extension: '
OPENW,lun,spename+'.spe'

PRINTF,lun,N_ELEMENTS(phi),N_ELEMENTS(e),format='(2I5)'

IF N_ELEMENTS(mask) GT 0 THEN BEGIN
  phi[*,mask] = 0  
  sppe[*,*,mask]=0
  esppe[*,*,mask]=0
ENDIF

PRINTF,lun,'### Phi Grid'
jp = N_ELEMENTS(phi)/8
temp = [REFORM(phi,N_ELEMENTS(phi),1),0]
FOR i = 0,jp-1 DO BEGIN
   PRINTF,lun,temp[0:7],FORMAT='(8f10.3)'
   temp=temp[8:*]
ENDFOR
n = N_ELEMENTS(temp)
fm = '('+string(n)+'f10.3)'
PRINTF,lun,temp,FORMAT=fm

PRINTF,lun,'### Energy Grid'
de = (e[1]-e[0])/2
je = N_ELEMENTS(e)/8
temp=[e[0]-de,e+de]
for i = 0,je-1 DO BEGIN
   PRINTF,lun,temp[0:7],FORMAT='(8f10.3)'
   temp=temp[8:*]
ENDFOR
n = N_ELEMENTS(temp)
fm = '('+string(n)+'f10.3)'
PRINTF,lun,temp,FORMAT=fm

sizephi=size(phi)
FOR it = 0,sizephi[2]-1 DO BEGIN
   FOR iy = 0,sizephi[1]-1 DO BEGIN
      PRINTF,lun,'### S(Phi,w)'
      IF eff[it] GT 0.0 THEN BEGIN
        temp=sppe[*,iy,it]/eff[it]
      ENDIF ELSE BEGIN
        temp=sppe[*,iy,it]
      ENDELSE
      FOR i = 0,je-1 DO BEGIN
            PRINTF,lun,temp[0:7],FORMAT='(8f10.3)'
            temp=temp[8:*]
      ENDFOR
      n = N_ELEMENTS(temp)
      fm = '('+string(n)+'f10.3)'
      PRINTF,lun,temp,FORMAT=fm

      PRINTF,lun,'### Errors'
      IF eff[it] GT 0.0 THEN BEGIN
        temp=esppe[*,iy,it]/eff[it]
      ENDIF ELSE BEGIN
        temp=esppe[*,iy,it]
      ENDELSE

      FOR i = 0,je-1 DO BEGIN
            PRINTF,lun,temp[0:7],FORMAT='(8f10.3)'
            temp=temp[8:*]
      ENDFOR
      n = N_ELEMENTS(temp)
      fm = '('+string(n)+'f10.3)'
      PRINTF,lun,temp,FORMAT=fm
   ENDFOR
ENDFOR

CLOSE,lun
PRINT,'SPE file saved as '+spename+'.spe'

END

