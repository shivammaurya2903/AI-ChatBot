# TODO: Improve Chatbot Data Consistency

## Steps to Complete:
- [ ] Consolidate ria_data, health_data, and daily_data into a single chatbot_data dictionary, merging overlapping keys with the most comprehensive or consistent responses.
- [ ] Update the get_bot_response function to use chatbot_data and streamline matching logic (remove redundancies like multiple intent detections).
- [ ] Remove the separate data dictionaries (ria_data, health_data, daily_data) from app.py.
- [ ] Test the chatbot by running the app and verifying responses for consistency.
- [ ] Check for any logged unanswered questions and ensure they are handled better if possible.
