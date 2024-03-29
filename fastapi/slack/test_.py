import unittest
from unittest.mock import MagicMock, patch
from services import slack_service
from models.slack import Message
from pymongo.collection import Collection
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from bson import ObjectId

class TestSlackServices(unittest.TestCase):
    @patch('services.slack_service.get_channels')
    def test_get_channels(self, mock_get_channels):
        # Mock get_channels to return expected channels
        mock_get_channels.return_value = ["Aruna", "Durga Devi", "prabha"]

        # Call the function
        channels = slack_service.get_channels()

        # Assertions
        self.assertEqual(channels, ["Aruna", "Durga Devi", "prabha"])

    @patch('services.slack_service.get_messages')
    def test_get_messages(self, mock_get_messages):
        # Mock MongoDB client and collection
        mock_collection = MagicMock(spec=Collection)
        mock_collection.find.return_value = [{'channel': 'Aruna', 'author': 'Chandran', 'text': ' random message.'}]
        mock_get_messages.return_value = [Message(**{'channel': 'Aruna', 'author': 'Chandran', 'text': ' random message.'})]  # Mocked list of messages

        # Call the function
        messages = slack_service.get_messages('Aruna')

        # Assertions
        self.assertEqual(len(messages), 1)
        self.assertIsInstance(messages[0], Message)
        self.assertEqual(messages[0].channel, 'Aruna')
        self.assertEqual(messages[0].author, 'Chandran')
        self.assertEqual(messages[0].text, ' random message.')

    @patch('services.slack_service.insert_message')
    def test_insert_message(self, mock_get_mongo_client):
        # Mock MongoDB client and collection
        mock_collection = MagicMock(spec=Collection)
        mock_result = MagicMock(spec=InsertOneResult)
        mock_result.acknowledged = True
        mock_collection.insert_one.return_value = mock_result
        mock_get_mongo_client.return_value.__enter__.return_value[slack_service.DB][slack_service.MSG_COLLECTION] = mock_collection

        # Call the function
        message = Message(channel='channel1', author='user1', text='message1')
        ack = slack_service.insert_message(message)

        # Assertions
        self.assertTrue(ack)

    @patch('services.slack_service.update_message')
    def test_update_message(self, mock_get_mongo_client):
        # Mock MongoDB client and collection
        mock_collection = MagicMock(spec=Collection)
        mock_result = MagicMock(spec=UpdateResult)
        mock_result.modified_count = 1
        mock_collection.update_one.return_value = mock_result
        mock_get_mongo_client.return_value.__enter__.return_value[slack_service.DB][slack_service.MSG_COLLECTION] = mock_collection

        # Call the function
        updated_message = Message(channel='channel1', author='user1', text='updated_message1')
        result = slack_service.update_message(ObjectId(), updated_message)  # Pass a valid ObjectId

        # Assertions
        self.assertTrue(result)

    @patch('services.slack_service.delete_message')
    def test_delete_message(self, mock_get_mongo_client):
        # Mock MongoDB client and collection
        mock_collection = MagicMock(spec=Collection)
        mock_result = MagicMock(spec=DeleteResult)
        mock_result.deleted_count = 1
        mock_collection.delete_one.return_value = mock_result
        mock_get_mongo_client.return_value.__enter__.return_value[slack_service.DB][slack_service.MSG_COLLECTION] = mock_collection

        # Call the function
        result = slack_service.delete_message(ObjectId())  # Pass a valid ObjectId

        # Assertions
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
