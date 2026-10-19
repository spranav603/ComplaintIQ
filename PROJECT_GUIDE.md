# ComplaintIQ Project Guide

## 1. What is ComplaintIQ?

ComplaintIQ is a smart customer-support help desk.

A customer writes a complaint, such as:

> My LumaView Monitor screen is flickering.

ComplaintIQ then:

1. Reads the complaint.
2. Finds the product or website involved.
3. Decides what kind of problem it is.
4. Measures how serious the problem is.
5. Sends it to the correct support team.
6. Estimates how quickly the team should respond.
7. Writes an automatic customer reply.
8. Shows the complaint to support agents.

Think of it as a digital receptionist that never gets tired.

## 2. The Main Parts

### Customer Portal

Customers can:

- Sign in or create an account.
- Choose how they contacted support.
- Tell ComplaintIQ which product or website has the problem.
- Describe the problem.
- Choose a response language.
- Submit the complaint.
- See the AI category, priority, support team, and reply.
- View previous complaints.
- Rate whether the AI response was helpful.

The product/site field is important. Examples include:

- ShopSphere Checkout
- LumaView Monitor
- ParcelPilot
- CloudDesk Reports
- Northstar Mobile App

### Agent Dashboard

Agents and administrators can:

- View all complaints.
- Search by customer, product, website, category, or complaint text.
- Filter by status.
- Review ticket details.
- Change ticket status.
- Export the queue as CSV.
- See category charts and complaint trends.
- View the Product Health scoreboard.
- See defect keywords such as `#screen-flicker` or `#delivery-delay`.
- Turn on Live Complaint Simulation.
- Generate AI replies using different tones and actions.

### Login Page

The login page supports:

- Customer and agent roles.
- Customer registration.
- Demo account buttons.
- Forgot-password recovery for this local workspace.

## 3. How a Complaint Moves Through the App

```text
Customer enters product/site and complaint
                    |
                    v
          Flask receives the request
                    |
                    v
       Machine-learning model predicts category
                    |
                    v
          Rule-based AI checks the result
                    |
                    v
     Complaint receives priority, team, and SLA
                    |
                    v
      Complaint is saved in the SQLite database
                    |
                    v
      Customer sees a reply and agent sees a ticket
```

## 4. What the AI Finds

### Category

The complaint is assigned to one of these groups:

- Billing
- Delivery
- Technical Support
- Product Quality

### Priority

Priority shows how quickly the team should react:

- High
- Medium
- Low

### Sentiment

The system estimates the customer mood:

- Urgent
- Frustrated
- Neutral
- Satisfied

### SLA

SLA means Service Level Agreement. It is the target time for handling a complaint.

Typical targets are:

- Billing: 4 hours
- Delivery: 6 hours
- Technical Support: 12 hours
- Product Quality: 24 hours

## 5. Machine Learning in Simple Terms

The training script reads examples from `complaints_dataset.csv`.

It learns which words are commonly connected to each category. For example:

- `charge`, `invoice`, and `refund` suggest Billing.
- `package`, `tracking`, and `parcel` suggest Delivery.
- `app`, `password`, and `error` suggest Technical Support.
- `broken`, `damaged`, and `leak` suggest Product Quality.

The model uses two steps:

1. TF-IDF turns words into numbers.
2. LinearSVC uses those numbers to predict a category.

The second rule-based AI check can correct the first prediction when important words clearly point to another category.

## 6. Database

ComplaintIQ uses SQLite, a small database stored locally in:

```text
complaints_full.db
```

The database stores:

- Users
- Password hashes
- Complaint text
- Product or site name
- Category
- Priority
- Support team
- Status
- Sentiment
- AI reply
- Customer feedback
- Dates and timestamps

Passwords are stored as hashes, not as readable passwords.

## 7. Important Files

| File | Purpose |
| --- | --- |
| `app.py` | Flask backend, API routes, AI logic, database setup |
| `train.py` | Trains the machine-learning model |
| `complaints_dataset.csv` | Training examples |
| `login.html` | Login, registration, and password reset UI |
| `customer.html` | Customer complaint portal |
| `agent.html` | Agent dashboard and analytics |
| `complaints_full.db` | Local SQLite database |
| `model/complaint_model.pkl` | Trained classifier |
| `model/categories.pkl` | Saved category names |
| `.vscode/launch.json` | VS Code start-and-debug configuration |
| `.vscode/settings.json` | Localhost browser behavior |

## 8. How to Run the Project

Open a PowerShell terminal in the project folder:

```powershell
cd C:\Users\sivap\complaint
.\.venv\Scripts\Activate.ps1
```

Train the model when needed:

```powershell
.\.venv\Scripts\python.exe train.py
```

Start the Flask server:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the application:

```text
http://localhost:5000/
```

Do not start two copies of Flask at the same time. Only one process can use port `5000`.

## 9. Demo Accounts

| Role | Email | Password |
| --- | --- | --- |
| Customer | `customer@example.com` | `customer123` |
| Administrator | `admin@complaintiq.com` | `admin123` |
| Billing Agent | `billing@complaintiq.com` | `billing123` |
| Logistics Agent | `logistics@complaintiq.com` | `logistics123` |
| Technical Agent | `tech@complaintiq.com` | `tech123` |
| Quality Agent | `qa@complaintiq.com` | `qa123` |

The local password recovery form can change a password when the correct email is entered. It does not send a real email because no email provider is configured.

## 10. Main API Routes

| Method | Route | Purpose |
| --- | --- | --- |
| `POST` | `/auth/login` | Sign in |
| `POST` | `/auth/register` | Create a customer account |
| `POST` | `/auth/reset-password` | Reset a local password |
| `POST` | `/predict` | Submit and classify a customer complaint |
| `GET` | `/my-complaints` | Get the signed-in customer's tickets |
| `GET` | `/complaints` | Get the agent queue |
| `PATCH` | `/complaints/<id>/status` | Change ticket status |
| `POST` | `/complaints/<id>/ai-reply` | Generate a selected-tone reply |
| `GET` | `/stats` | Get dashboard statistics |
| `GET` | `/stats/product-health` | Get product health scores and defect keywords |
| `POST` | `/simulate-complaint` | Add a realistic demo complaint |
| `GET` | `/health` | Check whether the server is running |

## 11. Common Problems

### The browser does not open

Make sure Flask is running, then open:

```text
http://localhost:5000/
```

### Port 5000 is already in use

A Flask process is already running. Use the existing browser page, or stop the old process before starting another one.

### Login says invalid

Check:

- The email spelling.
- The password spelling.
- Whether the account exists in the current local database.

### Product/site is required

Every complaint must name the product or website involved. This helps agents understand what is actually broken.

### The dashboard is empty

Sign in using an agent or administrator account. Customer accounts are sent to the customer portal.

## 12. One-Sentence Summary

ComplaintIQ takes a customer's complaint, uses AI to understand it, stores it safely, routes it to the right team, and gives both customers and agents a clear way to track what happens next.
