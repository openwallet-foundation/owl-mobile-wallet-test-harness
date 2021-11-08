# Aries Mobile Test Harness<!-- omit in toc -->

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

The Aries Mobile Test Harness (AMTH) is a [ATDD](https://en.wikipedia.org/wiki/Acceptance_test–driven_development)-based test execution engine and set of tests for evaluating the Mobile Wallet/Agents Apps on both Android and iOS. The harness can be used to develop a set of tests that can trigger app events as well as get screen results from the wallet apps running in a device cloud. It also can call Aries Issuer or Verifier controllers that can be used to round out end to end tests for the solution that includes Wallets, Issuers, and Verifiers. 

The framework consists of Python, Behave, Appium, BrowserStack, and Allure Reporting. It borrows concepts from Acceptance Test Driven Development methodologies to write and execute tests, it also utilizes a Page Object Pattern/Model to isolate tests from app UI changes. 
Note: If your wallet is an open source wallet, you can get free access to BrowserStack (or SauceLabs) to test the wallet. 

Want to see the Aries Mobile Test Harness in action? Give it a try using a git, docker and bash enabled system. Once you are in a bash shell, run the following commands to execute a set of sample tests. INCOMPLETE

```bash
git clone https://github.com/bcgov/aries-mobile-test-harness
cd aries-mobile-tests
docker build -f aries-mobile-tests/Dockerfile.harness -t aries-mobile-test-harness .
docker run aries-mobile-test-harness
/aries-mobile-test-harness/aries-mobile-tests> behave

```

## Contents<!-- omit in toc -->

- [Architecture](#architecture)
- [Aries Mobile Test Harness Terminology](#aries-agent-test-harness-terminology)
- [Test Script Guidelines](#test-script-guidelines)
- [Implementing Tests for Your Wallet](#aries-agent-backchannels)
  - [Writting Page Objects for your Wallet](#implemented-backchannels)
- [The `manage` bash script](#the-manage-bash-script)
- [Test Tags](#test-tags)
  - [Running Tagged Tests](#running-tagged-tests)
  - [Test Coverage](#test-coverage)
  - [Test Reporting](#test-reporting)

## Architecture

The following diagram provides an overview of the architecture of the AMTH.

![Aries Mobile Test Harness Architecture](docs/assets/amth-arch/amth-arch.png)


## Aries Mobile Test Harness Terminology


## Test Script Guidelines

AMTH test scripts are written in the [Gherkin](https://behave.readthedocs.io/en/latest/gherkin.html#gherkin-feature-testing-language) language, using the python [behave](https://behave.readthedocs.io/en/latest/) framework. Guidelines for writing test scripts are located [here]().

## Implementing Tests for Your Wallet


### Writting Page Objects for your Wallet


## The `manage` bash script

The AMTH `./manage` script in the repo root folder is used to manage running builds of images and initiate test runs. Running the script with no arguments or just `help` to see the script's usage information. The following summarizes the key concepts.


## Test Tags

The test harness has utilized tags in the BDD feature files to be able to narrow down a test set to be executed at runtime. The general AATH tags currently utilized are as follows:

- @AcceptanceTest - Tests based on requirements specifically stated in the RFC.
- @DerivedFunctionalTest - Tests derived on requirements but not specifically stated in the RFC.
- @P1, @P2, @P3, @P4 - Test Priority.
- @NegativeTest - Test that attempts to break the software. ie. change workflow order, use invalid data, etc.
- @ExceptionTest - Tests that are based on requirements that suggest exception cases.
- @SmokeTest - Tests that can be used as a builds smoke or sanity tests.
- @NeedsReview - Tests that have not been reviewed or approved.
- @ReviewedApproved - Tests that have been reviewed and approved.
- @wip - Tests that are a work in progress and incomplete.
- @Done - Finished tests that are expected to Pass if executed against a Test Agent.
- @T001-walletname-featurename - Unique Test Identifiers.

To get a list of all the tags in the current test suite, run the command: `./manage tags`

To get a list of the tests (scenarios) and the associated tags, run the command: `./manage tests`

### Running Tagged Tests (WIP)

Using tags, one can just run Acceptance Tests...

```bash
./manage run -t @AcceptanceTest
```

or all Priority 1 Acceptance Tests, but not the ones flagged Work In Progress...

```bash
./manage run -t @P1 -t @AcceptanceTest -t ~@wip
```

or derived functional tests

```bash
./manage run -t @DerivedFunctionalTest
```

or all the ExceptionTests...

```bash
./manage run -t @ExceptionTest
```

Using AND, OR in Test Execution Tags
Stringing tags together in one `-t` with commas as separators is equivalent to an `OR`. The separate `-t` options is equivalent to an `AND`.

```bash
./manage run -t @RFC0453,@RFC0454 -t ~@wip -t ~@CredFormat_JSON-LD
```

So the command above will run tests from RFC0453 or RFC0454, without the wip tag, and without the CredFormat_JSON-LD tag.

To read more on how one can control the execution of test sets based on tags see the [behave documentation](https://behave.readthedocs.io/en/stable/tutorial.html#controlling-things-with-tags)

The option `-i <inifile>` can be used to pass a file in the `behave.ini` format into behave. With that, any behave configuration settings can be specified to control how behave behaves. See the behave documentation about the `behave.ini` configuration file [here](https://behave.readthedocs.io/en/stable/behave.html#configuration-files).

### Test Coverage



### Test Reporting

For information on enhanced test reporting with Allure in the Aries Mobile Test Harness, see [Advanced Test Reporting]().
