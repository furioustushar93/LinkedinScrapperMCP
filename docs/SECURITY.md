# Security Policy

## Supported Versions

Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. Do Not Disclose Publicly

Please **do not** create a public GitHub issue for security vulnerabilities.

### 2. Report Privately

Send an email to: **security@yourproject.com** (or create a private security advisory on GitHub)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity

## Security Best Practices

### For Users

#### Credential Management

1. **Never Commit Credentials**
   ```bash
   # ✅ Good: Use environment variables
   LINKEDIN_EMAIL=your.email@example.com
   
   # ❌ Bad: Hardcode in code
   scraper = LinkedInScraper(email="myemail@gmail.com")
   ```

2. **Use Strong Passwords**
   - Minimum 12 characters
   - Mix of letters, numbers, symbols
   - Unique to LinkedIn
   - Consider a password manager

3. **Enable 2FA**
   - Enable Two-Factor Authentication on LinkedIn
   - Use authenticator apps over SMS
   - Keep backup codes secure

4. **Protect Your `.env` File**
   ```bash
   # Set proper permissions
   chmod 600 .env
   
   # Ensure it's in .gitignore
   echo ".env" >> .gitignore
   ```

#### Rate Limiting

1. **Respect LinkedIn's Limits**
   - Don't modify rate limit delays
   - Don't run multiple instances simultaneously
   - Monitor your request frequency

2. **Configure Delays**
   ```env
   # In .env
   RATE_LIMIT_DELAY=2  # Minimum 2 seconds recommended
   ```

#### Data Storage

1. **Don't Store Sensitive Data**
   - Don't save scraped data containing PII
   - If you must store, encrypt it
   - Follow data retention policies

2. **Clean Up Logs**
   ```bash
   # Regularly clean log files
   rm logs/*.log
   ```

#### Network Security

1. **Use HTTPS Only**
   - All LinkedIn requests use HTTPS
   - Don't disable SSL verification

2. **Secure Your Network**
   - Use VPN when on public WiFi
   - Avoid untrusted networks
   - Monitor outgoing connections

### For Developers

#### Code Security

1. **Input Validation**
   ```python
   # Always validate and sanitize inputs
   def scrape_profile(self, profile_url: str):
       profile_url = sanitize_url(profile_url)  # ✅
       # Don't trust user input directly
   ```

2. **Error Handling**
   ```python
   # Don't expose sensitive info in errors
   try:
       # operation
   except Exception as e:
       logger.error("Operation failed")  # ✅
       # Don't log credentials or tokens
   ```

3. **Dependency Management**
   ```bash
   # Keep dependencies updated
   pip list --outdated
   pip install --upgrade package_name
   ```

4. **Code Review**
   - Review all PRs for security issues
   - Use automated security scanning
   - Check for exposed secrets

#### Authentication

1. **Session Management**
   ```python
   # Close sessions properly
   def __del__(self):
       self.session.close()
   ```

2. **Token Storage**
   - Never log authentication tokens
   - Clear tokens from memory when done
   - Use secure storage for persistent tokens

3. **API Keys**
   - Rotate API keys regularly
   - Use separate keys for dev/prod
   - Revoke compromised keys immediately

## Known Security Considerations

### LinkedIn Terms of Service

This tool must be used in compliance with:
- [LinkedIn Terms of Service](https://www.linkedin.com/legal/user-agreement)
- [LinkedIn API Terms](https://legal.linkedin.com/api-terms-of-use)

**Important**: Web scraping may violate LinkedIn's ToS. Use at your own risk.

### Data Privacy

#### GDPR Compliance

If you're in the EU or processing EU residents' data:
- Obtain explicit consent for data collection
- Provide data access/deletion mechanisms
- Document data processing activities
- Implement data minimization

#### CCPA Compliance

If you're processing California residents' data:
- Disclose data collection practices
- Provide opt-out mechanisms
- Don't sell personal information

### Rate Limiting

- **Default delay**: 2 seconds between requests
- **Recommended**: 3-5 seconds for safety
- **Maximum**: Don't exceed 100 requests/hour

### IP Blocking

LinkedIn may block IPs that:
- Make too many requests
- Exhibit bot-like behavior
- Violate terms of service

**Mitigation**:
- Use reasonable delays
- Don't run 24/7
- Rotate user agents (already implemented)
- Use residential proxies (if necessary)

## Incident Response

### If You Suspect a Breach

1. **Stop the Server**
   ```bash
   # Kill the process
   pkill -f "python src/server.py"
   ```

2. **Rotate Credentials**
   - Change LinkedIn password
   - Generate new API keys
   - Update `.env` file

3. **Review Logs**
   ```bash
   # Check for suspicious activity
   tail -n 100 logs/linkedin_scraper.log
   ```

4. **Report**
   - Contact security team
   - Document the incident
   - Notify affected users (if applicable)

### If Your Account is Blocked

1. **Stop All Activity**
   - Don't attempt to bypass blocks
   - Don't create new accounts

2. **Contact LinkedIn**
   - Explain legitimate use case
   - Request unblock

3. **Review Settings**
   - Check rate limits
   - Review request frequency
   - Adjust delays

## Security Checklist

Before deploying to production:

- [ ] All credentials in environment variables
- [ ] `.env` file in `.gitignore`
- [ ] Strong passwords with 2FA
- [ ] Rate limiting configured
- [ ] Logging configured properly
- [ ] No secrets in code
- [ ] Dependencies up to date
- [ ] SSL verification enabled
- [ ] Error messages don't leak info
- [ ] Access controls in place
- [ ] Regular security audits scheduled

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [LinkedIn Security](https://www.linkedin.com/help/linkedin/answer/a1339724)

## Contact

For security concerns: **security@yourproject.com**

For general questions: Open an issue on GitHub

---

**Remember**: Security is everyone's responsibility. Stay vigilant! 🔒

