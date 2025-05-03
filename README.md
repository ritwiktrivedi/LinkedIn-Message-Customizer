# LinkedIn Message Customizer

A Streamlit application that helps students send personalized messages to potential LinkedIn referrers by customizing message templates based on contact information.

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://linkedinmessagecustomizer.streamlit.app/)

## Features

- Upload LinkedIn contacts from a CSV file
- Create message templates with dynamic placeholders
- Preview customized messages for each contact
- Export messages as a CSV file
- Built-in examples and best practices

### How to run it on your own machine

1. Clone this repository or download the script
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run streamlit_app.py
```

## How to Use

### 1. Prepare Your CSV File

Create a CSV file with your LinkedIn contacts. At a minimum, include these columns:

- `first_name`
- `last_name`
- `company`
- `position`

You can include additional columns for more personalization options. See the included sample CSV as a template.

### 2. Upload Your Data

- Use the "Upload Data" tab to upload your CSV file
- Review the preview to ensure data was loaded correctly
- Note the available fields shown on this page

### 3. Create Message Template

- Go to the "Create Template" tab
- Write your message using placeholders like `{first_name}`, `{company}`, etc.
- The app will detect all placeholders and check if they match your CSV columns
- For any fields not in your CSV, you'll provide custom values later

### 4. Preview Messages

- Go to the "Preview Messages" tab
- Provide custom values for any missing fields
- Click "Generate Preview Messages" to see personalized messages for each contact
- Review each message for accuracy
- Download all messages as a CSV file if needed

## Best Practices for LinkedIn Messages

- Keep messages concise (150-300 words)
- Be specific about why you're reaching out
- Mention something specific from their background
- Make a clear ask/call to action
- Thank them for their time
- Proofread each message before sending

## Example Templates

### Referral Request

```
Hi {first_name},

I hope this message finds you well. I noticed you work at {company} as a {position}. I'm very interested in the {role} position at {company} and was wondering if you might be open to referring me or chatting about your experience there.

I'm a recent graduate from {school} with experience in [your relevant experience]. I believe my background in [relevant skills] aligns well with this role.

I've attached my resume for your reference. I'd be very grateful for any insights you could share!

Thank you for your time.
```

### Informational Interview Request

```
Dear {first_name},

I'm a student at {school} interested in pursuing a career in {industry}. I came across your profile and was impressed by your experience at {company}.

Would you be willing to spare 15-20 minutes for a quick call to discuss your career path and any advice you might have for someone looking to enter the field? I'm particularly interested in learning more about [specific aspect of their work].

Thank you for considering.
```

## Limitations

- This app does not directly send messages to LinkedIn (due to API limitations)
- After generating messages, you'll need to manually copy them to LinkedIn
- Always personalize each message further if possible

## Contributing

Feel free to fork this repository and make improvements!

## License

MIT License
