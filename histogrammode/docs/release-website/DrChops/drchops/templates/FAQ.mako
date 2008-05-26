<div id="bd">
<div class="yui-g">


<div class="rst-doc">


<h1 class="pudge-member-page-heading">Frequently Asked Questions</h1>

<%
print 'OK1'
qas = c.doc
records = [ r.strip() for r in qas.splitlines() ]
pruned = []
for r in records:
  if len(r)==0: pass
  pruned.append(r)
  continue
qas = []
inanswer = False
a = ''
for r in pruned :
  if r.startswith( 'Q:'): 
    if len(a) > 0: qas.append( (q,a) )
    a = ''
    q = r; continue
  al = r # a line of answer
  if al.startswith( "A:" ): al = al[2:]
  a += ' ' + al
qas.append( (q,a) )
for q,a in qas:
  context.write( '<p><strong>%s</strong></p>' % q)
  context.write( '<blockquote><p>%s</p></blockquote>' % a )
%>

</div> <!--rst-doc-->


</div>
</div>
