import inspect
import types

import samp


t_unauthorized = 'You are not allowed to use this command'
t_unauthd_color = 0xFF1111FF
_cmd_list = dict()
current_cmd = None


def cmd(
    command, raw=False, requires=None, convert=None,
    unauthorized_text=t_unauthorized, unauthd_color=t_unauthd_color
):
    """function decorator for command functions

    Arguments:
    function:
        Command name as a string or a tuple of multiple aliases
        If there is no command name passed, the command's name will be the
        function's name
    raw:
        whether the cmdtext should be passed as the raw string (True) or parsed
        as a whitespace-seperated tuple
    requires:
        function object or a tuple with multiple function objects,
        which are called with a playerid and should return True if the player
        is allowed to use that command
    convert:
        contains a dictionary of callable objects, that take a string and
        return any other type, which is called for the given command parameter,
        for example the following will parse prm1 as int:
        @cmd("test", convert=dict(prm1=int))
        def cmd_test(playerid, prm1):
            pass
    unauthorized_text:
        a string which is sent to the player, if they are not allowed to use
        the command (see requires)
    unauthd_color:
        a color code which is used for sending the unauthorized message

    Example usages:
    >>> @cmd
    ... def testcmd(playerid, arg1):
    ...     pass

    >>> @cmd("testcmd", requires=samp.IsPlayerAdmin)
    ... def cmd_test(playerid, arg1):
    ...     pass
    """

    ret_obj = True
    # get command names
    cmd_names = []
    if type(command) == str:
        cmd_names.append(command)  # directly add this string as the name
    elif hasattr(command, '__iter__'):
        cmd_names.extend(command)  # extend the list with the iterable object
    # in that case we (should) have a decorator @cmd, where the function
    # object is passed here
    elif hasattr(command, '__call__'):
        cmd_names.append(command.__name__)
        # in that case we don't have to return the cmd_obj instance
        ret_obj = False
    else:  # invalid parameter
        raise TypeError('invalid type: command')

    inst = _cmd_obj(
        cmd_names,
        raw,
        requires,
        convert,
        unauthorized_text,
        unauthd_color,
    )
    if not ret_obj:
        # set function in inst and return command
        inst.function = command
        inst.read_function_data()
        return command
    return inst


class _cmd_obj:
    def __init__(
        self,
        aliases,
        raw,
        requires,
        convert,
        unauthorized_text,
        unauthd_color,
    ):
        # we always have a list of command names in aliases
        # iterate through all strings and add the commands
        for alias in aliases:
            # strip leading slash if there is one
            _cmd_list[(alias if alias[0] != '/' else alias[1:])] = self

        self.function = None
        self.raw = raw
        self.requires = (
            requires if hasattr(requires, '__iter__') else (requires,)
        )
        self.convert = convert if type(convert) == dict else dict()
        self.unauthorized_text = unauthorized_text
        self.unauthd_color = unauthd_color

    def __call__(self, funcobj):
        if not self.function:
            # in this case, we have a @cmd(...) decorator
            # the function object is passed here
            self.function = funcobj
            self.read_function_data()
        return funcobj

    def read_function_data(self):
        """
        reads parameter count and type of the function parameters
        """
        args = None
        # read parameter info, depending on what callable type it is
        if isinstance(self.function, types.FunctionType):
            args = inspect.getargspec(self.function)
        else:
            args = inspect.getargspec(self.function.__call__)
            # check if there is a self parameter
            if 'self' in args.args:
                args.args.remove('self')
        # set parameter count
        if args.varargs:
            # unlimited parameter count
            self.param_count = -1
        else:
            self.param_count = len(args.args) - 1
        # save the argument names for the convert parameter
        self.args = args.args


def handle_command(playerid, cmdtext):
    """Handles a command sent by a player.

    Should be called in OnPlayerCommandText.
    >>> @cmd
    ... def test(pid, prm1, prm2):
    ...     print('called')
    >>> @cmd("t2", convert=dict(prm1=int))
    ... def t2(pid, prm1):
    ...     print(type(prm1))
    >>> handle_command(0, "/test prm1 prm2")
    called
    True
    >>> handle_command(0, "/t2 5")
    <type 'int'>
    True
    >>> handle_command(1, "/nocmd")
    False
    """
    # split cmdtext
    prt = cmdtext.split()
    cmdname = prt[0][1:]
    # find the cmd instance
    if cmdname not in _cmd_list:
        return False  # command does not exist
    cmd = _cmd_list[cmdname]
    if not cmd.function:
        raise AttributeError(
            "command has no callable object assigned: [%d]: %s" % (
                playerid,
                cmdtext,
            )
        )

    # check if this user is authorized to use this command
    for req in cmd.requires:
        try:
            # it's the user's fault if he doesn't pass callable objects
            if not req(playerid):
                samp.SendClientMessage(
                    playerid,
                    cmd.unauthd_color,
                    cmd.unauthorized_text
                )
                return True
        except TypeError:
            pass

    if cmd.param_count != -1 and len(prt) - 1 > cmd.param_count:
        # too many parameters passed -> cut out
        prt = prt[:-(len(prt) - cmd.param_count - 1)]

    # convert parameters
    for p in range(len(prt)):
        if cmd.args[p] in cmd.convert:  # check if this parameter exists
            try:  # call the converter
                prt[p] = cmd.convert[cmd.args[p]](prt[p])
            except Exception:
                # we don't know which exceptions are thrown if conversion
                # fails, so always drop it
                pass

    # call the function object
    cmd.function(playerid, *prt[1:] if not cmd.raw else cmdtext)

    return True


# doctest
if __name__ == "__main__":
    # mock for samp module with needed functions for doctests
    class samp:  # noqa
        @staticmethod
        def IsPlayerAdmin(playerid):
            return True if playerid % 2 else False

        @staticmethod
        def SendClientMessage(playerid, color, text):
            return None

    import doctest
    doctest.testfile
