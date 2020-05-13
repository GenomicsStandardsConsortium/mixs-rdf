# MIXS-RDF notebooks
This directory contains Jupyter notebooks that demonstrate or perform tasks related to the MIXS-RDF project.  

We use `venv` to create virtual environments and manage module dependencies.  
To create a virtual environment run the command `python3 -m venv <environment name>` in the current directory.  
I typically name my environment `.env`, and configure `.gitignore` to ignore `.env` files. This prevents the environment libraries from being uploaded to the repository.  

After the environment is created, run the command `source <environment name>/bin/activate` to enter the environment.  
Once in the environment, use `pip` to install libraries (e.g., `pip install pandas`). Once all the libraries have been installed you can export a list of them using the `pip freeze` command. Typically, the list is saved to a file named `requirements.txt`.  
e.g., `pip freeze > requirements.txt`  

To load a list of dependencies, use the `pip install -r` command.  
e.g., `pip install -r requirements.txt`

You exit the environment by executing the command `deactivate` in the terminal.

# common-mixs-package-terms notebook  
This notebook outputs an analysis of which terms are shared across the different environmental packages. Terms were matched according to their label and definition. That is, if terms in different packages had the same values in the Package item and Definition fields, they were determined to be a match.  

The results of the analysis are contained in the files [output/mixs-package-term.xlsx](output/mixs-package-term.xlsx) and [output/multi-package-mixs-terms-only.xlsx](output/multi-package-mixs-terms-only.xlsx). The [output/multi-package-mixs-terms-only.xlsx](output/multi-package-mixs-terms-only.xlsx) file is simply the output/mixs-package-term.xlsx](output/mixs-package-term.xlsx) file filtered for terms that occur more than once.  

The name of the environmental package is contained in the column headers. If the term is contained in the package, it is marked with a "1". If not, it marked with a "0". The last column contains the list of MIXS IDs associated with the term.
