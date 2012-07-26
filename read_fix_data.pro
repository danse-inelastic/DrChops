;----------------------------------------------------------------------------
;----------------------------------------------------------------------------
;-- ROUTINE:    read_fix_data
;--
;-- USEAGE: read_fix_data, str
;--
;--     read_fix_data, str, filename='filename'
;--
;-- PURPOSE:    This program reads data from chosen file and outputs a
;--     data structure using function getobj included in this file.
;--
;-- INPUT:
;-- filename
;--   file to read data from; if not entered a dialog box will
;--   pop up to choose files from, to change path for the directory
;--   in the dialog box, modify 'datapath' definition.
;--
;-- OUTPUT:
;-- str
;--   Data structure to be used in further data analysis as input.
;--   Can be named differently if needed by calling
;--   >read_data, newname
;--   instead of
;--   >read_data, str
;--   but best to keep it called 'str' as further programs that use
;--   it as input, use this name in program description and comments.
;--
;-- MODIFICATIONS:
;-- 17June03; DinaP
;--   now reads zipped data files as well and deletes the
;--   unzipped file after its done
;--   added description and comments and made them of the same
;--   format as those of tvim.pro
;-- 9 April 2005; FT
;-- Version that throws out the short detectors
;-- 10 October 2006: FT
;-- Correct for swapped encoding of detectors 296-303 & 304-311
;----------------------------------------------------------------------------
;----------------------------------------------------------------------------

FUNCTION getobj,targ,tag,ref
;----------------------------------------------------------------------------
;-- function getobj gets called in read_data.pro; has to appear first in
;-- this file in order to get called in read_data successfully
;----------------------------------------------------------------------------
;----------------------------------------------------------------------------

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
if (pos eq -1) then begin   ;-- final segment
    pos=STRPOS(targ,"/attribute:")
    if (pos eq 0) then begin
       targ=STRMID(targ,11)
       ;print,"looking for attribute ",targ
       if (ref eq -1) then begin ;-- search global attributes
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
       ;----------------------------------------
        ;-- attribute is nonglobal
       ;----------------------------------------
       if (tag ne DFTAG_SDG and tag ne DFTAG_NDG) then return, 0 ; must be in SDS to get attribute
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
       if (tag ne DFTAG_VG) then return, 0   ;-- must be in VGroup to get SDS
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
;---------------------------------
;-- chase down more path segments
;---------------------------------
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

;--------------------------------------------------------------------------------------
;--------------------------------------------------------------------------------------
;--------------------------------------------------------------------------------------

