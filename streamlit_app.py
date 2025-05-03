import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="LinkedIn Message Customizer", layout="wide")


def main():
    st.title("LinkedIn Message Customizer")
    st.markdown("""
    ### Help students send personalized messages to potential LinkedIn referrers
    Upload a CSV of your LinkedIn contacts and customize your outreach messages.
    """)

    # Sidebar for instructions
    with st.sidebar:
        st.header("How to use this app")
        st.markdown("""
        1. **Upload your CSV file** with LinkedIn contacts
        2. **Create your message template** using placeholders like {name}, {company}, etc.
        3. **Customize messages** for each contact
        4. **Preview all messages** before sending
        
        **CSV Format Requirements:**
        Your CSV should include columns for the information you want to use in your templates.
        Common columns include: name, company, position, etc.
        """)

        st.header("Template Tips")
        st.markdown("""
        - Keep messages concise (150-300 words)
        - Be specific about why you're reaching out
        - Mention specific details about their background
        - Make a clear ask/call to action
        - Thank them for their time
        """)

        st.header("Common Placeholders")
        st.markdown("""
        - {first_name} - Contact's first name
        - {last_name} - Contact's last name
        - {full_name} - Contact's full name
        - {company} - Company name
        - {position} - Contact's position
        - {industry} - Industry
        """)

    # Main app content
    tab1, tab2, tab3 = st.tabs(
        ["Upload Data", "Create Template", "Preview Messages"])

    # Global state management
    if 'contacts_df' not in st.session_state:
        st.session_state.contacts_df = None
    if 'template' not in st.session_state:
        st.session_state.template = ""
    if 'placeholders' not in st.session_state:
        st.session_state.placeholders = []
    if 'custom_values' not in st.session_state:
        st.session_state.custom_values = {}

    with tab1:
        upload_data()

        # Add link to sample CSV
        st.markdown("""
        ### Need a template?
        Don't have a CSV file ready? You can download a sample CSV template from our 
        [GitHub repository](https://github.com/ritwiktrivedi/LinkedIn-Message-Customizer/blob/985e2d551bfd1a0f419bada1d5a908d3a44b492b/sample.csv).
        """)

    with tab2:
        create_template()

    with tab3:
        preview_messages()


def upload_data():
    st.header("Upload Your LinkedIn Contacts")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.contacts_df = df

            st.success(f"Successfully loaded {len(df)} contacts!")

            # Display the DataFrame
            st.subheader("Preview of your contacts")
            st.dataframe(df.head(5))

            # Show available columns for templating
            st.subheader("Available fields for your templates")
            st.write(", ".join([f"{{{'{'}{col}{'}'}}}" for col in df.columns]))

        except Exception as e:
            st.error(f"Error: {e}")


def extract_placeholders(template):
    """Extract all placeholders from template string."""
    return re.findall(r'\{([^{}]+)\}', template)


def create_template():
    st.header("Create Your Message Template")

    # Template examples
    with st.expander("See template examples"):
        st.markdown("""
        **Example 1: Asking for a referral**
        ```
        Hi {first_name},
        
        I hope this message finds you well. I noticed you work at {company} in {position}. I'm very interested in the {role} position at {company} and was wondering if you might be open to referring me or chatting about your experience there.
        
        I've attached my resume for your reference. I'd be very grateful for any insights you could share!
        
        Thank you for your time. I really appreciate it!
        ```
        
        **Example 2: Asking for informational interview**
        ```
        Dear {first_name},
        
        I'm a {degree_program} student at {university} interested in pursuing a career in {industry}. I came across your profile and was impressed by your experience at {company}.
        
        Would you be willing to spare 15-20 minutes for a quick call to discuss your career path and any advice you might have for someone looking to enter the field?
        
        Thank you for considering. I really appreciate it!
        ```
        """)

    # Template input
    template = st.text_area("Write your message template",
                            value=st.session_state.template,
                            height=300,
                            help="Use placeholders like {first_name}, {company}, etc.")

    if template:
        st.session_state.template = template
        placeholders = extract_placeholders(template)
        st.session_state.placeholders = placeholders

        if placeholders:
            st.success(
                f"Found {len(placeholders)} placeholders: {', '.join(placeholders)}")

            # Check if there are placeholders that don't match CSV columns
            if st.session_state.contacts_df is not None:
                missing_fields = [
                    p for p in placeholders if p not in st.session_state.contacts_df.columns]
                if missing_fields:
                    st.warning(
                        f"The following placeholders are not in your CSV: {', '.join(missing_fields)}. You'll need to provide custom values for these.")
        else:
            st.warning(
                "No placeholders found. Use {placeholder} syntax to create customizable messages.")


def preview_messages():
    st.header("Preview Customized Messages")

    if st.session_state.contacts_df is None:
        st.warning("Please upload your contacts data first.")
        return

    if not st.session_state.template:
        st.warning("Please create a message template first.")
        return

    # Custom values for missing placeholders
    missing_fields = [
        p for p in st.session_state.placeholders if p not in st.session_state.contacts_df.columns]

    if missing_fields:
        st.subheader("Custom Values for Missing Fields")
        st.write(
            "These fields weren't found in your CSV. Please provide values for them:")

        # Create input fields for each missing placeholder
        for field in missing_fields:
            if field not in st.session_state.custom_values:
                st.session_state.custom_values[field] = ""

            st.session_state.custom_values[field] = st.text_input(f"Value for {{{field}}}",
                                                                  value=st.session_state.custom_values[field])

    # Generate and preview messages
    if st.button("Generate Preview Messages"):
        preview_df = st.session_state.contacts_df.copy()

        # Add custom values to the dataframe
        for field, value in st.session_state.custom_values.items():
            preview_df[field] = value

        # Generate messages for each contact
        messages = []

        for i, row in preview_df.iterrows():
            message = st.session_state.template

            # Replace each placeholder with its value
            for placeholder in st.session_state.placeholders:
                if placeholder in row:
                    value = row[placeholder]
                    message = message.replace(f"{{{placeholder}}}", str(value))

            messages.append(message)

        preview_df['message'] = messages

        # Check for any remaining placeholders
        has_remaining_placeholders = any(
            '{' in msg and '}' in msg for msg in messages)

        if has_remaining_placeholders:
            st.error(
                "Some placeholders couldn't be replaced. Please check your template and data.")

        # Show the preview
        st.subheader("Message Previews")

        for i, (_, row) in enumerate(preview_df.iterrows()):
            with st.expander(f"Message for {row.get('first_name', '')} {row.get('last_name', '')} at {row.get('company', '')} ({i+1}/{len(preview_df)})"):
                st.markdown(row['message'])

        # Export option
        csv = preview_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download messages as CSV",
            data=csv,
            file_name='linkedin_messages.csv',
            mime='text/csv',
        )


if __name__ == "__main__":
    main()
