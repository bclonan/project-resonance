## How to Run the Demos

****1.  **Install Libraries:** Make sure you have run `pip install .` from the parent `resonance` directory to install the C++-backed libraries.
2.  **Install Demo Dependencies:** Navigate into the `resonance_demos` directory and run:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Web Server:** From inside the `resonance_demos` directory, run:
    ```bash
    uvicorn app:app --reload
    ```
4.  **Open Your Browser:** Navigate to `http://127.0.0.1:8000`. You will see the main landing page, and from there you can launch each of the four interactive demos.
5.  

## How to build and deploy the demos

1. 