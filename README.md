# Norway Housing

## Description
This project is designed to help make informed decisions on how to buy a house in Norway. The
data was collected from www.finn.no. The goal will be to take the data that is pulled from this
webpage and create an interactive dashboard that performs an analysis on the Norwegian housing market along
with predictions regarding the future.  

## Table of Contents
- [Installation](#installation)
- [How&nbsp;to&nbsp;Use](#how_to_use)
- [Features](#features)
- [Planned&nbsp;Features](#planned-features)
- [Contributing](#contributing)
- [Contact](#contact)
- [Features](#license)

## Installation
(There will be more on this as a version 1.0 release is approached)<br>
Steps:<br>
[1] Ensure that Python is installed on your machine. <br>
[2] Open your terminal.<br>
[3] Run ´cd path/to/the/norway_housing/project/on/your/local/machine´<br>
[4] Run ´python3 -m venv housing_env´<br>
[5] Run ´housing_env/Scripts/activate´ (Windows) or ´source housing_env/bin/activate´(MacOS & Linux)<br>
[6] Run ´pip install -r requirements.txt´<br>

## How to Use
[1] Run 'python3 src/data_fetcher.py'

- You will see it run 50 steps via a loading bar. Each step is the extraction of 
a webpage's worth of data. Afterwards, it will print the data that has been cleaned.

## Features
- The ability to grab the first 50 pages of house data based on a generic "relevant" search from finn.no
- The ability to clean data collected.  

## Planned Features
- A way of storing the data on the cloud.
- A way of downloading the data
- A data dashboard
- Unit tests
- In depth documentation

## Contributing
Blake Cromar, Artificial Intelligence Engineer

## Contact
- Blake Cromar, [blake.cromar@icloud.com] or [+47 458 11 997] or [https://www.linkedin.com/in/blake-cromar/]

## License
MIT License

Copyright (c) 2024 [Blake Cromar]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


