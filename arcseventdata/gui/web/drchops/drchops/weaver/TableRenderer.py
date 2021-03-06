# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class TableRenderer:

    def onTable(self, table):
        director = self.director
        home = director.home
        cgihome = director.cgihome
        
        csscode = []
        csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/tabulator/datePicker.css" />' % home )
        csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/tabulator/tabulator.css" />' % home )
        csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/tabulator/tabulator-color.css" />' % home )

        htmlcode = []
        gid = id(table)
        htmlcode.append( '<div id="%s">' % gid )
        htmlcode.append( '</div>' )

        includes = []
        javascriptpath = os.path.join(director.home, 'javascript')
        
        includes.append( '<SCRIPT src="%s/jquery/jquery.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/date.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/jquery.datePicker.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/tabulator.js"></SCRIPT>' % javascriptpath )

        jscode = []
        jscode.append('''
function make_form() {
  return $( '<form> </form>' );
}
''')
        jscode.append('''
function make_table_skeleton( ) {
  
  table = $( '<table border="1"></table>' );
  
  thead = $( '<thead></thead' );
  table.append(thead);
  
  headrow = $( '<tr></tr>' );
  thead.append( headrow );

  tbody = $( '<tbody></tbody>' );
  table.append( tbody );
  
  return table;
}
''')

        jscode.append('''
function add_headcell( id, text, headrow )
{
  cell = $( '<td id="' + id + '">' + text + '</td>' );
  headrow.append( cell );
}
''')

        jscode.append('''
function establish_headrow_from_column_descriptors( headrow, descriptors )
{
  for (var colid in descriptors) {
    descriptor = descriptors[ colid ];
    add_headcell( colid, descriptor.text, headrow );
  }
}
''')

        jscode.append('''
function make_table_head( thetable, descriptors ) {

  thead = $(thetable.children( 'thead' )[0]);
  headrow = $(thead.children( 'tr' )[0]);
  
  establish_headrow_from_column_descriptors( headrow, descriptors );
  thetable.table_setcolumndescriptors( descriptors );

}
''')

        jscode.append( '''
function make_table( div, descriptors ) {
  
  // table skeleton
  thetable = make_table_skeleton();

  // add table to a form
  form = make_form();
  form.append( thetable );
  
  // add form to the division
  div.append( form );
  
  // contents of table
  // head
  make_table_head( thetable, descriptors );
}
''');
        jscode.append( '$(document).ready(function() {')
        
        jscode.append( 'Date.firstDayOfWeek = 7;')
        jscode.append( 'Date.format = "mm/dd/yyyy";' )
        
        jscode.append( 'thetable = $("#%s");' % gid )
        descriptors = table.column_descriptors
        jscode.append(
            'descriptors={%s};' %
            ','.join( [jscode_descriptor( d ) for d in descriptors] )
            )
        jscode.append( 'make_table( thetable, descriptors);' )

        for i, row in enumerate(table.rows):
            jscode.append(
                'thetable.table_appendrow_dataonly(%d, [%s]);' %
                (i, ','.join( ['%r' % v for v in row] ) )
                )
            continue

        jscode.append( 'thetable.addClass( "tabulated" );' );

        jscode.append( '''
    thetable.find( 'tbody' ).find( "td[datatype=text]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );
''')
        
        jscode.append( '''
    thetable.find( 'tbody' ).find( "td[datatype=money]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );
''')

        jscode.append( '''
    thetable.find( 'tbody' ).find( "td[datatype=single_choice]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );
''')

        jscode.append( '''
    thetable.find( 'tbody' ).find( "td[datatype=date]" ).dblclick( function () {
	$(this).enable_cell_editing();
      } );
''')

        jscode.append( '});' );
        
        codes = csscode + includes + ['<script>']  + jscode + ['</script>'] + htmlcode
        return codes


def jscode_descriptor( descriptor ):
    d = { 'text': descriptor.text, 'datatype': descriptor.datatype }
    d.update(descriptor.options)
    
    return "%r : { %s }" % (descriptor.id, ','.join(
        [ '%s: %r' % (k,v) for k,v in d.iteritems() ] ) )


import os

# version
__id__ = "$Id$"

# End of file 
