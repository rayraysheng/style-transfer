# Development stage
FROM python:3.10 AS development

# Install HDF5 library
RUN apt-get update && apt-get install -y libhdf5-dev

# Install Cython
RUN python -m pip install Cython numpy pkgconfig Pillow

# Clone h5py repository
RUN git clone https://github.com/h5py/h5py /h5py

# Modify setup_configure.py
RUN sed -i 's|default_path = .*|default_path = "/opt/homebrew/lib/libhdf5.dylib"|' /h5py/setup_configure.py

# Build and install h5py
WORKDIR /h5py
RUN H5PY_SETUP_REQUIRES=0 python3 setup.py build
RUN python3 -m pip install . --no-build-isolation

# Clean up
WORKDIR /
RUN rm -rf /h5py

WORKDIR /app
COPY ./backend/requirements.txt ./

# Install application dependencies
RUN pip install -r requirements.txt

# Command to run application
CMD ["python", "app.py"]

# Production stage
FROM development as production
RUN pip3 install gunicorn
CMD ["gunicorn", "-w", "2", "-c", "config.py", "app:app"]
