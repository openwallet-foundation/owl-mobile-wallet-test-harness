from bc_wallet.change_language import *
from override_steps import overrides
from pageobjects.bc_wallet.pin import PINPage

@overrides('the language is set to {different_language}', 'then')
def verify_lang_change_on_relaunch_app_step_impl(context, different_language):
    # LambdaTest does not support biometric authentication
    if type(context.device_service_handler).__name__ != 'LambdaTestHandler':
        sleep(5)
        context.thisBiometricsPage = BiometricsPage(context.driver)
        assert context.thisBiometricsPage.on_this_page(different_language)
    else:
        sleep(5)
        context.thisPINPage = PINPage(context.driver)
        assert context.thisPINPage.on_this_page(different_language)
