pro save_spe2,e,phi,sppe,esppe,mask=mask

spename=''
lun=100   ;in a future version use get_lun to avoid conficts AC

read,spename,prompt='Enter filename to be saved without extension: '
openw,lun,spename+'.spe'

printf,lun,n_elements(phi),n_elements(e),format='(2I5)'  ;is 5 enough? seems to be AC.

phi[*,mask] = 0  
sppe[*,*,mask]=0
esppe[*,*,mask]=0

printf,lun,'### Phi Grid'
jp = n_elements(phi)/8
temp = [reform(phi,n_elements(phi),1),0]
for i = 0,jp-1 do begin
   printf,lun,temp[0:7],format='(8f10.3)'
   temp=temp[8:*]
endfor
n = n_elements(temp)
fm = '('+string(n)+'f10.3)'
printf,lun,temp,format=fm

printf,lun,'### Energy Grid'
de = (e[1]-e[0])/2
je = n_elements(e)/8
temp=[e[0]-de,e+de]
for i = 0,je-1 do begin
   printf,lun,temp[0:7],format='(8f10.3)'
   temp=temp[8:*]
endfor
n = n_elements(temp)
fm = '('+string(n)+'f10.3)'
printf,lun,temp,format=fm

sizephi=size(phi)
for it = 0,sizephi[2]-1 do begin
   for iy = 0,sizephi[1]-1 do begin
      printf,lun,'### S(Phi,w)'
      temp=sppe[*,iy,it]
      for i = 0,je-2 do begin
            printf,lun,temp[0:7],format='(8f10.3)'
            temp=temp[8:*]
      endfor
      n = n_elements(temp)
      fm = '('+string(n)+'f10.3)'
      printf,lun,temp,format=fm

      printf,lun,'### Errors'
      temp=esppe[*,iy,it]
      for i = 0,je-2 do begin
            printf,lun,temp[0:7],format='(8f10.3)'
            temp=temp[8:*]
      endfor
      n = n_elements(temp)
      fm = '('+string(n)+'f10.3)'
      printf,lun,temp,format=fm
   endfor
endfor
close,lun
print,'SPE file saved as '+spename+'.spe'

end

