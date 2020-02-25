import dia
import gtk
import sm_export_cfg
import sm_export_fsm

def delete_event(widget, event, data):
    data.save()
    return False
   
def warn_callback(widget, data):
    data.warn_connections = widget.get_active()

def header_file_callback(widget,data):
    data.header_file = widget.get_active()

def debug_state_change_cb(widget,data):
    data.debug_state_change = widget.get_active()

def multithread_enable_cb(widget,data):
    data.multithread_enable = widget.get_active()

def sm_export_version_cb(data,flags):
    cfg = sm_export_cfg.SmExportCfg()
    # Create a new window
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    # Set the window title
    window.set_title("FSM exporting tool version") 

    # Set a handler for delete_event that immediately
    # exits GTK.
    window.connect("delete_event", delete_event,cfg)

    # Sets the border width of the window.
    window.set_border_width(20)

    #Set window size
    window.set_default_size(400, 100)

    # Create a vertical box
    vbox = gtk.VBox(True)

    # Put the vbox in the main window
    window.add(vbox)
    
    # Create label
    label = gtk.Label("Version: %s" % sm_export_fsm.SM_EXPORT_VERSION)
    vbox.pack_start(label, True, True )
    label.show()

    vbox.show()
    window.show() 
    return 0

def sm_export_cfg_cb(data, flags) :
    cfg = sm_export_cfg.SmExportCfg()
    # Create a new window
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    # Set the window title
    window.set_title("FSM exporting tool configuration") 

    # Set a handler for delete_event that immediately
    # exits GTK.
    window.connect("delete_event", delete_event,cfg)

    # Sets the border width of the window.
    window.set_border_width(20)

    #Set window size
    window.set_default_size(400, 200)

    # Create a vertical box
    vbox = gtk.VBox(True, 3)

    # Put the vbox in the main window
    window.add(vbox)

    # Create first button
    button = gtk.CheckButton("Warn when not all events are weighted")
    button.set_active(cfg.warn_connections)

    # When the button is toggled, we call the "callback" method
    # with a pointer to "button" as its argument
    button.connect("toggled", warn_callback,cfg)
    # Insert button 1
    vbox.pack_start(button, True, True, 3)

    button2 = gtk.CheckButton("Create separated header file for data types definition")
    button2.set_active(cfg.header_file)
    button2.connect("toggled",header_file_callback,cfg)
    vbox.pack_start(button2, True, True, 3)

    button3 = gtk.CheckButton("Log state changes of the FSM")
    button3.set_active(cfg.debug_state_change)
    button3.connect("toggled",debug_state_change_cb,cfg)
    vbox.pack_start(button3, True, True, 3)

    button4 = gtk.CheckButton("Enable multithreading code")
    button4.set_active(cfg.multithread_enable)
    button4.connect("toggled",multithread_enable_cb,cfg)
    vbox.pack_start(button4, True, True, 3)

    button.show()
    button2.show()
    button3.show()
    button4.show()
    vbox.show()
    window.show() 

    return 0

dia.register_action ("sm_export_cfg", "Configuration of FSM exporting tool", 
                       "/DisplayMenu/Dialogs/DialogsExtensionStart", 
                       sm_export_cfg_cb)

dia.register_action ("sm_export_version", "FSM exporting tool version", 
                       "/DisplayMenu/Dialogs/DialogsExtensionStart",
                       sm_export_version_cb)
