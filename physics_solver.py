""" 
Library to solve One dimentional motion equations. 
   
    1) xf = x0 + v0*t + 1/2 * a * t**2
    2) vf = v0 + a*t
    3) vf**2 = v0**2 + 2a(xf - x0) 
    4) xf = x0 + 1/2 (vf + v0) t

"""


import numpy as np
import scipy as sp

def one_dimention_solver(*args, **kwargs):
    variables = {'x0': None, 'xf':None, 'v0':None, 'vf':None, 'a':None, 't':None}
    variables.update(kwargs)
    
    variable_mask = 0b000000
    for key, item in variables.items():
        if key == 'x0' and item is not None:
            variable_mask += 0b100000
        elif key == 'xf' and item is not None:
            variable_mask += 0b010000
        elif key == 'v0' and item is not None:
            variable_mask += 0b001000
        elif key == 'vf'and item is not None:
            variable_mask += 0b000100
        elif key == 'a' and item is not None:
            variable_mask += 0b000010
        elif key == 't' and item is not None:
            variable_mask += 0b000001
        
    loop_count = 0
    while None in variables.values():
        loop_count += 1
        print(variable_mask, loop_count)
        # Solving for x0
        if (variable_mask & 0b011011)==0b011011 and variables['x0'] is None:
            variables['x0'] = variables['xf'] - variables['v0'] * variables['t'] - 0.5 * variables['a'] * variables['t']**2
            variable_mask += 0b100000
        elif (variable_mask & 0b011110)==0b011110 and variables['x0'] is None:
            variables['x0'] = -1*( (variables['vf']**2 - variables['v0']**2) / (2 * variables['a']) - variables['xf'] )
            variable_mask += 0b100000
        elif (variable_mask & 0b011101)==0b011101 and variables['x0'] is None:
            variables['x0'] = variables['xf'] - 0.5*(variables['vf'] + variables['v0'])*variables['t']
            variable_mask += 0b100000
            
        # Solving for xf
        if (variable_mask & 0b101011)==0b101011 and variables['xf'] is None:
            variables['xf'] =  variables['x0'] + variables['v0'] * variables['t'] + 0.5 * variables['a'] * variables['t']**2
            variable_mask += 0b010000
        elif (variable_mask & 0b101110)==0b101110 and variables['xf'] is None and variables['a'] != 0:
            variables['xf'] = (variables['vf']**2 - variables['v0']**2) / (2*variables['a']) + variables['x0']
            variable_mask += 0b010000
        elif (variable_mask & 0b101101)==0b101101 and variables['xf'] is None:
            variables['xf'] = variables['x0'] + 0.5 * (variables['vf'] + variables['v0']) * variables['t']
            variable_mask += 0b010000
            
        # Solving for v0
        if (variable_mask & 0b000111)==0b000111 and variables['v0'] is None:
            variables['v0'] = variables['vf'] - variables['a']*variables['t']
            variable_mask += 0b001000
        elif (variable_mask & 0b110011)==0b110011 and variables['v0'] is None and variables['t'] != 0:
            variables['v0'] = (variables['xf'] - variables['x0'] - 0.5*variables['a']*variables['t']**2) / variables['t']
            variable_mask += 0b001000
        elif (variable_mask & 0b110110)==0b110110 and variables['v0'] is None:
            variables['v0'] = np.sqrt(variables['vf']**2 - 2*variables['a']*(variables['xf'] - variables['x0']))
            variable_mask += 0b001000
        elif (variable_mask & 0b110101)==0b110101 and variables['v0'] is None:
            variables['v0'] = (-2/variables['t'])*(variables['xf'] - variables['x0']) + variables['vf']
            variable_mask += 0b001000
            
        # Solving for vf 
        if (variable_mask & 0b001011)==0b001011 and variables['vt'] is None:
            variables['vf'] = variables['v0'] + variables['a']*variables['t']
            variable_mask += 0b000100
        elif (variable_mask & 0b111010)==0b111010 and variables['vf'] is None:
            variables['vf'] = np.sqrt(variables['v0']**2 + 2*variables['a']*(variables['xf'] - variables['x0']))
            variable_mask += 0b000100
        elif (variable_mask & 0b111001)==0b111001 and variables['vf'] is  None:
            variables['vf'] = (2/variables['t'])*(variables['xf'] - variables['x0']) - variables['v0']
            variable_mask += 0b000100
            
        # Solving for a
        if (variable_mask & 0b001101)==0b001101 and variables['a'] is None:
            variables['a'] = (variables['vf'] - variables['v0']) / variables['t']
            variable_mask += 0b000010
        elif (variable_mask & 0b111001)==0b111001 and variables['a'] is None:
            variables['a'] = (2/variables['t']**2) * (variables['xf'] - variables['x0'] - variables['v0']*variables['t'])
            variable_mask += 0b000010
        elif (variable_mask & 0b111100)==0b111100 and variables['a'] is None and variables['xf'] != variables['x0']:
            variables['a'] = (variables['vf']**2 - variables['v0']**2) / (2*(variables['xf'] - variables['x0']))
        
        # Solving for t
        if (variable_mask & 0b001110)==0b001110 and variables['t'] is None and variables['a'] != 0:
            variables['t'] = (variables['vf'] - variables['v0']) / variables['a']
            variable_mask += 0b000001
        elif (variable_mask & 0b111010)==0b111010 and variables['t'] is None and variables['a'] != 0:
            variables['t'] = positive_quadratic(0.5*variables['a'], variables['v0'], variables['x0'] - variables['xf'])
            variable_mask += 0b000001
        elif (variable_mask & 0b111100)==0b111100 and variables['t'] is None and (variables['vf'] + variables['v0']) != 0:
            variables['t'] = (variables['xf'] - variables['x0']) / (0.5*(variables['vf'] + variables['v0']))
            variable_mask += 0b000001

        if loop_count > 5:
            break
    return variables
        

def positive_quadratic(a, b, c):
    answer1 = (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)
    answer2 = (-b - np.sqrt(b**2 - 4*a*c)) / (2*a)
    print(answer1, answer2)
    if answer1 > 0:
        return answer1
    elif answer2 > 0:
        return answer2
    else:
        return "No positive answers"