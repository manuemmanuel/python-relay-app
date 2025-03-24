-- Create input_real_time_data table
CREATE TABLE IF NOT EXISTS input_real_time_data (
    id BIGSERIAL PRIMARY KEY,
    Computer_TS TIMESTAMP WITH TIME ZONE,
    "A Phase Voltage" DOUBLE PRECISION,
    "A Phase Current" DOUBLE PRECISION,
    "A Phase Active Power" DOUBLE PRECISION,
    "A Phase Reactive Power" DOUBLE PRECISION,
    "A Phase Apparent Power" DOUBLE PRECISION,
    "A Power Factor" DOUBLE PRECISION,
    "B Phase Voltage" DOUBLE PRECISION,
    "B Phase Current" DOUBLE PRECISION,
    "B Phase Active Power" DOUBLE PRECISION,
    "B Phase Reactive Power" DOUBLE PRECISION,
    "B Phase Apparent Power" DOUBLE PRECISION,
    "B Power Factor" DOUBLE PRECISION,
    "C Phase Voltage" DOUBLE PRECISION,
    "C Phase Current" DOUBLE PRECISION,
    "C Phase Active Power" DOUBLE PRECISION,
    "C Phase Reactive Power" DOUBLE PRECISION,
    "C Phase Apparent Power" DOUBLE PRECISION,
    "C Power Factor" DOUBLE PRECISION,
    "Frequency" DOUBLE PRECISION,
    "DC Voltage" DOUBLE PRECISION,
    "DC Current" DOUBLE PRECISION,
    "Temperature" DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create output_real_time_data table
CREATE TABLE IF NOT EXISTS output_real_time_data (
    id BIGSERIAL PRIMARY KEY,
    Computer_TS TIMESTAMP WITH TIME ZONE,
    "A Phase Voltage" DOUBLE PRECISION,
    "A Phase Current" DOUBLE PRECISION,
    "A Phase Active Power" DOUBLE PRECISION,
    "A Phase Reactive Power" DOUBLE PRECISION,
    "A Phase Apparent Power" DOUBLE PRECISION,
    "A Power Factor" DOUBLE PRECISION,
    "B Phase Voltage" DOUBLE PRECISION,
    "B Phase Current" DOUBLE PRECISION,
    "B Phase Active Power" DOUBLE PRECISION,
    "B Phase Reactive Power" DOUBLE PRECISION,
    "B Phase Apparent Power" DOUBLE PRECISION,
    "B Power Factor" DOUBLE PRECISION,
    "C Phase Voltage" DOUBLE PRECISION,
    "C Phase Current" DOUBLE PRECISION,
    "C Phase Active Power" DOUBLE PRECISION,
    "C Phase Reactive Power" DOUBLE PRECISION,
    "C Phase Apparent Power" DOUBLE PRECISION,
    "C Power Factor" DOUBLE PRECISION,
    "Frequency" DOUBLE PRECISION,
    "DC Voltage" DOUBLE PRECISION,
    "DC Current" DOUBLE PRECISION,
    "Temperature" DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_input_computer_ts ON input_real_time_data(Computer_TS);
CREATE INDEX IF NOT EXISTS idx_output_computer_ts ON output_real_time_data(Computer_TS);

-- Create unique constraints to prevent duplicates
CREATE UNIQUE INDEX IF NOT EXISTS idx_input_unique_ts ON input_real_time_data(Computer_TS);
CREATE UNIQUE INDEX IF NOT EXISTS idx_output_unique_ts ON output_real_time_data(Computer_TS); 