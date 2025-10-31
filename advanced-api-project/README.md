## Book API - Advanced Query Capabilities

The Book API now supports advanced filtering, searching, and ordering.

### Query Parameters

#### Filtering
Filter books by exact field matches:
- `title` - Filter by book title (case-insensitive partial match)
- `author` - Filter by author name (case-insensitive partial match)  
- `publication_year` - Filter by exact publication year
- `publication_year__gt` - Filter by publication year greater than
- `publication_year__lt` - Filter by publication year less than

**Examples:**
GET /api/books/?title=django
GET /api/books/?author=william&publication_year__gt=2020

#### Searching
Search across multiple fields using the `search` parameter:
- Searches in: `title`, `author`, `description`
- Case-insensitive partial matches

**Examples:**
GET /api/books/?search=web development
GET /api/books/?search=django

### Ordering
Sort results by any field using the `ordering` parameter:
- Use `-` prefix for descending order
- Multiple fields supported

**Available fields:** `title`, `author`, `publication_year`, `created_at`, `updated_at`

**Examples:**
GET /api/books/?ordering=title # A-Z
GET /api/books/?ordering=-publication_year # Newest first
GET /api/books/?ordering=author,title # Multiple fields

#### Combined Usage
All features can be combined in a single request:
GET /api/books/?search=python&publication_year__gt=2018&ordering=-publication_year
