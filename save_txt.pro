PRO save_txt,xn,yn

filename=''
;file=100

read,filename,prompt='Enter filename to be saved without extension: '
openw,1,filename+'.txt'

printf,1,'Energy','Intensity'
printf,1,format='(8f10.3)',xn[0],yn[0]
close,1
END
