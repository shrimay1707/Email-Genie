import streamlit as st
from emailautomator.pre_trained_classifier import load_models, classify_email
from emailautomator.reply import process_email
from emailautomator.custom_classifier import load_model_and_data
import asyncio
from emailautomator.custom_classifier import classify_email_custom

model_v1, model_v12, tokenizer_v1, tokenizer_v12, label_encoder_v1, label_encoder_v12 = asyncio.run(load_models())
model, word_to_idx, le_category, le_email_type = asyncio.run(load_model_and_data())

# Custom CSS for color-coded tags and smaller headings
st.markdown("""
    <style>
        .tag {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            color: white;
            margin: 5px;
        }
        .student-tag { background-color: #4CAF50; } 
        .academic-tag { background-color: #2196F3; } 
        .corporate-tag { background-color: #FF9800; } 
        .sensitive-tag { background-color: #F44336; } 
        .general-tag { background-color: #9C27B0; } 
        .research-tag { background-color: #3F51B5; } 
        .small-heading {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .alert {
            margin-top: 20px;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

def load_app(key_prefix):
    if st.session_state['email_flow'] == 'subject':
        st.session_state['subject'] = st.text_input("Enter the subject of the email:", key=f"{key_prefix}_subject")
        if st.session_state['subject']:
            st.session_state['email_flow'] = 'body'

    # Get body of the email
    if st.session_state['email_flow'] == 'body':
        st.session_state['body'] = st.text_area("Enter the body of the email:", key=f"{key_prefix}_body")
        if st.session_state['body']:
  
            if st.session_state['model'] == 'custom':
                category, email_type = classify_email_custom(model, st.session_state['subject'], st.session_state['body'], word_to_idx, le_category, le_email_type)
            else:
                category = classify_email(st.session_state['subject'], st.session_state['body'], model_v1, tokenizer_v1, label_encoder_v1)
                email_type = classify_email(st.session_state['subject'], st.session_state['body'], model_v12, tokenizer_v12, label_encoder_v12)


            category = [str(category)]
            st.session_state['category'] = category
            email_type = [str(email_type)]
        # Create two columns for side-by-side display
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<p class='small-heading'>Email Categories (Type)</p>", unsafe_allow_html=True)
                for t in category:
                    tag_class = {
                        "Student inquiries": "student-tag",
                        "Academic collaboration inquiries": "academic-tag",
                        "Corporate inquiries": "corporate-tag"
                    }[t]
                    st.markdown(f"<div class='tag {tag_class}'>{t}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<p class='small-heading'>Email Classes (Sensitivity)</p>", unsafe_allow_html=True)
                for c in email_type:
                    class_tag = {
                        "Sensitive Email": "sensitive-tag",
                        "General Information": "general-tag",
                        "Research Query": "research-tag"
                    }[c]
                    st.markdown(f"<div class='tag {class_tag}'>{c}</div>", unsafe_allow_html=True)

            if c == "Sensitive Emails":
              st.markdown("<p class='alert'>This email will be forwarded to the Head of Department (HOD).</p>", unsafe_allow_html=True)
              new_chat(key_prefix)

            else:
              st.session_state['email_flow'] = 'response'

    # Generate a response email
    if st.session_state['email_flow'] == 'response':
        response_email = process_email(st.session_state['subject'] + st.session_state['body'], st.session_state['category'][0])
        
        st.subheader("Response Email")
        st.text_area("Generated Response", response_email, height=300, key=f"{key_prefix}_response")
        
        new_chat(key_prefix)

def new_chat(key_prefix):
    # Offer to start a new chat
  if st.button("Start New Chat", key=f"{key_prefix}_new_chat"):
      # Reset all relevant session state variables
      for key in ['email_flow', 'subject', 'body']:
          if key in st.session_state:
              del st.session_state[key]
      st.rerun()

# Main app logic
def chatbot():
    st.title("Email Classifier Chatbot")

    if 'email_flow' not in st.session_state:
        st.session_state['email_flow'] = 'subject'

    # Get subject of the email
    tab1, tab2 = st.tabs(["Custom Model", "Pretrained Model"])

    with tab1:
        st.header("Custom Model")
        st.session_state['model'] = 'custom'
        load_app("tab1")

    with tab2:
        st.header("Pretrained Model")
        st.session_state['model'] = 'pretrained'
        load_app("tab2")
    

# Run the chatbot
if __name__ == "__main__":
    chatbot()