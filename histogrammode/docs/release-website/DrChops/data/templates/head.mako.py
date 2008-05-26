from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
_magic_number = 2
_modified_time = 1211651648.0733571
_template_filename=u'/home/drcsweb/dv/danse/buildInelast/DrChops-1.3pre1-website/src/DrChops/drchops/templates/head.mako'
_template_uri=u'/head.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack.push_frame()
    try:
        __M_locals = dict(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        # SOURCE LINE 1
        context.write(u'<head>\n    <title>')
        # SOURCE LINE 2
        context.write(unicode( c.title ))
        context.write(u'</title>\n<meta name="verify-v1" content="Hwu1zNHSgb3EjnnGq5164NXhLQwIckGnWEAxXiQ8qmA=" />\n    <meta http-equiv="content-type" content="text/html; charset=utf-8" />\n    <meta name="ROBOTS" content="ALL" />\n    <meta name="description" content="')
        # SOURCE LINE 6
        context.write(unicode(c.description))
        context.write(u'" />\n    <meta name="keywords" content=\n    "DANSE, neutron, scattering, science, python, reduction, ARCS, GUI, Density of States, Phonon" />\n    \n    \n    <!-- CSS Imports -->\n    <link rel="stylesheet" href="/style/reset-fonts-grids.css" type="text/css" media="screen" title="YUI Grids" charset="utf-8">    \n    <!--<link rel="stylesheet" href="/style/green.css" type="text/css" media="screen" />-->\n    <link rel="stylesheet" href="/style/blue.css" type="text/css" media="screen" />\n    <link rel="stylesheet" href="/style/silvercity.css" type="text/css" media="screen" />\n    <link type="text/css" rel="stylesheet" href="/style/pygments_default.css" />\n    \n\n    <!-- Favorite Icons -->\n    <!-- <link rel="icon" href="/img/green/icon-16.png" type="image/png" /> -->\n    \n</head>\n')
        return ''
    finally:
        context.caller_stack.pop_frame()


