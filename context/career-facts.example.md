# Career facts: Alex Example

This is an example. Alex Example and every company here are fictional. Copy this file to
`context/career-facts.md` and replace everything with your own facts.

This file is the only source of claims for résumés, cover letters and answers. If something is
not here or on the master résumé, the agents ask before using it. Keep each fact concrete
enough that you could explain it in an interview: what you did, with what, at what scale, and
for how long. Add a dated note when you confirm something new.

## Employment, newest first

### Northwind Systems, Senior QA Automation Engineer (Mar 2021 to present)

- Employer: Northwind Systems, a logistics software company. Direct hire, full-time.
- Product: a web portal and REST API that shippers use to book and track freight.
- Built the UI test suite in Playwright with TypeScript, about 600 tests, run on every pull
  request in GitHub Actions.
- Wrote API tests in REST Assured with Java against the booking and tracking services, and
  validated responses against the PostgreSQL database with SQL queries.
- Ran exploratory testing on releases and wrote risk-based regression plans for each release.
- Mentored two junior testers: pairing on test design, reviewing their pull requests.
- Moved flaky UI tests into a quarantine job and fixed the most common cause (fixed waits
  replaced by web-first assertions). No measured before and after numbers.

### Trey Research, QA Engineer (Jun 2018 to Feb 2021)

- Employer: Trey Research, a market-research software company. Direct hire, full-time.
- Tested a survey-building web app and its reporting module.
- Automated browser tests in Selenium WebDriver with Java and TestNG, run nightly in Jenkins.
- Tested the reporting exports (CSV, Excel) by comparing them with SQL query results.
- Worked in two-week Agile/Scrum sprints; joined refinement and wrote acceptance criteria with
  the product owner.

## Skills, with evidence

| Skill | Level | Where and how long |
|---|---|---|
| Playwright (TypeScript) | Strong | Northwind, 3.5 years, built the suite |
| Selenium WebDriver (Java) | Strong | Trey Research, 2.5 years |
| REST API testing (REST Assured, Postman) | Strong | Northwind, daily |
| SQL (PostgreSQL, SQL Server) | Working | Data validation at both employers |
| GitHub Actions | Working | Maintained the Northwind test workflows |
| Jenkins | Working | Nightly jobs at Trey Research |
| Docker | Basic | Ran local test environments with Docker Compose; never built images for production |
| k6 performance testing | None confirmed | Ask before claiming |

## Soft skills, with evidence

- Mentoring: two junior testers at Northwind, weekly pairing for about a year.
- Working with product owners: wrote acceptance criteria at Trey Research.
- Working independently: sole tester on the reporting module for one year.

## Known gaps

Do not paper over these. Report them as gaps.

- No mobile test automation (Appium, Espresso, XCUITest).
- No performance or load testing beyond running a colleague's JMeter script.
- No outcome metrics (defect escape rates, time saved). Do not invent them.
- Has not managed people or owned a QA budget.

## Claims that are always wrong

- "Led the QA department" (Alex mentored; there was a QA manager).
- "Built the CI/CD pipeline" (Alex maintained test jobs inside existing pipelines).
- Any certification. Alex holds none.

## Claims that are always safe

- "Over 8 years in software quality engineering."
- "Built and maintain a Playwright and TypeScript UI suite that runs on every pull request."

## Confirmed later

Dated notes added when Alex confirmed new experience during tailoring.

- Confirmed during an example tailoring run: used Postman collections with Newman in CI at
  Northwind for about six months. Fine to list Newman as a tool.
