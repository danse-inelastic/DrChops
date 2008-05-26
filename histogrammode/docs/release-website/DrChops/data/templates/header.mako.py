from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211651648.0849791
_template_filename=u'/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/header.mako'
_template_uri=u'/header.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'<div id="custom-doc" class="yui-t4">\n\n    <!-- We are only using a table to ensure old browsers see the message correctly -->\n    <a name="top"></a>\n    <noscript>\n        <div style="border-bottom: 1px solid #808080">\n            <div style="border-bottom: 1px solid #404040">\n                <table width="100%" border="0" cellpadding="0" bgcolor="#FFFFE1">\n                    <tr>\n                        <td valign="middle"><img src="/img/green/warning.gif" alt="Warning" /></td>\n                        <td>&nbsp;</td>\n                        <td><span style=\n                            "padding: 0px; margin: 0px; font-family: Tahoma, sans-serif; font-size: 11px">\n                            Warning, your browser does not support JavaScript and is not\n                            capable of displaying the latest web pages such as this one.</span></td>\n                    </tr>\n                </table>\n            </div>\n        </div>\n    </noscript>\n\n    <div id="hd">\n        <div id="logo"><h1 class="invisible"></h1></div>\n        <div id="download">Latest Version: <a href="/Install">')
        # SOURCE LINE 24
        context.write(unicode(c.latest_version))
        context.write(u'</a></div>\n        <div id="nav-items">\n\n<div id="nav-bar">\n<ul id="navlist">\n\n')
        # SOURCE LINE 30

        t={ True: '<li class="active"> <a href="%s" accesskey="%s" class="active"> %s </a></li>', False: '<li><a href="%s" accesskey="%s"> %s </a></li>', }
        for item in c.navigator.items:
          tt = t[item.active] % (item.link, item.accesskey, item.name)
          context.write( tt )
        
        
        __M_locals.update(dict([(__M_key, locals()[__M_key]) for __M_key in ['item','tt','t'] if __M_key in locals()]))
        # SOURCE LINE 35
        context.write(u'\n\n</ul>\n</div>\n</div>\n</div>\n    \n')
        return ''
    finally:
        context.caller_stack.pop_frame()


