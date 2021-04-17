# Development guide

## Environment

Prepare the build and test environment by setting up a Python virtual environment:

```bash
# Install the virtualenv package
python3 -m pip install --user virtualenv

# Create a new virtualenv for the plugin
python3 -m venv venv
```

The build and test scripts automatically activate the virtual environment where needed.
To manually activate it, run the following command:

```bash
source venv/bin/activate
```

## Building

Run the build script

```bash
./build.sh
```

The output of this script is a `.zip` file that can be uploaded in the [Ultimaker Contributor Portal](https://contribute.ultimaker.com).

> A GitHub Action has been configured to automatically create a build on every pull request.
  You can download the artifacts for each GitHub Action via the GitHub user interface.

## Testing

Run the test suite (~60% coverage):

```bash
./test.sh
```
