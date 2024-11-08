# Full Stack Fitness

[Live Link](https://full-stack-fitness-a73d59e5c070.herokuapp.com/)

Full Stack Fitness is a gym website that provides detailed information about our facilities, location, and hours to help users learn more about our offerings. Members can create an account to purchase and manage memberships—including canceling, upgrading, or downgrading—all through secure Stripe integration. The website also allows members to leave reviews, fostering a community and sharing experiences.

![Am I responsive screenshot](/readme/images/am-i-responsive.png)

Full Stack Fitness is also an e-commerce platform, offering three membership tiers tailored to suit different fitness needs and budgets:
 
1. Bronze at £25 per month
2. Silver at £35 per month
3. Gold at £50 per month

Each membership unlocks access to a variety of facilities and services, with easy management options for members to adjust their plan as needed. To reach more fitness enthusiasts and engage with our community, we also maintain an active presence on our Facebook page, where we share updates, promotions, and gym news.

![Facebook page](/readme/images/facebook.png)

# Database Scheme

This project uses a relational database to store information about users, orders, memberships, and reviews. Below is an overview of my models and their relationships:

1. **User**:
    - **Description**: Users are the customers who make orders and write reviews.
    - **Attributes**: I used Django Allauth
    - **Relationships**:
        - A **user** can only have one **order** (One to One)
        - A **user** can write multiple **reviews** (One to Many).

2. **Order**:
    - **Description**: An order represents a user's purchase of a membership.
    - **Attributes**: 
        - `order_number`: UUIDField
        - `user`: ForeignKey
        - `full_name`: CharField
        - `email`: EmailField
        - `membership`: ForeignKey
        - `pending_membership`: ForeignKey
        - `created_at`: DateTimeField
        - `last_renewed`: DateTimeField
        - `next_renewal`: DateTimeField
        - `expiry_date`: DateTimeField
        - `is_expired`: BooleanField
        - `is_paid`: BooleanField
        - `cancellation_date`: DateTimeField
        - `is_canceled`: BooleanField
        - `customer_id`: Charfield
        - `subscription_id`: CharField
        - `stripe_price_id`: CharField
        - `session_id`: CharField
        - `membership_price`: DecimalField
        - `has_changed`: BooleanField
        - `pending_membership_price`: DecimalField
        - `previous_membership_price`: DecimalField
        - `proration_amount`: DecimalField
        - `total_next_payment`: DecimalField
    - **Relationships**:
        - An **order** is linked to one **user** and one **membership** (Many to One)
        - A **membership** can be part of multiple **orders** (One to Many)
        - Each **order** has a **ForeignKey** to **user** and **membership**

3. **Membership**:
    - **Description**: Memberships represent the different subscription plans (e.g., Bronze, Silver, Gold).
    - **Attributes**:
        - `membership_type`: CharField
        - `price`: IntegerField
        - `description`: TextField
        - `stripe_price_id`: CharField
    - **Relationships**:
        - A **Membership** can be associated with multiple **orders** (One to Many)

4. **Review**:
    - **Desctipion**: Reviews allow users to leave feedback, for anyone to read.
    - **Attributes**:
        - `user`: ForeignKey
        - `rating`: IntegerField
        - `content`: TextField
        - `created_at`: DateTimeField
        - `updated_at`: DateTimeField
    - **Relationships**:
        - A **review** is linked to one **user** (Many to One)

## Relationships

1. **User** ↔ **Order (One to One)**:
    - One **user** can only have one **order**.
2. **Order** ↔ **Membership (Many to One)**:
    - Each **order** is for one specific **membership**, but a **membership** can be part of many **orders**.
3.  **User** ↔ **Review (One to Many)**:
    - One **user** can write many **reviews**.

# Testing

<table>
  <thead>
    <tr>
      <th>Test</th>
      <th>Test Description</th>
      <th>Expected Outcome</th>
      <th>Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Access to reviews and membership purchases as guest</td>
      <td>When clicking attempting to add a review, purchase a membership, or access any URLs realted to either, the user will be directed to the sign in or sign up page.</td>
      <td>✅ Pass</td>
    </tr>
  <tr>
      <td>2</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  <tr>
      <td>3</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

# Deployment

## Local Deployment

### Step 1: Creating a new Repository
- I navigated to the [Code Institute GitHub Template](https://github.com/Code-Institute-Org/ci-full-template) and clicked on **Use this template** and then clicked **Create a new repository**.
- I then chose my repository name and clicked **Create repository**
- Then I opened [GitPod](https://codeinstitute-ide.net/workspaces) and clicked **New Workspace**, selected my repository, and clicked **Continue**.

### Step 2: Installing Dependencies
- Once my IDE loaded, I installed the necessary project dependencies by installing requirments.txt

### Step 3: Setting Up Environment Variables
- I created a .env file in the root directory of my project
- I added my secret keys to this file

### Step 4: Database Setup and Migrations
- I then set up my database. I used [PostreSQL](https://dbs.ci-dbs.net/)
- Then I updated the database settings in `settings.py`
- And then applied database migrations using `python manage.py migrate`

### Step 5: Creating a Superuser
- I created a Superuser by writing `python manage.py createsuperuser` in the terminal and following the steps provided in the terminal.

### Step 6: Running the development server
- I finally started the application by writing `python manage.py runserver` in the terminal then opened in the browswer using `localhost:8000`

## Heroku Deployment

### Step 1: Creating a Heroku app
- I logged into Heroku and created a new app using the setup prompts

### Step 2: Coneecting to GitHub
- Once I created my app in heroku, I connected it with GitHub in the **Deploy** section of Heroku

### Step 3: Setting Environment Variables:
- I then set all my environment variables in the **Config Vars** section in **Settings**

### Step 4: Deploying Branch
- In the **Deploy** section of Heroku, I clicked the **Deploy Branch** button, to deploy from my connected GitHub branch.

### Launching the App
- Once deployed, I clicked on **Open App** to view my live app.