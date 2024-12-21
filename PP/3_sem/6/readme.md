# Movie Rating Dataset

## Overview

The **Movie Rating Dataset** provides comprehensive information about movies and user ratings. This dataset is ideal for performing various analyses such as understanding user preferences, evaluating movie popularity, and building recommendation systems. It encompasses details about movies, genres, user demographics, and their corresponding ratings.

## Dataset Structure

The dataset consists of multiple tables/files, each containing specific information. Below is a description of each column present in the dataset.

### 1. Users

Information about the users who have rated the movies.

| **Column Name** | **Description**                                    |
|-----------------|----------------------------------------------------|
| `UserID`        | A unique identifier for each user.                 |
| `Gender`        | The gender of the user (e.g., Male, Female).       |
| `Age`           | The age of the user.                               |
| `Occupation`    | The occupation category of the user.              |
| `Zip-code`      | The ZIP code representing the user's location.     |

### 2. Movies

Details about the movies included in the dataset.

| **Column Name** | **Description**                                    |
|-----------------|----------------------------------------------------|
| `MovieID`       | A unique identifier for each movie.                |
| `Title`         | The title of the movie.                            |
| `Genres`        | A pipe-separated list of genres associated with the movie (e.g., Action|Adventure|Sci-Fi). |

### 3. Ratings

Information about the ratings given by users to movies.

| **Column Name** | **Description**                                    |
|-----------------|----------------------------------------------------|
| `UserID`        | The unique identifier of the user who rated the movie. |
| `MovieID`       | The unique identifier of the movie that was rated.  |
| `Rating`        | The rating given by the user (typically on a scale of 1 to 5). |
| `Timestamp`     | The time at which the rating was given (in UNIX timestamp format). |

### 4. Links

Links to additional information about the movies.

| **Column Name** | **Description**                                    |
|-----------------|----------------------------------------------------|
| `MovieID`       | The unique identifier for each movie.              |
| `IMDb`          | The IMDb identifier for the movie.                 |
| `TMDb`          | The TMDb (The Movie Database) identifier for the movie. |

## Column Descriptions

### UserID

- **Type:** Integer
- **Description:** A unique identifier assigned to each user in the dataset. It is used to link user information with their corresponding ratings.

### Gender

- **Type:** Categorical
- **Description:** Represents the gender of the user. Common values include `Male` and `Female`.

### Age

- **Type:** Integer
- **Description:** Indicates the age of the user. This can be used to analyze rating behaviors across different age groups.

### Occupation

- **Type:** Categorical
- **Description:** Specifies the occupation category of the user (e.g., `Engineer`, `Artist`, `Student`). This helps in understanding how different professions rate movies.

### Zip-code

- **Type:** String
- **Description:** The ZIP code corresponding to the user's location. Useful for geographical analysis of movie ratings.

### MovieID

- **Type:** Integer
- **Description:** A unique identifier for each movie in the dataset. It links movie details with user ratings.

### Title

- **Type:** String
- **Description:** The official title of the movie. Useful for identifying movies in analyses and visualizations.

### Genres

- **Type:** String
- **Description:** A list of genres associated with the movie, separated by pipes (`|`). Examples include `Action|Adventure|Sci-Fi` or `Drama|Romance`.

### Rating

- **Type:** Integer
- **Description:** The rating given by a user to a movie, typically on a scale from 1 (lowest) to 5 (highest). This is the primary variable for evaluating user preferences.

### Timestamp

- **Type:** Integer
- **Description:** The exact time when the rating was made, represented as a UNIX timestamp. Useful for temporal analyses, such as rating trends over time.

### IMDb

- **Type:** String
- **Description:** The IMDb identifier for the movie, which can be used to fetch more detailed information from the IMDb database.

### TMDb

- **Type:** String
- **Description:** The TMDb (The Movie Database) identifier for the movie, allowing access to additional movie details and metadata.

## Usage Examples

- **User Demographics Analysis:** Examine how different age groups or occupations rate various genres of movies.
- **Movie Popularity:** Identify the most popular movies based on average ratings or the number of ratings received.
- **Recommendation Systems:** Develop algorithms to recommend movies to users based on their past ratings and preferences.
- **Temporal Trends:** Analyze how movie ratings fluctuate over time or in response to external events.

## Conclusion

The Movie Rating Dataset is a valuable resource for data analysis, providing insights into user preferences and movie popularity. By leveraging the detailed information across users, movies, and ratings, various analytical and machine learning applications can be developed to enhance the understanding of movie consumption patterns.