PRO read_fix_data,str,filename=filename
    COMMON nexus,fhandle,sdhandle,vname,vtype,vval

    ;-------------------------------------------------------
    ;-- defining path for the dialog box, to pick files from
    ;-------------------------------------------------------
    datapath='/home/pharos/unzipped/'
    IF (N_ELEMENTS(filename) EQ 0) THEN filename=DIALOG_PICKFILE(PATH=datapath)

    ;-------------------------------------------------------
    ;-- extracting last 4 characters from file name
    ;-------------------------------------------------------
    filename_ending = STRMID(filename, 3, /REVERSE_OFFSET)

    ;-------------------------------------------------------
    ;-- comparing filename_ending to '.zip' to see if it's a
    ;-- zipped file and unzipping it if it is.
    ;-------------------------------------------------------
    IF (STRCMP('.zip', filename_ending) EQ 1) THEN BEGIN
       n = STRLEN(filename)
       npath = STRLEN(datapath)
       zip_off = STRMID(filename, 0, n-4)
       print, 'zip_off = ', zip_off
       SPAWN, STRCOMPRESS("unzip "+zip_off+".zip")
    ;  file = STRMID(zip_off, npath, n)
        file = zip_off
       print, 'now reading file ', file
    ENDIF ELSE BEGIN
       file = filename
    ENDELSE

    ;-------------------------------------------------------
    ;-- opening the file and reading data into str
    ;-------------------------------------------------------
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

    st = getobj("/NXentry:run_*/NXdata:sed_chopper_2_phase/SDS:data",-1,-1)
    if (st ne 0) then chop2=vval
    st = getobj("/NXentry:run_*/NXdata:sed_chopper_2_phase/SDS:tof",-1,-1)
    if (st ne 0) then chop2_time=vval

    st = getobj("/NXentry:run_*/NXdata:sed_chopper_1_phase/SDS:data",-1,-1)
    if (st ne 0) then chop1=vval
    st = getobj("/NXentry:run_*/NXdata:sed_chopper_1_phase/SDS:tof",-1,-1)
    if (st ne 0) then chop1_time=vval

    st = getobj("/NXentry:run_*/NXdata:sed_monitor_3_tof/SDS:data",-1,-1)
    if (st ne 0) then mon3=vval
    st = getobj("/NXentry:run_*/NXdata:sed_monitor_3_tof/SDS:tof",-1,-1)
    if (st ne 0) then mon3_time=vval

    st = getobj("/NXentry:run_*/NXdata:sed_monitor_2_tof/SDS:data",-1,-1)
    if (st ne 0) then mon2=vval
    st = getobj("/NXentry:run_*/NXdata:sed_monitor_2_tof/SDS:tof",-1,-1)
    if (st ne 0) then mon2_time=vval

    st = getobj("/NXentry:run_*/NXdata:sed_monitor_1_tof/SDS:data",-1,-1)
    if (st ne 0) then mon1=vval
    st = getobj("/NXentry:run_*/NXdata:sed_monitor_1_tof/SDS:tof",-1,-1)
    if (st ne 0) then mon1_time=vval

    st = getobj("/NXentry:run_*/NXdata:psd_tof/SDS:data",-1,-1)
    if (st ne 0) then tof=vval
    st = getobj("/NXentry:run_*/NXdata:psd_tof/SDS:tof",-1,-1)
    if (st ne 0) then tof_time=vval

    st = getobj("/NXentry:run_*/NXdata:psd_pulseheights/SDS:data",-1,-1)
    if (st ne 0) then pulse=vval

    st = getobj("/NXentry:run_*/NXdata:psd_y_vs_tof/SDS:data",-1,-1)
    if (st ne 0) then big=vval
    st = getobj("/NXentry:run_*/NXdata:psd_y_vs_tof/SDS:tof",-1,-1)
    if (st ne 0) then big_time=vval
    st = getobj("/NXentry:run_*/NXdata:psd_y_vs_tof/SDS:Y",-1,-1)
    if (st ne 0) then big_y=vval

    st = getobj("/NXentry:run_*/NXdata:psd_longitudinal_position/SDS:data",-1,-1)
    if (st ne 0) then pos=vval
    st = getobj("/NXentry:run_*/NXdata:psd_longitudinal_position/SDS:Y",-1,-1)
    if (st ne 0) then pos_y=vval

    st = getobj("/NXentry:run_*/NXdata:psd_tof/SDS:data",-1,-1)
    if (st ne 0) then tof=vval
    st = getobj("/NXentry:run_*/NXdata:psd_tof/SDS:tof",-1,-1)
    if (st ne 0) then tof_time=vval

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

    str={runno:0, title:'', tstart:'', tend:'', uamphrs:0.0,   $
       chop1:FLTARR(SIZE(chop1,/DIMENSIONS)),         $
       chop1_time:FLTARR(SIZE(chop1_time,/DIMENSIONS)),  $
       chop2:FLTARR(SIZE(chop2,/DIMENSIONS)),         $
       chop2_time:FLTARR(SIZE(chop2_time,/DIMENSIONS)),  $
       mon1:FLTARR(SIZE(mon1,/DIMENSIONS)),       $
       mon1_time:FLTARR(SIZE(mon1_time,/DIMENSIONS)),       $
       mon2:FLTARR(SIZE(mon2,/DIMENSIONS)),       $
       mon2_time:FLTARR(SIZE(mon2_time,/DIMENSIONS)),       $
       mon3:FLTARR(SIZE(mon3,/DIMENSIONS)),       $
       mon3_time:FLTARR(SIZE(mon3_time,/DIMENSIONS)),       $
       tof:FLTARR(size_tof[0],size_tof[1] - 16),        $
       tof_time:FLTARR(size_tof[0]+1),          $
       big:FLTARR(size_big[0],size_big[1],size_big[2] - 16), $
       big_y:FLTARR(size_big[1]+1),          $
       big_time:FLTARR(size_big[0]+1),          $
       pulse:INTARR(size_pulse[1],size_pulse[1],size_pulse[2] - 16),$
       pos:INTARR(size_pos[0],size_pos[1] - 16),        $
       pos_y:FLTARR(size_pos[0]+1)}

    str.runno=runno
    str.title=title
    str.tstart=tstart
    str.tend=tend
    str.uamphrs=uamphrs
    str.chop1=chop1
    str.chop1_time=chop1_time/10.
    str.chop2=chop2
    str.chop2_time=chop2_time/10.
    str.mon1=mon1
    str.mon1_time=mon1_time/10.
    str.mon2=mon2
    str.mon2_time=mon2_time/10.
    str.mon3=mon3
    str.mon3_time=mon3_time/10.
    str.big_time=big_time/10.
    str.big_y=big_y
    str.tof_time=tof_time/10.
    str.pos_y=pos_y
    str.pos_y=pos_y

