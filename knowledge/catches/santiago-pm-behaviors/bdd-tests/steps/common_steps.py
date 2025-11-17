"""
Common BDD step definitions for Santiago PM behaviors.
These are placeholder steps for syntax validation.
"""

from behave import given, when, then


@given('Santiago PM MCP is running')
def step_impl(context):
    pass


@given('the knowledge graph is initialized')
def step_impl(context):
    pass


@given('the user has {capability} capability level')
def step_impl(context, capability):
    pass


@given('the user provides valid input data for {behavior}')
def step_impl(context, behavior):
    pass


@given('the user provides minimal or optional field data for {behavior}')
def step_impl(context, behavior):
    pass


@given('the user provides incomplete data missing required fields')
def step_impl(context):
    pass


@when('the {behavior} behavior is invoked')
def step_impl(context, behavior):
    pass


@then('a new {node_type} node is {action} in the knowledge graph')
def step_impl(context, node_type, action):
    pass


@then('the response contains the expected output fields')
def step_impl(context):
    pass


@then('the operation completes successfully')
def step_impl(context):
    pass


@then('the operation handles the edge case gracefully')
def step_impl(context):
    pass


@then('default values are applied where appropriate')
def step_impl(context):
    pass


@then('the response indicates partial success or warnings')
def step_impl(context):
    pass


@then('an error is returned with message "{message}"')
def step_impl(context, message):
    pass


@then('the knowledge graph remains unchanged')
def step_impl(context):
    pass


@then('the error includes details about which fields are missing')
def step_impl(context):
    pass
