# Changelog

## [Latest Update] - 2025-01-28

### Added
- **Consumer Complaints Section** - A new comprehensive tab has been added to display individual consumer complaint details
- Complete complaint details including:
  - Complaint ID with clickable CFPB.gov links
  - Company name and response information
  - Timely response indicator
  - Date received
  - Consumer's state
  - Product and sub-product categories
  - Issue and sub-issue details
  - Full consumer complaint narrative
- Interactive filtering system:
  - Filter by company (top 50 companies available)
  - Filter by product category
  - Adjustable number of complaints to display (10, 25, 50, 100, 200)
- Expandable card layout for easy viewing
- Direct links to verify each complaint on CFPB.gov

### Technical Improvements
- Added new `show_consumer_complaints()` function to web_dashboard.py
- Robust column name mapping to handle different case conventions
- Smart handling of missing or empty fields
- Efficient display with pandas data handling

### Deployment
- Changes pushed to both `restore-website` and `main` branches
- Ready for automatic deployment on Render.com
- No additional configuration needed

---

## [Previous Version]
- Professional analytics dashboard
- AI chat assistant integration
- Comprehensive data visualization
- Special categories analysis (AI bias, LEP issues, fraud)
- Excel export functionality

