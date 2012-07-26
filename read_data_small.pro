FUNCTION getobj,targ,tag,ref
	COMMON nexus,fhandle,sdhandle,vname,vtype,vval
	DFTAG_NDG = 720
	DFTAG_SDG = 700
	DFTAG_VG = 1965
	;print,"getobj: tag=",tag," ref=",ref," targ=",targ
	c = STRMID(targ,0,1)
	if (c ne "/") then begin
		print, "Expected '/' in ",targ
		return, 0
	endif
	pos=STRPOS(targ,"/",1)
	if (pos eq -1) then begin	; final segment
		pos=STRPOS(targ,"/attribute:")
		if (pos eq 0) then begin
			targ=STRMID(targ,11)
			;print,"looking for attribute ",targ
			if (ref eq -1) then begin	; search global attributes
				idx = 0
				found = 0
				CATCH,loopErr
				if (loopErr ne 0) then begin
				endif
				while (loopErr eq 0) do begin
					if (loopErr eq 0) then HDF_SD_ATTRINFO,sdhandle,idx,COUNT=c,DATA=vval,NAME=vname,TYPE=vtype
					if (vname eq targ) then begin
						found = 1
						break
					endif
					idx = idx+1
				endwhile
				CATCH,loopErr,/CANCEL
				return, found
			endif
			; attribute is nonglobal
			if (tag ne DFTAG_SDG and tag ne DFTAG_NDG) then return, 0	; must be in SDS to get attribute
			index = HDF_SD_REFTOINDEX(sdhandle,ref)
			sds_id = HDF_SD_SELECT(sdhandle,index)
			index = HDF_SD_ATTRFIND(sds_id,targ)
			if (index eq -1) then return, 0
			HDF_SD_ATTRINFO,sds_id,index,COUNT=n,DATA=vval,NAME=vname,TYPE=vtype
			HDF_SD_ENDACCESS,sds_id
			return, 1
		endif
		pos=STRPOS(targ,"/SDS:")
		if (pos eq 0) then begin
			if (tag ne DFTAG_VG) then return, 0	; must be in VGroup to get SDS
			targ=STRMID(targ,5)
			;print,"looking for SDS ",targ
			vgsub = HDF_VG_ATTACH(fhandle,ref,/READ)
			HDF_VG_GETINFO,vgsub,CLASS=clname,NAME=vgname,NENTRIES=nobjects
			HDF_VG_GETTRS,vgsub,Tags,Refs
			for i=0,nobjects-1 do begin
				if ((Tags(i) eq DFTAG_SDG) OR (Tags(i) eq DFTAG_NDG)) then begin
					index = HDF_SD_REFTOINDEX(sdhandle,Refs(i))
					sds_id=HDF_SD_SELECT(sdhandle,index)
					HDF_SD_GETINFO,sds_id,DIMS=dimen,NAME=vname
					if (vname eq targ) then begin
						HDF_SD_GETDATA,sds_id,vval
						HDF_SD_ENDACCESS,sds_id
						HDF_VG_DETACH,vgsub
						return, 1
					endif
					HDF_SD_ENDACCESS,sds_id
				endif
			endfor
			HDF_VG_DETACH,vgsub
			return, 0
		endif
	endif
	; chase down more path segments
	pos = STRPOS(targ,"/",1)
	leg = STRMID(targ,1,pos-1)
	;print, "Searching for leg ",leg
	targ = STRMID(targ,pos)
	srchtag = 0
	pos = STRPOS(leg,"SDS:")
	if (pos eq 0) then begin
		srchtag = DFTAG_SDG
		namepart = STRMID(leg,4)
	endif else begin
		pos = STRPOS(leg,"NX")
		if (pos eq 0) then begin
			srchtag = DFTAG_VG
			ppos = STRPOS(leg,":")
			nxclass = STRMID(leg,0,ppos)
			nxlabel = STRMID(leg,ppos+1)
		endif
	endelse
	if (srchtag eq 0) then begin
		print, targ,": bad target!"
		return, 0
	endif
	if (tag eq -1) then begin
		tref = -1
		while (1) do begin
			tref = HDF_VG_GETID(fhandle,tref)
			if (tref lt 0) then break
			vgsub = HDF_VG_ATTACH(fhandle,tref,/READ)
			HDF_VG_GETINFO,vgsub,CLASS=clname,NAME=vgname
			HDF_VG_DETACH,vgsub
			;print,tref,' ',clname," ",nxclass,",",vgname," ",nxlabel
			if (clname eq nxclass) then begin
				if (strpos(nxlabel,"*") ge 0) then begin
					nxlabelpart = strmid(nxlabel,0,strpos(nxlabel,"*"))
					if (strmid(vgname,0,strlen(nxlabelpart)) eq nxlabelpart) then begin
						st = getobj(targ,1965,tref)
						return, st
					endif
				endif else begin
					if (vgname eq nxlabel) then begin
						st = getobj(targ,1965,tref)
						return, st
					endif
				endelse
			endif
		endwhile
	endif
	if (tag ne DFTAG_VG) then begin
		print, "tag=",tag," should be in a VGroup!"
		return, 0
	endif
	vgsub = HDF_VG_ATTACH(fhandle,ref,/READ)
	HDF_VG_GETINFO,vgsub,CLASS=clname,NAME=vgname,NENTRIES=nobjects
	HDF_VG_GETTRS,vgsub,Tags,Refs
	HDF_VG_DETACH,vgsub
	st = 0
	for i=0,nobjects-1 do begin
		if (srchtag eq DFTAG_SDG AND (Tags(i) eq DFTAG_SDG OR Tags(i) eq DFTAG_NDG)) then begin
			index = HDF_SD_REFTOINDEX(sdhandle,Refs(i))
			sds_id=HDF_SD_SELECT(sdhandle,index)
			HDF_SD_GETINFO,sds_id,NAME=vname
			HDF_SD_ENDACCESS,sds_id
			if (vname eq namepart) then begin
				st = getobj(targ,Tags(i),Refs(i))
				return, st
			endif
		endif
		if (srchtag eq DFTAG_VG AND Tags(i) eq DFTAG_VG) then begin
			vgt = HDF_VG_ATTACH(fhandle,Refs(i),/READ)
			HDF_VG_GETINFO,vgt,CLASS=clname,NAME=vgname
			HDF_VG_DETACH,vgt
			if (clname eq nxclass) then begin
				if (strpos(nxlabel,"*") ge 0) then begin
					nxlabelpart = strmid(nxlabel,0,strpos(nxlabel,"*"))
					if (strmid(vgname,0,strlen(nxlabelpart)) eq nxlabelpart) then begin
						st = getobj(targ,Tags(i),Refs(i))
						return, st
					endif
				endif else begin
					if (vgname eq nxlabel) then begin
						st = getobj(targ,Tags(i),Refs(i))
						return, st
					endif
				endelse
			endif
		endif
	endfor
	return, st
