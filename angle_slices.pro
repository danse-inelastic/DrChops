pro angle_slice, spe, espe, angles, slices, errslices

; This procedure takes a 2D [m,n] array 'spe' and its error-array 'espe'
; and produces two smaller arrays [m, nslices]
; - slicevector should be a 1D array of dimension (nslices+1)
; - each slice returned contains the sum of spe[slicevector[i]:slicevector[i+1],*]

asz = size(angles)
numslices = asz[1] - 1

sz = size(spe)
nbin = sz[1]

slices = dblarr(nbin, numslices)
errslices = dblarr(nbin, numslices)

for i = 0,(numslices - 1) do begin
slices[*,i] = total(spe[*, angles[i]:(angles[i+1]-1)], 2)

error_square = espe^2
errslices[*,i] = total(error_square[*, angles[i]:(angles[i+1]-1)], 2)
errslices[*,i] = sqrt(errslices[*,i])

endfor

END

pro plot_slices, slices

asz = size(slices)
numslices = asz[2]

plot, slices[*,0], yrange=[0,100]

for i = 1, (numslices - 1) do begin
oplot, (5*i + slices[*,i])
endfor
END

pro make_slice, spe, espe, anglemin, anglemax, spe_slice, espe_slice
;spe_slice is the total counts (along angles: second dimension) in spe[*,*] between
;anglemin and anglemax

spe_slice = total(spe[*,anglemin:anglemax],2)

error_square = espe^2
espe_slice = total(error_square[*,anglemin:anglemax],2)
espe_slice = sqrt(espe_slice)

END

pro write_slices, ebins, slices, errslices

asz = size(slices)
numslices = asz[2]

for i = 0, numslices-1 do begin
    if i LT 9 then begin
      number=strmid(String(i+1),7,1)
    endif else begin
      number=strmid(String(i+1),6,2)
    endelse
	file = '0002.w'+number
	openw,fun,file,/GET_LUN
	numlines = asz[1]
	print,asz

	xlabel = 'mev06_'
	ylabel = 'S06_'
	errlabel = 'SE06_'

	;printf, fun, xlabel, i, ylabel, i, errlabel, i, format='(%"%s%d\t%s%d\t%s%d")'

	for j = 0, numlines-1 do begin
		printf, fun, ebins[j], slices[j,i], errslices[j,i]
	endfor
	close,fun
	free_lun,fun
endfor

END
