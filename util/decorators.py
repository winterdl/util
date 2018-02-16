# ==================================================================
#                         SameAs Decorator
# 
# Decorator that copies the documentation and arguemnts of another
# function (specified as input). Useful for making decorators (:P)
# 
# USAGE: 
# 
#   @same_as(<func_to_copy>)
#   def <function_to_decorate>(...):
#      ...
# 
#   OR
# 
#   <function> = same_as(<func_to_copy>)(<function_to_decorate>)
#   
def same_as(to_copy):
    import inspect
    # Create a function that takes one argument, a function to be
    # decorated. This will be called by python when decorating.
    def decorator_handler(func):
        # Set the documentation string for this new function
        documentation = inspect.getdoc(to_copy)
        if documentation == None: 
            documentation = inspect.getcomments(to_copy)
        # Store the documentation and signature into the wrapped function
        if hasattr(to_copy, "__name__"):
            func.__name__ = to_copy.__name__
        try:               func.__signature__ = inspect.signature(to_copy)
        except ValueError: pass
        func.__doc__ = documentation
        return func
    # Return the decorator handler
    return decorator_handler
# 
# ==================================================================

# ==================================================================
#                    "Cache in File" Decorator     
# 
# This decorator (when wrapped around a function) uses a hash of the
# string represenetation of the parameters to a function call in order
# to write a pickle file that contains the inputs to the function and
# the outputs to the function.
# 
# 
# USAGE: 
# 
#   @cache(<max_files>=10, <cache_dir>=os.curdir)
#   def <function_to_decorate>(...):
#      ...
# 
#   OR
# 
#   <function> = same_as(<max_files>, <cache_dir>)(<function_to_decorate>)
#   
def cache(func_to_cache=None, max_files=10, cache_dir=None):
    import os, hashlib, pickle, time
    # Handle alternate usage (using *args instead of **kwargs)
    if (type(func_to_cache) == int):
        max_files = func_to_cache
        if (type(max_files) == str):
            cache_dir = max_files
    # Check to see if a cache directory was provided
    if (type(cache_dir) == type(None)): cache_dir = os.curdir
    # Create a function that takes one argument, a function to be
    # decorated. This will be called by python when decorating.
    def decorator_handler(func):
        def new_func(*args, **kwargs):
            # Identify a cache name via sha256 hex over the serialization
            hash_value = hashlib.sha256(pickle.dumps((args, kwargs))).hexdigest()
            cache_prefix = "Cache_[" + func.__name__ + "]_"
            cache_suffix = ".pkl"
            cache_path = os.path.join(cache_dir, cache_prefix+hash_value+cache_suffix)
            # Check to see if a matching cache file exists
            if os.path.exists(cache_path):
                with open(cache_path, "rb") as f:
                    args, kwargs, output = pickle.load(f)
            else:
                # Calculate the output normally with the function
                output = func(*args, **kwargs)
                # Identify the names of existing caches in this directory
                existing_caches = [f for f in os.listdir(cache_dir)
                                   if cache_prefix in f[:len(cache_prefix)]]
                # Only save a cached file if there are fewer than "max_files"
                if len(existing_caches) < max_files:
                    with open(cache_path, "wb") as f:
                        pickle.dump((args, kwargs, output), f)
            # Return the output (however it was achieved)
            return output
        # Return the decorated version of the function with identical documntation
        return same_as(func)(new_func)
    # Return the appropriate function based on if the user specified
    # the maximum number of files or not when using the decorator.
    if (type(func_to_cache) != type(lambda:None)): 
        # Return a function that is capable of decorating
        return decorator_handler
    else:
        # Return the decorated function
        return decorator_handler(func_to_cache)
            
def test_cache():
    # Documentation for "simple_add"
    @cache(max_files=10, cache_dir=".")
    def simple_add(a, b):
        return a.union(b)
    # Run the function many times (with a non-hashable object) to
    # demonstrate that it all works
    for i in range(10):
        print(simple_add({1,2},{i}))
    help(simple_add)
# 
# ==================================================================

