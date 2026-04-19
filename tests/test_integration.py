from fastapi import status

def register_and_login(client, email, username, password="password123"):
    register_response = client.post(
        "/register",
        json={
            "email": email,
            "username": username,
            "password": password,
        },
    )
    assert register_response.status_code == status.HTTP_201_CREATED

    login_response = client.post(
        "/token",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == status.HTTP_200_OK
    return register_response.json(), login_response.json()["access_token"]

# --- TEST 1: Register a User via API ---
def test_register_user_integration(client):
    """
    Test that the POST /register endpoint successfully creates a user in the DB.
    """
    response = client.post(
        "/register",
        json={
            "email": "integration@test.com",
            "username": "int_tester",
            "password": "testpassword123"
        }
    )
    
    # Assertions
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "int_tester"
    assert "id" in data

# --- TEST 2: Duplicate Registration Error ---
def test_register_duplicate_user(client):
    """
    Test that the system prevents registering the same username twice.
    """
    # First registration
    client.post(
    "/register",
    json={"email": "a@test.com", "username": "same", "password": "password123"}
)
    
    # Second registration with same username
    response = client.post(
        "/register",
        json={"email": "b@test.com", "username": "same", "password": "password"}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username or email already exists"

# --- TEST 3: Get Jobs (Empty State) ---
def test_get_jobs_empty(client):
    """
    Test that the GET /jobs endpoint returns an empty list when no jobs exist.
    """
    response = client.get("/jobs")
    assert response.status_code == 200
    assert response.json() == []

def test_login_with_invalid_password_returns_401(client):
    client.post(
        "/register",
        json={
            "email": "login@test.com",
            "username": "login_user",
            "password": "correctpass",
        },
    )

    response = client.post(
        "/token",
        data={"username": "login_user", "password": "wrongpass"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"

def test_register_invalid_payload_returns_422(client):
    response = client.post(
        "/register",
        json={
            "email": "not-an-email",
            "username": "ab",
            "password": "short",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_job_requires_authentication(client):
    response = client.post(
        "/jobs",
        json={
            "title": "QA Engineer",
            "description": "Test software",
            "requirements": "Python",
            "location": "Remote",
            "salary": "90k",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_apply_to_missing_job_returns_404(client):
    _, token = register_and_login(client, "apply@test.com", "apply_user")
    response = client.post(
        "/jobs/999/apply",
        headers={"Authorization": f"Bearer {token}"},
        json={"cover_letter": "I would love to apply."},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Job not found"

def test_apply_with_invalid_payload_returns_422(client):
    _, employer_token = register_and_login(client, "employer@test.com", "employer_user")
    job_response = client.post(
        "/jobs",
        headers={"Authorization": f"Bearer {employer_token}"},
        json={
            "title": "Backend QA",
            "description": "Write API tests",
            "requirements": "FastAPI",
            "location": "Berlin",
            "salary": "80k",
        },
    )
    job_id = job_response.json()["id"]

    _, applicant_token = register_and_login(client, "candidate@test.com", "candidate_user")
    response = client.post(
        f"/jobs/{job_id}/apply",
        headers={"Authorization": f"Bearer {applicant_token}"},
        json={"cover_letter": ""},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
