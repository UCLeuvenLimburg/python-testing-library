from setuptools import setup, find_packages


setup(name='ucll_scripting',
      version='0.1',
      description='UCLL Scripting',
      url='http://github.com/UCLeuvenLimburg/ucll-scripting',
      author='Frederic Vogels',
      author_email='frederic.vogels@ucll.be',
      license='MIT',
      packages=find_packages(),
      test_suite='nose2.collector.collector',
      entry_points = {
          'console_scripts': [ 'run-tests=ucll_scripting.shell:run_tests' ]
      },
      zip_safe=False)
