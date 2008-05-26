from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211651910.4277079
_template_filename=u'/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/page.mako'
_template_uri=u'/page.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        # SOURCE LINE 1
        context.write(u"<div class='main-content'>\n")
        # SOURCE LINE 2
        context.write(unicode(c.page))
        context.write(u'\n</div>')
        return ''
    finally:
        context.caller_stack.pop_frame()


