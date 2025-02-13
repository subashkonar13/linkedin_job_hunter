# LinkedinJobApplier

# Usage
response = requests.post("http://localhost:8000/api/v1/bulk-apply", 
    json={
        "role": "Software Engineer",
        "location": "London",
        "visa_sponsorship": True,
        "work_type": "remote",
        "max_applications": 20
    }
)

# Check application status
status = requests.get("http://localhost:8000/api/v1/application-status")
print(status.json())

# Run Docker
# Start all services
docker-compose up -d

# Monitor applications
docker-compose logs -f app

# View traces
open http://localhost:16686
