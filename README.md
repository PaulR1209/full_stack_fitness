# Full Stack Fitness

[Live Link](https://full-stack-fitness-a73d59e5c070.herokuapp.com/)

Full Stack Fitness is a gym website that provides a seamless, fully integrated experience for both potential and current gym members. It simplifies the decision-making process for new users by offering detailed information on memberships, facilities, and pricing, and provides an easy-to-use interface for current members to manage their subscriptions, renewals, cancellations, and upgrades. The platform also fosters community engagement by allowing members to leave reviews, sharing their experiences with others. Ultimately, the website addresses the needs of users who prefer managing their gym interactions online with ease and security.


![Am I responsive screenshot](/readme/images/am-i-responsive.png)

## Target Audience

The taget audience for this website includes:

1. **Local Individuals Interested in Joining a Gym**

    This group includes people in the local area who are considering joining a gym. They may be looking for a convenient way to explore available membership options, learn about the gym’s facilities, services, and pricing, and make an informed decision about joining.

2. **Potential Members Seeking Information**

    Individuals who want to learn more about what the gym offers, such as types of memberships and facilities. These people may still be in the decision-making process and need easy access to information to help them decide.

3. **Existing Members**

    Current gym members who want to track and manage their membership details, such as renewal dates, payment status, or membership type. They may also want to upgrade, downgrade, or cancel their membership.

## Marketing Strategy

The primary marketing strategy for this website revolves around building and engaging a community through social media and email marketing. The current approach includes:

### Facebook Page

![Facebook page](/readme/images/facebook.png)

The Facebook page serves as the core platform for connecting with potential users and engaging with current members. It will be regularly updated with valuable content, updates about our gym, and interactive posts designed to increase engagement.

The Facebook page helps build brand awareness and drives traffic to the website by encouraging followers to explore more through the content shared.

As the audience grows, Facebook Ads may be considered to reach a wider, targeted audience.

### Newsletter

![Newsletter screenshot](/readme/images/newsletter.png)

The newsletter allows the gym to engage with members and potential customers directly. By signing up for the newsletter, subscribers receive the latest updates, exclusive promotions, and helpful fitness tips right in their inbox.

- **Benefits:**
  - Keeps the community informed and connected with gym updates.
  - Allows for targeted, personal engagement.
  - Encourages repeat visits to the website through links to new content and promotions.

## User Stories

1. As a **site user** I can **view the home page** so that **I can learn more about the gym**
2. As a **site user** I can **view the about us page** so that **I can learn more about the gyms mission and services**
3. As a **site user** I can **read and create reviews and ratings** so that **I can read other peoples experiences of the gym**
4. As a **site user** I can **view the different tiers of membership** so that **I can choose which membership to purchase**
5. As a **site user** I can **purchase a membership** so that **I can access gym services**
6. As a **site user** I can **view my membership details** so that **I know what membership I have and when it runs out**
7. As a **site user** I can **upgrade and cancel my membership** so that **I can change my plan or cancel based on my needs**

These stories demonstrate how the application meets real needs by simplifying membership interactions, building community through reviews, and providing self-service management tools for users. This project aims to create a convenient, accessible platform for all users interested in engaging with their gym online.

## UX Design and Features

### Wireframes

These wireframes, created using Balsamiq, represent the rough layout and structure of the website. They offer a simple, visual guide to the design and functionality of key pages, helping to plan the user experience and interface before final implementation.

![Home Wireframe Screenshot](/readme/images/home-wireframe.png)

![Reviews Wireframe Screenshot](/readme/images/reviews-wireframe.png)

![Membership Wireframe Screenshot](/readme/images/membership-wireframe.png)

### Homepage

![Hero Image Screenshot](/readme/images/hero-image.png)

**Explanation:** The homepage features a prominent call-to-action (CTA) button to explore memberships. This CTA is strategically placed within the hero image to immediately engage visitors and encourage them to either sign up or learn more about membership options. The goal of this section is to convert visitors into members by clearly guiding them towards the next step in their journey.

### Membership Page

![Membership Page Screenshot](/readme/images/memberships-auth.png)

**Explanation:** Upon clicking the CTA, users are presented with the membership options in a clear, color-coded layout featuring bronze, silver, and gold tiers. This design makes it easy for users to differentiate between available membership options. For new users who are not logged in, another CTA prompting them to sign up appears underneath the membership tiers. This ensures users can only purchase a membership after signing up.

### Admin Dashboard

![Admin Dashboard Screenshot](/readme/images/admin-dashboard.png)

**Explanation** The Admin Dashboard is a page accessible only to users with admin credentials. It provides an overview of all users, with the ability to view detailed information about each user's orders by clicking the "View Details" button. While the page is currently in progress, there are plans to enhance it by adding a search filter for more efficient user lookup. Future updates will also include the ability for admins to edit and create orders on behalf of users, improving overall functionality and control.

### Login/Sign Up Page

![Sign Up Page Screenshot](/readme/images/signup.png)

![Membership page screenshot for logged in users](/readme/images/memberships.png)

**Explanation:** When users click the CTA to sign up, they are redirected to this page, where they can create an account. Authentication is handled via AllAuth, which simplifies the process for users and administrators. Once signed up, users are redirected back to the membership page, where they can now purchase a membership.

### Purchasing a Membership

![Checkout page screenshot](/readme/images/stripe-payment.png)

![Checkout success](/readme/images/payment-success.png)

**Explanation:** After selecting a membership, the user is directed to the Stripe checkout page to complete the purchase. The Stripe API handles payment processing securely. Once payment is successful, the user is redirected to a success page, which includes a link back to the membership page, confirming the transaction and membership.

### Membership Management

![Manage membership page](/readme/images/manage.png)

**Explanation:** Once a user has purchased a membership, the membership page transforms into a management interface. Here, users can update or cancel their membership, or change their payment method. This feature offers flexibility and control over their membership, making it easier for users to manage their subscriptions.

### Reviews Page

![Reviews page screenshot](/readme/images/reviews.png)

**Explanation:** The Reviews page allows users who are logged in to leave a review for the gym. Each review consists of a title, star rating, and a comment, providing valuable feedback for both the gym and other potential customers. Reviews are visible to all visitors, but only logged-in users can leave, edit, or delete their own reviews. This functionality helps build trust and community within the website, as users can see others' experiences while sharing their own.

**Sorting Functionality:** Users can sort reviews by star rating and by the newest or oldest, which makes it easy to find the most relevant or recent feedback. This sorting mechanism enhances the user experience by allowing them to navigate the reviews efficiently.

### Reviews Page for Admin

![Reviews page admin screenshot](/readme/images/admin-review.png)

**Explanation** The Admin Reviews Page allows admins to view all user-submitted reviews. Admins have the ability to edit or delete reviews as needed, providing moderation tools to ensure content remains appropriate and in line with community guidelines.

## Pop up Notifications

### Confirmation Messages

![Modal Box Screenshot](/readme/images/upgrade-modal.png)

**Explanation:** Before making any changes to a user's membership (e.g., upgrading or downgrading), a modal box appears to confirm their action. The modal includes relevant information regarding the changes, providing users with clarity and ensuring they understand what they are about to do. This modal box is built using Bootstrap's modal component.

### Django Messages

![Django messages screenshot](/readme/images/manage-cancelled.png)

**Explanation:** Whenever a user makes changes to their membership, updates their payment method, or if a payment fails, a Django message appears. These pop-up messages notify the user of successful changes or alert them to important issues, such as membership expiration or payment failure. This ensures users are always informed about the status of their account.

# Agile Development Process

For this project, I used Agile methodologies to ensure continuous improvement and effective project management. This included working in short, focused sprints to develop and test features iteratively.

- **Project Board**: I created a GitHub Project Kanban board with columns for "Backlog," "In Progress," and "Done" to track the status of each task.
- **User Stories**: Each user story was broken down into individual tasks, which were then created as issues on GitHub and moved across the project board as progress was made.
- **Continuous Feedback**: The project was reviewed regularly to ensure it aligned with user expectations and to implement improvements quickly.

See my [Project Board](https://github.com/users/PaulR1209/projects/4/views/1) here.

# Database Schema

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
      <td>When attempting to add a review, purchase a membership, or access any URLs realted to either, the user will be directed to the sign in or sign up page.</td>
      <td>Pass</td>
    </tr>
  <tr>
      <td>2</td>
      <td>Leave a Review</td>
      <td>Users can leave a review, with a title, star rating, and comment. Once the review has been submitted, it will show on the reviews page.</td>
      <td>Pass</td>
    </tr>
  <tr>
      <td>3</td>
      <td>Edit or Delete their Reviews</td>
      <td>Users can edit and delete only their reviews, and will not have the option or access to edit and delete others reviews.</td>
      <td>Pass</td>
    </tr>
  <tr>
      <td>4</td>
      <td>Purchasing a Membership</td>
      <td>Users can choose a membership, and be directed to the stripe checkout page. If the payment is successful, you will be redirected to a success page, and your order will be added to the database.</td>
      <td>Pass</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Viewing Membership details</td>
      <td>Users, when they have purchased a membership, can view their membership, and details, such as start date, last renewel date, and next renewel date. They can see their expiry date if canceled.</td>
      <td>Pass</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Updating Membership details or payment methods</td>
      <td>Users can change and cancel their membership, and update their payment method. If done successfully, this will update the database and changes will be shown on the front end. The user will also get message pop ups when any changes are made.</td>
      <td>Pass</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Accessing other users memberships</td>
      <td>Users and guests will not have any access to other users membership details. Any attempt to access will be blocked.</td>
      <td>Pass</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Failed Payment Notification</td>
      <td>User will be notified by a pop up message if a payment has failed, or a membership has been canceled because of a failed payment.</td>
      <td>Pass</td>
    </tr>
  </tbody>
</table>

## Known Issues and Bugs

- **No known issues or bugs at this time**

This section will be updated if any bugs are identified in future testing or by users

## Validation

### JavaScript Type Attribute Warning

**Description:** A warning related to the type attribute in <script> tags (e.g., type="text/javascript"). This attribute is unnecessary in modern HTML5 as it is defaulted to JavaScript. This warning is not caused by any code within this project but might be coming from external resources or libraries included in the project.

**Resolution:** Since this is not related to the project’s code, no changes will be made within this project to address it.

### Charset Attribute Warning

**Description:** This error occurs when the <meta charset="utf-8"> tag appears after the first 1024 bytes in the HTML document. Like the previous warning, this is not a result of any code written in this project and may stem from external libraries or resources.

**Resolution:** Since this issue is not within the project's code, it will not be addressed here. The error is purely informational and doesn't impact functionality.

![Validation Errors](/readme/images/validation.png)

### AllAuth Issues

**Description:** There are a few errors related to the Allauth library, which are not under the direct control of this project. These errors are caused by Allauth's internal workings and cannot be fixed or modified without altering the Allauth library itself.

**Resolution:** These issues are acknowledged, but since they stem from an external package (Allauth), they are not expected to be resolved within this project. They should not affect the core functionality of the application.

![Validation Errors AllAuth](/readme/images/error-signup.png)

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

## Credits

- Pexels for all of my images
- AllAuth for my authentication
- Code Institute course material
- Bootstrap Documentation for my modal boxes