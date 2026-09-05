[← Previous: RESTful](16-restful.md) | [Next: Project Environment Setup →](18-project-environment-setup.md)

# 17 Second-Hand Housing Project Introduction

## 17.1 Project Overview

Starting from this chapter, we build a complete hands-on project — **Second-Hand Good Housing (二手好房网)** — that ties together everything we have learned about Flask so far (routing, templates, SQLAlchemy models, blueprints, RESTful, etc.).

Basic facts about the project:

- **Project type**: a second-hand housing / rental listing website named "Second-Hand Good Housing" (二手好房网).
- **Tech stack**: Flask + Flask-SQLAlchemy + MySQL (with Flask-Migrate for database migrations, introduced step by step in later chapters).
- **Data source**: real second-hand housing data, imported into MySQL via the `house.sql` file provided with the course (the `house_info` table holds about 110,000 listing records).

The project consists of five major functional modules, introduced one by one below.

## 17.2 Feature Overview

### 17.2.1 Home Page

The home page is the face of the website and mainly contains:

- A top banner with a search box supporting two search modes: **search by district** and **search by room layout**.
- Current city and total listing count (e.g. current city: Beijing, total listings: 113,318).
- A "Homes for You" section that displays recommended quality listings.

![[ch17-01.png]]

### 17.2.2 Login and Registration

User login and registration are provided as pop-up windows (modal dialogs):

- **Login**: username + password, with a "No account yet? Click to register" entry.
- **Registration**: username (6–15 letters or digits), password (at least 6 letters or digits), confirm password, and email, with an "Already have an account? Click to log in" entry.

![[ch17-02.png]]

### 17.2.3 Searching Listings

When the user types keywords into the search box, the page **auto-completes** matching listing addresses (e.g. "Chaoyang - Gaobeidian - Beihuayuan Community") and shows on the right roughly how many units are available in that community, helping the user quickly locate target listings.

![[ch17-03.png]]

### 17.2.4 Listing List

The list page displays listings as cards. Each listing includes:

- Listing image, title, and price
- Listing address (district - block - community)
- Floor area, room layout, and orientation
- Traffic conditions and view count (how many people have viewed it)

![[ch17-04.png]]

### 17.2.5 Listing Detail

The detail page shows complete information for a single listing:

- A large listing image, the price, and a **favorite (collect)** button
- "Basic Information": room layout, floor area, orientation, location, rent type, landlord's phone, traffic conditions, listing highlights, etc.
- **Data visualization charts** (based on ECharts):
  - A scatter chart of the **price trend** for the community
  - A pie chart of the **room-layout distribution** for the community

![[ch17-05.png]]

## 17.3 Database Tables Overview

The `house.sql` file provided with the course contains three tables; once imported, they supply all the data the project needs.

### 17.3.1 Listing Table house_info

The core data table, storing all listing information (about 110,000 records):

| Column | Type | Description |
| --- | --- | --- |
| `id` | int | Primary key, auto-increment |
| `title` | varchar(100) | Listing title |
| `rooms` | varchar(100) | Room layout (e.g. 2 bedrooms, 1 living room) |
| `area` | varchar(100) | Floor area |
| `price` | varchar(100) | Listing price |
| `direction` | varchar(100) | Orientation |
| `rent_type` | varchar(100) | Rent type (entire rental / shared master bedroom, etc.) |
| `region` | varchar(100) | District (e.g. Chaoyang District) |
| `block` | varchar(100) | Block / sub-district (e.g. Chaoyang - Gaobeidian) |
| `address` | varchar(200) | Community where the listing is located |
| `traffic` | varchar(100) | Traffic conditions |
| `publish_time` | int | Publish time (timestamp) |
| `facilities` | text | Supporting facilities |
| `highlights` | text | Listing advantages / highlights |
| `matching` | text | Nearby amenities |
| `travel` | text | Bus / public transport |
| `page_views` | int | View count |
| `landlord` | varchar(30) | Landlord name |
| `phone_num` | varchar(100) | Landlord phone number |
| `house_num` | varchar(100) | Listing number |

The CREATE TABLE statement (excerpt):

```sql
CREATE TABLE `house_info`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NULL DEFAULT NULL,        -- listing title
  `rooms` varchar(100) NULL DEFAULT NULL,        -- room layout
  `area` varchar(100) NULL DEFAULT NULL,         -- floor area
  `price` varchar(100) NULL DEFAULT NULL,        -- listing price
  `direction` varchar(100) NULL DEFAULT NULL,    -- orientation
  `rent_type` varchar(100) NULL DEFAULT NULL,    -- rent type
  `region` varchar(100) NULL DEFAULT NULL,       -- district
  `block` varchar(100) NULL DEFAULT NULL,        -- block / sub-district
  `address` varchar(200) NULL DEFAULT NULL,      -- community
  `traffic` varchar(100) NULL DEFAULT NULL,      -- traffic conditions
  `publish_time` int NULL DEFAULT NULL,          -- publish time
  `facilities` text NULL,                        -- supporting facilities
  `highlights` text NULL,                        -- listing highlights
  `matching` text NULL,                          -- nearby amenities
  `travel` text NULL,                            -- public transport
  `page_views` int NULL DEFAULT NULL,            -- view count
  `landlord` varchar(30) NULL DEFAULT NULL,      -- landlord name
  `phone_num` varchar(100) NULL DEFAULT NULL,    -- landlord phone
  `house_num` varchar(100) NULL DEFAULT NULL,    -- listing number
  PRIMARY KEY (`id`)
) ENGINE = InnoDB CHARACTER SET = utf8;
```

### 17.3.2 User Table user_info

Stores registered user information, plus each user's favorites and browsing history (saved as comma-separated listing numbers):

| Column | Type | Description |
| --- | --- | --- |
| `id` | int | Primary key, auto-increment |
| `name` | varchar(100) | User nickname |
| `password` | varchar(100) | User password |
| `email` | varchar(100) | Email address |
| `addr` | varchar(100) | User address |
| `collect_id` | varchar(250) | Listing numbers collected by the user |
| `seen_id` | varchar(250) | User's browsing history |

### 17.3.3 Recommendation Table house_recommend

Stores listings recommended to each user together with a recommendation score, powering the home-page recommendation and personalized recommendation features:

| Column | Type | Description |
| --- | --- | --- |
| `id` | int | Primary key, auto-increment |
| `user_id` | int | User id |
| `house_id` | int | Listing id |
| `title` | varchar(100) | Listing title |
| `address` | varchar(100) | Community |
| `block` | varchar(100) | Block / sub-district |
| `score` | int | Recommendation score |

## 17.4 Summary

- Second-Hand Good Housing is a hands-on project: a second-hand housing information website built with Flask + SQLAlchemy + MySQL.
- It has five major modules: home page, login and registration, listing search, listing list, and listing detail.
- Data comes from `house.sql`, which contains three tables: `house_info` (listings), `user_info` (users), and `house_recommend` (recommendations).
- In the next chapter we will set up the development environment and create the project structure.

[← Previous: RESTful](16-restful.md) | [Next: Project Environment Setup →](18-project-environment-setup.md)
