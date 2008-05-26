from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211652234.8169949
_template_filename='/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/Home.mako'
_template_uri='/Home.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'<div id="bd">\n<div class="yui-g">\n\n\n<div class="rst-doc">\n\n\n')
        # SOURCE LINE 8
        context.write(unicode(c.doc))
        context.write(u'\n\n\n</div> <!--rst-doc-->\n\n\n</div>\n</div>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


