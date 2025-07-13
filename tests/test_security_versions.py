"""Test to verify that requirements.txt contains secure package versions."""

import re


def test_requirements_have_secure_versions():
    """Test that requirements.txt specifies secure versions of packages."""
    with open("requirements.txt", "r") as f:
        requirements = f.read()

    # Check Flask-CORS version (should be 4.0.2+ to fix vulnerabilities)
    flask_cors_match = re.search(r"Flask-CORS==(\d+\.\d+\.\d+)", requirements)
    assert flask_cors_match, "Flask-CORS version not found in requirements.txt"
    flask_cors_version = flask_cors_match.group(1)

    # Parse version numbers for comparison
    def parse_version(version_str):
        return tuple(map(int, version_str.split('.')))

    # Flask-CORS should be at least 4.0.2
    assert parse_version(flask_cors_version) >= parse_version("4.0.2"), \
        f"Flask-CORS version {flask_cors_version} vulnerable, need 4.0.2+"

    # Check requests version (should be 2.32.0+ to fix GHSA-9wx4-h78v-vm56)
    requests_match = re.search(r"requests==(\d+\.\d+\.\d+)", requirements)
    assert requests_match, "requests version not found in requirements.txt"
    requests_version = requests_match.group(1)

    # requests should be at least 2.32.0
    assert parse_version(requests_version) >= parse_version("2.32.0"), \
        f"requests version {requests_version} vulnerable, need 2.32.0+"

    # Check black version (should be 24.3.0+ to fix PYSEC-2024-48)
    black_match = re.search(r"black==(\d+\.\d+\.\d+)", requirements)
    assert black_match, "black version not found in requirements.txt"
    black_version = black_match.group(1)

    # black should be at least 24.3.0
    assert parse_version(black_version) >= parse_version("24.3.0"), \
        f"black version {black_version} vulnerable, need 24.3.0+"


def test_no_vulnerable_versions():
    """Test that requirements.txt does not contain vulnerable versions."""
    with open("requirements.txt", "r") as f:
        requirements = f.read()

    # Known vulnerable versions that should not be present
    vulnerable_patterns = [
        r"Flask-CORS==4\.0\.0",  # Vulnerable to PYSEC-2024-71, etc.
        r"Flask-CORS==4\.0\.1",  # Still vulnerable to some issues
        r"requests==2\.31\.0",   # Vulnerable to GHSA-9wx4-h78v-vm56
        r"black==23\.11\.0",     # Vulnerable to PYSEC-2024-48
    ]

    for pattern in vulnerable_patterns:
        assert not re.search(pattern, requirements), \
            f"Vulnerable version found matching pattern: {pattern}"
