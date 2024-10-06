# import dependencies
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# configure API by loading key from .env file
# load environment variables
load_dotenv()

# configure key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


# initialize gemini pro model
def initialize_model(model_name="gemini-1.5-flash"):
    model = genai.GenerativeModel(model_name)
    return model



def get_image_bytes(uploaded_image):
    if uploaded_image is not None:
        # read the uploaded image in bytes
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
    


def get_response(model, model_behavior, image, prompt):
        response = model.generate_content([model_behavior, image[0], prompt])
        return response.text



    

def main():
    # create the streamlit ui and get prompt along with image
    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot 🤖 by Oracle Guy")
    st.subheader("I can help you in answering any question relted to the your invoice:")

    # Read teh prompt in text box
    prompt = st.text_input("Enter your prompt" ,key="prompt")
    # interface to upload image
    submit = st.button("Upload & Submit")
    with st.sidebar:
        uploaded_image = st.file_uploader("Choose an image and Click on the Submit Button", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None: # file upload handling
            image = Image.open(uploaded_image)
            # display the invoice image
            st.image(image, caption="Your image", use_column_width=True)

            # create submit button, to submit image along with image
            
    
            # initialize the gemini-pro-vision
            model = initialize_model("gemini-1.5-flash")

            # set the model behavior
            model_behavior = """
            Your are a finance operations expert who understands overall structure of the invoice and has a deep understanding of it.
            You will be shared, the invoice image and you have to answer the question based on the information available in the image.
            """

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