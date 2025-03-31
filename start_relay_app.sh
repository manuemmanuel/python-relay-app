#!/bin/bash

# Open first terminal and wait for 1 second
gnome-terminal -- bash -c "source ~/my_env/bin/activate; cd '/home/rahul/Desktop/python-relay-app/1_input-output data log code'; python3 input_data_log_code.py; exec bash"
sleep 1

# Open second terminal and wait for 1 second
gnome-terminal -- bash -c "source ~/my_env/bin/activate; cd '/home/rahul/Desktop/python-relay-app/1_input-output data log code'; python3 output_data_log_code.py; exec bash"
sleep 1

# Open third terminal and wait for 1 second
gnome-terminal -- bash -c "source ~/my_env/bin/activate; /usr/bin/python3 '/home/rahul/Desktop/python-relay-app/Relay Program/Jetson_Relay_code_prime_working.py'; exec bash"
sleep 1

# Open fourth terminal for main.py with conda environment
gnome-terminal -- bash -c "conda activate py13; cd '/home/rahul/Desktop/python-relay-app'; python main.py; exec bash"
sleep 1

# Open Chrome in the fifth terminal
gnome-terminal -- bash -c "cd '/home/rahul/Desktop'; chromium-browser --new-window https://protection-relay-02.vercel.app/login; exec bash"

