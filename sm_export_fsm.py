import dia
import os
import sm_export_cfg

class Transition :
    def __init__(self) :
        self.trigger = ""
        self.action = ""
        self.source = ""
        self.target = ""
        self.guard = ""
        self.priority=0
    
    def set_source(self,state):
        self.source = state
    
    def set_target(self,state):
        self.target = state
    
    def set_action(self,action):
        if action == "(NULL)":
            self.action = ""
        else:
            self.action = action    
    
    def set_trigger(self,trigger):
        idx = trigger.find(":")
        if idx > -1:
            self.priority=int(trigger[:idx])
            self.trigger = trigger[idx+1:]
            return True
        else:
            self.priority = 0
            if trigger == "(NULL)":
                self.trigger = ""
            else:
                self.trigger = trigger
            return False

    def set_guard(self,guard):
        if guard == "(NULL)" :
            self.guard = ""
        else:
            self.guard = guard
            
    def has_trigger(self):
        if len(self.trigger) > 0:
            return True
        else:
            return False
    
    def is_conditional(self):
        if (self.guard is not None and len(self.guard) > 0):
            return True
        else:
            return False

    def __str__(self):
        return "Trigger=%s  Action=%s Source=%s Target=%s Guard=%s Priority=%d" % (self.trigger,self.action,self.source,self.target,self.guard,self.priority)


class State :
    def __init__(self) :
        self.name = ""    
        self.iaction = ""
        self.oaction = ""
        self.do_action = ""
        self.type = 0        
        self.aux = ""
    
    def set_name(self,name):
        self.name = name
    
    def set_do_action(self,action):
        if action == "(NULL)":
            self.do_action = ""
        else:
            self.do_action = action
    
    def set_input_action(self,action):
        if action == "(NULL)":
            self.iaction = ""
        else:
            self.iaction = action
    
    def set_output_action(self,action):
        if action == "(NULL)":
            self.oaction = ""
        else:
            self.oaction = action
    def set_type(self,type):
        self.type = type                
    
    def set_aux(self,aux):
        self.aux = aux      

    def get_transitions(self,transitions):
        st_transitions = []
        for transition in transitions:
            if transition.source == self.name:
                st_transitions.append(transition)
        # Sorting st_transitions list by priority of transition
        for i in range(0, len(st_transitions)-1):
            for j in range(i+1, len(st_transitions)):
                if st_transitions[i].priority > st_transitions[j].priority:
                    aux = st_transitions[i]
                    st_transitions[i] = st_transitions[j]
                    st_transitions[j] = aux
        return st_transitions    

 
