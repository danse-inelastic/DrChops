from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211651474.232964
_template_filename=u'/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/footer.mako'
_template_uri=u'/footer.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        # SOURCE LINE 1
        context.write(u'    <div id="ft">\n        <div class="center">\n            <div class="footer-padding">\n            <p><a href="#top" accesskey="9" title=\n            "Return to the top of the navigation links">Top</a>\n\t    </p>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


