My personal project for IBM Capstone Project course in the IBM Data Analyst Professional Certificate program via Coursera, analyzing Stack Overflow Developer Survey data set modified by IBM 



[Here's the source](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/HLOosvsPgIwt5dgOOh1RSg/survey-data-updated.csv)



This repo showcase my skills, documenting my works as a start level Data Analyst and my findings for this project.

[Dashboard](https://datastudio.google.com/reporting/39b0a36c-e439-4149-9690-8613798ff677)
[Slide](./Presentation.pdf)

## Method
I performed Exploratory Data Analysis (EDA) and data wrangling in the `cleaning.py` file. According to the IBM course guidelines, columns intended for visualization need to be processed using `pd.explode()`. However, exploding all columns at once would expand the dataset excessively. To address this, I wrote a program that generates separate CSV files, each corresponding to a specific table required for a particular visualization, stored in the `data` folder.

---
### Brief findings

- Tech Stack Continuity: High alignment between production tools and desired technologies indicates strong ecosystem stability across:
  - Tools, frameworks, platforms, and databases

- Shift Toward Systems Efficiency: Learning trends demonstrate a strategic pivot toward modern systems languages (e.g., Rust, Go)

- Generational Divide in Web Frameworks:
  - Senior developers (\~12 yrs exp) maintain established enterprise stacks (ASP.NET, jQuery)
  - Junior developers (<8 yrs exp) lean toward modern JS/Python frameworks (Next.js, FastAPI)

- Young and highly educated workforce demographics