; fix for incorrectly encoded detectors during 06

    FOR i = 0,23 DO BEGIN
      str.big[*,*,i]=big[*,*,i]
      str.tof[*,i]=tof[*,i]
      str.pos[*,i]=pos[*,i]
      str.pulse[*,i]=pulse[*,i]
    ENDFOR

    FOR i = 24,295 DO BEGIN
      str.big[*,*,i]=big[*,*,i + 16]
      str.tof[*,i]=tof[*,i + 16]
      str.pos[*,i]=pos[*,i + 16]
      str.pulse[*,*,i]=pulse[*,*,i + 16]
    ENDFOR
    FOR i = 296,303 DO BEGIN
      str.big[*,*,i]=big[*,*,i + 24]
      str.tof[*,i]=tof[*,i + 24]
      str.pos[*,i]=pos[*,i + 24]
      str.pulse[*,*,i]=pulse[*,*,i + 24]
    ENDFOR
    FOR i = 304,311 DO BEGIN
      str.big[*,*,i]=big[*,*,i + 8]
      str.tof[*,i]=tof[*,i + 8]
      str.pos[*,i]=pos[*,i + 8]
      str.pulse[*,*,i]=pulse[*,*,i + 8]
    ENDFOR
    FOR i = 312,375 DO BEGIN
      str.big[*,*,i]=big[*,*,i + 16]
      str.tof[*,i]=tof[*,i + 16]
      str.pos[*,i]=pos[*,i + 16]
      str.pulse[*,*,i]=pulse[*,*,i + 16]
    ENDFOR

    swap_chan, str, 286, 287
    swap_chan, str, 305, 306
    swap_chan, str, 310, 311
    swap_chan, str, 336, 338


    ;-------------------------------------------------------------
    ;-- if the data file was unzipped deleting its unzipped copy
    ;-------------------------------------------------------------
    IF (STRCMP('.zip', filename_ending) EQ 1) THEN SPAWN, "rm "+file+""

END

PRO swap_chan,str,index1,index2

    tmp=str.tof[*,index1]
    str.tof[*,index1]=str.tof[*,index2]
    str.tof[*,index2]=tmp

    tmp=str.big[*,*,index1]
    str.big[*,*,index1]=str.big[*,*,index2]
    str.big[*,*,index2]=tmp

    tmp=str.pos[*,index1]
    str.pos[*,index1]=str.pos[*,index2]
    str.pos[*,index2]=tmp

    tmp=str.pulse[*,*,index1]
    str.pulse[*,*,index1]=str.pulse[*,*,index2]
    str.pulse[*,*,index2]=tmp
END
