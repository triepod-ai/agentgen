# Example Legacy PHP Application Structure

## Typical PHP Application to Migrate

This document shows a typical legacy PHP application structure that would be migrated to Node.js/React using our orchestration strategy.

```
legacy-php-app/
├── index.php                    # Main entry point
├── config/
│   ├── database.php            # DB configuration
│   ├── config.php              # App configuration
│   └── constants.php           # Global constants
├── includes/
│   ├── functions.php           # Global functions
│   ├── auth.php               # Authentication logic
│   └── session.php            # Session management
├── classes/
│   ├── User.php               # User model
│   ├── Product.php            # Product model
│   ├── Order.php              # Order model
│   └── Database.php           # Database wrapper
├── api/
│   ├── users.php              # User API endpoints
│   ├── products.php           # Product endpoints
│   └── orders.php             # Order endpoints
├── admin/
│   ├── index.php              # Admin dashboard
│   ├── users.php              # User management
│   └── reports.php            # Reporting
├── templates/
│   ├── header.php             # Page header
│   ├── footer.php             # Page footer
│   └── sidebar.php            # Navigation
├── css/
│   └── style.css              # Styles
├── js/
│   └── app.js                 # JavaScript
└── sql/
    └── schema.sql             # Database schema
```

## Migration Mapping

### PHP → Node.js Backend Structure
```
node-backend/
├── src/
│   ├── server.js              # Express server (← index.php)
│   ├── config/
│   │   ├── database.js        # Sequelize/Prisma config (← config/database.php)
│   │   ├── config.js          # App config (← config/config.php)
│   │   └── constants.js       # Constants (← config/constants.php)
│   ├── middleware/
│   │   ├── auth.js           # Auth middleware (← includes/auth.php)
│   │   └── session.js        # Session handling (← includes/session.php)
│   ├── models/
│   │   ├── User.js           # User model (← classes/User.php)
│   │   ├── Product.js        # Product model (← classes/Product.php)
│   │   └── Order.js          # Order model (← classes/Order.php)
│   ├── routes/
│   │   ├── users.js          # User routes (← api/users.php)
│   │   ├── products.js       # Product routes (← api/products.php)
│   │   └── orders.js         # Order routes (← api/orders.php)
│   ├── services/
│   │   ├── userService.js    # Business logic
│   │   ├── productService.js # Business logic
│   │   └── orderService.js   # Business logic
│   └── utils/
│       └── helpers.js         # Helper functions (← includes/functions.php)
├── prisma/
│   └── schema.prisma          # Database schema (← sql/schema.sql)
├── tests/
│   ├── unit/
│   └── integration/
└── package.json
```

### PHP Frontend → React Structure
```
react-frontend/
├── src/
│   ├── App.jsx                # Main app component
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.jsx    # Header (← templates/header.php)
│   │   │   ├── Footer.jsx    # Footer (← templates/footer.php)
│   │   │   └── Sidebar.jsx   # Navigation (← templates/sidebar.php)
│   │   ├── auth/
│   │   │   ├── Login.jsx     # Login component
│   │   │   └── Register.jsx  # Registration
│   │   └── admin/
│   │       ├── Dashboard.jsx # Admin dashboard (← admin/index.php)
│   │       └── Users.jsx     # User management (← admin/users.php)
│   ├── pages/
│   │   ├── Home.jsx          # Homepage
│   │   ├── Products.jsx      # Product listing
│   │   └── Admin.jsx         # Admin area
│   ├── services/
│   │   └── api.js            # API client
│   ├── store/
│   │   ├── index.js          # Redux store
│   │   └── slices/
│   │       ├── userSlice.js  # User state
│   │       └── productSlice.js # Product state
│   └── styles/
│       └── App.css            # Styles (← css/style.css)
├── public/
└── package.json
```

## Key Migration Transformations

### 1. Database Queries
**PHP (mysqli/PDO):**
```php
$result = mysqli_query($conn, "SELECT * FROM users WHERE email = '$email'");
$user = mysqli_fetch_assoc($result);
```

**Node.js (Prisma):**
```javascript
const user = await prisma.user.findUnique({
  where: { email }
});
```

### 2. API Endpoints
**PHP:**
```php
// api/users.php
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $users = getAllUsers();
    echo json_encode($users);
}
```

**Node.js (Express):**
```javascript
// routes/users.js
router.get('/', async (req, res) => {
    const users = await userService.getAllUsers();
    res.json(users);
});
```

### 3. Authentication
**PHP:**
```php
session_start();
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
}
```

**Node.js (JWT):**
```javascript
const authMiddleware = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'Unauthorized' });
    // Verify JWT...
    next();
};
```

### 4. Templates to Components
**PHP:**
```php
<?php include 'templates/header.php'; ?>
<div class="content">
    <?php foreach($products as $product): ?>
        <div><?php echo $product['name']; ?></div>
    <?php endforeach; ?>
</div>
<?php include 'templates/footer.php'; ?>
```

**React:**
```jsx
function Products({ products }) {
    return (
        <Layout>
            <div className="content">
                {products.map(product => (
                    <div key={product.id}>{product.name}</div>
                ))}
            </div>
        </Layout>
    );
}
```

## Agent Task Distribution

### Phase-Specific Agent Assignments

**Analysis Phase:**
- `@analyze-codebase`: Scan PHP files, identify patterns
- `@database-specialist`: Analyze schema.sql, relationships
- `@architect-specialist`: Review overall structure

**Conversion Phase:**
- `@python-specialist`: Convert PHP syntax to JavaScript
- `@build-backend`: Create Express routes, middleware
- `@build-frontend`: Convert templates to React components
- `@database-specialist`: Migrate schema to Prisma

**Testing Phase:**
- `@test-automation`: Create test suites
- `@debug-issue`: Fix conversion errors
- `@review-code`: Validate migrated code

**Deployment Phase:**
- `@deploy-application`: Dockerize application
- `@configure-environment`: Setup environments
- `@monitor-system`: Implement monitoring

## Sample Conversion Commands

```bash
# Analyze existing PHP structure
@analyze-codebase --path ./legacy-php-app --lang php --output analysis.json

# Convert database schema
@database-specialist convert --from mysql --schema ./sql/schema.sql --to prisma

# Generate Node.js structure
@architect-specialist generate --type express --from-analysis analysis.json

# Convert PHP classes to JS
@python-specialist convert --from ./classes/*.php --to ./src/models/ --target js

# Create React components from templates
@build-frontend convert-templates --from ./templates/ --to ./src/components/

# Setup testing
@test-automation generate --backend jest --frontend react-testing-library

# Deploy
@deploy-application dockerize --backend ./node-backend --frontend ./react-frontend
```

## Migration Validation Checklist

### Backend Validation
- [ ] All API endpoints migrated
- [ ] Authentication working
- [ ] Database queries converted
- [ ] Business logic preserved
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Performance benchmarked

### Frontend Validation
- [ ] All pages converted
- [ ] Forms functional
- [ ] Navigation working
- [ ] State management
- [ ] API integration
- [ ] Responsive design
- [ ] Browser compatibility

### Data Validation
- [ ] Schema migrated
- [ ] Data integrity maintained
- [ ] Relationships preserved
- [ ] Indexes optimized
- [ ] Backups created

### Testing Coverage
- [ ] Unit tests >80%
- [ ] Integration tests
- [ ] E2E tests
- [ ] Performance tests
- [ ] Security tests
- [ ] Load tests

This structure provides a concrete example for testing the migration orchestration strategy.