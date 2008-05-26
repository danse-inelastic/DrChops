
from Menu import MenuItem, Menu
menuitems = [
    MenuItem( "Home", link = '/Home' ),
    MenuItem( "Docs", link = '/Docs'),
    #MenuItem( "Wiki", link = '/Wiki/Blank'),
    MenuItem( "Trac", link = '/Trac'),
    MenuItem( "FAQ", link = '/FAQ'),
    MenuItem( "Install", link = '/Install'),
    ]
mainmenu = Menu( menuitems )
del menuitems