class DiagramRenderer :
    def __init__(self) :
        self.filename = ""   
        self.basename = ""
        self.states = {}
        self.transitions = []
        self.show_priority_warning  = False
        self.cfg = sm_export_cfg.SmExportCfg()

    def get_first_state_name(self):
        for t in self.transitions:
            if t.source ==  "INITIAL_STATE":
                return t.target
        return "Error"

    def begin_render (self, data, filename) :
        self.states = {}
        self.transitions = []
        self.generate_files = True
        self.filename, self.file_extension = os.path.splitext(filename)                
        self.basename = os.path.splitext(os.path.basename(self.filename+self.file_extension))[0]
        for layer in data.layers :
            for o in layer.objects :                            
                if o.type.name == "UML - State" :
                    state = State()
                    # properties are: ['obj_pos', 'obj_bb', 'elem_corner', 'elem_width' ,'elem_height', 'type','line_colour', 'fill_colour', 'text_font', 'text_height', 'text_colour', 'text', 'entry_action', 'do_action', 'exit_action' ]
                    state.set_name(o.properties["text"].value.text.strip())                                        

                    try :
                        p = o.properties["do_action"].value                        
                    except :
                        p = None                    
                    state.set_do_action(str(p))

                    try :
                        p = o.properties["entry_action"].value                        
                    except :
                        p = None                    
                    state.set_input_action(str(p))
                    
                    try :
                        p = o.properties["exit_action"].value                        
                    except :
                        p = None                                        
                    state.set_output_action(str(p))                    
                    state.set_type(STANDARD_STATE)
                    self.states[state.name] = state                    
                #elif o.type.name == "UML - State Term" :    
                    # properties are:[ 'obj_pos', 'obj_bb', 'elem_corner', 'elem_width', 'elem_height', 'is_final']                    
                elif o.type.name == "UML - Transition" :
                    # properties are: ['obj_pos', 'obj_bb', 'orth_points', 'orth_orient', 'orth_autoroute', 'trigger', 'action', 'guard', 'trigger_text_pos', 'guard_text_pos', 'direction_inverted']
                    transition = Transition()
                    try :
                        source = o.handles[0].connected_to.object
                    except AttributeError:
                        #Launch an error(2) message
                        dia.message(2, "The source of '%s' transition is wrong connected.\nDiagram will not be exported until the error is solved.\n" % o.properties["trigger"].value)
                        self.generate_files = False

                    try :
                        target = o.handles[1].connected_to.object
                    except AttributeError:
                        #Launch an error(2) message
                        dia.message(2, "The destination of '%s' transition is wrong connected.\nDiagram will not be exported until the error is solved.\n" % o.properties["trigger"].value)
                        self.generate_files = False

                    if source.type.name ==  "UML - State Term":
                        if not source.properties["is_final"].value :
                            transition.set_source("INITIAL_STATE")
                    elif source.type.name == "UML - State":
                         transition.set_source(source.properties["text"].value.text)

                    if target.type.name ==  "UML - State Term":                        
                        if target.properties["is_final"].value :
                            transition.set_target("FINAL_STATE")
                    elif target.type.name == "UML - State":
                        transition.set_target(target.properties["text"].value.text)
                        
                    try:
                        trigger = o.properties["trigger"].value
                    except:
                        trigger = ""

                    priority_assigned = transition.set_trigger(str(trigger))
                    if not priority_assigned:
                        self.show_priority_warning = True
                    
                    try:
                        guard = o.properties["guard"].value
                    except:
                        guard = ""
                    if len(guard) > 0:
                        transition.set_guard(str(guard))

                    try:
                        transition.set_action(o.properties["action"].value) 
                    except:
                        action = ""
                    self.transitions.append(transition)
 
    def write_machine_generated_warning(self,f):
        f.write("//Machine generated file, do not edit!!!\n")
        f.write("//Generated by sm_export_fsm.py script for DIA\n")
        f.write("//Script version:%s\n\n" % SM_EXPORT_VERSION)

    def write_fsm_file_sentinel(self,f):
        f.write("#ifndef "+self.basename.upper()+"_FSM\n")
        f.write("#define "+self.basename.upper()+"_FSM\n\n")

    def write_fsm_file_end_sentinel(self,f):
        f.write("#endif /* "+self.basename.upper()+"_FSM */")

    def write_header_file_sentinel(self,f):
        f.write("#ifndef "+self.basename.upper()+"_H\n")
        f.write("#define "+self.basename.upper()+"_H\n\n")
        
    def write_header_file_end_sentinel(self,f):
        f.write("\n#endif /* "+self.basename.upper()+"_H */\n")

    def end_render(self) :
        if self.generate_files:    
            self.cfg.load()
            f = open(self.filename+self.file_extension, "w")    
            self.write_machine_generated_warning(f)
            self.write_fsm_file_sentinel(f)
            if self.cfg.header_file:
                h = open(self.filename+".h","w")
                self.write_machine_generated_warning(h)
                self.write_header_file_sentinel(h)
                self.generate_includes(h)
                self.generate_events_defines(h)
                self.generate_states_typedef(h)
                self.generate_object(h)
                self.write_header_file_end_sentinel(h)
                f.write("#include \"%s\"\n" % (self.basename+".h"))
                f.write("\n")
            else:
                self.generate_includes(f)
                self.generate_events_defines(f)
                self.generate_states_typedef(f)
                self.generate_object(f)

            self.generate_funcs_decl(f)
            self.generate_internal_funcs_decl(f)
            self.generate_st_change_func(f)
            self.generate_raw_funcs(f)
            self.generate_events_fire_funcs(f)
            self.generate_init_func(f)
            self.generate_get_state_func(f)
            self.write_fsm_file_end_sentinel(f)
            f.close()
            if self.cfg.header_file:
                h.close()
            if self.show_priority_warning and self.cfg.warn_connections :
                #Launch a warning(1) message 
                dia.message(1, "Not all transitions has priority assigned!\nDiagram has been exported but is up to you if transitions are right\n")
        else:
            print("File will be generated in blank until errors are solved.")

    def generate_st_change_func(self,f):
        if self.cfg.debug_state_change:
            f.write("static const char* %s_state2txt(%s_fsm_st_t st)\n" % (self.basename,self.basename))
            f.write("{\n")
            f.write("\tswitch(st)\n\t{\n")
            for key in self.states.keys():
                state = self.states[key].name
                f.write('\tcase %s_%s_fsm_st: return "%s_%s_fsm_st";\n' %(self.basename,state,self.basename,state))
            f.write('\tdefault:return "unknown state";\n')
            f.write('\t}\n')
            f.write("}\n\n")
        f.write("static void %s_st_change(%s* fsm, %s_fsm_st_t target)\n{\n" % (self.basename,self.get_fsm_type_name(),self.basename))
        f.write("\tfsm->previous_state = fsm->current_state;\n")
        f.write("\tfsm->current_state = target;\n")
        if self.cfg.debug_state_change:
            f.write("\tfsm_api_debug(fsm->api, fsm->user_data);\n")
        f.write("}\n\n")

    def generate_internal_funcs_decl(self,f):
        f.write("/* Internal function declarations */\n")
        f.write("static const char* %s_state2txt(%s_fsm_st_t st);\n" % (self.basename,self.basename))
        f.write("static void %s_st_change(%s* fsm, %s_fsm_st_t target);\n" % (self.basename,self.get_fsm_type_name(),self.basename))
        type_name = self.get_fsm_type_name()
        f.write("static void %s_fsm_tick(%s* fsm);\n" % (self.basename,type_name))
        generated=[]
        for transition in self.transitions:
            if len(transition.trigger) > 0:
                if transition.trigger not in generated:
                    generated.append(transition.trigger)
                    f.write("void %s_fire_%s_event(%s* fsm);\n" % (self.basename,transition.trigger,self.get_fsm_type_name()))
        f.write("void %s_fsm_init(%s* fsm, fsm_api_t* fsm_api, void* fsm_user_data);\n" % (self.basename,self.get_fsm_type_name()))
        f.write("%s_fsm_st_t %s_get_state(%s* fsm);\n" % (self.basename,self.basename,self.get_fsm_type_name()))
        f.write("\n")

    def generate_funcs_decl(self,f):
        generated=[]
        generated_conditions=[]
        for key in self.states.keys():
            state = self.states[key]
            if len(state.do_action) > 0 and (state.do_action not in generated):
                f.write("static void %s_%s_action(%s* fsm);\n" % (self.basename,state.do_action,self.get_fsm_type_name()))
                f.write("static bool %s_%s_action_able(%s* fsm);\n" % (self.basename,state.do_action,self.get_fsm_type_name()))
                generated.append(state.do_action)
            if len(state.iaction) > 0 and (state.iaction not in generated):
                f.write("static void %s_%s_action(%s* fsm);\n" % (self.basename,state.iaction,self.get_fsm_type_name()))
                generated.append(state.iaction)
            if len(state.oaction) > 0 and (state.oaction not in generated):
                f.write("static void %s_%s_action(%s* fsm);\n" % (self.basename,state.oaction,self.get_fsm_type_name()))
                generated.append(state.oaction)
            transitions = state.get_transitions(self.transitions)
            for transition in transitions:
                if (transition.action not in generated) and (len(transition.action) > 0):
                    f.write("static void %s_%s_action(%s* fsm);\n" % (self.basename,transition.action,self.get_fsm_type_name()))
                    generated.append(transition.action)
                if (transition.guard not in generated_conditions) and (transition.guard is not None) and (len(transition.guard) > 0):
                    f.write("static bool %s_%s_condition(%s* fsm);\n" % (self.basename,transition.guard,self.get_fsm_type_name()))
                    generated_conditions.append(transition.guard)
        f.write("\n")

    def particular_state_action(self,*args):
        """Outputs the actions needed for a given state.
        Parameters:
            args: is a variable list of arguments
                args[0]:File descriptor to write the output
                args[1]:Transition object
                args[2]:Condition object
                args[3]:Prefix string to tab the name of the functions
        """
        f=args[0]
        condition=args[2]
        prefix=args[3]
        f.write("%sfsm->events = 0;\n" % prefix)
        transition_str=args[1].action
        source = args[1].source
        if len(self.states[source].oaction) > 0:
            f.write("%s%s_%s_action(fsm);\n" % (prefix,self.basename,self.states[source].oaction))
        if len(transition_str) > 0:
            f.write("%s%s_%s_action(fsm);\n" % (prefix,self.basename,transition_str))
        target = args[1].target
        f.write("%s%s_st_change(fsm, %s_%s_fsm_st);\n" % (prefix,self.basename,self.basename,target))
        if len(self.states[target].iaction) > 0:
            f.write("%s%s_%s_action(fsm);\n" % (prefix,self.basename,self.states[target].iaction))
        return False

    def write_condition_guard(self,f,transition):
        if (transition.guard is not None) and len(transition.guard)>0:
            guard = "%s_%s_condition(fsm)" % (self.basename,transition.guard)
            f.write("(%s)" % guard)
            return True
        else:
            return False

    def write_trigger(self,f,transition):
        if len(transition.trigger) > 0:
            condition = "%s_%s_EVENT" % (self.basename.upper(),transition.trigger.upper())
            f.write("(fsm->events & %s)" % condition)
            return True
        else:
            return False

    def write_switch_case(self,f,action,add_actions):
        f.write("\tswitch(fsm->current_state)\n\t{\n")
        for key in self.states.keys():
            state = self.states[key]
            f.write("\tcase %s_%s_fsm_st:\n" % (self.basename,state.name))
            transitions = state.get_transitions(self.transitions)
            for transition in transitions:
                condition = ""
                if transition.has_trigger() or transition.is_conditional():
                    f.write("\t\tif( ")
                    self.write_condition_guard(f,transition)
                    if transition.is_conditional():
                        f.write("&& \n\t\t    ")
                    trigger_writen = self.write_trigger(f,transition)
                    f.write(" ) \n\t\t{\n")
                    returned = action(f,transition,condition,"\t\t\t")
                    if not returned:
                        f.write("\t\t\tbreak;\n")
                    f.write("\t\t}\n")
                else:
                    action(f,transition,condition,"\t\t")
            if add_actions:
                if len(state.do_action) > 0:
                    f.write("\t\tif( %s_%s_action_able(fsm) )\n" % (self.basename,state.do_action))
                    f.write("\t\t{\n")
                    f.write("\t\t\t%s_%s_action(fsm);\n" % (self.basename,state.do_action))
                    f.write("\t\t}\n")
            else:
                if len(state.do_action) > 0:
                    f.write("\t\tif( %s_%s_action_able(fsm) )\n{\n\t\t\treturn true;\n}\n" % (self.basename,state.do_action))
            f.write("\t\tbreak;\n")
        f.write("\tdefault:\n")
        f.write("\t\tbreak;\n")
        f.write("\t}\n")

    def generate_raw_funcs(self,f):
        type_name = self.get_fsm_type_name()
        f.write("static void %s_fsm_tick(%s* fsm)\n{\n" % (self.basename,type_name))
        self.write_switch_case(f,self.particular_state_action,True)
        f.write("}\n")
        f.write("\n")
    
    def get_fsm_type_name(self):
        return "%s_fsm_t" % (self.basename)

    def generate_events_fire_funcs(self,f):
        generated=[]
        for transition in self.transitions:
            if len(transition.trigger) > 0:
                if transition.trigger not in generated:
                    generated.append(transition.trigger)
                    f.write("void %s_fire_%s_event(%s* fsm)\n{\n" % (self.basename,transition.trigger,self.get_fsm_type_name()))
                    if self.cfg.multithread_enable:
                        f.write("\tfsm_api_lock(fsm->api, fsm->user_data);\n")
                    f.write("\tfsm->events |=  %s_%s_EVENT;\n" % (self.basename.upper(),transition.trigger.upper()))
                    if self.cfg.multithread_enable:
                        f.write("\tfsm_api_unlock(fsm->api, fsm->user_data);\n")
                    f.write("}\n")
                    f.write("\n")

    def generate_get_state_func(self,f):
        f.write("%s_fsm_st_t %s_get_state(%s* fsm)\n{\n" % (self.basename,self.basename,self.get_fsm_type_name()))
        f.write("\t%s_fsm_st_t state;\n" % self.basename)
        if self.cfg.multithread_enable:
            f.write("\tfsm_api_lock(fsm->api, fsm->user_data);\n")
        f.write("\tstate = fsm->current_state;\n")
        if self.cfg.multithread_enable:
            f.write("\tfsm_api_unlock(fsm->api, fsm->user_data);\n")
        f.write("\treturn state;\n")
        f.write("}\n")
        f.write("\n")

    def generate_init_func(self,f):
        f.write("void %s_fsm_init(%s* fsm, fsm_api_t* fsm_api, void* fsm_user_data)\n{\n" % (self.basename,self.get_fsm_type_name()))
        f.write("\tmemset(fsm, 0, sizeof(%s));\n" % (self.get_fsm_type_name()))
        f.write("\tfsm->previous_state = %s_%s_fsm_st;\n" % (self.basename,self.get_first_state_name()))
        f.write("\tfsm->current_state = %s_%s_fsm_st;\n" % (self.basename,self.get_first_state_name()))
        f.write("\tfsm->api = fsm_api;\n")
        f.write("\tfsm->user_data = fsm_user_data;\n")
        f.write("}\n")
        f.write("\n")

    def generate_object(self,f):
        f.write("typedef struct _%s\n{\n" % (self.get_fsm_type_name()))
        f.write("\t%s_fsm_st_t previous_state;\n" % (self.basename))
        f.write("\t%s_fsm_st_t current_state;\n" % (self.basename))
        f.write("\tuint32_t events;\n")
        f.write("\tfsm_api_t* api;\n")
        f.write("\tvoid* user_data;\n")
        f.write("} %s;\n" % (self.get_fsm_type_name()))
        f.write("\n")

    def generate_includes(self,f):
        f.write("#include <stdbool.h>\n")
        f.write("#include <stdint.h>\n")
        f.write("#include <string.h>\n")
        f.write("#include \"fsm_api.h\"\n")
        f.write("\n")

    def generate_events_defines(self,f):
        value=1
        generated=[]
        for transition in self.transitions:
            if len(transition.trigger) > 0:
                if transition.trigger not in generated:
                    generated.append(transition.trigger)
                    f.write("#define %s_%s_EVENT    0x%02x \n" % (self.basename.upper(),transition.trigger.upper(),value))
                    value=value*2
        f.write("\n")

    def generate_states_typedef(self,f):
        f.write("typedef enum _%s_fsm_st_t\n{\n" % (self.basename))
        states_keys_list = self.states.keys()
        for key in states_keys_list:
            state = self.states[key].name
            if key == states_keys_list[-1]:
                f.write("\t%s_%s_fsm_st\n" % (self.basename,state))
            else:
                f.write("\t%s_%s_fsm_st,\n" % (self.basename,state))
        f.write("} %s_fsm_st_t;\n" % (self.basename))
        f.write("\n")


INITIAL_STATE,STANDARD_STATE,FINAL_STATE = range(3)
SM_EXPORT_VERSION="2.1"

# dia-python keeps a reference to the renderer class and uses it on demand
dia.register_export ("State Machine C code export", "fsm", DiagramRenderer())
