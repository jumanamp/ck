#
# Collective Knowledge
#
# See CK LICENSE.txt for licensing details
# See CK Copyright.txt for copyright details
#
# Developer: Grigori Fursin
#

cfg={}  # Will be updated by CK (meta description of this module)
work={} # Will be updated by CK (temporal data)
ck=None # Will be updated by CK (initialized CK kernel) 

# Local settings
import os

##############################################################################
# Initialize module

def init(i):
    """

    Input:  {}

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0
            }

    """
    return {'return':0}

##############################################################################
# Add module

def add(i):
    """
    Input:  {
              (repo_uoa)  - repo UOA
              module_uoa  - normally should be 'module' already
              data_uoa    - UOA of the module to be created

              (desc)      - module description
              (license)   - module license
              (copyright) - module copyright
              (developer) - module developer
              (actions)   - dict with actions {"func1":{}, "func2":{} ...}
              (dict)      - other meta description to add to entry
            }

    Output: {
              return       - return code =  0, if successful
                                         >  0, if error
              (error)      - error text if return > 0

              Output of the 'add' kernel function
            }

    """

    o=i.get('out','')

    # Find path to module 'module' to get dummies
    r=ck.access({'action':'load',
                 'module_uoa':work['self_module_uoa'],
                 'data_uoa':work['self_module_uoa'],
                 'common_func':'yes'})
    if r['return']>0: return r
    p=r['path']

    pm=os.path.join(p,cfg['dummy_module'])
    pma=os.path.join(p,cfg['dummy_module_action'])

    # Load module dummy
    r=ck.load_text_file({'text_file':pm})
    if r['return']>0: return r
    spm=r['string']

    # Load module action dummy
    r=ck.load_text_file({'text_file':pma})
    if r['return']>0: return r
    spma=r['string']

    # Prepare meta description
    desc=i.get('desc','')
    license=i.get('license','')
    copyright=i.get('copyright','')
    developer=i.get('developer','')
    actions=i.get('actions',{})

    # If console mode, ask some questions
    if o=='con':
       if desc=='':
          r=ck.inp({'text':'Add brief module description:                                '})
          desc=r['string']

       if license=='':
          r=ck.inp({'text':'Add brief module license (or Enter to use CK license):       '})
          license=r['string']
          if license=='': license=ck.cfg['default_license']

       if copyright=='':
          r=ck.inp({'text':'Add brief module copyright (or Enter to use CK copyright):   '})
          copyright=r['string']
          if copyright=='': copyright=ck.cfg['default_copyright']

       if developer=='':
          r=ck.inp({'text':'Add module\'s developer (or Enter to use cTuning foundation): '})
          developer=r['string']
          if developer=='': developer=ck.cfg['default_developer']

       if len(actions)==0:
          ck.out('')
          act='*'
          while act!='':
             r=ck.inp({'text':'Add action function   (or Enter to stop):  '})
             act=r['string']
             if act!='': 
                actions[act]={}

                r1=ck.inp({'text':'Support web (yes or Enter to skip):        '})
                fweb=r1['string']
                if fweb!='': actions[act]['for_web']=fweb

                r1=ck.inp({'text':'Add action description (or Enter to stop): '})
                adesc=r1['string']
                if adesc!='': 
                   actions[act]['desc']=adesc

    ck.out('')

    # Prepare meta description
    dd={}
    if desc!='': 
       dd['desc']=desc
    spm=spm.replace('$#desc#$', desc)

    if license!='': 
       dd['license']=license
    spm=spm.replace('$#license#$', license)

    if copyright!='': 
       dd['copyright']=copyright
    spm=spm.replace('$#copyright#$', copyright)

    if developer!='': 
       dd['developer']=developer
    spm=spm.replace('$#developer#$', developer)

    dd['actions']=actions

    # Substitute actions
    for act in actions:
        adesc=actions[act].get('desc','TBD: action description')
        spm+='\n'+spma.replace('$#action#$', act).replace('$#desc#$',adesc)

    dx=i.get('dict',{})

    r=ck.merge_dicts({'dict1':dx, 'dict2':dd})
    if r['return']>0: return r

    # Add entry (it will ask further questions about alias and user-friendly name)
    i['common_func']='yes'
    i['dict']=dx
    r=ck.access(i)
    if r['return']>0: return r

    # Add module code
    p=r['path']
    pf=os.path.join(p, ck.cfg['module_full_code_name'])
   
    if o=='con':
       ck.out('')
       ck.out('Creating module code '+pf+' ...')

    # Write module code
    rx=ck.save_text_file({'text_file':pf, 'string':spm})
    if rx['return']>0: return rx

    return r