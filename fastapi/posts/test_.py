from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from schemas.post_schema import PostBase, CreatePost


client = TestClient(app)
fake_token ="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJaNkJiZUpMcVYzTkk5NERtNlVIQXA2am9fTHhtTGxDNlBpdnZBYzd3UTFZIn0.eyJleHAiOjE3MTE3MDI1MTksImlhdCI6MTcxMTcwMjIxOSwiYXV0aF90aW1lIjoxNzExNzAxODk1LCJqdGkiOiI2ODM4M2FkYy05ZWM4LTQ4ZjgtOTJiNC0xYjkzNTA5MTFkNjQiLCJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjkwODAvcmVhbG1zL2poaXBzdGVyIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6IjRjOTczODk2LTU3NjEtNDFmYy04MjE3LTA3YzVkMTNhMDA0YiIsInR5cCI6IkJlYXJlciIsImF6cCI6IndlYl9hcHAiLCJzZXNzaW9uX3N0YXRlIjoiMzkxZGM1OGMtZGMxNy00NTY5LThhZWQtOGZkNDFjYWE3NDJiIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIlJPTEVfVVNFUiIsIm9mZmxpbmVfYWNjZXNzIiwiUk9MRV9BRE1JTiIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJlbWFpbCBwcm9maWxlIiwic2lkIjoiMzkxZGM1OGMtZGMxNy00NTY5LThhZWQtOGZkNDFjYWE3NDJiIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInJvbGVzIjpbIlJPTEVfVVNFUiIsIm9mZmxpbmVfYWNjZXNzIiwiUk9MRV9BRE1JTiIsInVtYV9hdXRob3JpemF0aW9uIl0sIm5hbWUiOiJBZG1pbiBBZG1pbmlzdHJhdG9yIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWRtaW4iLCJnaXZlbl9uYW1lIjoiQWRtaW4iLCJmYW1pbHlfbmFtZSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGxvY2FsaG9zdCJ9.Lfk-eZx_MdlaqpqO3ukksKfuvqSarcX5VP_u89xomMXxC19AtJe3b7k4E4OHhKzJ9nuH0jNi6uEwd5Q4ubW7WQq6Lmpj23sZ99w5HHHs8v7iWBPyF0LVjzeuL5Um7uiOZSbm-5g5f9MiE9AXhLZBEN1slMx8eqbDjKeZQynTiRNkycgcc3XDmJjZio29mNn2Z9DNyS0rTAGuPHb9kDO9onB5CMt4qLp_fU2ExXDoPgBZIIGeueSw9UwacuKvJLzGDEYJtybQ0m9nPUNlsOWjygSGGN6H8f5wASFzMvHgVfoSTbZvSkv5jXk1fK96719kq91tjUlCgAjhGsfARDMHtg"

# Mocking the database-related functions
@patch("services.post_service.get_posts")
def test_get_posts(mock_get_posts):
    # Arrange
    mock_get_posts.return_value = [PostBase(id=1, title="Post 1", content="Content 1")]

    # Act
    response = client.get("/posts", headers={"Authorization": f"Bearer {fake_token}"})
    
    # Assert
    assert response.status_code == 200
    assert response.json() == [{ "title": "Post 1", "content": "Content 1"}]

@patch("services.post_service.create_post")
def test_create_post(mock_create_post):
    # Arrange
    mock_create_post.return_value = PostBase(id=1, title="New Post", content="New Content")
    post_data = CreatePost(title="Prabha", content="New Content")

    # Act
    response = client.post("/posts", headers={"Authorization": f"Bearer {fake_token}"}, json=post_data.model_dump())
    
    # Assert
    assert response.status_code == 201  # Changed to 201 for created
    assert response.json() == {"title": "New Post", "content": "New Content"}

@patch("services.post_service.get_post")
def test_get_post(mock_get_post):
    # Arrange
    mock_get_post.return_value = PostBase(id=1, title="Post 1", content="Content 1")

    # Act
    response = client.get("/posts/1", headers={"Authorization": f"Bearer {fake_token}"})
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"title": "Post 1", "content": "Content 1"}

@patch("services.post_service.delete_post")
def test_delete_post(mock_delete_post):
    # Arrange
    mock_delete_post.return_value = None

    # Act
    response = client.delete("/posts/1", headers={"Authorization": f"Bearer {fake_token}"})
    
    # Assert
    assert response.status_code == 204  # Changed to 204 for no content
    assert response.content == b''  # No content in response

@patch("services.post_service.update_post")
def test_update_post(mock_update_post):
    # Arrange
    mock_update_post.return_value = PostBase(id=1, title="Updated Post", content="Updated Content")
    post_data = PostBase(id=1, title="Updated Post", content="Updated Content")

    # Act
    response = client.put("/posts/1", headers={"Authorization": f"Bearer {fake_token}"}, json=post_data.model_dump())
    
    # Assert
    assert response.status_code == 200
    assert response.json() == {"title": "Updated Post", "content": "Updated Content"}










# @patch("services.post_service.get_post", MagicMock(side_effect=Exception("Post not found")))
# def test_handle_post_not_found():
#     # Arrange

#     # Act
#     response = client.get("/posts/999", headers={"Authorization": f"Bearer {fake_token}"})
    
#     # Assert
#     assert response.status_code == 404
#     assert response.json()["detail"] == {"detail": "The id: 999 you requested for does not exist"}     

# @patch("services.post_service.get_post", MagicMock(side_effect=ValueError("Invalid post ID")))
# def test_handle_invalid_post_id():
#     # Arrange

#     # Act
#     response = client.get("/posts/invalid_id", headers={"Authorization": f"Bearer {fake_token}"})
    
#     # Assert
#     assert response.status_code == 400
#     assert response.json()["detail"] == "The id: invalid_id you requested for does not exist"

# @patch("routers.router_utils.RabbitMQProducer")
# def test_publish_message_to_queue(mock_producer):
#     # Arrange
#     mock_producer_instance = MagicMock()
#     mock_producer.return_value = mock_producer_instance

#     # Act
#     message = {"key": "value"}
#     response = client.get("/posts/get_response_from_slack", headers={"Authorization": f"Bearer {fake_token}"})
    
#     # Assert
#     assert response.status_code == 200
#     assert response.json()["Response of other microservice"] == {"key": "value"}
#     mock_producer_instance.publish_message.assert_called_once_with(routing_key='pro_queue', message=message)

