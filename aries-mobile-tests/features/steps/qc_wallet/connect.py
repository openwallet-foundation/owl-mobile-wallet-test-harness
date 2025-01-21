from bc_wallet.connect import *
from override_steps import overrides
from pageobjects.qc_wallet.biometrics import BiometricsPageQC


@overrides('a PIN has been set up with "{pin}"', "given")
def step_impl(context, pin):
    # context.execute_steps(f'''
    #     Given the User is on the PIN creation screen
    #     When the User enters the first PIN as "{pin}"
    #     And the User re-enters the PIN as "{pin}"
    #     And the User selects Create PIN
    #     And the User selects to use Biometrics
    #     Then the User has successfully created a PIN
    # ''')
    context.execute_steps(
        f"""
        Given the User is on the PIN creation screen
        When the User enters the first PIN as "{pin}"
        And the User re-enters the PIN as "{pin}"
        And the User selects Create PIN
    """
    )