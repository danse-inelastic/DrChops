#!/usr/bin/env python

def main():
    from reduction.applications.gui.FrontPanel.MainWindowApp import MainWindowApp

    applications = [
        { "name": "Lrmecs", "exe": "wxLrmecsReductionApp.py" },
        { "name": "Pharos", "exe": "wxPharosReductionApp.py" },
        #{ "name": "ARCS", "exe": "wxARCSReductionApp.py" },
        ]
    
    app = MainWindowApp(
        applications ,
        )

    app.MainLoop()
    return


if __name__ == "__main__" : main()
