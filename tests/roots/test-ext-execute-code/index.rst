tests
=====

This is a test

.. execute_code::

    print('execute_code:' + 'sample_1')

.. execute_code::
   :linenos:

   print('execute_code_linenos:' + 'sample_2')

.. execute_code::
   :output_language: javascript

   data = {'execute_code': 'sample_3', 'output_language': 'javascript', 'sample3': True}
   import json
   print(json.dumps(data))

.. sample_4:

.. execute_code::
   :filename: tests/example_class.py

.. execute_code::
   :filename: tests/example_class.py

   print('execute_code_should_not_run:' + 'sample_5')
   #execute_code_sample_5_comment_is_hidden

.. execute_code::
   :hide_code:

   print('execute_code_hide_code:sample_6')
   # This comment is hidden


.. execute_code::

   print('execute_code_show_header:' + 'sample_7')

.. execute_code::
   :hide_headers:

   print('execute_code_hide_header:' + 'sample_8')

.. execute_code::
   :filename: tests/hidden_filename.py
   :hide_filename:

.. execute_code::
   :hide_headers:
   :hide_import:

   import os
   print('execute_code_hide_import:' + 'sample_10')

.. execute_code::
   :results_caption: Results for example code

   print('execute_code_results_caption:' + 'sample_11')

.. execute_code::
   :code_caption: Example code

   print('execute_code_code_caption:' + 'sample_12')

.. execute_code::
   :input: ["sample_13-1","sample_13-2"]

   print('execute_code_input:' + 'sample_13')
   var = input("Enter first value")
   print('execute_code_input:' + var)
   var = input("Enter second value")
   print('execute_code_input:' + var)


.. execute_code::
   :hide_results_caption:

   print('execute_code_hide_results_caption:' + 'sample_14')

.. execute_code::
   :hide_code_caption:

   print('execute_code_hide_code_caption:' + 'sample_15')