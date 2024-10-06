# import dependencies
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# configure API by loading key from .env file
# load environment variables
load_dotenv()

# initialize configure key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


# method to initialize gemini model
def initialize_model(model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    return model


# method to read the uploaded image in bytes
def get_image_bytes(uploaded_image):
    if uploaded_image is not None:
        
        image_bytes = uploaded_image.getvalue()

        image_info = [
            {
            "mime_type": uploaded_image.type,
            "data": image_bytes
        }
        ]
        return image_info
    else:
        raise FileNotFoundError("Upload Valid image file!")
    

# method to get the response from the Gemini API
def get_response(model, model_behavior, image, prompt):
        response = model.generate_content([model_behavior, image[0], prompt])
        return response.text


def main():

    # initialize the gemini-pro-vision
    model = initialize_model("gemini-1.5-flash")

    # set the model behavior
    model_behavior = """
            You are a finance operations expert who understands the overall structure of the invoice and has a deep understanding of it.
            You will be shared with, the invoice image and you have to answer the question based on the information available in the image.
            """
    
    # create the streamlit ui and get prompt along with image
    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot 🤖 by Oracle Guy")
    st.subheader("I can help you in answering any question related to the your invoice:")

    # Read teh prompt in text box
    prompt = st.text_input("Enter your prompt" ,key="prompt")
  

     # create submit button, to submit image along with image
    submit = st.button("Upload & Submit")


    # interface to upload image
    with st.sidebar:
        uploaded_image = st.file_uploader("Choose an image and Click on the Submit Button", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None: # file upload handling
            image = Image.open(uploaded_image)
            # display the invoice image
            st.image(image, caption="Your image", use_column_width=True)


    # if user pressed submit button
    if submit or prompt:
            if len(prompt) > 0:
                    # get uploaded image file in bytes
                    image_info = get_image_bytes(uploaded_image)
                    response = get_response(model, model_behavior, image_info, prompt)
                    st.write(response)
            else:
                    raise ValueError("Please Enter Valid prompt!")


#Invoking main function
if __name__ == '__main__':
    main()
