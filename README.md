# Wiki-Web #
This is my first attempt at a wikipedia visualizer
I already want to rewrite the renderer such that we can display the page relationships visually rather than in tabular format.  Probably with OpenGL, either in a Gtk widget or a custom SDL window.  

## TODO ##
* Fix Comments  
* Fix highlights so it properly lets the user know the path they have taken  
* Put the WebKit widget URL loading in to a thread so the UI doesn't hang  
** What is going to happen while the thread is loading and we click on links?  
* Hide the sidebar and top of the wiki pages  
* Connect URL's in the wiki page to the UI  
** Any clicked link will go in to the center node I guess?  
* Rename node columns  
* Fix initial size of window  
* Investigate Gtk-WARNING's and make them stop  
* Design application start  
** How should we get the root node?  
* Unit Tests  
** Finish up window.py
