# stripsProblem.py - STRIPS Representations of Actions
# AIFCA Python code Version 0.9.18 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2026 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Strips(object):
    def __init__(self, name, preconds, effects, cost=1):
        """
        defines the STRIPS representation for an action:
        * name is the name of the action
        * preconds, the preconditions, is feature:value dictionary that must hold
        for the action to be carried out
        * effects is a feature:value map that this action makes
        true. The action changes the value of any feature specified
        here, and leaves other features unchanged.
        * cost is the cost of the action
        """
        self.name = name
        self.preconds = preconds
        self.effects = effects
        self.cost = cost

    def __repr__(self):
        return self.name

class STRIPS_domain(object):
    def __init__(self, feature_domain_dict, actions):
        """Problem domain
        feature_domain_dict is a feature:domain dictionary, 
                mapping each feature to its domain
        actions
        """
        self.feature_domain_dict = feature_domain_dict
        self.actions = actions

class Planning_problem(object):
    def __init__(self, prob_domain, initial_state, goal):
        """
        a planning problem consists of
        * a planning domain
        * the initial state
        * a goal 
        """
        self.prob_domain = prob_domain
        self.initial_state = initial_state
        self.goal = goal

boolean = {False, True}
delivery_domain = STRIPS_domain(
    {'RLoc':{'cs', 'off', 'lab', 'mr'}, 'RHC':boolean, 'SWC':boolean,
     'MW':boolean, 'RHM':boolean},           #feature:values dictionary
    { Strips('mc_cs', {'RLoc':'cs'}, {'RLoc':'off'}),   
     Strips('mc_off', {'RLoc':'off'}, {'RLoc':'lab'}),
     Strips('mc_lab', {'RLoc':'lab'}, {'RLoc':'mr'}),
     Strips('mc_mr', {'RLoc':'mr'}, {'RLoc':'cs'}),
     Strips('mcc_cs', {'RLoc':'cs'}, {'RLoc':'mr'}),   
     Strips('mcc_off', {'RLoc':'off'}, {'RLoc':'cs'}),
     Strips('mcc_lab', {'RLoc':'lab'}, {'RLoc':'off'}),
     Strips('mcc_mr', {'RLoc':'mr'}, {'RLoc':'lab'}),
     Strips('puc', {'RLoc':'cs', 'RHC':False}, {'RHC':True}),  
     Strips('dc', {'RLoc':'off', 'RHC':True}, {'RHC':False, 'SWC':False}),
     Strips('pum', {'RLoc':'mr','MW':True}, {'RHM':True,'MW':False}),
     Strips('dm', {'RLoc':'off', 'RHM':True}, {'RHM':False})
   } )

problem0 = Planning_problem(delivery_domain,
                            {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False, 
                             'RHM':False}, 
                            {'RLoc':'off'})
problem1 = Planning_problem(delivery_domain,
                            {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False, 
                             'RHM':False}, 
                            {'SWC':False})
problem2 = Planning_problem(delivery_domain,
                            {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False, 
                             'RHM':False}, 
                            {'SWC':False, 'MW':False, 'RHM':False})

### blocks world
def move(x,y,z):
    """string for the 'move' action"""
    return 'move_'+x+'_from_'+y+'_to_'+z
def on(x):
    """string for the 'on' feature"""
    return x+'_is_on'
def clear(x):
    """string for the 'clear' feature"""
    return 'clear_'+x
def create_blocks_world(blocks = {'a','b','c','d'}):
    blocks_and_table = blocks | {'table'}
    stmap =  {Strips(move(x,y,z),{on(x):y, clear(x):True, clear(z):True}, 
                                 {on(x):z, clear(y):True, clear(z):False})
                    for x in blocks
                    for y in blocks_and_table
                    for z in blocks
                    if x!=y and y!=z and z!=x}
    stmap.update({Strips(move(x,y,'table'), {on(x):y, clear(x):True}, 
                                 {on(x):'table', clear(y):True})
                    for x in blocks
                    for y in blocks
                    if x!=y})
    feature_domain_dict = {on(x):blocks_and_table-{x} for x in blocks}
    feature_domain_dict.update({clear(x):boolean for x in blocks_and_table})
    return STRIPS_domain(feature_domain_dict, stmap)

