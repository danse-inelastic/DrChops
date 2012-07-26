;-------------------------------------------------------------
; This is a wrapper for TVIM to let you zoom in on graphs by 
;	specifying XBNDS and YBNDS in units of XRANGE and 
;	YRANGE.  
; All keywords identical to tvim except XBNDS and YBNDS. 
; Assumes constant step size in x/yrange. 
; If x/ybnds entered are out of range tvimzoom will assume 
;	maximum range for x/y axis and print:
;	'**** lower/upper y/xbnds out of range ****'.
; NOTE: will not zoom in past 2*delta on x/yrange
; 12Nov02, Dina
;______________________________________________________________

PRO TVIMZOOM,xbnds=xbnds,ybnds=ybnds,imageof,scale=scale, $
	range=range,xrange=xrange,yrange=yrange,aspect=aspect, $
	title=title,xtitle=xtitle,ytitle=ytitle,noframe=noframe, $
     	noaxis=noaxis,interp=interp,colors=colors,c_map=c_map,$
        stitle=stitle,rmarg=rmarg,clip=clip,labels=labels,$
	clevels=clevels,pcharsize=pcharsize,lcharsize=lcharsize,$
	nbotclr=nbotclr,nodata=nodata,rgb_nodata=rgb_nodata,$
	barwidth=barwidth,position=position,rct=rct

;---------------------------------------------------------------
; Finding dimensions of data, and axis ranges entered
;_______________________________________________________________

sze = size(reform(imageof))	
szx = size(xrange)
szy = size(yrange)

;---------------------------------------------------------------
; Taking care of x/ybnds entered being out of range by assuming
; maximum range.
;_______________________________________________________________

IF (N_ELEMENTS(xbnds) NE 0) THEN BEGIN
	IF (xbnds[0] lt xrange[0]) THEN BEGIN
		xbnds[0]=xrange[0]
		PRINT,'***** lower xbnds out of range *****'
	ENDIF
	IF (xbnds[0] gt xrange[szx(1)-1]) THEN BEGIN
		xbnds[0]=xrange[0]
		PRINT,'***** lower xbnds out of range *****'
	ENDIF
	IF (xbnds[1] lt xrange[0]) THEN BEGIN
		xbnds[1]=xrange[szx(1)-1]
		PRINT,'***** upper xbnds out of range *****'
	ENDIF
	IF (xbnds[1] gt xrange[szx(1)-1]) THEN BEGIN
		xbnds[1]=xrange[szx(1)-1]
		PRINT,'***** upper xbnds out of range *****'
	ENDIF
ENDIF

IF (N_ELEMENTS(ybnds) NE 0) THEN BEGIN
	IF (ybnds[0] lt yrange[0]) THEN BEGIN
		ybnds[0]=yrange[0]
		PRINT,'***** lower ybnds out of range *****'
	ENDIF
	IF (ybnds[0] gt yrange[szy(1)-1]) THEN BEGIN
		ybnds[0]=yrange[0]
		PRINT,'***** lower ybnds out of range *****'
	ENDIF
	IF (ybnds[1] lt yrange[0]) THEN BEGIN
		ybnds[1]=yrange[szy(1)-1]
		PRINT,'***** upper ybnds out of range *****'
	ENDIF
	IF (ybnds[1] gt yrange[szy(1)-1]) THEN BEGIN
		ybnds[1]=yrange[szy(1)-1]
		PRINT,'***** upper ybnds out of range *****'
	ENDIF
ENDIF

;---------------------------------------------------------------
; Translating entered x/ybnds from units to indicies.
;_______________________________________________________________

IF (N_ELEMENTS(xbnds) EQ 0) THEN BEGIN
	xmin=0
	xmax=sze(1)
ENDIF ELSE BEGIN
	xmin=FLOOR((xbnds[0]-xrange[0])/ABS(xrange[1]-xrange[0]))
	xmax=CEIL((xbnds[1]-xrange[0])/ABS(xrange[1]-xrange[0]))
ENDELSE

IF (N_ELEMENTS(ybnds) EQ 0) THEN BEGIN
	ymin=0
	ymax=sze(2)
ENDIF ELSE BEGIN
	ymin=FLOOR((ybnds[0]-yrange[0])/ABS(yrange[1]-yrange[0]))
	ymax=CEIL((ybnds[1]-yrange[0])/ABS(yrange[1]-yrange[0]))
ENDELSE

;--------------------------------------------------------------
; Cutting out the stuff not to graph out of the data array and
; creating the new array to input into tvim.
;______________________________________________________________

a = fltarr(xmax-xmin,ymax-ymin)

FOR i=xmin,xmax-1 DO BEGIN
	FOR j=ymin,ymax-1 DO BEGIN
		a[i-xmin,j-ymin] = imageof[i,j]
	ENDFOR
ENDFOR

;---------------------------------------------------------------
; Passing new x/yrange values into tvim for axis labels.
;_______________________________________________________________

print,xmin,xmax,ymin,ymax
IF (N_ELEMENTS(xrange) NE 0) THEN xrng_new=xrange[xmin:xmax-1]
	
IF (N_ELEMENTS(yrange) NE 0) THEN yrng_new=yrange[ymin:ymax-1]

;---------------------------------------------------------------
; Calling tvim with the new (smaller) data array.
;_______________________________________________________________

tvim,a,scale=scale,range=range,xrange=xrng_new,yrange=yrng_new,$
	aspect=aspect,title=title,xtitle=xtitle,ytitle=ytitle,$
	noaxis=noaxis,interp=interp,colors=colors,c_map=c_map,$
        stitle=stitle,rmarg=rmarg,clip=clip,labels=labels, $
        pcharsize=pcharsize,lcharsize=lcharsize,nbotclr=nbotclr,$
        clevels=clevels,nodata=nodata,rgb_nodata=rgb_nodata,    $
        barwidth=barwidth,position=position,noframe=noframe,rct=rct


END 
