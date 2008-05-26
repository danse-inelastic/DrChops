from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211651648.0665231
_template_filename='/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/main.mako'
_template_uri='/main.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        # SOURCE LINE 1
        context.write(u'<html xmlns="http://www.w3.org/1999/xhtml" charset="utf-8">\n')
        # SOURCE LINE 2
        runtime._include_file(context, u'head.mako', _template_uri)
        context.write(u'\n<body>\n')
        # SOURCE LINE 4
        runtime._include_file(context, u'header.mako', _template_uri)
        context.write(u'\n    <!-- Main Content -->\n    \n')
        # SOURCE LINE 7
        runtime._include_file(context, u'page.mako', _template_uri)
        context.write(u'\n\n')
        # SOURCE LINE 9
        runtime._include_file(context, u'footer.mako', _template_uri)
        context.write(u'\n\n</div>\n</body>\n</html>\n\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