END

PRO read_data_small,str,file=file
	COMMON nexus,fhandle,sdhandle,vname,vtype,vval

	IF N_ELEMENTS(file) EQ 0 THEN file=DIALOG_PICKFILE(PATH='/home/pharos')
	fhandle = HDF_OPEN(file,/READ)
	sdhandle = HDF_SD_START(file,/READ)


	st = getobj("/NXentry:run_*/SDS:run_number",-1,-1)
	if (st ne 0) then runno=vval
	print,'Run number: ',runno

	st = getobj("/NXentry:run_*/SDS:title",-1,-1)
	if (st ne 0) then title=vval
	print,title

	st = getobj("/NXentry:run_*/SDS:start_time",-1,-1)
	if (st ne 0) then tstart=vval
	print,tstart
	st = getobj("/NXentry:run_*/SDS:end_time",-1,-1)
	if (st ne 0) then tend=vval
	print,tend

	st = getobj("/NXentry:run_*/NXinstrument:*/NXsource:*/SDS:integrated_current",-1,-1)
	if (st ne 0) then uamphrs=vval
	print,uamphrs

	st = getobj("/NXentry:run_*/NXdata:psd_y_vs_tof/SDS:data",-1,-1)
	if (st ne 0) then big=vval
	st = getobj("/NXentry:run_*/NXdata:psd_y_vs_tof/SDS:tof",-1,-1)
	if (st ne 0) then big_time=vval

	;st = getobj("/NXentry:run_*/NXdata:tof_detector_1/SDS:tof/attribute:units",-1,-1)
	;if (st ne 0) then help, vval
	;st = getobj("/NXentry:run_*/NXuser:user_*/SDS:name",-1,-1)
	;if (st ne 0) then help, vval
	;st = getobj("/NXentry:run_*/NXuser:user_*/SDS:address",-1,-1)
	;if (st ne 0) then help, vval
	HDF_SD_END,sdhandle
	HDF_CLOSE,fhandle


	size_tof=SIZE(tof,/DIMENSIONS)
	size_big=SIZE(big,/DIMENSIONS)
	size_pulse=SIZE(pulse,/DIMENSIONS)
	size_pos=SIZE(pos,/DIMENSIONS)

	str={runno:0, title:'', tstart:'', tend:'', uamphrs:0.0,	$
		big:FLTARR(size_big[0],size_big[1],size_big[2]),	$
		big_time:FLTARR(size_big[0]+1)}

	str.runno=runno
	str.title=title
	str.tstart=tstart
	str.tend=tend
	str.uamphrs=uamphrs
	str.big=big
	str.big_time=big_time/10.

END

