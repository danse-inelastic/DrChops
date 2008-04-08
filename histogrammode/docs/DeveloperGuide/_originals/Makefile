targets = \
	Docs.xmlt \
	HistogramViewer_Tutorial.xmlt \
	Install.xmlt \
	InstallFromBinaries.xmlt \
	InstallFromSource.xmlt \
	LRMECS_Reduction_GUI_Tutorial.xmlt \
	LRMECS_Reduction_commandline_Tutorial.xmlt \
	PHAROS_Reduction_GUI_Tutorial.xmlt \
	PHAROS_Reduction_commandline_Tutorial.xmlt \
	Prepare_Lrmecs_Reduction_Directory.xmlt \
	Prepare_Pharos_Reduction_Directory.xmlt \
	ReductionFlowCharts.xmlt \
	reduction-debug.xmlt \


%.xmlt: %.wml
	./wml2db.py $< $@


all: $(targets)

