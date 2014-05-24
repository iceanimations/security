import app.util as util
from auth import user as USER
reload(util)


def checkinability(search_key, context = None):

    '''
    @search_key: the search_key of the sobject whose checkinability
    is to be checked
    @context: context with which the checkin is to be made
    not considered yet
    @return: True if the user can checkin the file
    '''
    
    server = USER.get_server()
    user = USER.get_user()

    if user == 'admin':
        return True

    
    logins = server.query('sthpw/login_in_group', filters = [('login', user)])
    util.pretty_print(logins)
    if logins:
        for login in logins[:]:
           groups =  server.query('sthpw/login_group',
                                  filters = [('login_group',
                                              login['login_group'])])
           util.pretty_print(groups)
           project = groups[0]['project_code']
           if (project == util.get_project_from_search_key(search_key) and

               # modeling and rigging dept can checkin to asset
               ('/asset' in search_key and
                any([dpt in login['login_group'] for dpt in ['model',
                                                             'rig']])) or
               # animation dept can checkin to shot
               ('/shot' in search_key and
                any([dpt in login['login_group'] for dpt in ['animation']]))):
               return True
           
    return False
