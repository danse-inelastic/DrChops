PRO save_cut,xdat,ydat,yedat

arrsize = size(xdat)

filename=''
get_lun,lunno

read,filename,prompt='Enter filename to be saved without extension: '
openw,lunno,filename+'.dat'

FOR i = 0,arrsize[1]-1 DO BEGIN
;  printf,lunno,format='(8f10.3)',xdat[i],ydat[i],yedat[i]
  printf,lunno,xdat[i],ydat[i],yedat[i]
ENDFOR

close,lunno

END
