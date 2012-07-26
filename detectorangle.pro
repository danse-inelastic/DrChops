PRO detectorangle, detang

;finds angles for the corresponding detectors (detang). For detectors 41-376 uses Rob's formulas and
;detectors 1-40 are made up (to be between 0 and 10 degrees) until there is data on them.
;Dina 9/22/02


detang=fltarr(376)

FOR i=0,23 DO BEGIN
	detang[i] = -10.9/2.5 + 0.4/2.5*float(i)
ENDFOR

FOR i=24,39 DO BEGIN
	detang[i] = -7.83/2.5 + 0.4/2.5*float(i)
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