# ==================================================================
#                         Timeout Decorator     
# 
# Function decorator that uses the "signal" module in order to ensure
# that a function call does not take more than "allowed_seconds" to
# complete. If the function takes longer than "allowed_seconds" then
# the value "default" is returned.
# 
# USAGE: 
# 
#   @timeout_after(<allowed_seconds>, <default>)
#   def <function_to_decorate>(...):
#      ...
# 
#   OR
# 
#   <function> = timeout_after(<sec>, <default>)(<function_to_decorate>)
#   
def timeout_after(allowed_seconds=1, default=None):
    import signal, inspect
    # Create a function that takes one argument, a function to be
    # decorated. This will be called by python when decorating.
    def decorator_handler(func):
        # Create a new function (for return when decorating)
        def new_func(*args, **kwargs):
            # Create a custom exception, be sure to *only* catch it
            class TimeoutError(Exception): pass
            # Send our exception as a signal if this handler is called
            def handler(signum, frame):
                raise TimeoutError()
            # Set our handler function to be called by the alarm signal
            signal.signal(signal.SIGALRM, handler) 
            # Signal an alarm (our handler) if "allowed_seconds" elapses
            signal.alarm(round(allowed_seconds+0.5))
            try:
                # Try running the decorated function
                result = func(*args, **kwargs)
            except TimeoutError:
                # The decorated function did not finish
                result = default
            finally:
                # Cancel the alarm if the <try> completes successfully
                signal.alarm(0)
            return result
        # Set the documentation string for this new function
        return same_as(func)(new_func)
    # Check which type of usage is being implemented
    if type(allowed_seconds) == type(lambda:None):
        # If the user has applied the decorator without arguments,
        #  then the first argument provided is actually "func"
        func = allowed_seconds
        # Get the default value for "allowed_seconds"
        allowed_seconds = inspect.signature(timeout_after).parameters['allowed_seconds'].default
        decorated_func = decorator_handler(func)
    else:
        # The user must have given some arguments, normal decoration
        decorated_func = decorator_handler
    # Return the function that will return the decorated function
    return decorated_func

def test_timeout_after():
    # This is a testing function for the timeout_after decorator. These
    # comments will still be included in the documentation for the function.
    @timeout_after(2,"Failed...")
    def sample_func(sec):
        import time
        print(" Going to sleep for '%.1f' seconds."%(sec))
        time.sleep(sec)
        print(" Finished sleeping!")
    print()
    print(sample_func(1.5) == None)
    print(sample_func(2.5) == "Failed...")
    print()
# 
# ==================================================================


