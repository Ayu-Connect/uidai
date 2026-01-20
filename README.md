# 📊 Aadhaar Enrollment Smart Analytics Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Data_Science](https://img.shields.io/badge/Data-Science-blue?style=for-the-badge)

## 🌟 Overview
Ye project ek advanced analytics tool hai jo **Aadhaar enrollment data** ko process karta hai. Iska main objective un areas (districts) ko identify karna hai jahan enrollment piche hai (Gaps), aur machine learning ke zariye aane wale 7 dino ki enrollment demand ko predict karna hai.



## 🛠️ Key Features

### 1. Saturation Gap Index (USP) 🎯
Adult enrollment aur child enrollment ke beech ke ratio ko analyze karke ye tool ek **Priority Score** calculate karta hai. 
* Formula: $Saturation Gap = \frac{Age 18+}{Age 0-5 + 1}$
* Isse un districts ka pata chalta hai jahan adults ka enrollment toh ho chuka hai, par bachon ka baki hai.

### 2. Predictive Demand Forecasting 📈
Linear Regression model ka use karke ye system historical trends ko analyze karta hai aur aane wale 7 dino ke liye total enrollment volume predict karta hai.

### 3. Interactive Geographical Heatmaps 🗺️
Plotly Treemaps ka use karke pure desh ke states aur districts ka hierarchical view milta hai.
* **Red Color:** High Priority / High Saturation Gap.
* **Green Color:** Low Priority / Stable Enrollment.

## 📂 Project Structure
```text
├── api_data_aadhar_enrolment_0_500000.csv        # Dataset Part 1
├── api_data_aadhar_enrolment_500000_1000000.csv  # Dataset Part 2
├── api_data_aadhar_enrolment_1000000_1006029.csv # Dataset Part 3
├── app.py                                        # Streamlit Dashboard Code
├── requirements.txt                              # Required Libraries
└── README.md                                     # Project Documentation
