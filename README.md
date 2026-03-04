# Retail Sales Strategic Performance Dashboard

## Project Overview

This project is an advanced **Retail Sales Analytics Dashboard** designed to analyze business performance across regions, product categories, and customer segments.

The system integrates **SQL, Python, and Streamlit** to transform raw transactional data into meaningful business insights.

The dashboard helps evaluate:

- Revenue performance
- Profitability trends
- Customer revenue concentration
- Regional and category performance
- Growth trends over time

---

## Business Objective

The goal of this project is to simulate how a data analyst would analyze sales data for a retail company and convert raw data into strategic insights that support business decision-making.

Key business questions addressed:

- Which regions generate the highest revenue?
- Which product categories produce the best profit margins?
- How concentrated is revenue among top customers?
- What are the growth trends over time?
- Which regions or categories are underperforming?

---

## System Architecture

The project follows a structured analytics pipeline:

Raw Dataset → SQLite Database → SQL Queries → Python Analytics → Streamlit Dashboard

Technologies used:

- Python  
- SQL (SQLite)  
- Pandas  
- NumPy  
- Matplotlib  
- Streamlit  

---

## Key Dashboard Metrics

### Executive KPIs

- Total Revenue
- Total Profit
- Profit Margin %
- Year-over-Year Growth
- Revenue Volatility
- 90th Percentile Order Value

### Strategic Performance Analysis

- Revenue contribution by region
- Revenue contribution by product category
- Profit per order
- Revenue per customer

### Advanced Analytics

- Customer concentration analysis (Pareto principle)
- Monthly revenue trend analysis
- Identification of weakest performing region
- Identification of lowest margin category

---

## Dashboard Features

The dashboard includes interactive filters for:

- Region
- Product Category
- Customer Segment

All KPIs and charts update dynamically based on filter selections.

---

## Project Structure

retail-sales-strategic-dashboard

dashboard.py  
sql_analysis.py  
retail_sales_dataset.csv  
retail_sales.db  
requirements.txt  
README.md  

---

## Running the Project Locally

Clone the repository:

git clone https://github.com/bablu1845/Retail-Sales-Strategic-Dashboard

Install dependencies:

pip install -r requirements.txt

Run the dashboard:

streamlit run dashboard.py

---

## Skills Demonstrated

- Data Cleaning and Transformation
- SQL-based Business Analysis
- KPI Design and Metric Engineering
- Exploratory Data Analysis
- Interactive Dashboard Development
- Business Performance Diagnostics

---

## Author

Belide Adithya  
Data Science Student | Aspiring Data Analyst