# ==================================================================
#                       Type Check Decorator     
# 
# TODO: The 'list' arg_type should do checking along each of the
#       dimensions of the input, and should only require that the
#       input be iterable up to D dimensions deep. Add associated
#       errros as well.
# TODO: Clean up the arg type function to only reference arguments by
#       name in the error messages, no need to duplicate code.
# 
# Errors for type checking
class WrongType(Exception): pass
class WrongType_NotInSet(Exception): pass
class WrongType_NotListed(Exception): pass
class WrongType_FailedCheck(Exception): pass
class WrongNumberOfArguments(Exception): pass
class WrongUsageOfTypeCheck(Exception): pass
FUNCTION_TYPE = type(lambda:None)
# Function decorator that checks the types of arguments and keyword
# arguments. It's for guaranteeing proper usage (forgive how
# un-pythonic this is, but sometimes it's useful for producing better
# error messages). Given a list of arguments that is shorter than the
# actual list, it only checks the first N provided. Given keyword
# arguments to check, it only checks them if they are
# provided. Returns a function with a for loop over the arguments
# checking for minimum number of arguments and correct types. Also
# transfers the documentation to the decorated function.
# 
# USAGE:
# 
#   @type_check([<arg_type>, ...]=[], {<arg_name>:<arg_type>, ...}={})
#   def <func_name>( ... ):
# 
# OR
# 
#   <function> = type_check(<type_check_args>)(<function_to_decorate>)
# 
# "arg_type" can be one of the following:
#    type     -> Type checking is equality based         "type(arg) == arg_type"
#    set      -> Type checking is membership based       "type(arg) in arg_type"
#    list     -> Type checking is nested                 "(type(arg) == list) and all((type(arg_i) == t) for (arg_i,t) in zip(arg,arg_type))"
#    function -> Type checking is provided by function   "arg_type(arg)"
# 
def type_check(*types, **types_by_name):
    # Check for poor usage of the type-checking function (potentially bad types XD)
    for t in types + tuple(types_by_name.values()):
        if type(t) not in {type, set, list, FUNCTION_TYPE}:
            raise(WrongUsageOfTypeCheck(
                "Type checking can only handle types, sets of "+
                "types, and functions that return types. Type '%s' not allowed."%(type(t))))

    # Create a function that takes one argument, a function to be
    # decorated. This will be called by python when decorating.
    def decorator_handler(func):
        # Create a new function (for return when decorating)
        def new_func(*args, **kwargs):
            # Make sure the correct number of arguments were given
            if len(args) < len(types):
                raise(WrongNumberOfArguments("Type checked function expected %i arguments."%(len(types))))
            # Check types of all of the regular arguments
            for i,(a, t) in enumerate(zip(args, types)):
                # Check if type equals the expected type
                if type(t) == type:
                    if not (type(a) == t):
                        raise(WrongType(("Expected argument %i to be type '%s',"+
                                         "received type '%s' instead.")%(i,t,type(a))))
                # Check if type exists in a set of allowed types
                elif type(t) == set:
                    if not (type(a) in t):
                        raise(WrongType_NotInSet(("Expected argument %i to be one of types %s,"+
                                                  "received type '%s' instead.")%(i,t,type(a))))
                # Check if list argument is sub-typed correctly
                elif type(t) == list:
                    # Check for list type
                    if not (type(a) == list):
                        raise(WrongType(("Expected argument %i to be type '%s',"+
                                         "received type '%s' instead.")%(i,list,type(a))))
                    # Check for subtypes of list
                    if not all(type(ai) == ti for (ai, ti) in zip(a,t)):
                        raise(WrongType_NotListed((
                            "Types contained in list argument %i did not match "+
                            "match expected type listing %s.")%(i,t)))
                # Check if type passes a type-checking function
                elif type(t) == FUNCTION_TYPE:
                    if not t(a):
                        raise(WrongType_FailedCheck(("Argument %i of type '%s' did not pass "+
                                                     "required type checking function.")%(i,type(a))))
            # Check types of all of the keyword arguments
            for arg_name in kwargs:
                if arg_name in types_by_name:
                    a, t = kwargs[arg_name], types_by_name[arg_name]
                    # Check if type equals the expected type
                    if type(t) == type:
                        if not (type(a) == t):
                            raise(WrongType(("Expected keyword argument '%s' to be type '%s',"+
                                             "received type '%s' instead.")%(arg_name,t,type(a))))
                    # Check if type exists in a set of allowed types
                    elif type(t) == set:
                        if not (type(a) in t):
                            raise(WrongType_NotInSet(("Expected keyword argument '%s' to be one of types %s,"+
                                                      "received type '%s' instead.")%(arg_name,t,type(a))))
                    # Check if list argument is sub-typed correctly
                    elif type(t) == list:
                        # Check for list type
                        if not (type(a) == list):
                            raise(WrongType(("Expected keyword argument '%s' to be type '%s',"+
                                             "received type '%s' instead.")%(arg_name,list,type(a))))
                        # Check for subtypes of list
                        if not all(type(ai) == ti for (ai, ti) in zip(a,t)):
                            raise(WrongType_NotListed((
                                "Types contained in list keyword argument '%s' did not match "+
                                "match expected type listing %s.")%(arg_name,t)))
                    # Check if type passes a type-checking function
                    elif type(t) == type(lambda:None):
                        if not t(a):
                            raise(WrongType_FailedCheck(("Keyword argument for '%s' of type '%s' did not pass "+
                                                         "required type checking function.")%(arg_name,type(a))))
            return func(*args, **kwargs)
        # Set the documentation string for this new function
        return same_as(func)(new_func)
    # Return the function that will return the decorated function
    return decorator_handler

# This is a testing function for the timeout_after decorator. These
# comments will still be included in the documentation for the function.
def test_type_check():
    class TestCaseFailed(Exception): pass

    @type_check(int, {int,float}, [float, int], lambda arg: hasattr(arg, "__call__"))
    def func(arg_int, arg_int_or_float, arg_list_float_int, arg_callable):
        print("Passed", type(arg_int), type(arg_int_or_float), 
              type(arg_list_float_int), arg_callable)

    func(1, 1, [.0,1], lambda: None)
    func(0, 1.0, [.0,1], lambda: None)
    class test:
        def __call__(): pass
    func(1, 1, [.0,1], test)

    # Test case 0
    try:
        func()
        raise(TestCaseFailed())        
    except WrongNumberOfArguments:
        print("Passed correct exception for wrong number of arguments.")
    # Test case 1
    try:
        func(1.0, 0, [.0, 1], 0)
        raise(TestCaseFailed())
    except WrongType:
        print("Passed correct exception for wrong argument type.")
    # Test case 2
    try:
        func(0, 0, [.0, 1], 0)
        raise(TestCaseFailed())
    except WrongType_FailedCheck:
        print("Passed correct exception for wrong keyword argument type.")
    # Test case 3
    try:
        func(0, 0, 0, 0)
        raise(TestCaseFailed())
    except WrongType:
        print("Passed correct exception for wrong type for list argument.")
    # Test case 4
    try:
        func(0, 0, [0,0], 0)
        raise(TestCaseFailed())
    except WrongType_NotListed:
        print("Passed correct exception for wrong listed argument type.")
    # Test case 5
    try:
        func = type_check((int, float), float)(func)
        raise(TestCaseFailed())
    except WrongUsageOfTypeCheck:
        print("Passed correct exception for improper developer usage.")
# 
# ==================================================================