blocks1dom = create_blocks_world({'a','b','c'})
blocks1 = Planning_problem(blocks1dom,
     {on('a'):'table', clear('a'):True,
      on('b'):'c',  clear('b'):True,
      on('c'):'table', clear('c'):False}, # initial state
     {on('a'):'b', on('c'):'a'})  #goal

blocks2dom = create_blocks_world({'a','b','c','d'})
tower4 = {clear('a'):True, on('a'):'b',
          clear('b'):False, on('b'):'c',
          clear('c'):False, on('c'):'d',
          clear('d'):False, on('d'):'table'}
blocks2 = Planning_problem(blocks2dom,
     tower4, # initial state
     {on('d'):'c',on('c'):'b',on('b'):'a'})  #goal

blocks3 = Planning_problem(blocks2dom,
     tower4, # initial state
     {on('d'):'a', on('a'):'b', on('b'):'c'})  #goal


def create_gripper_world(num_balls=4):
    balls = [f'ball{i}' for i in range(1, num_balls + 1)]
    rooms = {'roomA', 'roomB'}
    grippers = {'left', 'right'}
    
    actions = set()
    
    for r_from in rooms:
        for r_to in rooms:
            if r_from != r_to:
                actions.add(Strips(f'move_{r_from}_{r_to}', 
                                   {'rob_at': r_from}, 
                                   {'rob_at': r_to}))
    
    for b in balls:
        for r in rooms:
            for g in grippers:
                actions.add(Strips(f'pick_{b}_{g}_{r}',
                                   {'rob_at': r, f'at_{b}': r, f'free_{g}': True},
                                   {f'at_{b}': g, f'free_{g}': False}))
                actions.add(Strips(f'drop_{b}_{g}_{r}',
                                   {'rob_at': r, f'at_{b}': g},
                                   {f'at_{b}': r, f'free_{g}': True}))
    
    feature_domain = {'rob_at': rooms}
    for b in balls:
        feature_domain[f'at_{b}'] = rooms | grippers
    for g in grippers:
        feature_domain[f'free_{g}'] = {True, False}
        
    return STRIPS_domain(feature_domain, actions)

gripper_dom = create_gripper_world(4)
initial_gripper = {'rob_at': 'roomA', 'free_left': True, 'free_right': True}
initial_gripper.update({f'at_ball{i}': 'roomA' for i in range(1, 5)})

gripper_problem = Planning_problem(gripper_dom,
    initial_gripper,
    {'at_ball1': 'roomB', 'at_ball2': 'roomB', 'at_ball3': 'roomB', 'at_ball4': 'roomB'})


monkey_domain = STRIPS_domain(
    {'m_loc': {'l1', 'l2', 'l3'}, 'b_loc': {'l1', 'l2', 'l3'}, 
     'box_loc': {'l1', 'l2', 'l3'}, 'on_box': {True, False}, 'has_bananas': {True, False}},
    {
        Strips('go_l1', {'on_box': False}, {'m_loc': 'l1'}),
        Strips('go_l2', {'on_box': False}, {'m_loc': 'l2'}),
        Strips('go_l3', {'on_box': False}, {'m_loc': 'l3'}),
        
        Strips('push_box_l1', {'on_box': False, 'm_loc': 'l2', 'box_loc': 'l2'}, {'m_loc': 'l1', 'box_loc': 'l1'}),
        Strips('push_box_l2', {'on_box': False, 'm_loc': 'l1', 'box_loc': 'l1'}, {'m_loc': 'l2', 'box_loc': 'l2'}),
        Strips('push_box_l3', {'on_box': False, 'm_loc': 'l2', 'box_loc': 'l2'}, {'m_loc': 'l3', 'box_loc': 'l3'}),
        
        Strips('climb_on', {'m_loc': 'l1', 'box_loc': 'l1'}, {'on_box': True}),
        Strips('climb_on', {'m_loc': 'l2', 'box_loc': 'l2'}, {'on_box': True}),
        Strips('climb_on', {'m_loc': 'l3', 'box_loc': 'l3'}, {'on_box': True}),

        Strips('grasp_bananas', {'on_box': True, 'm_loc': 'l3', 'b_loc': 'l3'}, {'has_bananas': True})
    }
)

monkey_problem = Planning_problem(monkey_domain,
    {'m_loc': 'l1', 'box_loc': 'l2', 'b_loc': 'l3', 'on_box': False, 'has_bananas': False},
    {'has_bananas': True})