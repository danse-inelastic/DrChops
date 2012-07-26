;____________________________________________________________
; This is a wrapper for read_data.pro to allow to read
; in zipped files. It unzips the file and when 
; read_data is done with it, read_zipdata deletes the 
; unzipped copy.
; INPUTS:
;	zipfile = the zipped data file, if not entered 
;		 can be chosen from a dialog box.
; OUTPUTS:
;	str = data structure
; NOTES: 
;	need to change path for dialog box if change
; 	data location
; Dina, 6Dec02
;------------------------------------------------------------

PRO READ_ZIPDATA, str, zipfile=zipfile

datapath = '/home/zorak/cemin5/'
IF N_ELEMENTS(zipfile) EQ 0 THEN zipfile=DIALOG_PICKFILE(PATH=datapath)

n = STRLEN(zipfile)
npath=STRLEN(datapath)
 
file = STRMID(zipfile,0,n-4)

SPAWN, STRCOMPRESS("unzip "+file+".zip")
 
unzipfile=STRMID(file,npath,n)
print,unzipfile

read_data, str, file=unzipfile

SPAWN, "rm "+unzipfile+""

END
