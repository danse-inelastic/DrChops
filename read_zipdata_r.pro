PRO READ_ZIPDATA_R, str, zipfile=zipfile
;------------------------------------------------------------------
;------------------------------------------------------------------
;-- This is a wrapper for read_data.pro to allow to read in zipped
;-- files. It unzips the file and when read_data is done with it,
;-- read_zipdata deletes the unzipped copy.
;------------------------------------------------------------------
;-- INPUTS:
;--  zipfile    the zipped data file, if not entered can be chosen
;--     from a dialog box.
;-- OUTPUTS:
;--  str    data structure
;------------------------------------------------------------------
;-- NOTES:
;--  need to change path for dialog box if change data location
;------------------------------------------------------------------
;-- 06Dec02 DinaP
;------------------------------------------------------------------
;-- MODIFICATIONS: (date, name, change description)
;------------------------------------------------------------------
;------------------------------------------------------------------

datapath = '/home/pharos/data/'
IF N_ELEMENTS(zipfile) EQ 0 THEN zipfile=DIALOG_PICKFILE(PATH=datapath)

n = STRLEN(zipfile)
npath=STRLEN(datapath)

file = STRMID(zipfile,0,n-4)

SPAWN, STRCOMPRESS("unzip "+file+".zip")

unzipfile=STRMID(file,npath,n)
print,unzipfile

read_data_r, str, file=unzipfile

;SPAWN, "rm "+unzipfile+""

END
