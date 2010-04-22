out1=ARCS-allpixels.par
make-tobyfit-par.py --x=ARCS.xml --o=$out1
diff $out1 oracle/tobyfit-pars/$out1

out2=ARCS-res2.par
make-tobyfit-par.py --x=ARCS.xml --r=2 --o=$out2
diff $out2 oracle/tobyfit-pars/$out2
