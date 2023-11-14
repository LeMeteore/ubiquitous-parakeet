# Introduction

## 1.1 Purpose

The purpose of this document is to build an online system to automate the mapping of each result returned by a spectrophotometer to the correct patient, build a recap, draw some charts.

## 1.2 Intended Audience:

The intended and primary audience of this document are all the people at IPD labs dealing with PCR plate plans, all the people at the DDSI. This document will be written with no technical terms (_hopefully_) for the benefit of everyone on the team. It will define the business rules of this application.

## 1.3 Scope:

One of the chore at the IPD immunology lab is (_among other things_) to get the results returned by their [spectrophotometer](https://www.thermofisher.com/sn/en/home/life-science/lab-equipment/microplate-instruments/plate-readers/models/multiskan-skyhigh.html) and for each result, retrieve what is the associated patient. The patients samples are retrieved from a [96 wells PCR plate](https://www.azenta.com/products/96-well-skirted-pcr-plate). This task is actually done manually, using Excel files. the current project will try to ease this process.

# Overall Description of the product

The system stores the following informations:

- Patients (firstname, lastname, date of birth, sex,)
- PCR plate plans (name, shape, size, controls, patients list)
- PCR plate associated results 

## 2.1 User Needs

The user of the system should be able to do the following: 

- Register patients using an Excel files
- Register one patient using a form
- Create a PCR plate using a form 
- Add a patient or a control inside a PCR plate
- Map spectrophotometer results to a PCR plate plan
- Draw some charts 
- Download results

# System Features and Requirements

Forms... Tables.... Charts... Submit & Download buttons... Everywhere...

## 3.1 Functional Requirements

This project is a proof of conept built to quickly iterate and validate the desired features. In the long run, the system will be broken and rebuilt in 3 parts:

- A frontend
- A backend
- A database 

## Installation and Usage:

To run the project locally, one may want to :

- git clone the repository: `git clone ...`
- cd into the repository `cd ...`
- create a Python virtualenv `python -m venv .env`
- activate the Python virtualenv `source .env/bin/activate`
- install Dependencies: `pip install -r requirements.txt`
- go inside the poc directory then: `streamlit run application.py`
- open a web browser and visit the following url: `http://localhost:8501`

For those afraid by the command line, a not yet fully working PoC is available [here](https://applicationpy-nsk3kpmtdwb9azmg9o7gra.streamlit.app/Process_results)

