def overrides(step_text, step_keyword='step'):
    from behave.runner import the_step_registry
    step_type = step_keyword.lower()
    assert step_type in ('given', 'when', 'then', 'step'), f'Invalid step type: {step_type}'
    step_definitions = the_step_registry.steps[step_type]

    def step_decorator(func):
        deco = the_step_registry.make_decorator(step_type)
        for index, existing in enumerate(step_definitions):
            if existing.match(step_text):
                break
        else:
            print('no existing definition to override!')
            deco = deco(step_text)
            return deco(func)

        print(f'replacing step {existing.describe()} from {existing.location} with {func}')
        step_definitions.pop(index)
        deco = deco(step_text)
        return deco(func)  # apply the decorator normally

    return step_decorator
