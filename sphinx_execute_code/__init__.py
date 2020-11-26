#!/usr/bin/env/python
"""
sphinx-execute-code module for execute_code directive
To use this module, add: extensions.append('sphinx_execute_code')

Available options:

        'linenos': directives.flag,
        'output_language': directives.unchanged,
        'hide_code': directives.flag,
        'hide_results': directives.flag,
        'hide_headers': directives.flag,
        'filename': directives.path,
        'hide_filename': directives.flag,
        'hide_import': directives.flag,
        'code_caption': directives.unicode_code,
        'results_caption': directives.unicode_code,
        'hide_code_caption': directives.flag,
        'hide_results_caption': directives.flag,
        'input': string_list,

Usage:

.. example_code:
   :linenos:
   :hide_code:

   print 'Execute this python code'

   See Readme.rst for documentation details
"""
import os
import re
import sys
import ast

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from .mocked_input import MockedInput

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# execute_code function thanks to Stackoverflow code post from hekevintran
# https://stackoverflow.com/questions/701802/how-do-i-execute-a-string-containing-python-code-in-python

__author__ = 'jp.senior@gmail.com'
__docformat__ = 'restructuredtext'
__version__ = '0.3a4'


def string_list(argument):
    """
    Converts a list of values into a Python list of strings.
    (Directive option conversion function.)

    """
    return ast.literal_eval(argument)

class ExecuteCode(Directive):
    """ Sphinx class for execute_code directive
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 5

    option_spec = {
        'linenos': directives.flag,
        'output_language': directives.unchanged,  # Runs specified pygments lexer on output data
        'hide_code': directives.flag,
        'hide_results': directives.flag,
        'hide_headers': directives.flag,
        'filename': directives.path,
        'hide_filename': directives.flag,
        'hide_import': directives.flag,
        'code_caption': directives.unicode_code,
        'results_caption': directives.unicode_code,
        'hide_code_caption': directives.flag,
        'hide_results_caption': directives.flag,
        'input': string_list,
    }

    @classmethod
    def execute_code(cls, code, inputs=None):
        """ Executes supplied code as pure python and returns a list of stdout, stderr

        Args:
            code (string): Python code to execute

        Results:
            (list): stdout, stderr of executed python code

        Raises:
            ExecutionError when supplied python is incorrect

        Examples:
            >>> execute_code('print("foobar")')
            'foobar'
        """

        output = StringIO()
        err = StringIO()

        sys.stdout = output
        sys.stderr = err

        if inputs:
            import builtins
            builtins.input = MockedInput(inputs)

        try:
            # pylint: disable=exec-used
            exec(code, globals())
        # If the code is invalid, just skip the block - any actual code errors
        # will be raised properly
        except TypeError:
            pass
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        results = list()
        results.append(output.getvalue())
        results.append(err.getvalue())
        results = ''.join(results)

        return results

    def run(self):
        """ Executes python code for an RST document, taking input from content or from a filename

        :return:
        """
        language = self.options.get('language') or 'python'
        output_language = self.options.get('output_language') or 'none'
        filename = self.options.get('filename')
        code = ''

        if not filename:
            code = '\n'.join(self.content)
        if filename:
            try:
                with open(filename, 'r') as code_file:
                    code = code_file.read()
                    self.warning('code is %s' % code)
            except (IOError, OSError) as err:
                # Raise warning instead of a code block
                error = 'Error opening file: %s, working folder: %s' % (err, os.getcwd())
                self.warning(error)
                return [nodes.warning(error, error)]

        output = []

        # Show the example code
        if not 'hide_code' in self.options:
            if 'hide_import' in self.options:
                m = re.compile(r"import\s+[\.\w]+\s*\n+", re.MULTILINE)
                displayed_code = m.sub("", code)
            else:
                displayed_code = code
            input_code = nodes.literal_block(displayed_code, displayed_code)

            input_code['language'] = language
            input_code['linenos'] = 'linenos' in self.options
            if not 'hide_headers' in self.options and not 'hide_code_caption' in self.options:
                suffix = ''
                if not 'hide_filename' in self.options:
                    suffix = '' if filename is None else str(filename)
                code_caption = self.options.get('code_caption') or 'Code'

                output.append(nodes.caption(
                    text='%s %s' % (code_caption, suffix)))
            output.append(input_code)

        # Show the code results
        if not 'hide_headers' in self.options and not 'hide_results_caption' in self.options:
            results_caption = self.options.get('results_caption') or 'Results'
            output.append(nodes.caption(text=results_caption))

        inputs = self.options.get('input') or None
        # In all cases evaluate code...
        code_results = self.execute_code(code, inputs)
        #... but optionnally show the results
        if not 'hide_results' in self.options:
                code_results = nodes.literal_block(code_results, code_results)

                code_results['linenos'] = 'linenos' in self.options
                code_results['language'] = output_language
                output.append(code_results)
        return output


def setup(app):
    """ Register sphinx_execute_code directive with Sphinx """
    app.add_directive('execute_code', ExecuteCode)
    return {'version': __version__}
