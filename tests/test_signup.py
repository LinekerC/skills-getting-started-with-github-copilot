"""
Tests for activity signup endpoint (POST /activities/{activity_name}/signup).
Uses AAA (Arrange-Act-Assert) pattern for test structure.
"""
import pytest


class TestSignupForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_for_activity_success(self, client, reset_activities):
        """
        Test that a student can successfully sign up for an activity.
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "new_student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert new_email in reset_activities[activity_name]["participants"]
    
    def test_signup_adds_participant_to_list(self, client, reset_activities):
        """
        Test that signup correctly adds the email to the participants list.
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "alice@mergington.edu"
        original_count = len(reset_activities[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert len(reset_activities[activity_name]["participants"]) == original_count + 1
        assert reset_activities[activity_name]["participants"][-1] == new_email
    
    def test_signup_duplicate_email_returns_error(self, client, reset_activities):
        """
        Test that signing up with an email already in the activity returns 400 error.
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = reset_activities[activity_name]["participants"][0]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={existing_email}"
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        Test that signing up for a non-existent activity returns 404 error.
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team"
    ])
    def test_signup_works_for_multiple_activities(self, client, reset_activities, activity_name):
        """
        Test that signup works for various activities (parametrized test).
        """
        # Arrange
        new_email = f"student_{activity_name.replace(' ', '_')}@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )
        
        # Assert
        assert response.status_code == 200
        assert new_email in reset_activities[activity_name]["participants"]
    
    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """
        Test that multiple different students can sign up for the same activity.
        """
        # Arrange
        activity_name = "Art Studio"
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        # Act
        responses = [
            client.post(f"/activities/{activity_name}/signup?email={email}")
            for email in emails
        ]
        
        # Assert
        for response in responses:
            assert response.status_code == 200
        
        # Verify all were added
        participants = reset_activities[activity_name]["participants"]
        for email in emails:
            assert email in participants
    
    def test_signup_response_message_format(self, client, reset_activities):
        """
        Test that the signup response message has the correct format.
        """
        # Arrange
        activity_name = "Drama Club"
        email = "actor@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        message = response.json()["message"]
        assert email in message
        assert activity_name in message
        assert "Signed up" in message
