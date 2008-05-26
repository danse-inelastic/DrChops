from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211653012.3008609
_template_filename='/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/FAQ.mako'
_template_uri='/FAQ.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'<div id="bd">\n<div class="yui-g">\n\n\n<div class="rst-doc">\n\n\n<h1 class="pudge-member-page-heading">Frequently Asked Questions</h1>\n\n')
        # SOURCE LINE 10

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
        
        
        __M_locals.update(dict([(__M_key, locals()[__M_key]) for __M_key in ['a','pruned','qas','al','q','records','r','inanswer'] if __M_key in locals()]))
        # SOURCE LINE 34
        context.write(u'\n\n</div> <!--rst-doc-->\n\n\n</div>\n</div>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


