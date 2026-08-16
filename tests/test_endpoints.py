"""
Tests for core API endpoints (GET / and GET /activities).
Uses AAA (Arrange-Act-Assert) pattern for test structure.
"""
import pytest


class TestRootEndpoint:
    """Tests for the GET / endpoint."""
    
    def test_root_redirects_to_static_index(self, client):
        """
        Test that the root endpoint redirects to /static/index.html
        """
        # Arrange
        expected_redirect_url = "/static/index.html"
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == expected_redirect_url


class TestGetActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        Test that GET /activities returns all activities from the database.
        """
        # Arrange
        expected_activity_count = len(reset_activities)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert isinstance(activities, dict)
        assert len(activities) == expected_activity_count
    
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """
        Test that each activity in the response has the correct structure.
        """
        # Arrange
        expected_keys = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert set(activity_data.keys()) == expected_keys
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_get_activities_contains_sample_activities(self, client, reset_activities):
        """
        Test that GET /activities contains expected sample activities.
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name in expected_activities:
            assert activity_name in activities
    
    def test_get_activities_preserves_participant_list(self, client, reset_activities):
        """
        Test that GET /activities returns activities with existing participants.
        """
        # Arrange
        chess_club = reset_activities["Chess Club"]
        expected_participants = chess_club["participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        assert activities["Chess Club"]["participants"] == expected_participants
