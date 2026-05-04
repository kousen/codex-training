Python Refactoring Starter
===========================

This documentation describes the refactored data-processing package used in
the Codex CLI training lab.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Architecture
------------

The repository includes Mermaid architecture diagrams in ``architecture.md``.

Usage
-----

Run the command-line wrapper with explicit input and output files:

.. code-block:: bash

   python legacy_processor.py --input /tmp/input.json --output /tmp/output.json

Quality Checks
--------------

.. code-block:: bash

   make test
   make typecheck
   make lint
   make docs
