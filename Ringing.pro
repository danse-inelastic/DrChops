 pro rings,phi,cntsin,errcntsin,cntsringed,errcntsringed,	$
 		minang,maxang,numangs,ringangs,norms,eff=eff,		$
		mask=mask,hmin=hmin,hmax=hmax

; This line doesnt do anything, just checking if CVS works...
; Seeing if CVS lock works...
; testing CVS again
; testing cvs tags 

;	takes a Pharos dataset from det # and pixel height to scattering angle phi
;	phi: 2D array with the phi values for each pixel.
;	cntsin: Counts before ringing. Expects 3D array (from rebinning for instance)
;	errcntsin: Errors associated with cntsin
;	cntsringed: Counts after sorting into rings. Will be 2D array
;	errcntsringed: Errors assoc. with cntsringed
;	minang: angle to start binning at
;	maxang:
;	numangs: number new angles
;	ringangs: for fun--the angles will be stored in this variable
;       norms: number of pixels in each ring
;	eff: the detector efficiency variation per tube (not including Ef variation)
;	hmin: minimum height index for height range
;	hmax: maximum height index for height range
;	Really unimaginative algorithm: just three nested for loops. Runs in ~1-2 sec
;	on P4 2 GHz
;
;	TK 8/21/02

tstart = systime(1)
;
; Default values for the height indices (i.e. full range)
;
	IF (N_ELEMENTS(hmin) EQ 0) THEN hmin=0
	IF (N_ELEMENTS(hmax) EQ 0) THEN hmax=39

deltaPhi = float(maxang-minang)/numangs
AngBC = fltarr(numangs)		;Angle bin centers
AngBB = fltarr(numangs+1)	;Angle bin boundaries


for i=0,numangs-1 do AngBC[i] = minang + deltaPhi*(float(i)+0.5)
for i=0,numangs   do AngBB[i] = minang + deltaPhi*float(i)

ringangs = AngBC

sznew = size(cntsin)
if(sznew[0] NE 3) then begin
	print,'Unexpected dimensions for cntsin array'
	return
ENDIF

IF (N_ELEMENTS(eff) EQ 0) THEN BEGIN
	eff=FLTARR(sznew[3])
	eff[*]=1.
ENDIF

cntsringed = fltarr(sznew[1],numangs)
errcntsringed = fltarr(sznew[1],numangs)

;numdets = sznew[3]
s=size(phi)
numdets=s(2)
print,numdets
numhts  = sznew[2]

norms = fltarr(numangs)
;
	IF (N_ELEMENTS(eff) EQ 0) THEN BEGIN
		eff=FLTARR(376)
		eff[*]=1.
	ENDIF
;
	big_mask=FLTARR(376)
	big_mask[*]=1.
	big_mask[mask]=0.
;
for k=0,numangs-1 do begin
   for i=hmin,hmax do begin
      for j=0,numdets - 1 do begin
	 IF ((phi[i,j] GT AngBB[k]) AND (phi[i,j] LT AngBB[k+1])) then begin
	    cntsringed[*,k] = cntsringed[*,k] +		$
		big_mask[j]*cntsin[*,i,j]/eff[j]
	    norms[k] = norms[k] + big_mask[j]
	    errcntsringed[*,k] = errcntsringed[*,k] + 	$
		big_mask[j]*errcntsin[*,i,j]^2/eff[j]^2
	 ENDIF
      ENDFOR	;for j=0,numdets - 1
   ENDFOR	;for i=hmin,hmax
ENDFOR		;for k=0,numangs-1

errcntsringed = Sqrt(errcntsringed)

FOR k=0,numangs-1 DO BEGIN
   IF (norms[k] NE 0) THEN BEGIN
	cntsringed[*,k] = cntsringed[*,k]/norms[k]
	errcntsringed[*,k] = errcntsringed[*,k]/norms[k]
   ENDIF ELSE BEGIN
	cntsringed[*,k] = 0.	
	errcntsringed[*,k] = 0.	
   ENDELSE	
ENDFOR

plot,norms,psym=2
print,'Total pixels looked at: ',total(norms)

tend = systime(1)

print,'Elapsed time: ',tend-tstart

end


pro findPhi,heights,detang,phi

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

l_2 = 4000.		;Pharos secondary
pi = 3.1415926535898
for i=0,numdets-1 do begin
	for j=0,numhts-1 do begin
		phi[j,i] = ACOS(Cos(detang[i]*pi/180.)/sqrt(1+heights[j]^2/l_2^2))*180./pi
	ENDFOR
ENDFOR

end


PRO detectorangle, detang

;finds angles for the corresponding detectors (detang). For detectors 41-376 uses Rob's formulas and
;detectors 1-40 are made up (to be between 0 and 10 degrees) until there is data on them.
;Dina 9/22/02


detang=fltarr(376)

FOR i=0,23 DO BEGIN
	detang[i] = -10.9 + 0.4*float(i)
ENDFOR

FOR i=24,39 DO BEGIN
	detang[i] = -7.83 + 0.4*float(i)
ENDFOR

FOR i=40, 151 do begin
	detang[i] = 0.4011*float(i) - 6.1665
ENDFOR

FOR i=152, 263 do begin
	detang[i] = 0.4029*float(i) - 5.6868
ENDFOR

FOR i=264, 375 do begin
	detang[i] = 0.412*float(i) - 7.4276
ENDFOR

END
