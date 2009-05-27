<div id="custom-doc" class="yui-t4">

    <!-- We are only using a table to ensure old browsers see the message correctly -->
    <a name="top"></a>
    <noscript>
        <div style="border-bottom: 1px solid #808080">
            <div style="border-bottom: 1px solid #404040">
                <table width="100%" border="0" cellpadding="0" bgcolor="#FFFFE1">
                    <tr>
                        <td valign="middle"><img src="/img/green/warning.gif" alt="Warning" /></td>
                        <td>&nbsp;</td>
                        <td><span style=
                            "padding: 0px; margin: 0px; font-family: Tahoma, sans-serif; font-size: 11px">
                            Warning, your browser does not support JavaScript and is not
                            capable of displaying the latest web pages such as this one.</span></td>
                    </tr>
                </table>
            </div>
        </div>
    </noscript>

    <div id="hd">
        <div id="logo" onclick="window.location='http://danse.us';"><h1 class="invisible" ></h1></div>
        <div id="download">Latest Version: <a href="/Install">${c.latest_version}</a></div>
        <div id="nav-items">

<div id="nav-bar">
<ul id="navlist">

<%
t={ True: '<li class="active"> <a href="%s" accesskey="%s" class="active"> %s </a></li>', False: '<li><a href="%s" accesskey="%s"> %s </a></li>', }
for item in c.navigator.items:
  tt = t[item.active] % (item.link, item.accesskey, item.name)
  context.write( tt )
%>

</ul>
</div>
</div>
</div>
    
