---
name: financial-calculator
description: Advanced financial calculator with future value tables, present value, discount calculations, markup pricing, and compound interest. Use when calculating investment growth, pricing strategies, loan values, discounts, or comparing financial scenarios across different rates and time periods. Includes both CLI and interactive web UI.
---

# Financial Calculator

Comprehensive financial calculations including future value, present value, discount/markup pricing, compound interest, and comparative tables.

## Quick Start

### CLI Usage

```bash
# Future Value
python3 scripts/calculate.py fv 10000 0.05 10 12
# PV=$10,000, Rate=5%, Years=10, Monthly compounding

# Present Value
python3 scripts/calculate.py pv 20000 0.05 10 12
# FV=$20,000, Rate=5%, Years=10, Monthly compounding

# Discount
python3 scripts/calculate.py discount 100 20
# Price=$100, Discount=20%

# Markup
python3 scripts/calculate.py markup 100 30
# Cost=$100, Markup=30%

# Future Value Table
python3 scripts/calculate.py fv_table 10000 0.03 0.05 0.07 --periods 1 5 10 20
# Principal=$10,000, Rates=3%,5%,7%, Periods=1,5,10,20 years

# Discount Table
python3 scripts/calculate.py discount_table 100 10 15 20 25 30
# Price=$100, Discounts=10%,15%,20%,25%,30%
```

### Web UI

Launch the interactive calculator:

```bash
./scripts/launch_ui.sh [port]
# Default port: 5050
# Opens at: http://localhost:5050
# Auto-creates venv and installs Flask if needed
```

Or manually:
```bash
cd skills/financial-calculator
python3 -m venv venv  # First time only
venv/bin/pip install flask  # First time only
venv/bin/python scripts/web_ui.py [port]
```

**Features:**
- 7 calculator types with intuitive tabs
- Real-time calculations
- Interactive tables
- Beautiful gradient UI
- Mobile-responsive design
