import streamlit as st

st.title("UK Renting Cost Calculator")

tab_upfront, tab_monthly = st.tabs(["UpFront", "Monthly & Affordability"])

with tab_upfront:
    st.markdown("<h2 style='font-size:2.2em;'>UpFront Cost Calculator</h2>", unsafe_allow_html=True)
    st.markdown("Enter your expected monthly rent and add upfront items one by one to see your total upfront cost.")

    monthly_rent_upfront = st.number_input(
        "Enter the monthly rent (£)", min_value=0.0, step=10.0, format="%.2f", key="monthly_rent2"
    )
    weekly_rent_upfront = monthly_rent_upfront * 12 / 52

    holding_deposit_upfront = weekly_rent_upfront  # 1 week
    deposit_upfront = 5 * weekly_rent_upfront      # 5 weeks
    first_month_rent = monthly_rent_upfront

    # Use session state to track which items are added
    if "upfront_items" not in st.session_state:
        st.session_state.upfront_items = set()

    # Display each item in a row with a plus button
    def add_row(label, value, key_name, item_code):
        colA, colB = st.columns([3, 1])
        with colA:
            st.write(f"{label}: £{value:.2f}")
        with colB:
            if item_code not in st.session_state.upfront_items:
                if st.button("➕", key=key_name):
                    st.session_state.upfront_items.add(item_code)
            else:
                st.markdown("<span style='color:green;font-weight:bold;'>Added</span>", unsafe_allow_html=True)

    add_row("Holding deposit (1 week)", holding_deposit_upfront, "add_holding", "holding")
    add_row("Tenancy deposit (5 weeks)", deposit_upfront, "add_tenancy", "tenancy")
    add_row("First month rent", first_month_rent, "add_first_rent", "first_rent")

    # Calculate total upfront cost
    total_upfront_cost = 0
    breakdown = []
    if "holding" in st.session_state.upfront_items:
        total_upfront_cost += holding_deposit_upfront
        breakdown.append(f"- Holding deposit: £{holding_deposit_upfront:.2f}")
    if "tenancy" in st.session_state.upfront_items:
        total_upfront_cost += deposit_upfront
        breakdown.append(f"- Tenancy deposit: £{deposit_upfront:.2f}")
    if "first_rent" in st.session_state.upfront_items:
        total_upfront_cost += first_month_rent
        breakdown.append(f"- First month rent: £{first_month_rent:.2f}")

    st.markdown("### Upfront Cost Breakdown")
    if breakdown:
        st.markdown("\n".join(breakdown))
        st.markdown(f"**Total upfront cost:** £{total_upfront_cost:.2f}")
        if st.button("Reset Upfront Items"):
            st.session_state.upfront_items = set()
    else:
        st.info("Add items using the ➕ buttons to see your total upfront cost.")

    st.caption("Add each upfront item you expect to pay. You can reset and try again.")

with tab_monthly:
    st.markdown("<h2 style='font-size:2.2em;'>Monthly & Affordability Calculator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("What's your name?", key="name1")
        income_type = st.radio(
            "Is your income Gross (before tax) or Net (after tax)?", 
            ("Gross", "Net"), horizontal=True, key="income_type1"
        )
        income_period = st.selectbox(
            "Is your income Monthly or Yearly?", 
            ("Monthly", "Yearly"), key="income_period1"
        )
        if income_period == "Yearly":
            income = st.number_input(
                "Your yearly income (£)", min_value=0.0, step=1000.0, format="%.2f", key="income_year1"
            )
            monthly_income = income / 12
        else:
            income = st.number_input(
                "Your monthly income (£)", min_value=0.0, step=100.0, format="%.2f", key="income_month1"
            )
            monthly_income = income

        rent_period = st.radio(
            "Is the rent amount weekly or monthly?", 
            ("Weekly", "Monthly"), horizontal=True, key="rent_period2"
        )
        if rent_period == "Weekly":
            weekly_rent = st.number_input(
                "Your weekly rent (£)", min_value=0.0, step=10.0, format="%.2f", key="weekly_rent1"
            )
            monthly_rent = weekly_rent * 52 / 12
        else:
            monthly_rent = st.number_input(
                "Your monthly rent (£)", min_value=0.0, step=10.0, format="%.2f", key="monthly_rent1"
            )
            weekly_rent = monthly_rent * 12 / 52

        deposit_weeks = st.number_input(
            "Weeks' rent for deposit (5-6 typical)", min_value=0, max_value=12, value=6, key="deposit_weeks1"
        )
        holding_deposit = st.number_input(
            "Holding deposit (£, up to 1 week)", min_value=0.0, step=10.0, format="%.2f", key="holding_deposit1"
        )

    with col2:
        council_tax = st.number_input(
            "Monthly council tax (£)", min_value=0.0, step=10.0, format="%.2f", key="council_tax1"
        )
        utilities = st.number_input(
            "Monthly utilities (£)", min_value=0.0, step=10.0, format="%.2f", key="utilities1"
        )
        internet = st.number_input(
            "Monthly internet/phone (£)", min_value=0.0, step=5.0, format="%.2f", key="internet1"
        )
        contents_insurance = st.number_input(
            "Monthly contents insurance (£)", min_value=0.0, step=5.0, format="%.2f", key="contents_insurance1"
        )
        other_costs = st.number_input(
            "Other monthly housing-related costs (£)", min_value=0.0, step=5.0, format="%.2f", key="other_costs1"
        )

    # Calculations
    deposit_amount = deposit_weeks * weekly_rent
    total_upfront = deposit_amount + holding_deposit + monthly_rent
    total_monthly_costs = monthly_rent + council_tax + utilities + internet + contents_insurance + other_costs

    rent_percent_income = (monthly_rent / monthly_income) * 100 if monthly_income > 0 else 0
    total_cost_percent_income = (total_monthly_costs / monthly_income) * 100 if monthly_income > 0 else 0

    st.divider()
    st.subheader(f"Summary for {name if name else 'User'}")
    st.markdown(f"""
    - **Monthly income:** £{monthly_income:.2f} ({income_type}, {income_period})
    - **Monthly rent:** £{monthly_rent:.2f}
    - **Total monthly housing costs (rent + bills):** £{total_monthly_costs:.2f}
    - **Rent as % of monthly income:** {rent_percent_income:.2f}%
    - **Total housing costs as % of monthly income:** {total_cost_percent_income:.2f}%
    - **Upfront costs (deposit + holding + first month rent):** £{total_upfront:.2f}
    """)

    if rent_percent_income > 45:
        st.warning("⚠️ Your rent is more than 45% of your monthly income, which may be financially stressful.")
    elif rent_percent_income > 30:
        st.info("ℹ️ Your rent is between 30-45% of your income, which is generally considered the upper affordable range.")
    else:
        st.success("✅ Your rent is within a comfortable affordability range (less than 30% of your income).")

    if total_cost_percent_income > 50:
        st.warning("⚠️ Your total housing costs exceed 50% of your income, which is likely unaffordable.")
    elif total_cost_percent_income > 35:
        st.info("ℹ️ Your total housing costs are between 35-50% of your income; consider budgeting carefully.")

    st.caption("All calculations update automatically as you change any value.")
