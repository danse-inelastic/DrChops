pro findPhi_10m,heights,detang,phi

;get phi for each pixel given the height and angle of the center of the
;det tube from the incident beam.
;
;heights: heights for pixels
;detang: angles psi for detector tubes
;phi: array for angles
; TK 08/13/02
;------------------------------------------------------------------------

szdets=size(detang)
numdets=szdets[1]
szhts=size(heights)
numhts=szhts[1]
phi = fltarr(numhts,numdets)
pi = 3.1415926535898

l_2 = 10000.		;Pharos secondary
for i=0,39 do begin
	for j=0,numhts-1 do begin
		phi[j,i] = ACOS(Cos(detang[i]*pi/180.)/sqrt(1+heights[j]^2/l_2^2))*180./pi
	ENDFOR
ENDFOR
l_2 = 4000.		;Pharos secondary

for i=39,numdets-1 do begin
	for j=0,numhts-1 do begin
		phi[j,i] = ACOS(Cos(detang[i]*pi/180.)/sqrt(1+heights[j]^2/l_2^2))*180./pi
	ENDFOR
ENDFOR

end
