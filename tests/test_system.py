import pytest
import uuid

def test_full_career_workflow(client):
    """
    System Test: Simulate full user story with unique IDs to avoid DB conflicts.
    """
    # Create unique usernames for this specific test run
    unique_id = str(uuid.uuid4())[:8]
    emp_user = f"boss_{unique_id}"
    app_user = f"seeker_{unique_id}"

    # 1. Employer Setup (Register & Login)
    employer = client.post("/register", json={
        "email": f"{emp_user}@corp.com", 
        "username": emp_user, 
        "password": "password123"
    })
    assert employer.status_code == 201
    employer_id = employer.json()["id"]
    login_res = client.post("/token", data={"username": emp_user, "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Job
    job_res = client.post("/jobs", headers=headers, json={
        "title": "QA Engineer", "description": "Pytest Expert",
        "requirements": "Python", "location": "Remote", "salary": "90k"
    })
    assert job_res.status_code == 201
    job_id = job_res.json()["id"]
    assert job_res.json()["created_by_id"] == employer_id

    # 3. Applicant Setup (Register & Login)
    applicant_res = client.post("/register", json={
        "email": f"{app_user}@dev.com", 
        "username": app_user, 
        "password": "password123"
    })
    assert applicant_res.status_code == 201
    applicant_id = applicant_res.json()["id"]
    app_login = client.post("/token", data={"username": app_user, "password": "password123"})
    app_token = app_login.json()["access_token"]
    app_headers = {"Authorization": f"Bearer {app_token}"}

    # 4. Apply as the applicant user
    apply_res = client.post(
        f"/jobs/{job_id}/apply", 
        headers=app_headers, 
        json={
            "cover_letter": "I have completed the Software Testing project with 100% test coverage!"
        }
    )

    # Assertions
    assert apply_res.status_code == 201
    assert apply_res.json()["job_id"] == job_id
    assert apply_res.json()["applicant_id"] == applicant_id
    assert "id" in apply_res.json()
