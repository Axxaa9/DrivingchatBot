# Approach for Solving the Generative AI-powered Vehicle Personalization and Predictive Maintenance System Project

### 1. Problem Understanding and Requirement Gathering:
- the personalization aspects : Preferred settings (e.g., seat settings, climate control) 
- car services :  
    - predictive maintenance of the Engine.
    - notifying about abnormal pattern like oil lost very fast, a compounant heating more than the normal.

- the types of data involved: 
    - strucure data:
        -  [vehicle sensor data](https://www.kaggle.com/datasets/parvmodi/automotive-vehicles-engine-health-dataset/data)
        -  driver preferences (in needed, we can summarize the past interactions and be given to the model with a suitable prompt like "do you want to apply your Preferred settings ").
    - unstructure data: (if needed) for fine tune the LLM but in the comming version if necessary.

- the Generative AI (LLM) will interact with users (natural language conversations, recommendations) and collaborate with ML models.(TODO: explain more)

### 2. Data Collection and Preprocessing:
- Collect vehicle sensor data, driver behavior data, and maintenance history.
- Clean and preprocess data for both ML models (structured data for predictive maintenance) and LLM fine-tuning (if needed, with domain-specific dialogues).

### 3. Classic ML Models for Personalization & Predictive Maintenance:
- **Personalization**: Now, this version will use LLM for personalization.
- **Predictive Maintenance**: Build regression or classification models (e.g., Random Forests, XGBoost, LSTM) to predict [component failure](https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems) (if needed), schedule maintenance, or identify fault patterns.

### 4. Integrating LLM for Interaction:
- Use a pretrained LLM (e.g., GPT-4) to enable natural language interaction with the driver.
- Train or fine-tune the LLM with vehicle-specific scenarios and dialogues for more relevant communication (e.g., explaining maintenance needs, interpreting vehicle diagnostics).
- LLMs can also assist by generating summaries of sensor data or explaining complex results from predictive models in simple terms.

### 5. Action Selection & Decision-Making:
- Combine predictions from the ML models with LLM-based suggestions. For example:
  - ML model predicts an oil change.
  - LLM suggests when to schedule it and explains the need to the driver.
- Use the LLM to handle the decision-making process based on contextual data (e.g., if traffic and weather conditions make it better to take a certain route).

### 6. System Architecture with FastAPI:
- Use FastAPI to create APIs for:
  - Sending and receiving vehicle sensor data. (Done)
  - Requesting maintenance predictions. (Done) but not by api
  - Handling user queries and generating responses using the LLM. (running)
- The API will allow real-time communication between the car’s systems, the ML models, and the LLM.

### 7. Model Deployment and Real-time Updates:
- Deploy ML models for real-time prediction of driver preferences and vehicle issues.
- Deploy the LLM for conversation and decision-making in real-time, integrated with vehicle interfaces (e.g., infotainment system).
- Monitor performance and retrain models periodically as more data becomes available.

### 8. Driver Experience and UI:
- The LLM communicates with the driver in a human-friendly way, suggesting actions or giving updates.
- It can be used to enable hands-free vehicle management through voice commands, making interaction smooth and conversational.

### Summary of Key Components:
- **ML Models**: Handle data-driven predictions (e.g., maintenance schedules, preference optimizations).
- **LLM**: Facilitates user interaction and decision-making, explaining outcomes and generating actions.
- **FastAPI**: Interfaces between the vehicle’s systems, ML models, and LLM, enabling real-time interactions.
