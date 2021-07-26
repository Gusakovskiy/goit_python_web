"""

Recursion can be considered bad in Python when there is a more optimal way to
implement the same algorithm using iteration or the recursive use case has the potential to
generate more than 1000 function calls on the call stack. This is because Python has a function
call overhead where the interpreter does dynamic type checking of function arguments
done before and after the function call, which results in additional runtime latency.
"""