	PRO Q_INTERP,e,phi,spe,qbin,sqe
;
;	Program converts phi to Q for pharos data.
;       It can then interpolate the irregular Q-grid into a
;	regular one of the users choice.
;	The program outputs an array with regular Q-bin boundaries.
;
;
;    Array bounds and declarations
;
	nnrg = N_ELEMENTS(e)	;where e are bin centers
	nphi = N_ELEMENTS(phi)
	qmat = FLTARR(nphi,nnrg)
;
	READ, ei, PROMPT='Enter incident neutron energy: '
	READ, nq, PROMPT='Enter number of Q-bins: '
	READ, qmin ,qmax, PROMPT='Enter min and max Q-boundaries: '

	qbin = FLTARR(nq)
	qbound = FLTARR(nq+1)
	nint = FLTARR(nq)
	sqe = FLTARR(nq,nnrg)
	err = FLTARR(nq,nnrg)
;
; Read angle array
;
;	title=''
;	OPENR,1,'/home/mcqueene/pharos/detector_angle_map.txt'
;	READF,1,title
;
;	FOR i=0,nphi-1 DO BEGIN
;	   READF,1,num1,num2
;	   phi[i]=num2
;	ENDFOR
;	CLOSE,1
;
;    Define array for center and boundaries of Q-bins
;
	dq=(qmax-qmin)/nq
	qbin=qmin+0.5*dq+findgen(nq)*dq
	qbound=qmin+findgen(nq+1)*dq

;    Create 2D irregular array of Q-bin centers which correspond
;    to the phi bin centers.
;
	FOR i=0,nnrg-1 DO qmat[*,i]=    	$
	    SQRT(ei/2.08*(2.-e[i]/ei-2*COS(!PI*phi[*]/180.)*SQRT(1.-e[i]/ei)))
;
;    Interpolate irregular S(Q,E) onto a regular Q-grid.  Also propagate
;    errors by interpolating the square of the error matrix.
;
	spe1d=FLTARR(nphi)
	sqe1d=FLTARR(nq)
	FOR i=0,nnrg-1 DO BEGIN
		qmin=MIN(qmat[*,i])
		qmax=MAX(qmat[*,i])
;	   dq=(MAX(qmat[*,i])-MIN(qmat[*,i]))/nphi  ;spacing of irregular grid
;		FOR j=0,nq-1 DO BEGIN
;	   		nint[j]=(qbin[j]-MIN(qmat[*,i]))/dq  ;indices of reg. grid points
												 ;rel. to irregular grid
;		ENDFOR
		FOR k=0,nphi-1 DO spe1d[k]=spe[k,i]
;	    sqe1d=INTERPOLATE(spe1d,nint,MISSING=1000.)
		sqe1d=INTERPOL(spe1d,qmat[*,i],qbin)
;	    err[*,i]=INTERPOLATE(spe.error[*,i]^2,nint[*,i],MISSING=0.)
		FOR k=0,nq-1 DO	BEGIN
			IF ((qbin[k] GE qmin) AND (qbin[k] LE qmax)) THEN sqe[k,i]=sqe1d[k]
			IF (qbin[k] LT qmin) THEN sqe[k,i]=1000.
			IF (qbin[k] GT qmax) THEN sqe[k,i]=1000.
		ENDFOR
	ENDFOR

;	err=SQRT(err)
;
;    Define and fill S(Q,E) data structure
;
;	type='S(Q,E)'
;	title=STRCOMPRESS(spe.title)+' Q-interpolated'
;	FILL_SQE_STRUC, sqe,nq,nnrg,type,title,qbound,spe.e,sqw,err

	END
