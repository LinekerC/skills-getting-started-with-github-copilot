"""
Tests for participant removal endpoint (DELETE /activities/{activity_name}/signup/{email}).
Uses AAA (Arrange-Act-Assert) pattern for test structure.
"""
import pytest


class TestRemoveParticipant:
    """Tests for the DELETE /activities/{activity_name}/signup/{email} endpoint."""
    
    def test_remove_participant_success(self, client, reset_activities):
        """
        Test that a participant can be successfully removed from an activity.
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = reset_activities[activity_name]["participants"][0]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]
        assert email_to_remove not in reset_activities[activity_name]["participants"]
    
    def test_remove_participant_reduces_count(self, client, reset_activities):
        """
        Test that removing a participant decreases the participant count.
        """
        # Arrange
        activity_name = "Programming Class"
        email_to_remove = reset_activities[activity_name]["participants"][0]
        original_count = len(reset_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        assert len(reset_activities[activity_name]["participants"]) == original_count - 1
    
    def test_remove_nonparticipant_returns_error(self, client, reset_activities):
        """
        Test that removing a non-participant returns 400 error.
        """
        # Arrange
        activity_name = "Gym Class"
        non_participant_email = "not_signed_up@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup/{non_participant_email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_remove_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        Test that removing from a non-existent activity returns 404 error.
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup/{email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_all_participants_one_by_one(self, client, reset_activities):
        """
        Test that all participants can be removed from an activity sequentially.
        """
        # Arrange
        activity_name = "Basketball Team"
        participants = reset_activities[activity_name]["participants"].copy()
        
        # Act & Assert
        for email in participants:
            response = client.delete(
                f"/activities/{activity_name}/signup/{email}"
            )
            assert response.status_code == 200
            assert email not in reset_activities[activity_name]["participants"]
        
        # Final assertion: list should be empty
        assert len(reset_activities[activity_name]["participants"]) == 0
    
    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Tennis Club"
    ])
    def test_remove_from_multiple_activities(self, client, reset_activities, activity_name):
        """
        Test that removal works for various activities (parametrized test).
        """
        # Arrange
        email_to_remove = reset_activities[activity_name]["participants"][0]
        original_count = len(reset_activities[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        assert len(reset_activities[activity_name]["participants"]) == original_count - 1
    
    def test_remove_response_message_format(self, client, reset_activities):
        """
        Test that the removal response message has the correct format.
        """
        # Arrange
        activity_name = "Science Club"
        email_to_remove = reset_activities[activity_name]["participants"][0]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup/{email_to_remove}"
        )
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert email_to_remove in message
        assert activity_name in message
        assert "Removed" in message
    
    def test_remove_same_participant_twice_fails(self, client, reset_activities):
        """
        Test that removing the same participant twice fails with appropriate error.
        """
        # Arrange
        activity_name = "Drama Club"
        email = reset_activities[activity_name]["participants"][0]
        
        # Act - First removal
        response1 = client.delete(
            f"/activities/{activity_name}/signup/{email}"
        )
        
        # Act - Second removal (should fail)
        response2 = client.delete(
            f"/activities/{activity_name}/signup/{email}"
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "not signed up" in response2.json()["detail"]
