from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211654737.3556941
_template_filename='/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/lrmecs2ascii/form.mako'
_template_uri='/lrmecs2ascii/form.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'<div id="bd">\n<div class="yui-g">\n\n\n<div class="rst-doc">\n\n\n')
        # SOURCE LINE 8
        context.write(unicode( h.form(h.url(action='upload'), multipart=True) ))
        context.write(u'\n<h1>Convert LRMECS data file in binary format to ascii format</h1>\n<p>\nUpload lrmecs data file in binary format: \n')
        # SOURCE LINE 12
        context.write(unicode( h.file_field('uploaded_file') ))
        context.write(u' <br />\n</p>\n<p></p>\n<p>\n')
        # SOURCE LINE 16
        context.write(unicode( h.submit('Submit') ))
        context.write(u'\n</p>\n')
        # SOURCE LINE 18
        context.write(unicode( h.end_form() ))
        context.write(u'\n\n\n</div> <!--rst-doc-->\n\n\n</div>\n</div>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


